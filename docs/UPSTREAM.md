# Upstream tracking

**Two GitHub repos:**

| Repo | Visibility | Purpose |
|------|------------|---------|
| [`codeflunky/nexus-agent-harness-dev`](https://github.com/codeflunky/nexus-agent-harness-dev) | Private | Day-to-day fork work, PRs, CI |
| [`codeflunky/nexus-agent-harness`](https://github.com/codeflunky/nexus-agent-harness) | Public | Install / release mirror for one-liners |

Upstream Hermes is a git remote only — not a second product. How to publish the
public mirror: [PUBLISH.md](PUBLISH.md).

## Update policy (Nexus)

| Command | What it does |
|---------|----------------|
| `hermes update` | Updates from **origin** only (this product checkout). Does **not** merge NousResearch/hermes-agent. |
| `hermes update --sync-upstream` | After origin update, may merge `upstream/main` (Hermes). Opt-in; can overwrite fork patches. |

ZIP fallback (when git update cannot run) downloads from
**`codeflunky/nexus-agent-harness`** (public), via `PRODUCT_REPOSITORY` in
[`hermes_cli/fork_policy.py`](../hermes_cli/fork_policy.py).

## Remotes (developer checkout)

```bash
# origin → private -dev (default after rename)
git remote -v

git remote add upstream https://github.com/NousResearch/hermes-agent.git
git remote add public https://github.com/codeflunky/nexus-agent-harness.git
git fetch upstream
```

## Sync cadence (pinned)

| Cadence | What |
|---------|------|
| **Monthly** | Planned `upstream/main` merge on a dated branch (`sync/upstream-YYYYMMDD`). Default for Nexus. |
| **Sooner** | Security advisories, critical runtime bugs, or dependency CVEs that affect CLI/TUI Linux. |
| **Not automatic** | `hermes update` never merges Hermes; only `hermes update --sync-upstream` or a manual git merge does. |

Record the last intentional sync in a PR description (and optionally a short note under *Verified baseline* below). Skip months when nothing material landed upstream.

## Syncing Hermes (deliberate)

Prefer a working branch — do **not** rely on `hermes update --sync-upstream` for routine merges:

```bash
git fetch upstream
git checkout -b sync/upstream-$(date +%Y%m%d)
git merge upstream/main
# resolve conflicts; keep protected fork files (below)
```

### Protected fork files (prefer ours)

Enforced by CI (`scripts/ci/check_nexus_fork_files.py`) from
`hermes_cli.fork_policy.PROTECTED_FORK_CHECKS` (paths + required Nexus markers).
Listed paths include:

| Path | Prefer |
|------|--------|
| `LICENSE`, `NOTICE` | Ours (MIT + required notices) |
| `README.md` | Ours (Craft Anything–style fork homepage) |
| `docs/STATUS.md`, `docs/UPSTREAM.md`, `docs/SECURE_DEFAULTS.md`, `docs/GATEWAY.md`, `docs/PROVIDERS.md`, `docs/WINDOWS.md`, `docs/PUBLISH.md` | Ours |
| `hermes_cli/config_defaults.py` (`approvals.mode: manual`) | Ours |
| `hermes_cli/fork_policy.py` | Ours |
| Nexus branding surfaces (`banner.py`, `skin_engine.py`, TUI theme/i18n, `assets/nexus-banner.png`) | Ours |
| Everything else | Upstream unless we have intentional fork patches |

## Verified baseline (Linux)

After sync, re-check:

```bash
bash setup-hermes.sh --runtime-only --test-environment
source ./activate
hermes --version
hermes doctor
just js-install
pnpm --dir ui-tui run build
```
