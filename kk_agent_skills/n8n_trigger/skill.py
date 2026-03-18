"""
n8n_trigger — SkillManifest

Trigger registered n8n automation workflows via the personal-assistant API.
"""
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="n8n_trigger",
    display_name="N8N Workflow Trigger",
    description=(
        "Trigger registered n8n automation workflows by name. "
        "Use this to fire email, Slack, social publishing, or any other "
        "n8n workflow configured in the personal-assistant backend."
    ),
    version="1.0.0",
    tags=["n8n", "automation", "workflow", "trigger"],
    collection=None,
    capabilities=["tool_provider"],
    min_access_level="user",
)
