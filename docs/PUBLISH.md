# Publishing the public install mirror

Nexus development is **private**; Windows/Linux one-liners need a **public**
clone target.

| Remote | GitHub | Visibility |
|--------|--------|------------|
| `origin` (developers / CI) | [`codeflunky/nexus-agent-harness-dev`](https://github.com/codeflunky/nexus-agent-harness-dev) | Private |
| `public` (install one-liners) | [`codeflunky/nexus-agent-harness`](https://github.com/codeflunky/nexus-agent-harness) | Public |

`HERMES_REPO_URL` and raw `install.ps1` / `install.sh` URLs always point at the
**public** repo.

## First-time seed (required once)

From a machine that can push to **both** remotes (your laptop, or after
granting `cursor[bot]` write on the public repo):

```bash
git clone https://github.com/codeflunky/nexus-agent-harness-dev.git
cd nexus-agent-harness-dev
git remote add public https://github.com/codeflunky/nexus-agent-harness.git
git push -u public main
```

Verify:

```powershell
# should return 200, not 404
irm https://raw.githubusercontent.com/codeflunky/nexus-agent-harness/main/scripts/install.ps1 | Select-Object -First 1
```

## Refresh after merges to `-dev` `main`

```bash
git fetch origin
git push public origin/main:main
```

Optional: add a GitHub Action on `-dev` that pushes `main` to `public` using a
PAT/fine-grained token stored as `PUBLIC_MIRROR_TOKEN` (contents: write on the
public repo only).

## What not to mirror blindly

- Do not push private-only branches, secrets, or internal notes to `public`.
- Prefer publishing **`main`** (and release tags) only.
- `hermes update` / ZIP fallback use `PRODUCT_REPOSITORY` =
  `codeflunky/nexus-agent-harness` (the public install repo).
