"""
Internal HTTP client for skill → personal-assistant API calls.

Skills use this instead of importing kk-utils services directly.
This enforces the architecture rule:
  kk-agent-skills calls personal-assistant API (never kk-utils services)

Configuration via environment variables:
  PERSONAL_ASSISTANT_API_URL  Base URL of the personal-assistant backend
                               (default: http://localhost:8000)
  SKILL_INTERNAL_KEY          Shared secret sent as X-Internal-Key header
                               (optional — if unset, no auth header is added)
"""
import os
import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)

_PA_BASE_URL: str = os.environ.get("PERSONAL_ASSISTANT_API_URL", "http://localhost:8000").rstrip("/")
_INTERNAL_KEY: str = os.environ.get("SKILL_INTERNAL_KEY", "")

# Reuse a single session for connection pooling
_session = requests.Session()
_session.headers.update({"Content-Type": "application/json"})
if _INTERNAL_KEY:
    _session.headers.update({"X-Internal-Key": _INTERNAL_KEY})


def call_tool(
    tool_name: str,
    payload: Dict[str, Any],
    user_token: Optional[str] = None,
    timeout: int = 60,
) -> Dict[str, Any]:
    """
    POST to POST /api/v1/tools/{tool_name} and return the parsed JSON response.

    Args:
        tool_name:   Tool endpoint name, e.g. "web-search", "create-note"
        payload:     JSON body to send
        user_token:  Optional Bearer token for user-context calls.
                     If provided, overrides the X-Internal-Key header.
        timeout:     Request timeout in seconds (default: 60)

    Returns:
        Parsed JSON dict from the API.  Always contains "success" key.
        On network/HTTP error returns {"success": False, "error": "<message>"}.
    """
    url = f"{_PA_BASE_URL}/api/v1/tools/{tool_name}"
    headers = {}
    if user_token:
        headers["Authorization"] = f"Bearer {user_token}"

    try:
        resp = _session.post(url, json=payload, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as exc:
        body = {}
        try:
            body = exc.response.json()
        except Exception:
            pass
        error_detail = body.get("detail", str(exc))
        logger.error("Tool call %s HTTP error %s: %s", tool_name, exc.response.status_code, error_detail)
        return {"success": False, "error": error_detail, "status_code": exc.response.status_code}
    except requests.exceptions.ConnectionError as exc:
        logger.error("Tool call %s connection error: %s", tool_name, exc)
        return {"success": False, "error": f"Cannot connect to personal-assistant API at {_PA_BASE_URL}"}
    except requests.exceptions.Timeout:
        logger.error("Tool call %s timed out after %ss", tool_name, timeout)
        return {"success": False, "error": f"Tool call {tool_name} timed out"}
    except Exception as exc:
        logger.error("Tool call %s unexpected error: %s", tool_name, exc, exc_info=True)
        return {"success": False, "error": str(exc)}
