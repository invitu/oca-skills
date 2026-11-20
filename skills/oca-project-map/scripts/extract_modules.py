#!/usr/bin/env python3
"""Deterministic inventory of the Odoo modules found in one or more folders.

Usage:
  python3 -I extract_modules.py [--target 18.0] [--external-licenses f.json] [--full] <folder> [...]

--target             Odoo series of the project (version state of each module).
--external-licenses  JSON {"module": "LGPL-3"} or {"module": {"license": "...",
                     "depends": [...]}} for dependencies outside the project.
Output: JSON on stdout (modules, alerts, migration_order, errors, repos).
Compact by default (one module per entry, no indentation, no name, summary,
path, installable or per-module license list). --full gives every field,
indented.

Licenses allowed by a repository come from `license-allowed` in its
.pylintrc-mandatory or .pylintrc (absent: no check, reported as unknown).
"""
import ast
import json
import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", "setup", "static", "i18n", "tests", "__pycache__"}
OPEN = ("AGPL", "LGPL", "GPL")
PROPRIETARY = ("OPL-1", "OEEL-1", "OTHER PROPRIETARY")
OTHER_KNOWN = ("OTHER OSI APPROVED LICENCE",)


def up(license_):
    return str(license_ or "").strip().upper()


def starts(license_, prefixes):
    return up(license_).startswith(prefixes)


def kind(license_):
    """agpl: forces AGPL-3 downstream; gpl2_only: to confirm; other: no effect."""
    lic = up(license_)
    if lic.startswith("AGPL") or lic == "GPL-3" or (lic.startswith("GPL") and "LATER" in lic):
        return "agpl"
    if lic == "GPL-2":
        return "gpl2_only"
    return "other"


def read_allowed(repo_root, cache):
    if repo_root in cache:
        return cache[repo_root]
    allowed = None
    for fname in (".pylintrc-mandatory", ".pylintrc"):
        try:
            with open(os.path.join(repo_root, fname), encoding="utf-8") as fh:
                match = re.search(r"^license-allowed\s*=\s*(.+)$", fh.read(), re.M)
        except OSError:
            continue
        if match:
            allowed = [x.strip() for x in match.group(1).split(",") if x.strip()]
            break
    cache[repo_root] = allowed
    return allowed


def read_manifest(path):
    # The manifest is a dict literal; literal_eval avoids executing the file.
    with open(path, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Dict):
            return ast.literal_eval(node.value)
    raise ValueError("no manifest dict found")


def str_values(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, (ast.List, ast.Tuple)):
        return [e.value for e in node.elts
                if isinstance(e, ast.Constant) and isinstance(e.value, str)]
    return []


def read_models(module_dir, errors):
    created, extended = set(), set()
    for dirpath, dirnames, filenames in os.walk(module_dir):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if not fname.endswith(".py") or fname == "__manifest__.py":
                continue
            path = os.path.join(dirpath, fname)
            try:
                with open(path, encoding="utf-8") as fh:
                    tree = ast.parse(fh.read())
            except (SyntaxError, UnicodeDecodeError) as exc:
                errors.append("%s: %s" % (path, exc))
                continue
            for cls in (n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)):
                name, inherit = [], []
                for stmt in cls.body:
                    if isinstance(stmt, ast.Assign):
                        for tgt in stmt.targets:
                            if isinstance(tgt, ast.Name) and tgt.id == "_name":
                                name = str_values(stmt.value)
                            if isinstance(tgt, ast.Name) and tgt.id == "_inherit":
                                inherit = str_values(stmt.value)
                if name:
                    created.update(n for n in name if n not in inherit)
                    extended.update(n for n in name if n in inherit)
                elif inherit:
                    extended.update(inherit)
    return sorted(created), sorted(extended)


def repo_info(module_dir, roots):
    # Walk up to the first folder containing .git, without leaving the given roots.
    cur = os.path.dirname(os.path.abspath(module_dir))
    stops = {os.path.abspath(r) for r in roots}
    while True:
        if os.path.isdir(os.path.join(cur, ".git")):
            url = ""
            try:
                with open(os.path.join(cur, ".git", "config"), encoding="utf-8") as fh:
                    for line in fh:
                        if line.strip().startswith("url"):
                            url = line.split("=", 1)[1].strip()
                            break
            except OSError:
                pass
            return os.path.basename(cur), url, cur
        if cur in stops or os.path.dirname(cur) == cur:
            return os.path.basename(cur), "", cur
        cur = os.path.dirname(cur)


def is_oca_repo(url):
    """True/False from the repository URL, None when the URL is unknown."""
    if not url:
        return None
    return "github.com/oca/" in url.lower() or "github.com:oca/" in url.lower()


