"""
deep_research — agents/notifier.py

Sends the research report via Resend email API.
Replaces the SendGrid-based email_agent from the playground prototype.

Uses the same Resend pattern as the backend's resume request endpoint
(personal-assistant/backend/app/api/v1/portfolio.py lines 469-537).
"""
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


def _markdown_to_html(markdown_text: str) -> str:
    """Convert markdown to HTML. Falls back to pre-wrapped plain text."""
    try:
        import markdown as md
        return md.markdown(markdown_text, extensions=["fenced_code", "tables"])
    except ImportError:
        # Graceful fallback if markdown library not installed
        escaped = markdown_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"<pre style='font-family:sans-serif;white-space:pre-wrap'>{escaped}</pre>"


def send_research_report(
    markdown_report: str,
    subject: str,
    recipient: Optional[str] = None,
) -> dict:
    """
    Send a research report as an HTML email via Resend.

    Args:
        markdown_report: The full markdown report content.
        subject: Email subject line.
        recipient: Recipient email address. Falls back to RESEARCH_NOTIFICATION_EMAIL env var.

    Returns:
        dict with status and Resend message ID.

    Raises:
        ValueError: If no recipient is configured.
        RuntimeError: If RESEND_API_KEY is missing.
    """
    import resend  # lazy import — only needed when sending

    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        raise RuntimeError(
            "RESEND_API_KEY environment variable not set. Cannot send notification."
        )

    from_email = os.environ.get("RESEND_FROM_EMAIL", "noreply@example.com")
    to_email = recipient or os.environ.get("RESEARCH_NOTIFICATION_EMAIL")
    if not to_email:
        raise ValueError(
            "No recipient email configured. Set RESEARCH_NOTIFICATION_EMAIL env var "
            "or pass recipient explicitly."
        )

    resend.api_key = api_key

    html_body = _markdown_to_html(markdown_report)

    params: resend.Emails.SendParams = {
        "from": f"Deep Research <{from_email}>",
        "to": [to_email],
        "subject": subject,
        "html": html_body,
    }

    logger.info(f"Sending research report to {to_email}: '{subject}'")
    result = resend.Emails.send(params)
    msg_id = result.get("id") if isinstance(result, dict) else getattr(result, "id", None)
    logger.info(f"Research report sent. Resend ID: {msg_id}")

    return {"status": "sent", "id": msg_id, "to": to_email}
