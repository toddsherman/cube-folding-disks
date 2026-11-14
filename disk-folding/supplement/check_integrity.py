#!/usr/bin/env python3
"""Check the packaged SHA-256 manifest using only the standard library."""
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent


def main():
    manifest = ROOT / "SHA256SUMS"
    failures = []
    seen = set()
    for number, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        try:
            digest, relative = line.split("  ", 1)
            path = Path(relative)
            if (len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest)
                    or path.is_absolute() or ".." in path.parts or relative in seen):
                raise ValueError("malformed or duplicate manifest entry")
            seen.add(relative)
            target = ROOT / path
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            if actual != digest:
                failures.append(f"SHA-256 mismatch: {relative}")
        except (ValueError, OSError) as exc:
            failures.append(f"Manifest line {number}: {exc}")
    if not seen:
        failures.append("Manifest has no entries")
    # Every distributed file must be listed (added 9 November 2026). Exempt are the
    # manifest itself, bytecode caches, .DS_Store, and verifier outputs written here
    # as verification*.json, the pattern of the documented output name.
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT).as_posix()
        generated = p.parent == ROOT and p.name.startswith("verification") and p.suffix == ".json"
        if (p.is_file() and "__pycache__" not in p.parts and p.name != ".DS_Store"
                and rel != "SHA256SUMS" and rel not in seen and not generated):
            failures.append(f"File not listed in SHA256SUMS: {rel}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"Verified SHA-256 hashes for {len(seen)} packaged files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
