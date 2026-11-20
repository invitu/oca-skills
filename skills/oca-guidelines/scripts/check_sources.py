#!/usr/bin/env python3
"""Detects when an official source behind a guideline has changed.

Usage:
  python3 -I check_sources.py [options] <guideline> [<guideline> ...]
  python3 -I check_sources.py [options] --all
  python3 -I check_sources.py --accept <id>     (after a human reviewed a change)
  python3 -I check_sources.py --report          (broken sources logged so far)
  python3 -I check_sources.py --issue-text      (ready-to-post issue for them)
  python3 -I check_sources.py --open-issue --confirmed   (only after a human said yes)

Options: --registry FILE, --max-age 7d, --series 18.0, --cache-dir DIR,
--verbose (list every entry, indented; by default only the entries that need
a decision are listed, with a count of the others)

Only the entries of the given guidelines are checked. Output: JSON on stdout,
one state per entry: OK, CHANGED, SECTION_NOT_FOUND, NOT_FOUND, UNREACHABLE,
NEEDS_SERIES, POINTER. A missing source never stops anything: it is logged in
`sources-issues.jsonl` for a maintainer of the skills.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REGISTRY = os.path.join(HERE, "..", "sources.json")
MAX_EXTRACT = 6000
ADORN = re.compile(r"^([!-/:-@\[-`{-~])\1{2,}\s*$")


def parse_age(text):
    match = re.fullmatch(r"(\d+)([mhd])", text)
    if not match:
        sys.exit("--max-age expects a value like 30m, 24h or 7d")
    return int(match.group(1)) * {"m": 60, "h": 3600, "d": 86400}[match.group(2)]


def rst_titles(lines):
    titles = []
    for i in range(len(lines) - 1):
        text = lines[i].strip()
        under = lines[i + 1].strip()
        if text and not ADORN.match(text) and ADORN.match(under) and len(under) >= len(text):
            titles.append((i, text, under[0]))
    return titles


def rst_section(text, heading):
    lines = text.splitlines()
    titles = rst_titles(lines)
    rank = {}
    for _i, _t, char in titles:
        rank.setdefault(char, len(rank))
    for pos, (start, title, char) in enumerate(titles):
        if title != heading:
            continue
        end = len(lines)
        for nxt, _t, nchar in titles[pos + 1:]:
            if rank[nchar] <= rank[char]:
                end = nxt - 1 if nxt > 0 and ADORN.match(lines[nxt - 1].strip()) else nxt
                break
        return "\n".join(lines[start:end])
    return None


def extract(entry, text):
    mode = entry["extract"]["type"]
    if mode == "file":
        return text
    if mode == "rst_section":
        return rst_section(text, entry["extract"]["heading"])
    if mode == "regex":
        match = re.search(entry["extract"]["pattern"], text, re.S | re.M)
        return match.group(0) if match else None
    sys.exit("unknown extract type: %s" % mode)


def normalize(text):
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").splitlines()).strip()


def digest(text):
    return hashlib.sha256(normalize(text).encode("utf-8")).hexdigest()


def fetch(url):
    """Returns (status, text). status: 'ok', 'not_found' or 'unreachable'."""
    if not (url.startswith("https://") or url.startswith("http://127.0.0.1")):
        return "unreachable", ""
    request = urllib.request.Request(url, headers={"User-Agent": "oca-skills-check-sources"})
    try:
        with urllib.request.urlopen(request, timeout=20) as resp:
            return "ok", resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return ("not_found" if exc.code in (404, 410) else "unreachable"), ""
    except (urllib.error.URLError, OSError, ValueError):
        return "unreachable", ""


def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


def log_issue(cache_dir, entry_id, state, url):
    path = os.path.join(cache_dir, "sources-issues.jsonl")
    try:
        with open(path, encoding="utf-8") as fh:
            known = [json.loads(line) for line in fh if line.strip()]
    except (OSError, ValueError):
        known = []
    if any(k.get("id") == entry_id and k.get("state") == state for k in known):
        return
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"id": entry_id, "state": state, "url": url,
                             "date": time.strftime("%Y-%m-%d")}) + "\n")


def clear_issues(cache_dir, entry_id):
    path = os.path.join(cache_dir, "sources-issues.jsonl")
    try:
        with open(path, encoding="utf-8") as fh:
            keep = [line for line in fh if line.strip() and json.loads(line).get("id") != entry_id]
        with open(path, "w", encoding="utf-8") as fh:
            fh.writelines(keep)
    except (OSError, ValueError):
        pass


def read_issues(cache_dir):
    path = os.path.join(cache_dir, "sources-issues.jsonl")
    try:
        with open(path, encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]
    except (OSError, ValueError):
        return []


def write_issues(cache_dir, issues):
    path = os.path.join(cache_dir, "sources-issues.jsonl")
    with open(path, "w", encoding="utf-8") as fh:
        fh.writelines(json.dumps(i) + "\n" for i in issues)


def issue_text(cache_dir, entries):
    """Title and body of one issue for the broken sources not yet reported."""
    todo = [i for i in read_issues(cache_dir) if not i.get("issue")]
    if not todo:
        return None, None, []
    by_id = {e["id"]: e for e in entries}
    title = "Sources to fix: " + ", ".join(i["id"] for i in todo)
    rows = ["| Entry | Guideline | State | URL | First seen |", "|---|---|---|---|---|"]
    for i in todo:
        guidelines = ", ".join(by_id.get(i["id"], {}).get("guidelines", []))
        rows.append("| `%s` | %s | %s | %s | %s |" % (
            i["id"], guidelines, i["state"], i["url"], i["date"]))
    body = "\n".join([
        "`scripts/check_sources.py` could not read these sources:", "", *rows, "",
        "`NOT_FOUND`: the URL no longer exists. `SECTION_NOT_FOUND`: the page exists but",
        "the part used by the guideline is gone or renamed.", "",
        "To fix: find the new location of the source, update the entry in",
        "`sources.json` (`url`, `alt` or `extract`), check that the guideline still",
        "matches the source, then run `check_sources.py --accept <id>`.",
    ])
    return title, body, todo


def gh(args):
    try:
        done = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)
    return done.returncode, (done.stdout or done.stderr).strip()


def open_issue(cache_dir, registry):
    repo = registry.get("issues_repo", "")
    title, body, todo = issue_text(cache_dir, registry["entries"])
    if not todo:
        print("Nothing to report.")
        return
    if not repo:
        sys.exit("FAILED: no issues_repo in the registry. Create the issue by hand.")
    code, out = gh(["issue", "list", "-R", repo, "--state", "open", "--search",
                    "Sources to fix in:title", "--json", "title,url"])
    if code == 0:
        try:
            for found in json.loads(out or "[]"):
                if all(i["id"] in found["title"] for i in todo):
                    print("ALREADY OPEN: %s" % found["url"])
                    return
        except ValueError:
            pass
    code, out = gh(["issue", "create", "-R", repo, "--title", title, "--body", body])
    if code != 0:
        sys.exit("FAILED: %s\nCreate the issue by hand: https://github.com/%s/issues/new" % (out, repo))
    url = out.splitlines()[-1]
    issues = read_issues(cache_dir)
    for i in issues:
        if any(i["id"] == t["id"] and i["state"] == t["state"] for t in todo):
            i["issue"] = url
    write_issues(cache_dir, issues)
    print("CREATED: %s" % url)


def check_entry(entry, series, cache, max_age, cache_dir):
    result = {"id": entry["id"], "guidelines": entry["guidelines"]}
    if entry.get("mode") == "pointer":
        result.update(state="POINTER", url=entry["url"])
        return result
    urls = [entry["url"]] + list(entry.get("alt", []))
    if any("<series>" in u for u in urls):
        if not series:
            result["state"] = "NEEDS_SERIES"
            return result
        urls = [u.replace("<series>", series) for u in urls]
    cached = cache.get(entry["id"])
    if (cached and cached.get("state") == "OK" and cached.get("sha") == entry.get("sha256")
            and time.time() - cached.get("checked", 0) < max_age):
        result.update(state="OK", cached=True)
        return result
    worst = "NOT_FOUND"
    for url in urls:
        status, text = fetch(url)
        if status == "unreachable":
            worst = "UNREACHABLE"
            continue
        if status == "not_found":
            continue
        part = extract(entry, text)
        if part is None:
            worst = "SECTION_NOT_FOUND" if worst == "NOT_FOUND" else worst
            continue
        sha = digest(part)
        result["url"] = url
        if sha == entry.get("sha256"):
            result["state"] = "OK"
            cache[entry["id"]] = {"state": "OK", "sha": sha, "checked": time.time()}
        else:
            result.update(state="CHANGED", sha256=sha, extract=normalize(part)[:MAX_EXTRACT])
        return result
    result.update(state=worst, url=urls[0], tried=urls)
    if worst in ("NOT_FOUND", "SECTION_NOT_FOUND"):
        log_issue(cache_dir, entry["id"], worst, urls[0])
    return result


def main(argv):
    opts = {"--registry": DEFAULT_REGISTRY, "--max-age": "7d", "--series": "",
            "--cache-dir": os.environ.get("OCA_SKILLS_CACHE",
                                          os.path.expanduser("~/.cache/oca-skills"))}
    flags, names, it = set(), [], iter(argv)
    for arg in it:
        if arg in opts:
            opts[arg] = next(it, "")
        elif arg in ("--all", "--report", "--issue-text", "--open-issue", "--confirmed",
                     "--verbose"):
            flags.add(arg)
        elif arg == "--accept":
            flags.add(arg)
            names.append(next(it, ""))
        else:
            names.append(arg)
    cache_dir = opts["--cache-dir"]
    os.makedirs(cache_dir, exist_ok=True)

    if "--report" in flags:
        path = os.path.join(cache_dir, "sources-issues.jsonl")
        try:
            with open(path, encoding="utf-8") as fh:
                print(fh.read() or "No broken source logged.")
        except OSError:
            print("No broken source logged.")
        return

    registry = load_json(opts["--registry"], None)
    if registry is None:
        sys.exit("registry not readable: %s" % opts["--registry"])
    if "--issue-text" in flags:
        title, body, todo = issue_text(cache_dir, registry["entries"])
        if not todo:
            print("Nothing to report.")
        else:
            print("Repository: %s\nTitle: %s\n\n%s" % (
                registry.get("issues_repo") or "(none configured)", title, body))
        return
    if "--open-issue" in flags:
        if "--confirmed" not in flags:
            sys.exit("--open-issue needs --confirmed, only after a human said yes")
        open_issue(cache_dir, registry)
        return
    entries = registry["entries"]
    cache_path = os.path.join(cache_dir, "sources-cache.json")
    cache = load_json(cache_path, {})
    series = opts["--series"]

    if "--accept" in flags:
        entry = next((e for e in entries if e["id"] == names[0]), None)
        if not entry:
            sys.exit("unknown id: %s" % names[0])
        urls = [u.replace("<series>", series) for u in [entry["url"]] + list(entry.get("alt", []))]
        for url in urls:
            status, text = fetch(url)
            part = extract(entry, text) if status == "ok" else None
            if part is not None:
                entry["sha256"] = digest(part)
                entry["checked"] = time.strftime("%Y-%m-%d")
                with open(opts["--registry"], "w", encoding="utf-8") as fh:
                    json.dump(registry, fh, indent=2, ensure_ascii=False)
                    fh.write("\n")
                clear_issues(cache_dir, entry["id"])
                cache.pop(entry["id"], None)
                with open(cache_path, "w", encoding="utf-8") as fh:
                    json.dump(cache, fh)
                print("accepted %s %s" % (entry["id"], entry["sha256"]))
                return
        sys.exit("source not readable, nothing accepted: %s" % entry["id"])

    if "--all" not in flags and not names:
        sys.exit("Usage: check_sources.py [options] <guideline> [...] | --all | --accept <id> | --report")
    def wanted(entry):
        return any(g in names or os.path.basename(g) in names for g in entry["guidelines"])

    selected = [e for e in entries if "--all" in flags or wanted(e)]
    results = [check_entry(e, series, cache, parse_age(opts["--max-age"]), cache_dir) for e in selected]
    with open(cache_path, "w", encoding="utf-8") as fh:
        json.dump(cache, fh)
    unlisted = [n for n in names if not any(
        n in e["guidelines"] or n in map(os.path.basename, e["guidelines"]) for e in entries)]
    if "--verbose" in flags:
        out, kwargs = {"results": results, "unlisted": unlisted}, {"indent": 2}
    else:
        out = {"checked": len(results),
               "ok": sum(r["state"] == "OK" for r in results),
               "pointer": sum(r["state"] == "POINTER" for r in results),
               "results": [r for r in results if r["state"] not in ("OK", "POINTER")],
               "unlisted": unlisted}
        kwargs = {"separators": (",", ":")}
    json.dump(out, sys.stdout, ensure_ascii=False, **kwargs)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main(sys.argv[1:])
