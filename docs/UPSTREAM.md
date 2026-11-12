# Upstream tracking

**Single repo:** all fork work stays in [codeflunky/nexus-agent-harness](https://github.com/codeflunky/nexus-agent-harness). Upstream is a git remote, not a second product repository.

## Remote

```bash
git remote add upstream https://github.com/NousResearch/hermes-agent.git
git fetch upstream
```

Initial import used `git merge upstream/main --allow-unrelated-histories` onto the previous empty-repo history.

## Syncing

Prefer a working branch:

```bash
git fetch upstream
git checkout -b sync/upstream-$(date +%Y%m%d)
git merge upstream/main
# resolve conflicts; keep our LICENSE, NOTICE, README.md, docs/STATUS.md, docs/UPSTREAM.md
```

Expect recurring conflict surfaces:

| Path | Prefer |
|------|--------|
| `LICENSE`, `NOTICE` | Ours (MIT + required notices) |
| `README.md` | Ours (Craft Anything–style fork homepage) |
| `docs/STATUS.md`, `docs/UPSTREAM.md` | Ours |
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
