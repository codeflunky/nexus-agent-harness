# Secure defaults (Nexus collaborative profile)

Nexus is a **collaborative agent harness**. Defaults should favor human approval and
tight secret handling on shared or multi-user Linux machines. OS isolation is still
the real security boundary — see upstream [SECURITY.md](../SECURITY.md).

## Recommended profile

```yaml
approvals:
  mode: manual              # always prompt (Nexus default; upstream Hermes uses smart)
  timeout: 300
  cron_mode: deny
  single_query_mode: deny
  unattended_mode: deny
  approvers: []             # when using messaging gateways: requester + admins only
  deny: []                  # optional team globs (still apply under --yolo)
security:
  allow_private_urls: false
  redact_secrets: true
  protected_instruction_files: true
  approval:
    transport: builtin
    transport_fallback: deny
terminal:
  backend: local            # host shell; strongest isolation → docker (+ optional docker_network: false)
hooks_auto_accept: false
```

Seed comments live in `cli-config.yaml.example`. Effective defaults come from
`hermes_cli/config_defaults.py` (Nexus sets `approvals.mode: manual`).

## Secrets

| Practice | Detail |
|----------|--------|
| Store secrets in `$HERMES_HOME/.env` | Not in `config.yaml` or git |
| File mode `600` | `chmod 600 ~/.hermes/.env` |
| Directory mode `700` | `~/.hermes` should be owner-only |
| Never commit `.env` | Use `.env.example` as the template |

`hermes doctor` warns (and can `--fix`) when `.env` or `$HERMES_HOME` is group/world accessible.

## Approvals footguns

| Setting | Risk | Prefer |
|---------|------|--------|
| `approvals.mode: off` | Same as `--yolo` — auto-approves dangerous commands | `manual` (or `smart` only if you accept aux-LLM auto-approve) |
| `--yolo` / `HERMES_YOLO_MODE=1` | Session/env bypass | Leave unset on shared hosts |
| `approvers: ["*"]` | Any admitted chat member can approve | `[]` for gateway/shared rooms |
| `terminal.backend: local` | Agent runs on the host | `docker` (+ `docker_network: false`) when you need a sandbox |

Hardline deny patterns and fail-closed approval timeouts still apply under YOLO.

## Egress

There is **no** global “deny all network” default for the local terminal backend.

Optional tighter postures:

```yaml
terminal:
  backend: docker
  docker_network: false     # --network=none inside the container
# Optional: hermes egress setup  →  proxy.enabled: true (iron-proxy)
```

`security.allow_private_urls` stays **false** so web/vision tools do not reach RFC1918 by default.

## Verify

```bash
source ./activate
hermes doctor              # look for secure-defaults / permissions findings
just nexus-smoke
python3 scripts/ci/nexus_secure_defaults_check.py
```

## Related

- [docs/GETTING_STARTED.md](GETTING_STARTED.md) — first-run path  
- [docs/GATEWAY.md](GATEWAY.md) — Telegram / Discord / Slack recipes  
- [docs/DOCTOR.md](DOCTOR.md) — expected setup gaps  
- [docs/UPSTREAM.md](UPSTREAM.md) — origin-only updates + Hermes sync cadence  
- [SECURITY.md](../SECURITY.md) — upstream trust model  
