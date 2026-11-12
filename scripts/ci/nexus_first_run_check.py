#!/usr/bin/env python3
"""Verify the Nexus first-run gate (setup → provider → chat) without live API calls.

Checks:
  1. Unconfigured home: classic ``hermes chat -q`` exits 1 with Nexus first-run copy
  2. ``hermes setup --non-interactive`` prints Nexus headless guidance
  3. With a dummy provider env var, ``_has_any_provider_configured()`` is true

Usage:
  python3 scripts/ci/nexus_first_run_check.py
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _hermes(env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
    python = env.get("HERMES_PYTHON") or env.get("PYTHON") or sys.executable
    return subprocess.run(
        [python, str(ROOT / "hermes"), *args],
        cwd=ROOT,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def _base_env(home: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["HERMES_HOME"] = str(home)
    # Avoid inheriting a developer’s keys into the “unconfigured” probe.
    for key in list(env):
        if key.endswith("_API_KEY") or key in {
            "OPENAI_BASE_URL",
            "OPENROUTER_API_KEY",
            "ANTHROPIC_API_KEY",
            "HERMES_API_KEY",
        }:
            env.pop(key, None)
    return env


def check_unconfigured_guard(home: Path) -> None:
    env = _base_env(home)
    proc = _hermes(env, "chat", "--cli", "-q", "ping")
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 1:
        raise SystemExit(f"expected exit 1 when unconfigured, got {proc.returncode}\n{out}")
    if "Nexus isn't configured yet" not in out:
        raise SystemExit(f"missing Nexus first-run message:\n{out}")
    if "hermes setup" not in out:
        raise SystemExit(f"missing setup hint:\n{out}")
    print("✓ unconfigured classic chat is gated")


def check_noninteractive_setup(home: Path) -> None:
    env = _base_env(home)
    proc = _hermes(env, "setup", "--non-interactive")
    out = (proc.stdout or "") + (proc.stderr or "")
    if "Nexus Setup — Non-interactive mode" not in out:
        raise SystemExit(f"missing non-interactive Nexus setup banner:\n{out}")
    if "OPENROUTER_API_KEY" not in out and "hermes config set" not in out:
        raise SystemExit(f"missing headless configuration guidance:\n{out}")
    print("✓ non-interactive setup guidance OK")


def check_provider_probe(home: Path) -> None:
    env = _base_env(home)
    env["OPENROUTER_API_KEY"] = "sk-or-nexus-first-run-check-dummy"
    # Import after env is set so dotenv/provider probe sees the key.
    sys.path.insert(0, str(ROOT))
    os.environ.update({k: v for k, v in env.items() if k.startswith("HERMES") or k.endswith("_API_KEY")})
    os.environ["HERMES_HOME"] = str(home)
    os.environ["OPENROUTER_API_KEY"] = env["OPENROUTER_API_KEY"]
    from hermes_cli.main import _has_any_provider_configured

    if not _has_any_provider_configured():
        raise SystemExit("_has_any_provider_configured() false with OPENROUTER_API_KEY set")
    print("✓ provider probe accepts OPENROUTER_API_KEY")


def main() -> int:
    os.chdir(ROOT)
    with tempfile.TemporaryDirectory(prefix="nexus-first-run-") as tmp:
        home = Path(tmp)
        check_unconfigured_guard(home)
        check_noninteractive_setup(home)
        check_provider_probe(home)
    print("Nexus first-run checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
