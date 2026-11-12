#!/usr/bin/env python3
"""Fail when Nexus protected fork files are missing or lost their markers.

Enforces ``hermes_cli.fork_policy.PROTECTED_FORK_CHECKS`` so an upstream sync
or accidental revert cannot silently restore Hermes product identity on the
paths this fork owns.

Run by the ``Nexus protected fork files`` step of
``.github/workflows/repo-guards.yml``. Locally:

    python3 scripts/ci/check_nexus_fork_files.py
    # or: just check-nexus-fork

Exit codes: 0 = intact, 1 = missing/reverted markers.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from hermes_cli.fork_policy import PROTECTED_FORK_CHECKS, check_protected_fork_files


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    problems = check_protected_fork_files(root)
    if not problems:
        print(f"::notice::Nexus protected fork files OK ({len(PROTECTED_FORK_CHECKS)} paths)")
        for rel, markers in PROTECTED_FORK_CHECKS:
            kind = "exists" if not markers else f"{len(markers)} marker(s)"
            print(f"  ✓ {rel} ({kind})")
        return 0
    print("::error::Nexus protected fork files failed — restore fork identity before merge:")
    for problem in problems:
        print(f"  ✗ {problem}")
    print()
    print("These paths are owned by the Nexus fork (see hermes_cli/fork_policy.py")
    print("and docs/UPSTREAM.md). Prefer ours when resolving upstream merges.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
