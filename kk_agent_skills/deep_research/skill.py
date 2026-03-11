"""
deep_research — SkillManifest

Multi-agent deep research skill. Supports general, technical, market,
and article-optimized research variants via YAML-driven prompts.
"""
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="deep_research",
    display_name="Deep Research",
    description=(
        "Multi-agent deep research pipeline. Plans targeted web searches, executes them "
        "in parallel, and synthesizes a comprehensive structured report. Supports general, "
        "technical, market, and article-optimized research variants. Can email reports via "
        "Resend and auto-post articles to the Portfolio site."
    ),
    version="1.0.0",
    tags=["research", "web", "analysis", "report", "article", "multi-agent"],
    capabilities=["tool_provider"],
    min_access_level="user",
)
