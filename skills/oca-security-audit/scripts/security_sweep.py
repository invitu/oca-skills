#!/usr/bin/env python3
"""Sweep a diff or files for the patterns of security-audit.md.

Usage:
  security_sweep.py --repo <dir> --range <git range>
  security_sweep.py --files <file> [<file> ...]

Output (compact JSON): {"audit_required": bool, "hits": [[file, line, pattern]]}
"""
import argparse
import json
import os
import re
import subprocess
import sys

PATTERNS = (
    ("sudo", r"\.(sudo|with_user|with_company)\("),
    ("sql", r"\bcr\.execute\(|\bSQL\("),
    ("domain-string", r"domain\w*\s*=\s*(f[\"']|.*\.format\(|.*[\"']\s*%)"),
    ("public-method", r"^\s*def [a-z]\w*\("),
    ("route", r"@http\.route"),
    ("html", r"\b[Mm]arkup\(|innerHTML|insertAdjacentHTML|t-raw"),
    ("related", r"\brelated\s*="),
    ("open", r"(?<![\w.])open\("),
    ("eval", r"\beval\(|\bexec\(|safe_eval"),
    ("pickle", r"\bpickle\b"),
    ("getattr", r"\b(getattr|setattr)\("),
    ("secret-compare", r"(password|token|secret|api_key)\w*\s*==|==\s*\w*(password|token|secret|api_key)"),
    ("create-override", r"def create\("),
    ("mutable-default", r"def .*=\s*(\[\]|\{\})"),
    ("commit", r"\bcr\.commit\("),
    ("secret-literal", r"(password|passwd|secret|token|api_key)\w*\s*=\s*[\"'][^\"']+[\"']"),
    ("dependency", r"external_dependencies"),
)
COMPILED = tuple((name, re.compile(rx, re.I if name == "secret-literal" else 0)) for name, rx in PATTERNS)
EXTENSIONS = (".py", ".xml", ".js", ".csv")
SKIP = ("/i18n/", "/static/description/", "/readme/")


def sensitive_path(path):
    parts = "/" + path
    return "/security/" in parts or path.endswith("requirements.txt")


def scannable(path):
    return path.endswith(EXTENSIONS) and not any(s in "/" + path for s in SKIP)


def scan_line(path, number, text, hits):
    for name, rx in COMPILED:
        if rx.search(text):
            hits.append([path, number, name])


def from_diff(repo, rng):
    out = subprocess.run(
        ["git", "-C", repo, "diff", "-U0", "--no-color", rng],
        capture_output=True, text=True, check=True,
    ).stdout
    hits, path, number = [], None, 0
    flagged = set()
    for line in out.splitlines():
        if line.startswith("diff --git "):
            path = line.rsplit(" b/", 1)[-1]
            if sensitive_path(path) and path not in flagged:
                flagged.add(path)
                hits.append([path, 0, "security-file"])
        elif line.startswith("@@"):
            number = int(re.search(r"\+(\d+)", line).group(1)) - 1
        elif line.startswith("+") and not line.startswith("+++"):
            number += 1
            if path and scannable(path):
                scan_line(path, number, line[1:], hits)
    return hits


def from_files(files):
    hits = []
    for path in files:
        if sensitive_path(path):
            hits.append([path, 0, "security-file"])
        if not scannable(path) or not os.path.isfile(path):
            continue
        with open(path, errors="replace") as handle:
            for number, text in enumerate(handle, 1):
                scan_line(path, number, text.rstrip("\n"), hits)
    return hits


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--range")
    parser.add_argument("--files", nargs="+")
    args = parser.parse_args()
    if bool(args.range) == bool(args.files):
        parser.error("give --range or --files")
    hits = from_diff(args.repo, args.range) if args.range else from_files(args.files)
    print(json.dumps({"audit_required": bool(hits), "hits": hits}, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
