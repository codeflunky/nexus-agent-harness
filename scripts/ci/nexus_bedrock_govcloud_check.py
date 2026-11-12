#!/usr/bin/env python3
"""Verify Nexus Bedrock GovCloud + Mantle URL helpers (no live AWS calls).

Usage:
  scripts/hermes-python scripts/ci/nexus_bedrock_govcloud_check.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))

    from agent.bedrock_adapter import (
        BEDROCK_GOVCLOUD_REGIONS,
        bedrock_openai_base_url,
        bedrock_region_from_runtime_url,
        bedrock_runtime_base_url,
        bedrock_use_fips,
        is_bedrock_govcloud_region,
    )
    from hermes_cli.model_setup_flows_bedrock import bedrock_region_geo_prefix

    if BEDROCK_GOVCLOUD_REGIONS != frozenset({"us-gov-west-1", "us-gov-east-1"}):
        raise SystemExit(f"unexpected GovCloud set: {BEDROCK_GOVCLOUD_REGIONS}")
    for region in ("us-gov-west-1", "us-gov-east-1"):
        if not is_bedrock_govcloud_region(region):
            raise SystemExit(f"expected GovCloud: {region}")
    if is_bedrock_govcloud_region("us-east-1"):
        raise SystemExit("us-east-1 must not count as GovCloud")
    print("✓ GovCloud region set OK")

    west = "us-gov-west-1"
    if not bedrock_use_fips({"bedrock": {"fips": None}}, west):
        raise SystemExit("GovCloud should default FIPS on")
    if bedrock_use_fips({"bedrock": {"fips": False}}, west):
        raise SystemExit("explicit fips: false should win")
    if bedrock_use_fips({"bedrock": {"fips": None}}, "us-east-1"):
        raise SystemExit("commercial should default FIPS off")
    print("✓ FIPS auto policy OK")

    runtime = bedrock_runtime_base_url(west, config={"bedrock": {"fips": None}})
    if runtime != "https://bedrock-runtime-fips.us-gov-west-1.amazonaws.com":
        raise SystemExit(f"unexpected FIPS runtime URL: {runtime}")
    plain = bedrock_runtime_base_url("us-east-1", config={"bedrock": {"fips": None}})
    if plain != "https://bedrock-runtime.us-east-1.amazonaws.com":
        raise SystemExit(f"unexpected commercial runtime URL: {plain}")
    if bedrock_region_from_runtime_url(runtime) != west:
        raise SystemExit("failed to parse FIPS runtime region")
    print("✓ runtime URL helpers OK")

    mantle = bedrock_openai_base_url(west)
    if mantle != "https://bedrock-mantle.us-gov-west-1.api.aws/openai/v1":
        raise SystemExit(f"unexpected Mantle URL: {mantle}")
    print("✓ Mantle GovCloud URL OK")

    if bedrock_region_geo_prefix(west) != "":
        raise SystemExit("GovCloud geo prefix should be empty (no commercial us.* filter)")
    if bedrock_region_geo_prefix("us-east-1") != "us.":
        raise SystemExit("commercial us-east-1 should map to us.")
    print("✓ geo prefix GovCloud handling OK")

    docs = (ROOT / "docs/PROVIDERS.md").read_text(encoding="utf-8")
    for marker in (
        "us-gov-west-1",
        "us-gov-east-1",
        "Mantle",
        "ChatGPT",
        "IAM role",
        "AWS_PROFILE",
        "AWS_BEARER_TOKEN_BEDROCK",
    ):
        if marker not in docs:
            raise SystemExit(f"docs/PROVIDERS.md missing marker: {marker}")
    print("✓ docs/PROVIDERS.md present")

    print("Nexus Bedrock GovCloud checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
