"""
web_search — SkillManifest

Real-time web search skill powered by Tavily.
"""
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="web_search",
    display_name="Web Search",
    description=(
        "Real-time web search powered by Tavily. Finds current information, news, "
        "and factual answers from the web."
    ),
    version="1.0.0",
    tags=["web_search", "search", "tavily"],
    collection=None,
    capabilities=["tool_provider"],
    min_access_level="user",
)
