"""
hot_topics — SkillManifest

Discovers trending and hot topics for any given subject.
Uses web search and AI analysis to identify the most discussed,
controversial, and emerging topics in a field.
"""
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="hot_topics",
    display_name="Hot Topics Discovery",
    description=(
        "Discovers trending and hot topics for any given subject. "
        "Analyzes recent web content to identify the most discussed, controversial, "
        "and emerging topics in a field. Returns ranked topics with explanations "
        "of why they're trending and suggested angles for exploration."
    ),
    version="1.0.0",
    tags=["topics", "trending", "research", "analysis", "web"],
    capabilities=["tool_provider"],
    min_access_level="user",
)
