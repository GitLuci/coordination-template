"""FE/BE contract versions: sign (register) and verify that nothing changed without a new version.

    python scripts/contract.py register --version 2    # signs the current state of contract/ as v2
    python scripts/contract.py verify                  # fails if contract/ changed since the last signed version
    python scripts/contract.py verify --against ../coordination-x/contract   # and if it differs from the shared copy

The sha256 covers the schema and the examples (everything in contract/ except VERSIONS.json, CHANGES.md and README.md),
with line endings normalized so Windows and Linux give the same value. Standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "contract"
EXCLUDED = {"VERSIONS.json", "CHANGES.md", "README.md"}


def sha(folder: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(p for p in folder.rglob("*") if p.is_file() and p.name not in EXCLUDED):
        h.update(f.relative_to(folder).as_posix().encode() + b"\0")
        h.update(f.read_bytes().replace(b"\r\n", b"\n") + b"\0")
    return h.hexdigest()


def versions(folder: Path) -> dict[str, str]:
    f = folder / "VERSIONS.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def register(folder: Path, version: int) -> int:
    v = versions(folder)
    if v and version <= max(map(int, v)):
        print(f"the version must be greater than {max(map(int, v))}", file=sys.stderr)
        return 2
    current = sha(folder)
    if v and current == v[max(v, key=int)]:
        print("the contract hasn't changed since the last signed version", file=sys.stderr)
        return 2
    v[str(version)] = current
    (folder / "VERSIONS.json").write_text(json.dumps(v, indent=2) + "\n", encoding="utf-8")
    print(f"contract v{version} signed ({current[:12]}). Record the line in CHANGES.md and notify the devs.")
    return 0


def verify(folder: Path, against: Path | None) -> int:
    v = versions(folder)
    if not v:
        print("no signed version: run `register --version 1` first", file=sys.stderr)
        return 1
    latest = max(v, key=int)
    current = sha(folder)
    if current != v[latest]:
        print(f"the contract changed since v{latest} without a new signed version (ask the coordinator)", file=sys.stderr)
        return 1
    if against is not None:
        shared = versions(against)
        if not shared:
            print(f"{against}: no signed versions", file=sys.stderr)
            return 1
        latest_shared = max(shared, key=int)
        if latest_shared != latest or sha(against) != current:
            print(f"this copy is at v{latest}; the shared one is at v{latest_shared}: update the copy", file=sys.stderr)
            return 1
    print(f"contract v{latest} ok")
    return 0


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("--folder", type=Path, default=ROOT, help="contract folder (default: the repository's contract/)")
    sub = a.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("register")
    r.add_argument("--version", type=int, required=True)
    c = sub.add_parser("verify")
    c.add_argument("--against", type=Path, help="the shared contract folder (separate repositories)")
    args = a.parse_args(argv)
    if args.cmd == "register":
        return register(args.folder, args.version)
    return verify(args.folder, args.against)


if __name__ == "__main__":
    sys.exit(main())
