"""Nexus fork update / sync policy.

This checkout's product remote is ``origin`` (codeflunky/nexus-agent-harness).
``hermes update`` refreshes from that remote. Merging NousResearch/hermes-agent
is opt-in only (``hermes update --sync-upstream``), so an update cannot silently
overwrite Nexus branding and other fork patches.
"""

from __future__ import annotations

from typing import Optional

# Display name for user-facing update copy.
PRODUCT_NAME = "Nexus Agent"

# GitHub identity of this product repository (ZIP fallback / clone hints).
PRODUCT_REPOSITORY = "codeflunky/nexus-agent-harness"
PRODUCT_CLONE_URL = f"https://github.com/{PRODUCT_REPOSITORY}.git"

# Upstream Hermes (deliberate sync only).
UPSTREAM_REPOSITORY = "NousResearch/hermes-agent"
UPSTREAM_CLONE_URL = f"https://github.com/{UPSTREAM_REPOSITORY}.git"

# Paths this fork owns across upstream merges. Sync workflows should prefer ours.
PROTECTED_FORK_PATHS: tuple[str, ...] = (
    "LICENSE",
    "NOTICE",
    "README.md",
    "docs/STATUS.md",
    "docs/UPSTREAM.md",
    "hermes_cli/fork_policy.py",
    "hermes_cli/skin_engine.py",
    "hermes_cli/banner.py",
    "assets/nexus-banner.png",
    "ui-tui/src/theme.ts",
    "ui-tui/src/i18n/en",
)


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
