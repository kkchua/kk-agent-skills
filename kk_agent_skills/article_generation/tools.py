"""
article_generation skill — tools.py

agentskills.io-compatible tool module.
Research a topic via Tavily web search and generate a structured article draft.
Backend service calls are lazy imports — resolved at call time within the backend.
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
    name="Research and Write Article",
    description=(
        "Research a topic using web search and write a structured technical article. "
        "Saves the article as a draft in the portfolio blog for admin review before publishing. "
        "Use this when asked to write, research, or create an article, post, or guide about a technical topic. "
        "Example: 'write an article about ChromaDB' or 'research RAG pipeline design and create a blog post'."
    ),
    tags=["research", "writing", "blog", "article"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def research_and_write_article(
    topic: str,
    category: Optional[str] = None,
    tone: str = "technical",
    num_search_results: int = 4,
    user_id: Optional[str] = None,
) -> dict:
    """
    Research a topic and generate a structured technical article saved as a draft.

    Args:
        topic: The article topic or subject to research and write about
        category: Optional category label (e.g. "Architecture", "Tools", "Tutorial")
        tone: Writing tone — technical | accessible | reference (default: technical)
        num_search_results: Number of web search results to use for research (1–8)
        user_id: User ID (auto-injected by Governor)
    """
    from app.services.article_generation_service import get_article_generation_service
    from app.database.session import get_db_context

    logger.info(f"Research & write article: '{topic}' (tone={tone}) for user {user_id}")

    service = get_article_generation_service()

    with get_db_context() as db:
        result = _asyncio_run(
            service.generate(
                topic=topic,
                db_session=db,
                category=category,
                tone=tone,
                num_search_results=num_search_results,
            )
        )

    logger.info(f"Article generated: '{result.title}' (slug: {result.slug})")

    return {
        "title": result.title,
        "slug": result.slug,
        "excerpt": result.excerpt,
        "tags": result.tags,
        "category": result.category,
        "search_results_used": result.search_results_used,
        "status": "draft",
        "message": (
            f"Article '{result.title}' has been researched and saved as a draft. "
            f"Visit /admin to preview and publish it."
        ),
        "success": True,
    }


_auto_register()
