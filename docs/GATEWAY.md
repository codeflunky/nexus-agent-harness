# Gateway recipes (Nexus, Linux)

Optional: talk to Nexus from **Telegram**, **Discord**, **Slack**, or **Microsoft Teams**.  
CLI/TUI works without any of this — see [GETTING_STARTED.md](GETTING_STARTED.md).

Deep platform guides (upstream): [website/docs/user-guide/messaging/](../website/docs/user-guide/messaging/index.md).

## Prerequisites

1. Provider configured (`hermes setup` / `.env` API key).
2. Secrets only in `$HERMES_HOME/.env` with mode `600` ([SECURE_DEFAULTS.md](SECURE_DEFAULTS.md)).
3. Prefer `approvals.mode: manual` and narrow allowlists (`TELEGRAM_ALLOWED_USERS`, `TEAMS_ALLOWED_USERS`, etc.).
4. If doctor warns about missing messaging SDKs, install the extras for your stack (e.g. project `[messaging]` / `teams` extras).

## Quick path (any platform)

```bash
source ./activate
hermes gateway setup      # pick Telegram / Discord / Slack / Microsoft Teams
hermes gateway            # foreground (dev)
# or persist:
hermes gateway install
hermes gateway start
hermes gateway status
```

Same wizard via `hermes setup` → Messaging Platforms (Gateway), or `hermes setup gateway`.

## Telegram

1. Create a bot with [@BotFather](https://t.me/BotFather); copy the token.
2. Configure:

```bash
# Wizard
hermes gateway setup      # select Telegram

# Or manual (~/.hermes/.env)
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_ALLOWED_USERS=your_telegram_user_id
# optional: TELEGRAM_HOME_CHANNEL=...
```

3. Run: `hermes gateway` (or install the user service).
4. DM the bot. If pairing is required: `hermes pairing approve telegram <code>`.

Details: [telegram.md](../website/docs/user-guide/messaging/telegram.md).

## Discord

1. Create a bot in the [Discord Developer Portal](https://discord.com/developers/applications). Enable **Message Content Intent**.
2. Invite the bot to a server; copy the bot token.
3. Configure:

```bash
hermes gateway setup      # select Discord

# Or ~/.hermes/.env
DISCORD_BOT_TOKEN=...
DISCORD_ALLOWED_USERS=your_discord_user_id
# optional: DISCORD_HOME_CHANNEL=...
```

4. Run: `hermes gateway`.

Details: [discord.md](../website/docs/user-guide/messaging/discord.md).

## Slack

1. Generate a manifest: `hermes slack manifest --agent-view --write`
2. Create a Slack app from that manifest (Socket Mode); install to the workspace.
3. Put both tokens in `.env`:

```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
SLACK_ALLOWED_USERS=U...
# optional: SLACK_HOME_CHANNEL=...
```

Or use `hermes gateway setup` and select Slack.

4. Run: `hermes gateway`.

Details: [slack.md](../website/docs/user-guide/messaging/slack.md).

## Microsoft Teams

Teams uses a **public HTTPS webhook** (unlike Slack Socket Mode). Locally you need a tunnel; in production, a real domain.

1. Install the Teams extra (source checkout):

```bash
python -c "import pm; pm.sync_venv(['teams'], explicit=True)"
```

2. Expose the webhook port (default `3978`) with a public HTTPS URL:

```bash
# examples
devtunnel host …          # or: ngrok http 3978  /  cloudflared tunnel --url http://localhost:3978
```

3. Register the bot (Teams CLI or Azure portal) with endpoint `https://<public-host>/api/messages`.

4. Configure `~/.hermes/.env`:

```bash
# Wizard
hermes gateway setup      # select Microsoft Teams

# Or manual
TEAMS_CLIENT_ID=...
TEAMS_CLIENT_SECRET=...
TEAMS_TENANT_ID=...       # or "common" for multi-tenant
TEAMS_ALLOWED_USERS=...   # AAD object IDs (from `teams status --verbose`)
# optional: TEAMS_PORT=3978
# optional: TEAMS_HOME_CHANNEL=...
```

5. Run: `hermes gateway` (tunnel must stay up for local/dev).

Meeting-summary pipeline (Graph subscriptions) is separate: [teams-meetings.md](../website/docs/user-guide/messaging/teams-meetings.md).

Details: [teams.md](../website/docs/user-guide/messaging/teams.md).

## Persist on Linux

| Scope | Commands |
|-------|----------|
| User (default) | `hermes gateway install` → `hermes gateway start` |
| System (boot) | `sudo hermes gateway install --system` → `sudo hermes gateway start` |

Useful: `hermes gateway status` / `stop` / `restart` / `uninstall`.

## Doctor / smoke

Missing bot tokens / Teams credentials and optional messaging packages are **warnings**, not CI blockers.  
[DOCTOR.md](DOCTOR.md) / `just nexus-smoke` stay green without gateway credentials.

## Other platforms (one-liners)

WhatsApp (`hermes whatsapp`), Signal, Matrix, Mattermost, Email, Feishu, WeCom, QQ, webhooks, and more — see the [messaging index](../website/docs/user-guide/messaging/index.md).

## Related

- [SECURE_DEFAULTS.md](SECURE_DEFAULTS.md) — approvals / allowlists for shared rooms  
- [STATUS.md](STATUS.md) — milestones  
- [UPSTREAM.md](UPSTREAM.md) — origin-only updates  
