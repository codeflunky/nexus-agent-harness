# Provider curation (Nexus) — AWS Bedrock & Mantle

Nexus keeps upstream providers, then **curates** AWS Bedrock for collaborative and
**GovCloud** use. OpenAI **ChatGPT** model IDs on Bedrock are **Mantle-only**
(including in GovCloud).

Deep upstream guide: [website/docs/guides/aws-bedrock.md](../website/docs/guides/aws-bedrock.md).

## Surfaces

| Surface | When | Host |
|---------|------|------|
| **Bedrock runtime (Converse / AnthropicBedrock)** | Claude, Nova, Llama, most foundation models | `bedrock-runtime[-fips].<region>.amazonaws.com` |
| **Bedrock Mantle** | OpenAI ChatGPT / Mantle Responses models | `bedrock-mantle.<region>.api.aws/openai/v1` |

`hermes model` → AWS Bedrock:

1. **IAM role / SSO** (recommended) → runtime Converse path  
2. **Mantle API key** → OpenAI ChatGPT / Mantle-only IDs  

Bare OpenAI Mantle model IDs auto-route to Mantle even when `model.provider: bedrock`.

## GovCloud regions (first-class)

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

FIPS applies to **runtime** hosts only (`bedrock-runtime-fips…`). Mantle stays on
`bedrock-mantle.<region>.api.aws`.

## Auth ranking (Nexus secure native)

Prefer short-lived, auditable credentials — no long-lived keys in shared `.env`:

1. **IAM role on compute** — EC2 instance profile, ECS task role, Lambda role, EKS IRSA  
2. **IAM Identity Center (SSO)** — `AWS_PROFILE` + short sessions (`aws configure sso`)  
3. **Assume-role / web identity** — least-privilege Bedrock role via profile or IRSA  
4. **Short-lived Bedrock API key** — `AWS_BEARER_TOKEN_BEDROCK` (≤12h); required convenience path for some Mantle clients  
5. **Long-lived access keys** — last resort; avoid on collaborative / gateway hosts  

Env knobs: `AWS_REGION`, `AWS_PROFILE`, `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`,
`AWS_BEARER_TOKEN_BEDROCK`, `AWS_WEB_IDENTITY_TOKEN_FILE`, container relative URI.

## Suggested GovCloud profiles

**Claude / Nova on Converse (role/SSO):**

```yaml
model:
  provider: bedrock
  default: anthropic.claude-sonnet-4-6   # use your partition's enabled ID
bedrock:
  region: us-gov-west-1
```

Authenticate with an instance/task role or `export AWS_PROFILE=gov-sso`.

**OpenAI ChatGPT on Mantle:**

```bash
# short-lived bearer from your admin / Secrets Manager
export AWS_BEARER_TOKEN_BEDROCK=...
```

```yaml
model:
  provider: bedrock
  default: openai.gpt-…                # Mantle-only ID for your partition
bedrock:
  region: us-gov-west-1
```

Or run `hermes model` → Bedrock → choose **Mantle API key**.

## IAM (minimum sketch)

Runtime: `bedrock:InvokeModel`, `bedrock:InvokeModelWithResponseStream`,
`bedrock:ListFoundationModels`, `bedrock:ListInferenceProfiles` (as needed).

Mantle: grant the partition’s **`bedrock-mantle:*`** actions your org documents for
OpenAI Responses / ChatGPT models (ARNs use `arn:aws-us-gov:bedrock-mantle:…`).

## Verify

```bash
source ./activate
python -c "import pm; pm.sync_venv(['bedrock'], explicit=True)"
just nexus-bedrock-govcloud    # region/FIPS/Mantle URL helpers (no AWS call)
hermes model                  # pick Bedrock; set us-gov-west-1
```

## Related

- [SECURE_DEFAULTS.md](SECURE_DEFAULTS.md) — secrets / approvals  
- [GETTING_STARTED.md](GETTING_STARTED.md) — first-run provider setup  
- [STATUS.md](STATUS.md) — milestones  
