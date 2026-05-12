"""
csv_generator — SkillManifest

Schema-driven image-to-CSV generator for vision workflows.
"""
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="csv_generator",
    display_name="CSV Generator",
    description=(
        "Schema-driven image-to-CSV generator. Analyzes uploaded images and produces "
        "structured JSON and CSV outputs for downstream workflows."
    ),
    version="1.0.0",
    tags=["csv", "studio", "image", "generation"],
    capabilities=["tool_provider"],
    min_access_level="user",
)
