"""
deep_research skill — tools.py

agentskills.io-compatible tools for the deep research pipeline.
Exposes two public tools:
  - deep_research: Full multi-agent research → structured report
  - research_to_article: Research → portfolio blog article draft
"""
import asyncio
import logging
from typing import Optional

from kk_utils.agent_tools import _auto_register, agent_tool

logger = logging.getLogger(__name__)

_VALID_VARIANTS = ("general", "technical", "market", "article")


def _asyncio_run(coroutine):
    """Run async coroutine in sync context (mirrors web_search skill pattern)."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
        return loop.run_until_complete(coroutine)
    except RuntimeError:
        return asyncio.run(coroutine)


async def _collect_research(
    query: str,
    variant: str,
    send_notification: bool,
    notification_recipient: Optional[str],
) -> dict:
    """Run ResearchManager and collect all yielded output, returning final result dict."""
    from kk_agent_skills.deep_research.research_manager import ResearchManager
    from kk_agent_skills.deep_research.agents._prompt_loader import load_prompt

    config = load_prompt(variant)
    manager = ResearchManager()

    status_messages: list[str] = []
    final_content: str = ""

    async for chunk in manager.run(
        query=query,
        variant=variant,
        send_notification=send_notification,
        notification_recipient=notification_recipient,
    ):
        status_messages.append(chunk)
        final_content = chunk  # last chunk is always the main content

    output_type = config["writer"].get("output_type", "report")
    return {
        "success": True,
        "variant": variant,
        "query": query,
        "output_type": output_type,
        "content": final_content,
        "status_log": status_messages[:-1],  # exclude final content from log
    }


@agent_tool(
    name="Deep Research",
    description=(
        "Run a multi-agent deep research pipeline on any topic. "
        "Plans targeted web searches, executes them in parallel, then synthesizes "
        "a comprehensive structured report. "
        "Choose a variant: 'general' (default), 'technical' (code/architecture focus), "
        "'market' (competitive landscape), or 'article' (blog-ready output). "
        "Returns a detailed markdown report with summary and follow-up questions."
    ),
    tags=["research", "web", "analysis", "report", "multi-agent"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def deep_research(
    query: str,
    variant: str = "general",
    send_notification: bool = False,
    notification_recipient: Optional[str] = None,
    user_id: Optional[str] = None,
) -> dict:
    """
    Run the full multi-agent deep research pipeline.

    Args:
        query: The research topic or question.
        variant: Prompt variant — general | technical | market | article
        send_notification: Email the report via Resend when done.
        notification_recipient: Override recipient email (else uses RESEARCH_NOTIFICATION_EMAIL env var).
        user_id: Auto-injected by Governor.
    """
    if variant not in _VALID_VARIANTS:
        return {
            "success": False,
            "error": f"Unknown variant '{variant}'. Valid: {_VALID_VARIANTS}",
        }

    logger.info(f"Deep research: query='{query}' variant='{variant}' user={user_id}")

    try:
        return _asyncio_run(
            _collect_research(
                query=query,
                variant=variant,
                send_notification=send_notification,
                notification_recipient=notification_recipient,
            )
        )
    except Exception as exc:
        logger.exception(f"Deep research failed: {exc}")
        return {"success": False, "error": str(exc), "query": query, "variant": variant}


@agent_tool(
    name="Research to Article",
    description=(
        "Research a topic and automatically generate a portfolio blog article saved as a draft. "
        "Runs the deep research pipeline with the 'article' prompt variant, then posts the result "
        "to the Portfolio site as a draft. Optionally auto-publishes. "
        "Returns the article slug, title, and draft URL."
    ),
    tags=["research", "article", "portfolio", "blog", "multi-agent"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def research_to_article(
    topic: str,
    category: Optional[str] = None,
    auto_publish: bool = False,
    user_id: Optional[str] = None,
) -> dict:
    """
    Research a topic and create a portfolio blog article draft.

    Args:
        topic: The article topic to research and write about.
        category: Optional category label (e.g. "AI", "Architecture", "Tutorial").
        auto_publish: If True, publish immediately instead of saving as draft.
        user_id: Auto-injected by Governor.
    """
    logger.info(f"Research to article: topic='{topic}' category={category} user={user_id}")

    # Step 1: Run research with article variant
    try:
        research_result = _asyncio_run(
            _collect_research(
                query=topic,
                variant="article",
                send_notification=False,
                notification_recipient=None,
            )
        )
    except Exception as exc:
        logger.exception(f"Research phase failed: {exc}")
        return {"success": False, "error": f"Research failed: {exc}", "topic": topic}

    if not research_result.get("success"):
        return research_result

    # Step 2: Parse structured article output from the research manager
    # The research_manager returns ArticleReportData for the 'article' variant.
    # We need to reconstruct it from the raw content for posting.
    # The content is raw markdown — extract via the article generation service.
    try:
        from kk_agent_skills.portfolio_publisher.tools import create_article_from_research
        return create_article_from_research(
            research_result=research_result,
            category=category,
            auto_publish=auto_publish,
            user_id=user_id,
        )
    except Exception as exc:
        logger.exception(f"Portfolio posting failed: {exc}")
        # Return research result even if posting fails
        return {
            "success": False,
            "error": f"Portfolio post failed: {exc}",
            "research_content": research_result.get("content", "")[:500] + "...",
            "topic": topic,
        }


_auto_register()
