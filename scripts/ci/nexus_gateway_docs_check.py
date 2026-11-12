#!/usr/bin/env python3
"""Verify Nexus gateway recipe docs and that ``hermes gateway --help`` loads.

No bot tokens required. Usage:
  scripts/hermes-python scripts/ci/nexus_gateway_docs_check.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    os.chdir(ROOT)
    gateway = (ROOT / "docs/GATEWAY.md").read_text(encoding="utf-8")
    for marker in (
        "hermes gateway setup",
        "TELEGRAM_BOT_TOKEN",
        "DISCORD_BOT_TOKEN",
        "SLACK_BOT_TOKEN",
        "SLACK_APP_TOKEN",
        "TEAMS_CLIENT_ID",
        "TEAMS_CLIENT_SECRET",
        "TEAMS_TENANT_ID",
        "Microsoft Teams",
    ):
        if marker not in gateway:
            raise SystemExit(f"docs/GATEWAY.md missing marker: {marker}")
    print("✓ docs/GATEWAY.md recipes present")

    python = os.environ.get("HERMES_PYTHON") or os.environ.get("PYTHON") or sys.executable
    proc = subprocess.run(
        [python, str(ROOT / "hermes"), "gateway", "--help"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        raise SystemExit(f"hermes gateway --help failed ({proc.returncode}):\n{out}")
    if "gateway" not in out.lower():
        raise SystemExit(f"unexpected gateway help output:\n{out}")
    print("✓ hermes gateway --help OK")
    print("Nexus gateway docs checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
