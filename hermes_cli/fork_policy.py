"""Nexus fork update / sync policy.

This checkout's product remote is ``origin`` (codeflunky/nexus-agent-harness).
``hermes update`` refreshes from that remote. Merging NousResearch/hermes-agent
is opt-in only (``hermes update --sync-upstream``), so an update cannot silently
overwrite Nexus branding and other fork patches.

``PROTECTED_FORK_CHECKS`` is the enforcement contract: CI
(``scripts/ci/check_nexus_fork_files.py``) requires each path to exist and
contain the listed markers (empty marker tuple = existence only).
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

# Display name for user-facing update copy.
PRODUCT_NAME = "Nexus Agent"

# GitHub identity of this product repository (ZIP fallback / clone hints).
PRODUCT_REPOSITORY = "codeflunky/nexus-agent-harness"
PRODUCT_CLONE_URL = f"https://github.com/{PRODUCT_REPOSITORY}.git"

# Upstream Hermes (deliberate sync only).
UPSTREAM_REPOSITORY = "NousResearch/hermes-agent"
UPSTREAM_CLONE_URL = f"https://github.com/{UPSTREAM_REPOSITORY}.git"

# (relative path, required UTF-8 substrings). Empty markers => file must exist.
# Keep this list tight: every entry is blocking in CI.
PROTECTED_FORK_CHECKS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("LICENSE", ("MIT License", "nexus-agent-harness contributors")),
    ("NOTICE", ("nexus-agent-harness", "MIT-licensed fork of Hermes Agent")),
    (
        "README.md",
        (
            "Nexus Agent",
            "assets/nexus-banner.png",
            "codeflunky/nexus-agent-harness",
        ),
    ),
    ("docs/STATUS.md", ("Nexus", "Origin-only", "M1 complete", "M2 complete")),
    (
        "docs/UPSTREAM.md",
        (
            "PROTECTED_FORK",
            "Updates from **origin** only",
            "codeflunky/nexus-agent-harness",
            "Sync cadence",
            "Monthly",
        ),
    ),
    ("docs/DOCTOR.md", ("hermes doctor", "expected warnings", "Nexus")),
    (
        "docs/GETTING_STARTED.md",
        ("setup → model → chat", "hermes setup", "Nexus isn't configured yet"),
    ),
    (
        "docs/SECURE_DEFAULTS.md",
        ("mode: manual", "chmod 600", "collaborative"),
    ),
    (
        "docs/GATEWAY.md",
        (
            "hermes gateway setup",
            "TELEGRAM_BOT_TOKEN",
            "DISCORD_BOT_TOKEN",
            "SLACK_BOT_TOKEN",
            "TEAMS_CLIENT_ID",
            "Microsoft Teams",
        ),
    ),
    (
        "hermes_cli/config_defaults.py",
        ("Nexus collaborative default", '"mode": "manual"'),
    ),
    (
        "hermes_cli/fork_policy.py",
        ("PROTECTED_FORK_CHECKS", "PRODUCT_REPOSITORY", "wants_upstream_sync"),
    ),
    ("hermes_cli/skin_engine.py", ('"Nexus"', "Classic Nexus")),
    ("hermes_cli/banner.py", ("Nexus Agent v",)),
    ("hermes_cli/doctor.py", ("Nexus Doctor",)),
    ("hermes_cli/setup.py", ("Nexus Agent Setup Wizard",)),
    ("hermes_cli/status.py", ("Nexus Agent Status",)),
    ("assets/nexus-banner.png", ()),
    ("ui-tui/src/theme.ts", ("Nexus Agent",)),
    ("ui-tui/src/i18n/en/chrome.ts", ("summoning nexus",)),
)

PROTECTED_FORK_PATHS: tuple[str, ...] = tuple(path for path, _ in PROTECTED_FORK_CHECKS)


def wants_upstream_sync(
    *,
    is_fork: bool,
    branch: str,
    release_sha: Optional[str],
    sync_upstream_flag: bool,
) -> bool:
    """True only when an explicit ``--sync-upstream`` requests Hermes upstream merge.

    Default ``hermes update`` on this fork never auto-merges ``upstream/main``.
    """
    return bool(
        is_fork
        and branch == "main"
        and not release_sha
        and sync_upstream_flag
    )


def check_protected_fork_files(root: Path | str | None = None) -> list[str]:
    """Return human-readable problems for missing/reverted protected fork files.

    An empty list means the fork identity markers are intact.
    """
    base = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    problems: list[str] = []
    for rel, markers in PROTECTED_FORK_CHECKS:
        path = base / rel
        if not path.exists():
            problems.append(f"missing protected fork file: {rel}")
            continue
        if path.is_dir():
            problems.append(f"protected fork path must be a file, not a directory: {rel}")
            continue
        if not markers:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Binary assets (e.g. banner PNG): existence-only checks use empty markers.
            problems.append(f"protected fork file is not UTF-8 text (add empty markers if binary): {rel}")
            continue
        missing = [m for m in markers if m not in text]
        if missing:
            shown = ", ".join(repr(m) for m in missing)
            problems.append(f"{rel}: missing required Nexus marker(s): {shown}")
    return problems


def iter_protected_paths() -> Iterable[str]:
    """Yield protected relative paths (for docs / update copy)."""
    yield from PROTECTED_FORK_PATHS
