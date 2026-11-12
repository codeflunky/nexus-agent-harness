#!/usr/bin/env python3
"""Minimal Nexus CLI/TUI smoke for CI and local use.

Checks:
  1. ``hermes --version`` reports Nexus Agent
  2. ``hermes doctor`` runs and only reports allowlisted setup gaps
     (missing .env / API keys are expected without secrets in CI)
  3. Optional: build ``ui-tui`` (``--tui``)

Usage:
  python3 scripts/ci/nexus_smoke.py
  python3 scripts/ci/nexus_smoke.py --tui
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Doctor returns exit 1 when any issues remain. In CI we have no provider keys
# and often no ~/.local/bin launcher link; these are expected "configure me"
# findings, not toolchain breakage.
_ALLOWED_DOCTOR_ISSUES = (
    "Run 'hermes setup' to create .env",
    "Run 'hermes setup' to configure missing API keys",
    "Run 'hermes setup' to configure missing API keys for full tool access",
    "Repair or reinstall the Nexus launcher through the installation owner",
    "Missing ~/.local/bin/hermes symlink — run 'hermes doctor --fix'",
    "Add ~/.local/bin to your PATH",
)

_ISSUE_LINE = re.compile(r"^\s*\d+\.\s+(.*\S)\s*$")


def _run(cmd: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=ROOT,
        env=env or os.environ.copy(),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def _hermes_cmd() -> list[str]:
    # Prefer the activated interpreter; fall back to repo launcher.
    python = os.environ.get("HERMES_PYTHON") or os.environ.get("PYTHON") or sys.executable
    return [python, str(ROOT / "hermes")]


def check_version() -> None:
    proc = _run([*_hermes_cmd(), "--version"])
    out = (proc.stdout or "") + (proc.stderr or "")
    print(out.rstrip())
    if proc.returncode != 0:
        raise SystemExit(f"hermes --version failed (exit {proc.returncode})")
    if "Nexus Agent" not in out:
        raise SystemExit("hermes --version did not report 'Nexus Agent'")
    print("✓ version smoke OK")


def check_doctor() -> None:
    proc = _run([*_hermes_cmd(), "doctor"])
    out = (proc.stdout or "") + (proc.stderr or "")
    print(out.rstrip())
    if "Nexus Doctor" not in out:
        raise SystemExit("hermes doctor did not show 'Nexus Doctor' banner")

    issues = [m.group(1) for m in (_ISSUE_LINE.match(line) for line in out.splitlines()) if m]
    unexpected = [issue for issue in issues if not any(issue.startswith(a) or issue == a for a in _ALLOWED_DOCTOR_ISSUES)]
    # Also allow substring match for slight wording drift
    unexpected = [
        issue
        for issue in unexpected
        if not any(allowed in issue for allowed in _ALLOWED_DOCTOR_ISSUES)
    ]
    if unexpected:
        joined = "\n  - ".join(unexpected)
        raise SystemExit(f"hermes doctor reported unexpected issue(s):\n  - {joined}")

    if proc.returncode not in (0, 1):
        raise SystemExit(f"hermes doctor crashed (exit {proc.returncode})")
    print("✓ doctor smoke OK (allowlisted setup gaps only)" if issues else "✓ doctor smoke OK (clean)")


def check_tui_build() -> None:
    install = _run(
        ["pnpm", "install", "--frozen-lockfile", "--filter", "{./ui-tui}...", "--ignore-scripts"]
    )
    sys.stdout.write(install.stdout or "")
    sys.stderr.write(install.stderr or "")
    if install.returncode != 0:
        raise SystemExit(f"pnpm install for ui-tui failed (exit {install.returncode})")

    build = _run(["pnpm", "--dir", "ui-tui", "run", "build"])
    sys.stdout.write(build.stdout or "")
    sys.stderr.write(build.stderr or "")
    if build.returncode != 0:
        raise SystemExit(f"ui-tui build failed (exit {build.returncode})")

    entry = ROOT / "ui-tui" / "dist" / "entry.js"
    if not entry.is_file():
        raise SystemExit(f"ui-tui build missing {entry.relative_to(ROOT)}")
    print(f"✓ TUI build OK ({entry.relative_to(ROOT)})")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tui", action="store_true", help="Also install+build ui-tui")
    parser.add_argument("--skip-doctor", action="store_true", help="Skip doctor smoke")
    args = parser.parse_args()

    os.chdir(ROOT)
    check_version()
    if not args.skip_doctor:
        check_doctor()
    if args.tui:
        check_tui_build()
    print("Nexus smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
