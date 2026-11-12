#!/usr/bin/env python3
"""Verify Nexus local + OAuth provider curation markers (no live logins or network).

Checks:
  1. docs/PROVIDERS.md covers local + OAuth + Bedrock triangle
  2. Registry overlays for nous / openai-codex / lmstudio / custom aliases
  3. ``hermes auth --help`` and ``hermes model --help`` load

Usage:
  scripts/hermes-python scripts/ci/nexus_providers_check.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _hermes(*args: str) -> str:
    python = os.environ.get("HERMES_PYTHON") or os.environ.get("PYTHON") or sys.executable
    proc = subprocess.run(
        [python, str(ROOT / "hermes"), *args],
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


def main() -> int:
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))

    docs = (ROOT / "docs/PROVIDERS.md").read_text(encoding="utf-8")
    for marker in (
        "Local (OpenAI-compatible)",
        "Ollama",
        "LM Studio",
        "custom:local",
        "OAuth",
        "nous",
        "openai-codex",
        "hermes setup --portal",
        "hermes auth add openai-codex",
        "us-gov-west-1",
        "Mantle",
    ):
        if marker not in docs:
            raise SystemExit(f"docs/PROVIDERS.md missing marker: {marker}")
    print("✓ docs/PROVIDERS.md local + OAuth recipes present")

    from hermes_cli.providers import ALIASES, HERMES_OVERLAYS, _ALIAS_GROUPS, _LABEL_OVERRIDES

    nous = HERMES_OVERLAYS.get("nous")
    if nous is None or getattr(nous, "auth_type", "") != "oauth_device_code":
        raise SystemExit(f"nous overlay auth_type unexpected: {nous!r}")
    codex = HERMES_OVERLAYS.get("openai-codex")
    if codex is None or getattr(codex, "auth_type", "") != "oauth_external":
        raise SystemExit(f"openai-codex overlay auth_type unexpected: {codex!r}")
    lm = HERMES_OVERLAYS.get("lmstudio")
    if lm is None or "1234" not in getattr(lm, "base_url_override", ""):
        raise SystemExit(f"lmstudio overlay base_url unexpected: {lm!r}")
    custom_aliases = set(_ALIAS_GROUPS.get("custom") or ())
    for alias in ("ollama", "local", "vllm"):
        if alias not in custom_aliases:
            raise SystemExit(f"custom provider missing alias {alias!r}")
        if ALIASES.get(alias) != "custom":
            raise SystemExit(f"alias {alias!r} should resolve to custom, got {ALIASES.get(alias)!r}")
    if "nous" not in _LABEL_OVERRIDES.get("nous", "").lower():
        raise SystemExit(f"nous label unexpected: {_LABEL_OVERRIDES.get('nous')!r}")
    print("✓ provider registry overlays OK (nous / openai-codex / lmstudio / custom)")

    auth_help = _hermes("auth", "--help").lower()
    if "auth" not in auth_help:
        raise SystemExit(f"unexpected hermes auth --help:\n{auth_help}")
    model_help = _hermes("model", "--help").lower()
    if "model" not in model_help:
        raise SystemExit(f"unexpected hermes model --help:\n{model_help}")
    print("✓ hermes auth --help / model --help OK")

    print("Nexus providers checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
