<p align="center">
  <img src="assets/banner.png" alt="Nexus Agent Harness" width="100%">
</p>

<div align="center">

# Nexus Agent Harness

**An MIT-licensed Hermes fork — secure collaborative agent harness, CLI/TUI first.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Upstream](https://img.shields.io/badge/Upstream-NousResearch%2Fhermes--agent-blue?style=for-the-badge)](https://github.com/NousResearch/hermes-agent)
[![Focus](https://img.shields.io/badge/Focus-CLI%20%2F%20TUI-0ea5e9?style=for-the-badge)](#get-started)
[![Platform](https://img.shields.io/badge/Linux-ready-informational?style=for-the-badge)](#status)
[![Desktop](https://img.shields.io/badge/Desktop-Win%2FMac%20later-lightgrey?style=for-the-badge)](#status)

`hermes` · `hermes --tui` · Linux now · Desktop later

[How it works](#how-it-works) ·
[Status](#status) ·
[Get started](#get-started) ·
[Upstream](#upstream) ·
[License](#license-and-credits)

</div>

---

| | |
|---|---|
| **Terminal-first** | Classic CLI plus Ink TUI — multiline chat, slash commands, streaming tools. |
| **Same agent core** | Sessions, skills, memory, and providers from upstream Hermes. |
| **Fork, not a second repo** | All work lives in this GitHub repository; upstream is tracked as a git remote. |
| **Desktop later** | Windows/macOS desktop packaging is a later milestone, not the current focus. |

## How it works

1. **Provision** — `setup-hermes.sh` / `source ./activate` installs the PM-pinned Python 3.14 toolchain, Node, pnpm, and deps.
2. **Talk** — `hermes` opens the classic CLI; `hermes --tui` launches the modern terminal UI (needs a TTY and Node ≥ 20).
3. **Configure** — `hermes setup` / `hermes model` / `hermes doctor` wire providers and check the install.
4. **Extend** — skills, plugins, gateway channels, and cron stay available from upstream; we prioritize hardening the harness surface next.

## Get started

**Linux (from this repo):**

```bash
git clone https://github.com/codeflunky/nexus-agent-harness
cd nexus-agent-harness
bash setup-hermes.sh --runtime-only --test-environment
source ./activate          # each new shell
hermes --version
hermes doctor
```

**TUI (interactive terminal):**

```bash
just js-install            # once, after activate
pnpm --dir ui-tui run build
hermes --tui
```

Without a TTY, `hermes --tui` exits with `hermes-tui: no TTY` (expected in CI/pipes). Use a real terminal for interactive TUI.

**Useful commands:**

```bash
hermes              # classic interactive CLI
hermes --tui        # Ink TUI
hermes model        # pick provider / model
hermes setup        # wizard
hermes doctor       # diagnose the install
```

Upstream one-liner installs and Desktop packages still belong to [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent); this fork is meant to be developed and run from source.

## Status

> [!IMPORTANT]
> **Status:** early fork bootstrap. What works today, what is partial, and what's next:
>
> - **Works today (Linux):** import of [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent); MIT root license + [NOTICE](NOTICE); PM setup; `hermes` CLI (`--version`, `--help`, `doctor`); `ui-tui` build (`ui-tui/dist/entry.js`); TTY-gated `hermes --tui`.
> - **Partly there:** full interactive chat needs API keys via `hermes setup`; gateway/messaging channels unconfigured by default; Desktop app not a current deliverable.
> - **Next:** see [docs/STATUS.md](docs/STATUS.md) — harness hardening, CI for CLI/TUI on Linux, upstream sync cadence, then Desktop Win/Mac.

## Upstream

This repository **is** the fork. Do not invent a second remote product repo.

```bash
git remote add upstream https://github.com/NousResearch/hermes-agent.git   # once
git fetch upstream
git merge upstream/main   # or rebase, on a working branch
```

Details and sync notes: [docs/UPSTREAM.md](docs/UPSTREAM.md).

## License and credits

Nexus Agent Harness is licensed under the [MIT License](LICENSE).

- Upstream Hermes Agent © Nous Research — [https://github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- Required third-party notices (including Apache-2.0 attribution for `plugins/security-guidance`) are in [NOTICE](NOTICE)

Bundled skills and plugins may keep their own `LICENSE` files; those terms still apply to those components.
