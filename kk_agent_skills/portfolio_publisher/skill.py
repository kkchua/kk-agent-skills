"""
portfolio_publisher — SkillManifest

CRUD tools for Portfolio-01 article management.
Wraps the personal-assistant backend blog API.
"""
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="portfolio_publisher",
    display_name="Portfolio Publisher",
    description=(
        "Create, publish, archive, list, and update articles on the Portfolio-01 site. "
        "Wraps the personal-assistant backend blog API with admin-authenticated CRUD tools. "
        "Used by the deep_research skill to auto-post research-derived articles."
    ),
    version="1.0.0",
    tags=["portfolio", "article", "blog", "publish", "crud"],
    capabilities=["tool_provider"],
    min_access_level="user",
)
