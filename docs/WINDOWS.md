# Windows install (Nexus)

Nexus does **not** use the Hermes CDN one-liner
(`hermes-agent.nousresearch.com`). Install from **this GitHub repo** so you get
the fork (Nexus branding, GovCloud Bedrock, provider recipes), not upstream Hermes.

**Recommendation for a first VM smoke:** **WSL2 (Ubuntu)** — same path as Linux
milestones. Native PowerShell is fine for CLI/gateway smoke.

Deep upstream references (behavior/quirks):  
[Windows WSL2](../website/docs/user-guide/windows-wsl-quickstart.md) ·
[Windows native](../website/docs/user-guide/windows-native.md).

---

## Option A — WSL2 (recommended)

From **Admin PowerShell** (once):

```powershell
wsl --install
# reboot if prompted; finish Ubuntu user setup
```

Inside **Ubuntu (WSL2)**:

```bash
# One-liner bootstrap (clones this fork, then PM setup)
export HERMES_REPO_URL=https://github.com/codeflunky/nexus-agent-harness.git
curl -fsSL https://raw.githubusercontent.com/codeflunky/nexus-agent-harness/main/scripts/install.sh | bash
```

Or clone + activate (dev-style, matches Linux docs):

```bash
git clone https://github.com/codeflunky/nexus-agent-harness
cd nexus-agent-harness
bash setup-hermes.sh --runtime-only --test-environment
source ./activate
hermes --version          # expect Nexus Agent
hermes doctor
```

First-run / providers: [GETTING_STARTED.md](GETTING_STARTED.md), [PROVIDERS.md](PROVIDERS.md).

---

## Option B — Native Windows (PowerShell)

In **PowerShell** (Windows Terminal preferred):

```powershell
# Point the installer at the Nexus fork (default would be NousResearch/hermes-agent)
$env:HERMES_REPO_URL = 'https://github.com/codeflunky/nexus-agent-harness.git'
iex (irm https://raw.githubusercontent.com/codeflunky/nexus-agent-harness/main/scripts/install.ps1)
```

Typical layout after install:

| Path | Purpose |
|------|---------|
| `%LOCALAPPDATA%\hermes\hermes-agent\` | Checkout |
| `%LOCALAPPDATA%\hermes\bin\` | `hermes` on PATH |
| `%LOCALAPPDATA%\hermes\` | `HERMES_HOME` (`.env`, config, sessions) |

Open a **new** terminal, then:

```powershell
hermes --version
hermes doctor
hermes setup          # or hermes model / provider recipes
```

### Dev-style (clone + `setup-hermes.ps1`)

```powershell
git clone https://github.com/codeflunky/nexus-agent-harness
cd nexus-agent-harness
.\setup-hermes.ps1 -RuntimeOnly
.\activate.ps1
hermes --version
```

---

## What *not* to run

```powershell
# Upstream Hermes CDN — installs NousResearch/hermes-agent, not this fork
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Unless you set `HERMES_REPO_URL` first, that path is **not** Nexus.

---

## After install (smoke checklist)

1. `hermes --version` shows **Nexus Agent**  
2. `hermes doctor` — setup gaps OK ([DOCTOR.md](DOCTOR.md))  
3. Pick a provider ([PROVIDERS.md](PROVIDERS.md)): OpenRouter / OAuth / local / Bedrock  
4. Optional: `hermes gateway setup` ([GATEWAY.md](GATEWAY.md))  
5. Desktop MSIX / signed Win installers remain **M4** — out of scope for this smoke  

---

## Related

- [GETTING_STARTED.md](GETTING_STARTED.md) — Linux-oriented first-run (same CLI once activated)  
- [STATUS.md](STATUS.md) — M4 Desktop later  
- Upstream: [installation.md](../website/docs/getting-started/installation.md)  
