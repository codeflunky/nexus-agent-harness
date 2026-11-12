# Upstream tracking

**Single repo:** all fork work stays in [codeflunky/nexus-agent-harness](https://github.com/codeflunky/nexus-agent-harness). Upstream is a git remote, not a second product repository.

## Update policy (Nexus)

| Command | What it does |
|---------|----------------|
| `hermes update` | Updates from **origin** only (this product repo). Does **not** merge NousResearch/hermes-agent. |
| `hermes update --sync-upstream` | After origin update, may merge `upstream/main` (Hermes). Opt-in; can overwrite fork patches. |

ZIP fallback (when git update cannot run) downloads from **this checkout’s origin** GitHub repo, not from NousResearch by default.

Policy code: [`hermes_cli/fork_policy.py`](../hermes_cli/fork_policy.py).

## Remote

```bash
git remote add upstream https://github.com/NousResearch/hermes-agent.git
git fetch upstream
```

## Syncing Hermes (deliberate)

Prefer a working branch — do **not** rely on `hermes update --sync-upstream` for routine merges:

```bash
git fetch upstream
git checkout -b sync/upstream-$(date +%Y%m%d)
git merge upstream/main
# resolve conflicts; keep protected fork files (below)
```

### Protected fork files (prefer ours)

Listed in `hermes_cli.fork_policy.PROTECTED_FORK_PATHS`, including:

| Path | Prefer |
|------|--------|
| `LICENSE`, `NOTICE` | Ours (MIT + required notices) |
| `README.md` | Ours (Craft Anything–style fork homepage) |
| `docs/STATUS.md`, `docs/UPSTREAM.md` | Ours |
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
