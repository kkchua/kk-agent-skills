"""
ai_tools skill — tools.py

agentskills.io-compatible tool module.
AI text processing: summarize, rewrite, extract tasks, classify intent.
All AI calls route through kk_utils.ai.AIService (provider-agnostic).
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
    name="Summarize Text",
    description="Summarize text content into a concise summary with key bullet points",
    tags=["ai", "summarize", "text-processing"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def summarize_text(
    text: str,
    max_length: int = 150,
    bullet_points: bool = True,
    user_id: Optional[str] = None,
) -> dict:
    """
    Summarize text content.

    Args:
        text: Text to summarize
        max_length: Maximum summary length in words (default: 150)
        bullet_points: Whether to extract key bullet points (default: True)
        user_id: User ID (auto-injected by Governor)
    """
    from kk_utils.ai import get_ai_service, CallContext
    ai_service = get_ai_service()
    context = CallContext(agent_name="personal_assistant", feature_name="summarize_text", user_id=user_id)
    result = _asyncio_run(ai_service.summarize(text=text, max_length=max_length, bullet_points=bullet_points, context=context))
    return {"summary": result.summary, "key_points": result.key_points, "word_count": result.word_count, "success": True}


@agent_tool(
    name="Rewrite Text",
    description="Rewrite text with a different tone or style (professional, casual, friendly, etc.)",
    tags=["ai", "rewrite", "text-processing"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def rewrite_text(
    text: str,
    tone: str = "professional",
    style: Optional[str] = None,
    user_id: Optional[str] = None,
) -> dict:
    """
    Rewrite text with different tone/style.

    Args:
        text: Text to rewrite
        tone: Desired tone (professional, casual, friendly, formal, etc.)
        style: Additional style instructions (optional)
        user_id: User ID (auto-injected by Governor)
    """
    from kk_utils.ai import get_ai_service, CallContext
    ai_service = get_ai_service()
    context = CallContext(agent_name="personal_assistant", feature_name="rewrite_text", user_id=user_id)
    result = _asyncio_run(ai_service.rewrite(text=text, tone=tone, style=style, context=context))
    return {"rewritten_text": result.rewritten_text, "tone": result.tone, "changes_made": result.changes_made, "success": True}


@agent_tool(
    name="Extract Tasks",
    description="Extract actionable tasks from text with priority and due dates",
    tags=["ai", "tasks", "extraction"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def extract_tasks(
    text: str,
    user_id: Optional[str] = None,
) -> dict:
    """
    Extract actionable tasks from text.

    Args:
        text: Text to extract tasks from
        user_id: User ID (auto-injected by Governor)
    """
    from kk_utils.ai import get_ai_service, CallContext
    ai_service = get_ai_service()
    context = CallContext(agent_name="personal_assistant", feature_name="extract_tasks", user_id=user_id)
    result = _asyncio_run(ai_service.extract_tasks(text=text, context=context))
    return {"tasks": result.tasks, "total_tasks": result.total_tasks, "success": True}


@agent_tool(
    name="Classify Intent",
    description="Classify user intent and extract entities for routing to appropriate tools",
    tags=["ai", "intent", "classification"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def classify_intent(
    text: str,
    user_id: Optional[str] = None,
) -> dict:
    """
    Classify user intent and extract entities.

    Args:
        text: User input text to classify
        user_id: User ID (auto-injected by Governor)
    """
    from kk_utils.ai import get_ai_service, CallContext
    ai_service = get_ai_service()
    context = CallContext(agent_name="personal_assistant", feature_name="classify_intent", user_id=user_id)
    result = _asyncio_run(ai_service.classify_intent(text=text, context=context))
    return {"intent": result.intent, "confidence": result.confidence, "entities": result.entities, "suggested_tools": result.suggested_tools, "success": True}


_auto_register()
