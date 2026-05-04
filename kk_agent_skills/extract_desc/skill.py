"""
extract_desc — SkillManifest

Structured visual description extraction from images using a fixed vision model.
"""
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="extract_desc",
    display_name="Extract Image Descriptions",
    description=(
        "Analyze uploaded images with AI vision and produce structured visual descriptions "
        "covering subject, mood, composition, lighting, style, color palette, and animatable elements. "
        "Uses a fixed vision model configured in skill config — not user-overridable."
    ),
    version="1.0.0",
    tags=["vision", "image", "description", "csv"],
    collection=None,
    capabilities=["tool_provider"],
    min_access_level="user",
)
