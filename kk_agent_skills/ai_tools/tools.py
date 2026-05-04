"""
ai_tools skill — tools.py

agentskills.io-compatible tool module.
AI text processing: summarize, rewrite, extract tasks, classify intent.
Calls personal-assistant API instead of kk-utils AI service directly.
"""
import logging
from typing import Optional

from kk_utils.agent_tools import agent_tool, _auto_register

logger = logging.getLogger(__name__)


@agent_tool(
    name="Summarize Text",
    description="Summarize text content into a concise summary with key bullet points",
    tags=["ai_tools", "ai", "summarize", "text-processing"],
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
    from kk_agent_skills._http_client import call_tool
    return call_tool("summarize-text", {"text": text, "max_length": max_length, "bullet_points": bullet_points})


@agent_tool(
    name="Rewrite Text",
    description="Rewrite text with a different tone or style (professional, casual, friendly, etc.)",
    tags=["ai_tools", "ai", "rewrite", "text-processing"],
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
    from kk_agent_skills._http_client import call_tool
    return call_tool("rewrite-text", {"text": text, "tone": tone, "style": style})


@agent_tool(
    name="Extract Tasks",
    description="Extract actionable tasks from text with priority and due dates",
    tags=["ai_tools", "ai", "tasks", "extraction"],
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
    from kk_agent_skills._http_client import call_tool
    return call_tool("extract-tasks", {"text": text})


@agent_tool(
    name="Classify Intent",
    description="Classify user intent and extract entities for routing to appropriate tools",
    tags=["ai_tools", "ai", "intent", "classification"],
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
    from kk_agent_skills._http_client import call_tool
    return call_tool("classify-intent", {"text": text})


_auto_register()
