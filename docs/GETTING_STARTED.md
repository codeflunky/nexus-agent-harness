# Getting started (Nexus, Linux source)

End-to-end path: **toolchain → setup → model → chat / TUI**.

This fork is developed from source in this repo. Upstream CDN installers are optional; prefer the steps below.

## 1. Provision the checkout

```bash
git clone https://github.com/codeflunky/nexus-agent-harness
cd nexus-agent-harness
bash setup-hermes.sh --runtime-only --test-environment
source ./activate          # each new shell
hermes --version           # must say Nexus Agent
```

Optional TUI build (once per lockfile change):

```bash
just js-install
pnpm --dir ui-tui run build
```

## 2. Configure a provider (first run)

Classic CLI and `hermes chat` refuse to start until a provider is configured.
You’ll see:

```text
It looks like Nexus isn't configured yet -- no API keys or providers found.
  Run:  hermes setup
```

### Interactive (recommended)

```bash
hermes setup               # full wizard
# or:
hermes setup model         # provider + default model only
hermes setup --portal      # Nous Portal one-shot (OAuth)
```

On a TTY, bare `hermes` may offer to run setup for you.

### Headless / CI (no wizard)

`hermes setup --non-interactive` prints guidance only; it does **not** write keys.
Set secrets yourself:

```bash
mkdir -p "${HERMES_HOME:-$HOME/.hermes}"
# Example: OpenRouter
printf 'OPENROUTER_API_KEY=sk-or-...\n' >> "${HERMES_HOME:-$HOME/.hermes}/.env"
chmod 600 "${HERMES_HOME:-$HOME/.hermes}/.env"

hermes config set model.provider openrouter
hermes config set model.default openrouter/auto
```

Other common env keys: `OPENAI_API_KEY`, `OPENAI_BASE_URL` (local OpenAI-compatible),
or complete OAuth via `hermes model` / `hermes setup --portal` on a TTY.

## 3. Chat

```bash
hermes                     # classic CLI (default)
hermes --tui               # Ink TUI (needs a real TTY + ui-tui build)
hermes chat -q "hello"     # one-shot (non-interactive)
```

TUI skips the classic first-run prompt and shows **Setup Required** in-app until a provider exists; use `/setup` or exit and run `hermes setup`.

## 4. Verify

```bash
hermes doctor              # exit 1 with only setup gaps is OK — see docs/DOCTOR.md
just nexus-smoke           # version + doctor allowlist
just nexus-first-run       # unconfigured gate + setup guidance + provider probe
```

## What “configured” means

Any one of:

- A provider API key in the environment or `$HERMES_HOME/.env`
- OAuth credentials in `$HERMES_HOME` auth store
- `config.yaml` `model` with `provider` / `base_url` / `api_key`

Probe: `hermes_cli.main._has_any_provider_configured()`.

## Related

- [docs/SECURE_DEFAULTS.md](SECURE_DEFAULTS.md) — approvals, secrets, egress  
- [docs/GATEWAY.md](GATEWAY.md) — Telegram / Discord / Slack recipes  
- [docs/DOCTOR.md](DOCTOR.md) — expected doctor warnings  
- [docs/STATUS.md](STATUS.md) — milestones  
- [docs/UPSTREAM.md](UPSTREAM.md) — origin-only updates / Hermes sync cadence  
