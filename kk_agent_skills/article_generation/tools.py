"""
article_generation skill — tools.py

agentskills.io-compatible tool module.
Research a topic via Tavily web search and generate a structured article draft.
Calls personal-assistant API instead of kk-utils services directly.
"""
import logging
from typing import Optional

from kk_utils.agent_tools import agent_tool, _auto_register

logger = logging.getLogger(__name__)


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
    from kk_agent_skills._http_client import call_tool

    logger.info(f"Research & write article: '{topic}' (tone={tone}) for user {user_id}")
    return call_tool("generate-article", {
        "topic": topic,
        "category": category,
        "tone": tone,
        "num_search_results": num_search_results,
    })


_auto_register()
