# `hermes doctor` — expected warnings (Nexus)

`hermes doctor` exits **1** when anything remains to configure. That is normal on a fresh Nexus checkout without provider keys. CI (`scripts/ci/nexus_smoke.py`) allows the setup-gap issues below and fails on unexpected ones.

## Healthy enough for CLI/TUI work

After `source ./activate` (or PM setup), these are **OK to ignore** until you need the feature:

| Finding | Meaning | When to fix |
|---------|---------|-------------|
| `.env` missing / “Run `hermes setup` to create `.env`” | No local secrets yet | Before first real chat: `hermes setup` |
| Missing API keys / OpenRouter not configured | No inference provider | `hermes setup` or `hermes model` |
| OAuth not logged in (Nous Portal, Codex, MiniMax, xAI, …) | Optional auth backends | Only if you use that provider |
| Docker/Podman not found (optional) | No container terminal backend | Only if you want Docker/SSH sandbox backends |
| Optional packages (`discord.py`, `python-telegram-bot`, …) | Messaging extras not installed | Gateway / platform features |
| Discord / X / other tool tokens missing | Platform tools disabled | When enabling that tool |
| Chromium not installed | Local browser tool unavailable | Browser automation |
| Skills Hub not initialized | Skills catalog not pulled | `hermes skills list` when you need it |
| `computer_use` / `vision` / `video` “system dependency not met” | Optional multimodal stacks | When you need those tools |

## Blocking for day-to-day use

Fix these before expecting a working interactive agent:

1. **Create `.env` and pick a model/provider** — `hermes setup` (or `hermes model`).
2. **Confirm `hermes --version` shows Nexus Agent** and the PM env is activated (`source ./activate`).

## Install / PATH noise

On some machines doctor also reports launcher/symlink gaps:

- Nexus entry point / “Repair or reinstall the Nexus launcher…”
- Missing `~/.local/bin/hermes` symlink
- `~/.local/bin` not on `PATH`

From a PM-activated checkout, `python hermes …` (or the activated `hermes` function) is enough. To publish a user command: `hermes doctor --fix` or ensure `~/.local/bin` is on `PATH`.

## CI allowlist

The Nexus smoke job treats only these **numbered issues** as non-fatal (see `scripts/ci/nexus_smoke.py`):

- Run `hermes setup` to create `.env`
- Run `hermes setup` to configure missing API keys…
- Repair or reinstall the Nexus launcher…
- Missing `~/.local/bin/hermes` symlink…
- Add `~/.local/bin` to your PATH

Anything else listed under “issue(s) to address” fails CI.

## Quick check

```bash
source ./activate
hermes doctor          # warnings OK; note the numbered issues
hermes setup           # when ready to chat
hermes --tui           # needs a real TTY
```
