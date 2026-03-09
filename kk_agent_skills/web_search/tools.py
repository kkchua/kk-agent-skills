"""
web_search skill — tools.py

agentskills.io-compatible tool module.
Tavily-powered web search for real-time information retrieval.
"""
import asyncio
import logging
from typing import Optional

from kk_utils.agent_tools import agent_tool, _auto_register

logger = logging.getLogger(__name__)


def _asyncio_run(coroutine):
    """Run async coroutine in sync context."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
        return loop.run_until_complete(coroutine)
    except RuntimeError:
        return asyncio.run(coroutine)


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
    from app.services.web_search_service import get_web_search_service

    logger.info(f"Web search: '{query}' (max_results={max_results}) for user {user_id}")

    service = get_web_search_service()
    result = _asyncio_run(service.search(query=query, max_results=max_results, search_depth=search_depth))

    if not result.success:
        logger.warning(f"Web search failed: {result.error}")
        return {"results": [], "total": 0, "query": query, "success": False, "error": result.error}

    return {"results": [r.model_dump() for r in result.results], "total": result.total, "query": result.query, "success": True}


_auto_register()
