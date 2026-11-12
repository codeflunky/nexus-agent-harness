"""Nexus fork update policy: origin-only by default."""

from hermes_cli.fork_policy import (
    PRODUCT_REPOSITORY,
    PROTECTED_FORK_PATHS,
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
    assert "hermes_cli/fork_policy.py" in PROTECTED_FORK_PATHS
    assert "LICENSE" in PROTECTED_FORK_PATHS