def version_series(version):
    # Odoo series = first two components of a version shaped like 18.0.x.y.z.
    match = re.match(r"^(\d+\.\d+)\.\d+", str(version))
    return match.group(1) if match else ""


def load_externals(path):
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    externals = {}
    for name, val in raw.items():
        if isinstance(val, str):
            externals[name] = {"license": val, "depends": []}
        else:
            externals[name] = {"license": str(val.get("license", "")),
                               "depends": list(val.get("depends", []))}
    return externals


def closure(name, deps_of):
    seen, stack = set(), list(deps_of(name))
    while stack:
        dep = stack.pop()
        if dep in seen:
            continue
        seen.add(dep)
        stack.extend(deps_of(dep))
    return seen


def migration_levels(modules, to_migrate):
    # Level 0 = modules to migrate whose project dependencies are none to migrate themselves.
    levels, remaining, done = [], set(to_migrate), set()
    while remaining:
        level = sorted(n for n in remaining
                       if all(d in done or d not in to_migrate
                              for d in modules[n]["project_depends"]))
        if not level:
            levels.append({"cycle_or_blocked": sorted(remaining)})
            break
        levels.append(level)
        done.update(level)
        remaining.difference_update(level)
    return levels


def find_cycles(graph):
    cycles, state = [], {}

    def visit(node, path):
        state[node] = 1
        for dep in graph.get(node, []):
            if state.get(dep) == 1:
                cycles.append(path[path.index(dep):] + [dep] if dep in path else [node, dep])
            elif dep not in state:
                visit(dep, path + [dep])
        state[node] = 2

    for n in graph:
        if n not in state:
            visit(n, [n])
    return cycles


def scan(roots, errors):
    modules, cache = {}, {}
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            if "__manifest__.py" not in filenames:
                continue
            dirnames[:] = []
            name = os.path.basename(dirpath)
            try:
                man = read_manifest(os.path.join(dirpath, "__manifest__.py"))
            except (ValueError, SyntaxError, UnicodeDecodeError) as exc:
                errors.append("%s: %s" % (dirpath, exc))
                continue
            repo, url, repo_root = repo_info(dirpath, roots)
            created, extended = read_models(dirpath, errors)
            author = str(man.get("author", ""))
            entry = {
                "module": name,
                "repo": repo,
                "repo_url": url,
                "path": os.path.relpath(dirpath, root),
                "name": man.get("name", ""),
                "summary": man.get("summary", ""),
                "version": man.get("version", ""),
                "series": version_series(man.get("version", "")),
                "license": man.get("license", ""),
                "author": author,
                "installable": man.get("installable", True),
                "oca_repo": is_oca_repo(url),
                "license_allowed": read_allowed(repo_root, cache),
                "depends": list(man.get("depends", [])),
                "models_created": created,
                "models_extended": extended,
            }
            if name in modules:
                errors.append("duplicate module: %s (%s and %s)" % (
                    name, modules[name]["path"], entry["path"]))
                continue
            modules[name] = entry
    return modules


def check_versions(modules, target, alerts):
    for m in modules.values():
        if not target:
            m["version_state"] = ""
        elif not m["series"]:
            m["version_state"] = "unknown"
            alerts.append({"type": "UNKNOWN_VERSION", "module": m["module"],
                           "version": m["version"]})
        else:
            m["version_state"] = "up_to_date" if m["series"] == target else "to_migrate"
    to_migrate = {n for n, m in modules.items() if m["version_state"] == "to_migrate"}
    for m in modules.values():
        if m["version_state"] == "up_to_date":
            for dep in m["project_depends"]:
                if dep in to_migrate:
                    alerts.append({"type": "UP_TO_DATE_DEPENDS_ON_MODULE_TO_MIGRATE",
                                   "module": m["module"], "depends_on": dep})
    return to_migrate


def license_options(minimum, allowed):
    """Licenses a human can choose from; None when the repository list is unknown."""
    if allowed is None or minimum in ("undetermined", "TO CONFIRM"):
        return None
    if minimum == "AGPL-3":
        return [x for x in allowed if up(x).startswith("AGPL")]
    return list(allowed)


