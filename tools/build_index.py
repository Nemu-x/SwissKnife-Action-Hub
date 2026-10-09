#!/usr/bin/env python3
"""Build index.json for the SwissKnife Action Hub.

The pack digest is computed exactly as the app does: every file of the pack
folder except pack.digest / pack.digest.minisig, one line per file
"<path>\0<sha256>\n" (forward slashes), lines sorted, SHA-256 of the result.
The app re-checks the digest after downloading, so an index that does not
match the files simply cannot be installed.

Usage: python tools/build_index.py [--check]
"""
import hashlib
import json
import os
import sys

import yaml  # pip install pyyaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKS = os.path.join(ROOT, "packs")
SIGN_FILES = {"pack.digest", "pack.digest.minisig"}
CATEGORIES = {"security", "exchange", "hr", "teams", "intune", "reports", "other"}


def files_of(folder):
    out = []
    for base, _, names in os.walk(folder):
        for n in names:
            rel = os.path.relpath(os.path.join(base, n), folder).replace(os.sep, "/")
            out.append(rel)
    return sorted(out)


def digest(folder):
    lines = []
    for rel in files_of(folder):
        if rel in SIGN_FILES:
            continue
        with open(os.path.join(folder, rel), "rb") as f:
            lines.append(rel + "\x00" + hashlib.sha256(f.read()).hexdigest() + "\n")
    lines.sort()
    return hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()


def entry(name):
    folder = os.path.join(PACKS, name)
    with open(os.path.join(folder, "manifest.yaml"), encoding="utf-8") as f:
        m = yaml.safe_load(f) or {}
    if m.get("name") != name:
        raise SystemExit(f"packs/{name}: the folder must be named like the pack ({m.get('name')!r})")
    kind = "workflow"
    if m.get("actions") and m.get("workflows"):
        kind = "mixed"
    elif m.get("actions"):
        kind = "script"
    cat = m.get("category") if m.get("category") in CATEGORIES else "other"
    desc = m.get("summary") or ({"en": m["description"]} if m.get("description") else {})
    return {
        "name": name,
        "version": str(m.get("version", "")),
        "category": cat,
        "kind": kind,
        "title": m.get("title") or {"en": name},
        "description": desc,
        "author": m.get("author", ""),
        "path": "packs/" + name,
        "files": files_of(folder),
        "digest": digest(folder),
        "signed": os.path.exists(os.path.join(folder, "pack.digest.minisig")),
    }


def main():
    names = sorted(n for n in os.listdir(PACKS) if os.path.isdir(os.path.join(PACKS, n)))
    index = {"version": 1, "packs": [entry(n) for n in names]}
    text = json.dumps(index, indent=2, ensure_ascii=False) + "\n"
    path = os.path.join(ROOT, "index.json")
    if "--check" in sys.argv:
        current = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
        if current != text:
            raise SystemExit("index.json is out of date: run python tools/build_index.py and commit it")
        print(f"index.json is up to date ({len(names)} packs)")
        return
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"{len(names)} pack(s) indexed")


if __name__ == "__main__":
    main()
