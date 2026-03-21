"""
web_search skill — tools.py

agentskills.io-compatible tool module.
Tavily-powered web search for real-time information retrieval.
Calls personal-assistant API instead of kk-utils services directly.
"""
import logging
from typing import Optional

from kk_utils.agent_tools import agent_tool, _auto_register

logger = logging.getLogger(__name__)


@agent_tool(
    name="Web Search",
    description=(
        "Search the web for current information on any topic. "
        "Returns titles, URLs, and content snippets from relevant pages. "
        "Use this to research facts, find documentation, get references, "
        "or look up anything that requires up-to-date information."
    ),
    tags=["search", "research", "web"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def web_search(
    query: str,
    max_results: int = 5,
    search_depth: str = "basic",
    user_id: Optional[str] = None,
) -> dict:
    """
    Search the web using Tavily API.

    Args:
        query: Search query string
        max_results: Number of results to return (1–10, default 5)
        search_depth: "basic" (fast) or "advanced" (higher quality)
        user_id: User ID (auto-injected by Governor)
    """
    from kk_agent_skills._http_client import call_tool

    logger.info(f"Web search: '{query}' (max_results={max_results}) for user {user_id}")
    return call_tool("web-search", {"query": query, "max_results": max_results, "search_depth": search_depth})


_auto_register()
