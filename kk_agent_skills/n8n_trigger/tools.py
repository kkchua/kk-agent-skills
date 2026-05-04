"""
n8n_trigger skill — tools.py

agentskills.io-compatible tool module.
Trigger registered n8n automation workflows via the personal-assistant API.
"""
import logging
from typing import Any, Dict, Optional

from kk_utils.agent_tools import agent_tool, _auto_register

logger = logging.getLogger(__name__)


@agent_tool(
    name="List N8N Workflows",
    description=(
        "List all registered n8n automation workflows with their parameter schemas. "
        "Each workflow entry includes: name, description, and a 'params' dict where each key "
        "is a parameter name with 'type', 'required', and 'description' fields. "
        "Always call this before triggering a workflow to know exactly what data to pass."
    ),
    tags=["n8n_trigger", "n8n", "automation", "workflow"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def list_n8n_workflows(
    user_id: Optional[str] = None,
) -> dict:
    """
    List all registered n8n workflows with parameter schemas.

    Returns a list of workflow objects, each with:
      - name: str — workflow identifier used in trigger_n8n_workflow
      - description: str — what the workflow does
      - params: dict — parameter schema, e.g.:
          {
            "to":      {"type": "string", "required": true,  "description": "Recipient email"},
            "subject": {"type": "string", "required": true,  "description": "Email subject"},
            "cc":      {"type": "string", "required": false, "description": "CC address"},
          }

    Args:
        user_id: User ID (auto-injected by Governor)
    """
    from kk_agent_skills._http_client import call_tool
    return call_tool("list-n8n-workflows", {})


@agent_tool(
    name="Trigger N8N Workflow",
    description=(
        "Trigger a registered n8n automation workflow by name, passing the required parameters. "
        "IMPORTANT: Call 'List N8N Workflows' first to get the exact parameter names and types "
        "required by the workflow. Then build the 'data' dict with those keys. "
        "Required params must be present or the backend will reject the request. "
        "Example: trigger 'send-email' with data={'to': 'x@y.com', 'subject': 'Hi', 'body': '...'}."
    ),
    tags=["n8n_trigger", "n8n", "automation", "workflow", "trigger"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=True,
    is_destructive=False,
)
def trigger_n8n_workflow(
    workflow_name: str,
    data: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None,
) -> dict:
    """
    Trigger a registered n8n workflow by name.

    Args:
        workflow_name: Exact workflow name from list_n8n_workflows (e.g. 'send-email')
        data: Payload dict with keys matching the workflow's params schema.
              Required params must be included or the call will fail with a validation error.
              Example for 'send-email':
                {"to": "user@example.com", "subject": "Hello", "body": "Hi there"}
        user_id: User ID (auto-injected by Governor)

    Returns:
        {"success": True, "workflow": "...", "data": <n8n response>}
        or
        {"success": False, "error": "Missing required parameter(s): ..."}
    """
    from kk_agent_skills._http_client import call_tool

    logger.info(f"Triggering n8n workflow '{workflow_name}' for user {user_id}")
    return call_tool("trigger-n8n", {"workflow": workflow_name, "data": data or {}})


_auto_register()
