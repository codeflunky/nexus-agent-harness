"""Nexus fork update policy: origin-only by default + protected file markers."""

from pathlib import Path

from hermes_cli.fork_policy import (
    DEV_REPOSITORY,
    PRODUCT_REPOSITORY,
    PROTECTED_FORK_CHECKS,
    PROTECTED_FORK_PATHS,
    check_protected_fork_files,
    wants_upstream_sync,
)


def test_wants_upstream_sync_default_off_for_fork_main():
    assert wants_upstream_sync(
        is_fork=True, branch="main", release_sha=None, sync_upstream_flag=False
    ) is False


def test_wants_upstream_sync_opt_in():
    assert wants_upstream_sync(
        is_fork=True, branch="main", release_sha=None, sync_upstream_flag=True
    ) is True


def test_wants_upstream_sync_skips_non_main_and_releases():
    assert wants_upstream_sync(
        is_fork=True, branch="develop", release_sha=None, sync_upstream_flag=True
    ) is False
    assert wants_upstream_sync(
        is_fork=True, branch="main", release_sha="a" * 40, sync_upstream_flag=True
    ) is False
    assert wants_upstream_sync(
        is_fork=False, branch="main", release_sha=None, sync_upstream_flag=True
    ) is False


def test_product_repository_and_protected_paths():
    assert PRODUCT_REPOSITORY == "codeflunky/nexus-agent-harness"
    assert DEV_REPOSITORY == "codeflunky/nexus-agent-harness-dev"
    assert "hermes_cli/fork_policy.py" in PROTECTED_FORK_PATHS
    assert "LICENSE" in PROTECTED_FORK_PATHS
    assert "docs/PUBLISH.md" in PROTECTED_FORK_PATHS
    assert PROTECTED_FORK_PATHS == tuple(path for path, _ in PROTECTED_FORK_CHECKS)


def test_protected_fork_files_pass_on_repo_root():
    root = Path(__file__).resolve().parents[2]
    assert check_protected_fork_files(root) == []


def test_protected_fork_files_detect_missing_marker(tmp_path: Path):
    # Minimal tree: LICENSE missing Nexus contributor line should fail.
    (tmp_path / "LICENSE").write_text("MIT License\n", encoding="utf-8")
    problems = check_protected_fork_files(tmp_path)
    assert any("LICENSE" in p and "nexus-agent-harness contributors" in p for p in problems)
    assert any("missing protected fork file" in p for p in problems)
