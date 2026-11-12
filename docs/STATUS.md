# Status and milestones

Early bootstrap of **nexus-agent-harness** as an MIT-licensed Hermes fork. Focus is **CLI/TUI on Linux**. Desktop (Windows/macOS) comes later.

## Works today

| Area | Notes |
|------|--------|
| Upstream import | `NousResearch/hermes-agent` merged into this repo; `upstream` remote documented |
| License | Root [LICENSE](../LICENSE) is MIT; required notices in [NOTICE](../NOTICE) |
| PM / Python | `setup-hermes.sh` + `source ./activate` → Python 3.14 toolchain |
| CLI | `hermes --version`, `--help`, `doctor`, subcommands load |
| TUI build | `pnpm --dir ui-tui run build` → `ui-tui/dist/entry.js` |
| TUI launch | `hermes --tui` on a TTY; clean `hermes-tui: no TTY` without one |

## Partly there

- Interactive agent sessions need provider/API setup (`hermes setup` / `.env`)
- Messaging gateway optional — recipes in [GATEWAY.md](GATEWAY.md); tokens not in fork defaults
- Desktop Electron app exists upstream under `apps/desktop` but is **out of scope** for the current milestone

## Next milestones

### M1 — CLI/TUI Linux baseline

- [x] Import upstream into this GitHub repo only
- [x] MIT license + NOTICE
- [x] Craft Anything–style README
- [x] Prove `hermes` + TUI build on Linux
- [x] Visible product rebrand to **Nexus** (TUI/CLI chrome; `hermes` / `~/.hermes` unchanged)
- [x] Minimal CI: `.github/workflows/nexus-smoke.yml` (version + doctor allowlist + first-run gate + secure-defaults markers + `ui-tui` build + protected-fork check); local `just nexus-smoke` / `just nexus-first-run` / `just nexus-secure-defaults`
- [x] Document known doctor warnings ([docs/DOCTOR.md](DOCTOR.md))

**M1 complete. M2 complete** (secure defaults + monthly sync cadence). **M3** first-run + gateway recipes landed; remaining: broader eval/smoke scripts.

### M2 — Harness hardening

- [x] Secure defaults for collaborative use (approvals, egress, secrets) — [docs/SECURE_DEFAULTS.md](SECURE_DEFAULTS.md); `approvals.mode: manual`; doctor perms / YOLO advisories; `just nexus-secure-defaults`
- [x] Clear fork identity in CLI banners / version strings without breaking upstream sync
- [x] Origin-only `hermes update` by default; Hermes merge via `--sync-upstream` / sync branch (`docs/UPSTREAM.md`, `hermes_cli/fork_policy.py`)
- [x] Protected fork files enforced in CI (`PROTECTED_FORK_CHECKS` + `scripts/ci/check_nexus_fork_files.py` in repo-guards)
- [x] Pin / document a recurring upstream sync cadence — monthly (sooner for security) in [docs/UPSTREAM.md](UPSTREAM.md)

### M3 — Product surfaces (still terminal-first)

- [x] Reliable first-run path: setup → model → chat/TUI — [docs/GETTING_STARTED.md](GETTING_STARTED.md); gate smoke `scripts/ci/nexus_first_run_check.py` (no live API keys)
- [x] Optional gateway recipes — [docs/GATEWAY.md](GATEWAY.md) (Telegram / Discord / Slack / Microsoft Teams); `just nexus-gateway-docs`
- [ ] Eval / smoke scripts for regressions beyond first-run / doctor

### M4 — Desktop Win/Mac (later)

- [ ] Revisit `apps/desktop` packaging after CLI/TUI is solid
- [ ] Windows and macOS installers / signed builds as a separate track
- [ ] Do not block Linux terminal work on Desktop

## Non-goals (for now)

- Publishing a second repository
- Replacing upstream's public install CDN as the primary distribution for this fork
- Shipping Desktop as part of M1–M3
