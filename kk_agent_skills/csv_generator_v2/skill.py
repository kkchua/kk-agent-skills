"""
csv_generator_v2 — SkillManifest

Two-phase image-to-CSV pipeline: extract structured descriptions first,
then generate enriched prompts using those descriptions as context.
"""
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="csv_generator_v2",
    display_name="CSV Generator V2",
    description=(
        "Two-phase image-to-CSV pipeline for ComfyUI T2I batch workflows. "
        "Phase 1: extract structured visual descriptions from each image (fixed vision model). "
        "Phase 2: generate variation prompts enriched by those descriptions. "
        "Produces JSON + CSV download links."
    ),
    version="1.0.0",
    tags=["csv_generator", "csv", "studio", "image", "generation", "vision"],
    collection="csv_generator",
    capabilities=["tool_provider"],
    min_access_level="user",
)
