#!/usr/bin/env python3
"""Nexus CLI/import regression smoke beyond first-run / doctor (no live API keys).

Checks:
  1. ``hermes --help`` loads with Nexus branding / core subcommands
  2. ``hermes model --help`` / ``hermes config --help`` / ``hermes setup --help``
  3. ``hermes_cli.fork_policy`` product identity + origin-only sync default

Does **not** run upstream ``evals/`` harnesses (live providers / long benches).

Usage:
  scripts/hermes-python scripts/ci/nexus_evals_smoke.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _hermes_cmd() -> list[str]:
    python = os.environ.get("HERMES_PYTHON") or os.environ.get("PYTHON") or sys.executable
    return [python, str(ROOT / "hermes")]


def _run(*args: str) -> str:
    proc = subprocess.run(
        [*_hermes_cmd(), *args],
        cwd=ROOT,
        env=os.environ.copy(),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        raise SystemExit(f"hermes {' '.join(args)} failed ({proc.returncode}):\n{out}")
    return out


def check_root_help() -> None:
    out = _run("--help")
    lower = out.lower()
    if "nexus" not in lower:
        raise SystemExit(f"hermes --help missing Nexus branding:\n{out}")
    for name in ("model", "config", "doctor", "gateway", "setup"):
        if name not in lower:
            raise SystemExit(f"hermes --help missing subcommand {name!r}:\n{out}")
    print("✓ hermes --help OK")


def check_subcommand_help() -> None:
    for sub in ("model", "config", "setup", "status"):
        out = _run(sub, "--help")
        if sub not in out.lower():
            raise SystemExit(f"hermes {sub} --help unexpected:\n{out}")
        print(f"✓ hermes {sub} --help OK")


def check_fork_policy_import() -> None:
    sys.path.insert(0, str(ROOT))
    from hermes_cli import fork_policy as fp

    if fp.PRODUCT_NAME != "Nexus Agent":
        raise SystemExit(f"PRODUCT_NAME={fp.PRODUCT_NAME!r}")
    if fp.PRODUCT_REPOSITORY != "codeflunky/nexus-agent-harness":
        raise SystemExit(f"PRODUCT_REPOSITORY={fp.PRODUCT_REPOSITORY!r}")
    if not fp.PROTECTED_FORK_CHECKS:
        raise SystemExit("PROTECTED_FORK_CHECKS empty")
    if fp.wants_upstream_sync(
        is_fork=True, branch="main", release_sha=None, sync_upstream_flag=False
    ):
        raise SystemExit("wants_upstream_sync should be False without --sync-upstream")
    if not fp.wants_upstream_sync(
        is_fork=True, branch="main", release_sha=None, sync_upstream_flag=True
    ):
        raise SystemExit("wants_upstream_sync should be True with --sync-upstream")
    print("✓ hermes_cli.fork_policy import OK")


def main() -> int:
    os.chdir(ROOT)
    check_root_help()
    check_subcommand_help()
    check_fork_policy_import()
    print("Nexus evals smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
