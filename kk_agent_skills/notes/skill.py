"""
notes — SkillManifest

Full CRUD note management skill. Supports search, create, and update operations.
"""
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="notes",
    display_name="Notes",
    description=(
        "Full CRUD note management. Supports searching, creating, and updating notes "
        "stored in the personal assistant database."
    ),
    version="1.0.0",
    tags=["notes", "crud"],
    collection=None,
    capabilities=["tool_provider"],
    min_access_level="user",
)
