# Provider curation (Nexus)

Nexus keeps upstream providers, then **curates** the paths that fit a collaborative
harness: **AWS Bedrock / Mantle (GovCloud)**, **local OpenAI-compatible**,
**OAuth logins**, and **OpenRouter** (one API key → many models).

| Need | Path |
|------|------|
| FedRAMP / GovCloud Claude–Nova | Bedrock Converse + IAM role/SSO (+ FIPS) |
| GovCloud **ChatGPT** models | Bedrock **Mantle** (bearer or SigV4) |
| Air-gapped / private GPU | **Local** OpenAI-compatible (`/v1`) |
| Cloud login without API keys | **OAuth** (Nous Portal, OpenAI Codex, …) |
| Day-one multi-model with one key | **OpenRouter** (`OPENROUTER_API_KEY`) |

Upstream deep dives: [integrations/providers.md](../website/docs/integrations/providers.md),
[aws-bedrock.md](../website/docs/guides/aws-bedrock.md),
[provider routing](../website/docs/user-guide/features/provider-routing.md).

---

## Local (OpenAI-compatible)

Point Nexus at a model server **you** run. No cloud inference key is required for
many local stacks.

| Stack | Base URL | Notes |
|-------|----------|--------|
| **Ollama** | `http://localhost:11434/v1` | Usually no API key |
| **LM Studio** | `http://127.0.0.1:1234/v1` | First-class `lmstudio` provider; or custom |
| **vLLM / SGLang / llama.cpp** | `http://localhost:8000/v1` (etc.) | Optional key |
| **On-prem NIM / other** | your `…/v1` | Use placeholder key if authless |

### Wizard

```bash
hermes model
# → Custom endpoint  (aliases: ollama / local / vllm …)
#    URL: http://localhost:11434/v1
#    API key: skip for local
# or → LM Studio (defaults to http://127.0.0.1:1234/v1)
```

### Config examples

**Named local (recommended):**

```yaml
providers:
  local:
    base_url: http://localhost:11434/v1
    # api_key: optional
model:
  provider: custom:local
  default: qwen2.5          # whatever /v1/models reports
```

**LM Studio:**

```yaml
model:
  provider: lmstudio
  default: <model-id>
# optional: LM_BASE_URL / LM_API_KEY in ~/.hermes/.env
```

**Generic custom:**

```yaml
model:
  provider: custom
  base_url: http://localhost:8000/v1
  default: my-model
```

### Local caveats (Nexus)

- Prefer `approvals.mode: manual` on shared machines ([SECURE_DEFAULTS.md](SECURE_DEFAULTS.md)).
- Full default toolsets can overflow small context windows — shrink tools or raise context.
- Gateway hosts must be able to reach the URL (loopback on a laptop ≠ loopback on a server).
- Do not commit local URLs with secrets; leave keys empty when the server is authless.

---

## OAuth (login, not long-lived API keys)

Sign in once; Hermes stores refreshable tokens under `$HERMES_HOME` (typically
`auth.json`, mode `600`). Prefer this over pasting cloud API keys into `.env` for
laptop / interactive use.

| Provider | ID | How to start |
|----------|-----|----------------|
| **Nous Portal** | `nous` | `hermes setup --portal` or `hermes model` → Nous |
| **OpenAI Codex / ChatGPT** | `openai-codex` | `hermes auth add openai-codex` or `hermes model` |
| xAI Grok OAuth | `xai-oauth` | `hermes model` / `hermes auth add xai-oauth` |
| Qwen OAuth | `qwen-oauth` | `hermes auth add qwen-oauth` |
| MiniMax OAuth | `minimax-oauth` | `hermes auth add minimax-oauth` |

### Recipes (highest leverage)

**Nous Portal (device code):**

```bash
hermes setup --portal
# or
hermes model    # pick Nous Portal → follow device-code prompt
hermes doctor   # OAuth “not logged in” clears after success
```

**OpenAI Codex (device code default; browser PKCE optional):**

```bash
hermes auth add openai-codex
# Organizations that disable device code:
hermes auth add openai-codex --browser
# Over SSH, tunnel the PKCE callback port — see upstream oauth-over-ssh guide
```

Tokens live in Hermes’ auth store (not `OPENAI_API_KEY`). Optional import from an
existing Codex CLI `~/.codex/auth.json` when present.

### OAuth vs API key vs AWS role

| Situation | Prefer |
|-----------|--------|
| Interactive laptop, Nous / ChatGPT subscription | **OAuth** |
| Shared server / CI worker in AWS GovCloud | **IAM role / SSO** (Bedrock) |
| Private GPU box, no cloud | **Local** `/v1` |
| Multi-vendor models from one key (non-GovCloud) | **OpenRouter** |
| Automation with a single-vendor key | API key in `~/.hermes/.env` (`chmod 600`) — last resort for shared hosts |

