"""
extract_desc skill — tools.py

Extracts structured visual descriptions from uploaded images using a fixed
vision model. Delegates to the existing generate-csv PA endpoint with the
extract_desc prompt, so no new API routes are needed.
"""
import json
import logging
from pathlib import Path
from typing import List, Optional

from kk_utils.agent_tools import agent_tool, _auto_register

logger = logging.getLogger(__name__)

_CONFIG_PATH = Path(__file__).parent / "config.json"


def _load_config() -> dict:
    with _CONFIG_PATH.open() as f:
        return json.load(f)


@agent_tool(
    name="Extract Image Descriptions",
    description=(
        "Analyze uploaded images with AI vision and return structured visual descriptions "
        "covering subject, mood, composition, lighting, style, color palette, and animatable elements. "
        "The vision model is fixed by skill configuration and cannot be overridden by the caller. "
        "Returns one description object per image."
    ),
    tags=["extract_desc", "vision", "image", "description", "csv"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def extract_image_descriptions(
    image_ids: List[str],
    user_id: Optional[str] = None,
) -> dict:
    """
    Analyze uploaded images and return structured visual descriptions.

    Args:
        image_ids: List of uploaded file IDs (from agent file upload)
        user_id: User ID (auto-injected by Governor)

    Returns:
        {"success": True, "variations": [{image_filename, subject, mood, composition,
          lighting, style, color_palette, animatable_elements}, ...]}
    """
    from kk_agent_skills._http_client import call_tool

    config = _load_config()
    return call_tool("extract-image-desc", {
        "image_ids": image_ids,
        "prompt_name": config["prompt_name"],
        "model": config["model"],  # hardcoded — not user-overridable
    })


_auto_register()
