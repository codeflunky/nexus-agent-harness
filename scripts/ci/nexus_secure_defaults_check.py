#!/usr/bin/env python3
"""Verify Nexus M2 secure-default markers without live API keys.

Checks:
  1. ``DEFAULT_CONFIG["approvals"]["mode"]`` is ``manual``
  2. ``docs/SECURE_DEFAULTS.md`` and monthly sync cadence docs exist
  3. ``path_has_group_or_other_access`` flags a deliberately loose ``.env``

Usage:
  scripts/hermes-python scripts/ci/nexus_secure_defaults_check.py
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))

    from hermes_cli.config_defaults import DEFAULT_CONFIG
    from hermes_cli.doctor_config import path_has_group_or_other_access

    mode = (DEFAULT_CONFIG.get("approvals") or {}).get("mode")
    if mode != "manual":
        raise SystemExit(f"expected approvals.mode default 'manual', got {mode!r}")
    print("✓ approvals.mode default is manual")

    secure = (ROOT / "docs/SECURE_DEFAULTS.md").read_text(encoding="utf-8")
    for marker in ("approvals:", "mode: manual", "chmod 600", "docker_network"):
        if marker not in secure:
            raise SystemExit(f"docs/SECURE_DEFAULTS.md missing marker: {marker}")
    print("✓ docs/SECURE_DEFAULTS.md present")

    upstream = (ROOT / "docs/UPSTREAM.md").read_text(encoding="utf-8")
    if "Sync cadence" not in upstream or "Monthly" not in upstream:
        raise SystemExit("docs/UPSTREAM.md missing Sync cadence / Monthly pin")
    print("✓ upstream sync cadence documented")

    example = (ROOT / "cli-config.yaml.example").read_text(encoding="utf-8")
    if "Approvals (Nexus collaborative defaults" not in example:
        raise SystemExit("cli-config.yaml.example missing Nexus approvals section")
    print("✓ cli-config.yaml.example approvals section present")

    with tempfile.TemporaryDirectory(prefix="nexus-secure-") as tmp:
        env_path = Path(tmp) / ".env"
        env_path.write_text("OPENROUTER_API_KEY=dummy\n", encoding="utf-8")
        os.chmod(env_path, 0o644)
        if not path_has_group_or_other_access(env_path):
            raise SystemExit("path_has_group_or_other_access failed to detect 0644 .env")
        os.chmod(env_path, 0o600)
        if path_has_group_or_other_access(env_path):
            raise SystemExit("path_has_group_or_other_access false-positive on 0600 .env")
    print("✓ secret path permission probe OK")

    print("Nexus secure-defaults checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
