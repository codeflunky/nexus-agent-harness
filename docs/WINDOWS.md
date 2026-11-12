# Windows install (Nexus)

Nexus does **not** use the Hermes CDN
(`hermes-agent.nousresearch.com`). Install from the **public** GitHub repo
[`codeflunky/nexus-agent-harness`](https://github.com/codeflunky/nexus-agent-harness)
so `irm` / `curl` work without a GitHub login.

| Repo | Role |
|------|------|
| [`nexus-agent-harness`](https://github.com/codeflunky/nexus-agent-harness) | **Public** install / release mirror |
| [`nexus-agent-harness-dev`](https://github.com/codeflunky/nexus-agent-harness-dev) | **Private** day-to-day development |

**Azure VDI / no local admin:** use **native PowerShell** below — installs under
`%LOCALAPPDATA%\hermes\` and User PATH only. WSL usually needs elevation.

Deep upstream references:  
[Windows WSL2](../website/docs/user-guide/windows-wsl-quickstart.md) ·
[Windows native](../website/docs/user-guide/windows-native.md).

If `irm` still 404s, the public mirror has not been seeded yet — see
[PUBLISH.md](PUBLISH.md).

---

## Option B — Native Windows (PowerShell) — VDI / no admin

```powershell
$env:HERMES_REPO_URL = 'https://github.com/codeflunky/nexus-agent-harness.git'
iex (irm https://raw.githubusercontent.com/codeflunky/nexus-agent-harness/main/scripts/install.ps1)
```

Open a **new** terminal, then:

```powershell
hermes --version          # expect Nexus Agent
hermes doctor
hermes setup              # or provider recipes in PROVIDERS.md
```

| Path | Purpose |
|------|---------|
| `%LOCALAPPDATA%\hermes\hermes-agent\` | Checkout |
| `%LOCALAPPDATA%\hermes\bin\` | `hermes` on PATH |
| `%LOCALAPPDATA%\hermes\` | `HERMES_HOME` (`.env`, config, sessions) |

### Contributor / private tip (optional)

Working tree is private `-dev`. After `gh auth login`:

```powershell
gh repo clone codeflunky/nexus-agent-harness-dev
cd nexus-agent-harness-dev
.\setup-hermes.ps1 -RuntimeOnly
.\activate.ps1
```

---

## Option A — WSL2 (needs admin for `wsl --install`)

```powershell
wsl --install
```

Inside Ubuntu:

```bash
export HERMES_REPO_URL=https://github.com/codeflunky/nexus-agent-harness.git
curl -fsSL https://raw.githubusercontent.com/codeflunky/nexus-agent-harness/main/scripts/install.sh | bash
```

---

## What *not* to run

```powershell
# Upstream Hermes CDN — not this fork
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

---

## After install (smoke checklist)

1. `hermes --version` shows **Nexus Agent**  
2. `hermes doctor` — setup gaps OK ([DOCTOR.md](DOCTOR.md))  
3. Pick a provider ([PROVIDERS.md](PROVIDERS.md))  
4. Optional: `hermes gateway setup` ([GATEWAY.md](GATEWAY.md))  
5. Desktop MSIX remains **M4**

---

## Related

- [PUBLISH.md](PUBLISH.md) — seed / refresh the public mirror  
- [GETTING_STARTED.md](GETTING_STARTED.md) · [STATUS.md](STATUS.md)  
