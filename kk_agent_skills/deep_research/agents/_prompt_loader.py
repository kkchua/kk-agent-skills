"""
deep_research — _prompt_loader.py

Loads YAML prompt configs from the prompts/ directory and returns
typed dicts for use by agent factory functions.
"""
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
_VALID_VARIANTS = {"general", "technical", "market", "article"}


@lru_cache(maxsize=16)
def load_prompt(variant: str) -> dict[str, Any]:
    """
    Load a prompt YAML by variant name.

    Args:
        variant: One of "general", "technical", "market", "article"

    Returns:
        Parsed YAML dict.

    Raises:
        ValueError: If variant is unknown.
        FileNotFoundError: If YAML file is missing.
    """
    import yaml  # lazy import — yaml only needed at load time

    if variant not in _VALID_VARIANTS:
        raise ValueError(
            f"Unknown prompt variant '{variant}'. Valid: {sorted(_VALID_VARIANTS)}"
        )

    path = _PROMPTS_DIR / f"{variant}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    logger.debug(f"Loaded prompt variant '{variant}' from {path}")
    return config


def get_planner_instruction(variant: str) -> tuple[str, int]:
    """Returns (rendered_instruction, num_searches) for the planner agent."""
    config = load_prompt(variant)
    planner = config["planner"]
    num_searches = planner.get("num_searches", 5)
    instruction = planner["instruction"].format(num_searches=num_searches)
    return instruction, num_searches


def get_search_instruction(variant: str) -> tuple[str, str]:
    """Returns (instruction, context_size) for the search agent."""
    config = load_prompt(variant)
    search = config["search"]
    return search["instruction"], search.get("context_size", "low")


def get_writer_instruction(variant: str) -> tuple[str, str]:
    """Returns (instruction, output_type) for the writer agent."""
    config = load_prompt(variant)
    writer = config["writer"]
    return writer["instruction"], writer.get("output_type", "report")


def get_notification_config(variant: str) -> dict[str, Any]:
    """Returns notification config dict."""
    config = load_prompt(variant)
    return config.get("notification", {"enabled": False, "subject_template": "Research: {query}"})
