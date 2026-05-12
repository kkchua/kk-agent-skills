"""
article_generation — SkillManifest

Single-shot research and article drafting.
"""
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="article_generation",
    display_name="Article Generation",
    description=(
        "Single-shot research and article drafting. Searches the web, synthesizes "
        "the results, and saves a structured markdown article as a draft."
    ),
    version="1.0.0",
    tags=["research", "writing", "blog", "article"],
    capabilities=["tool_provider"],
    min_access_level="user",
)
