"""
ai_tools — SkillManifest

AI text-processing utilities for summarizing, rewriting, extracting tasks,
and classifying intent.
"""
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="ai_tools",
    display_name="AI Tools",
    description=(
        "AI text processing utilities for summarizing, rewriting, extracting tasks, "
        "and classifying intent."
    ),
    version="1.0.0",
    tags=["ai", "text-processing", "summarize", "rewrite", "tasks", "intent"],
    capabilities=["tool_provider"],
    min_access_level="user",
)