Doctor may warn “OAuth not logged in” until you opt in — that is expected and
non-blocking for CLI smoke ([DOCTOR.md](DOCTOR.md)).

---

## OpenRouter (aggregator)

OpenRouter is a first-class **API-key aggregator**: one `OPENROUTER_API_KEY` reaches
many upstream models through `https://openrouter.ai/api/v1`. Good for day-one
multi-model access — **not** a GovCloud / FedRAMP plane (use Bedrock/Mantle there).

### Baseline recipe

```bash
# Key from https://openrouter.ai/keys — store only in Hermes home
printf 'OPENROUTER_API_KEY=sk-or-...\n' >> "${HERMES_HOME:-$HOME/.hermes}/.env"
chmod 600 "${HERMES_HOME:-$HOME/.hermes}/.env"

hermes config set model.provider openrouter
hermes config set model.default openrouter/auto
# or: hermes model  →  OpenRouter  →  pick a slug
```

```yaml
model:
  provider: openrouter
  default: openrouter/auto          # or anthropic/claude-sonnet-4.6, google/gemini-…, etc.
# optional mirror/proxy:
# OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

Also covered in [GETTING_STARTED.md](GETTING_STARTED.md) headless setup.

### Recommended Nexus defaults

| Goal | Model / knob |
|------|----------------|
| Quick start / let OpenRouter choose | `openrouter/auto` |
| Pin a vendor model | `anthropic/…`, `google/…`, `openai/…` (OpenRouter slugs) |
| Coding-oriented routing | `openrouter/pareto-code` + `openrouter.min_coding_score` (default `0.65`) |
| Aux / fallback tasks | Often fall through OpenRouter when the key is present |

```yaml
openrouter:
  response_cache: true
  response_cache_ttl: 300
  min_coding_score: 0.65    # used with openrouter/pareto-code
```

Optional provider-order / routing prefs: see upstream
[provider routing](../website/docs/user-guide/features/provider-routing.md).

### Security posture (Nexus)

- Keep the key in `$HERMES_HOME/.env` only (`chmod 600`); never commit it.
- Prefer **OAuth** or **Bedrock role/SSO** when those fit — OpenRouter is convenience, not regulated isolation.
- Do **not** use OpenRouter for GovCloud-bound inference; data leaves the AWS Gov partition.
- On shared/gateway hosts, treat the key like any long-lived secret (rotate; avoid world-readable homes).

---

## AWS Bedrock & Mantle (GovCloud)

OpenAI **ChatGPT** model IDs on Bedrock are **Mantle-only** (including GovCloud).

| Surface | When | Host |
|---------|------|------|
| **Bedrock runtime (Converse / AnthropicBedrock)** | Claude, Nova, Llama, most foundation models | `bedrock-runtime[-fips].<region>.amazonaws.com` |
| **Bedrock Mantle** | OpenAI ChatGPT / Mantle Responses models | `bedrock-mantle.<region>.api.aws/openai/v1` |

### GovCloud regions (first-class)

| Region | Runtime | Mantle (OpenAI ChatGPT) |
|--------|---------|-------------------------|
| `us-gov-west-1` | Yes | Primary Mantle availability |
| `us-gov-east-1` | Yes | Confirm Mantle SKU availability in your partition |

```yaml
model:
  provider: bedrock
  default: <model-id>          # openai.* ChatGPT IDs → Mantle automatically
bedrock:
  region: us-gov-west-1        # or us-gov-east-1
  fips: null                   # null = auto (ON for GovCloud, OFF elsewhere)
```

FIPS applies to **runtime** hosts only. Mantle stays on `bedrock-mantle.<region>.api.aws`.

### Auth ranking (Bedrock)

1. **IAM role on compute** — EC2 / ECS / Lambda / IRSA  
2. **IAM Identity Center (SSO)** — `AWS_PROFILE`  
3. **Assume-role / web identity**  
4. **Short-lived** `AWS_BEARER_TOKEN_BEDROCK` (Mantle convenience; ≤12h)  
5. **Long-lived access keys** — last resort  

`hermes model` → AWS Bedrock: **role/SSO first**, **Mantle API key** for ChatGPT IDs.

---

## Verify (no live keys / logins)

```bash
source ./activate
just nexus-bedrock-govcloud     # GovCloud/FIPS/Mantle URL helpers
just nexus-providers            # local + OAuth + OpenRouter markers (no live key)
hermes model --help
hermes auth --help              # OAuth entrypoints present
```

## Related

- [SECURE_DEFAULTS.md](SECURE_DEFAULTS.md) — secrets / approvals  
- [GETTING_STARTED.md](GETTING_STARTED.md) — first-run provider setup  
- [STATUS.md](STATUS.md) — milestones  