def check_licenses(modules, externals, alerts):
    def deps_of(name):
        if name in modules:
            return modules[name]["depends"]
        return externals.get(name, {}).get("depends", [])

    def license_of(name):
        if name in modules:
            return modules[name]["license"]
        return externals.get(name, {}).get("license", "")

    unknown_users = {}
    for m in modules.values():
        name, declared = m["module"], m["license"]
        allowed = m["license_allowed"]
        clos = closure(name, deps_of)
        upstream = sorted(d for d in clos if kind(license_of(d)) == "agpl")
        gpl2 = sorted(d for d in clos if kind(license_of(d)) == "gpl2_only")
        unknown = sorted(d for d in clos if not license_of(d))
        for dep in unknown:
            if dep not in modules:
                unknown_users.setdefault(dep, []).append(name)
        for dep in gpl2:
            alerts.append({"type": "TO_CONFIRM_GPL2_ONLY", "module": name, "depends_on": dep})

        if gpl2:
            minimum = "TO CONFIRM"
        elif upstream:
            minimum = "AGPL-3"
        elif unknown:
            minimum = "undetermined"
        else:
            minimum = "none"
        m["minimum_license"] = minimum
        m["license_options"] = license_options(minimum, allowed)
        m["upstream_copyleft"] = upstream
        m["unknown_licenses"] = unknown

        if not declared:
            alerts.append({"type": "MISSING_LICENSE", "module": name})
        elif not (starts(declared, OPEN) or up(declared) in PROPRIETARY
                  or up(declared) in OTHER_KNOWN):
            alerts.append({"type": "UNKNOWN_LICENSE", "module": name, "license": declared})
        if declared:
            refused = (allowed is not None and up(declared) not in {up(x) for x in allowed}) or (
                allowed is None and m["oca_repo"] and up(declared) in PROPRIETARY)
            if refused:
                alerts.append({"type": "LICENSE_NOT_ALLOWED", "module": name,
                               "license": declared, "allowed": allowed})
        if declared and minimum == "AGPL-3" and not starts(declared, ("AGPL",)):
            alerts.append({"type": "INSUFFICIENT_LICENSE", "module": name,
                           "license": declared, "upstream_copyleft": upstream})
        if starts(declared, ("AGPL",)):
            for dep in sorted(d for d in clos if up(license_of(d)) in PROPRIETARY):
                alerts.append({"type": "TO_CONFIRM_OPEN_DEPENDS_ON_PROPRIETARY",
                               "module": name, "license": declared, "depends_on": dep,
                               "dependency_license": license_of(dep), "direct": dep in m["depends"]})
        if m["oca_repo"]:
            for dep in sorted(d for d in clos if d in modules and modules[d]["oca_repo"] is False):
                alerts.append({"type": "OCA_DEPENDS_ON_NON_OCA", "module": name,
                               "depends_on": dep, "direct": dep in m["depends"]})
    for dep, users in sorted(unknown_users.items()):
        alerts.append({"type": "UNKNOWN_EXTERNAL_LICENSE", "dependency": dep,
                       "used_by": sorted(set(users))})


COMPACT_DROP = ('name', 'summary', 'path', 'installable', 'license_allowed')


def main(roots, target, externals, full):
    errors, alerts = [], []
    modules = scan(roots, errors)
    for m in modules.values():
        m["project_depends"] = [d for d in m["depends"] if d in modules]
        m["external_depends"] = [d for d in m["depends"] if d not in modules]
    to_migrate = check_versions(modules, target, alerts)
    check_licenses(modules, externals, alerts)
    for cyc in find_cycles({n: m["project_depends"] for n, m in modules.items()}):
        alerts.append({"type": "DEPENDENCY_CYCLE", "path": cyc})
    repos = {m["repo"]: {"url": m["repo_url"], "license_allowed": m["license_allowed"]}
             for m in modules.values()}
    listed = sorted(modules.values(), key=lambda x: x["module"])
    if not full:
        listed = [{k: v for k, v in m.items() if k not in COMPACT_DROP} for m in listed]
    json.dump({"target": target, "modules": listed, "repos": repos, "alerts": alerts,
               "migration_order": migration_levels(modules, to_migrate), "errors": errors},
              sys.stdout, ensure_ascii=False,
              **({"indent": 2} if full else {"separators": (",", ":")}))
    sys.stdout.write("\n")


def parse_args(argv):
    target, ext_path, roots, full = "", "", [], False
    it = iter(argv)
    for arg in it:
        if arg == "--full":
            full = True
        elif arg == "--target":
            target = next(it, "")
            if not re.match(r"^\d+\.\d+$", target):
                sys.exit("--target expects a series like 18.0")
        elif arg == "--external-licenses":
            ext_path = next(it, "")
            if not ext_path:
                sys.exit("--external-licenses expects a JSON file")
        else:
            roots.append(arg)
    if not roots:
        sys.exit("Usage: extract_modules.py [--target 18.0] [--external-licenses f.json] [--full] <folder> [...]")
    return target, ext_path, roots, full


if __name__ == "__main__":
    target_arg, ext_arg, roots_arg, full_arg = parse_args(sys.argv[1:])
    main(roots_arg, target_arg, load_externals(ext_arg) if ext_arg else {}, full_arg)
