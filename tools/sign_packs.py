#!/usr/bin/env python3
"""Sign the packs whose files changed since they were last signed.

Runs in CI (.github/workflows/sign.yml) after a merge to main, with the pack
key from the PACK_SIGNING_KEY secret written to the file named by --key. For
every pack it writes pack.digest (the digest the app computes, see
build_index.py) and pack.digest.minisig, then checks the signature against
pack.pub. A pack whose pack.digest already matches its files and is signed is
left alone, so signatures only change when a pack does.

Usage: python tools/sign_packs.py --key <secret key file>
Needs: minisign on PATH; the key's password, if any, in PACK_SIGNING_PASSWORD.
"""
import argparse
import os
import subprocess
import sys

import yaml  # pip install pyyaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_index import PACKS, ROOT, digest  # noqa: E402

PUB = os.path.join(ROOT, "pack.pub")


def needs_signing(folder, d):
    path = os.path.join(folder, "pack.digest")
    if not os.path.exists(path) or not os.path.exists(path + ".minisig"):
        return True
    with open(path, encoding="utf-8") as f:
        return f.read().strip() != d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True)
    args = ap.parse_args()
    password = os.environ.get("PACK_SIGNING_PASSWORD", "")
    signed = []
    for name in sorted(os.listdir(PACKS)):
        folder = os.path.join(PACKS, name)
        if not os.path.isdir(folder):
            continue
        d = digest(folder)
        target = os.path.join(folder, "pack.digest")
        if needs_signing(folder, d):
            with open(os.path.join(folder, "manifest.yaml"), encoding="utf-8") as f:
                version = str((yaml.safe_load(f) or {}).get("version", ""))
            with open(target, "w", encoding="utf-8", newline="\n") as f:
                f.write(d + "\n")
            # The password goes on stdin; an unencrypted key does not ask.
            subprocess.run(["minisign", "-S", "-s", args.key, "-m", target, "-x", target + ".minisig",
                            "-t", f"pack {name} {version}"],
                           input=password + "\n", text=True, check=True, stdout=subprocess.DEVNULL)
            signed.append(name)
        # Whatever was signed, before or now, must verify against pack.pub.
        subprocess.run(["minisign", "-V", "-p", PUB, "-m", target, "-x", target + ".minisig"],
                       check=True, stdout=subprocess.DEVNULL)
    print("signed: " + (", ".join(signed) if signed else "nothing changed"))


if __name__ == "__main__":
    main()
