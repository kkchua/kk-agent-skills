"""
csv_generator_v2 skill — tools.py

Two-phase image-to-CSV pipeline:
  Phase 1 — extract structured visual descriptions via POST /api/v1/tools/generate-csv
             (vision call, fixed model from extract_desc/config.json)
  Phase 2 — generate variation prompts via POST /api/v1/tools/generate-csv-from-desc
             (text-only, NO images attached, descriptions passed as structured data)
"""
import json
import logging
from pathlib import Path
from typing import List, Optional

from kk_utils.agent_tools import agent_tool, _auto_register

logger = logging.getLogger(__name__)

_EXTRACT_DESC_CONFIG_PATH = Path(__file__).parent.parent / "extract_desc" / "config.json"


def _load_extract_desc_config() -> dict:
    with _EXTRACT_DESC_CONFIG_PATH.open() as f:
        return json.load(f)


def _extract_prompts(csv_result: dict) -> List[str]:
    """Extract all t2i prompts from a generate-csv result."""
    prompts = []
    for variation in csv_result.get("variations", []):
        for key in ("t2i_prompt", "t2i_prompt1", "t2i_prompt2", "prompt"):
            p = variation.get(key, "").strip()
            if p:
                prompts.append(p)
                break
    return prompts


def _submit_prompts(prompts: List[str], user_id: Optional[str]) -> dict:
    """Submit a list of prompts as UGC image jobs."""
    from kk_agent_skills._http_client import call_tool
    jobs, failed = [], []
    for prompt in prompts:
        res = call_tool("submit-ugc-image", {"prompt": prompt, "user_id": user_id})
        if res.get("success"):
            jobs.append({"job_id": res["job_id"], "prompt": prompt[:80]})
        else:
            failed.append({"prompt": prompt[:80], "error": res.get("error", "unknown")})
    return {"submitted": len(jobs), "failed": len(failed), "jobs": jobs, "errors": failed}


@agent_tool(
    name="Generate CSV from Images V2",
    description=(
        "Two-phase image-to-CSV pipeline for ComfyUI T2I batch workflows. "
        "Phase 1 extracts structured visual descriptions from each image using a fixed vision model. "
        "Phase 2 generates variation prompts enriched by those descriptions. "
        "Returns download links for JSON and CSV files. "
        "Set auto_submit=True to automatically submit all generated prompts as UGC image jobs."
    ),
    tags=["csv_generator_v2", "csv_generator", "csv", "studio", "image", "generation"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def generate_csv_v2(
    image_ids: List[str],
    adapter_name: str = "image_variation",
    prompt_name: str = "vertical_master_prompt_v2",
    num_rows: int = 4,
    model: Optional[str] = None,
    auto_submit: bool = False,
    user_id: Optional[str] = None,
) -> dict:
    """
    Generate CSV variation prompts from uploaded images using a two-phase pipeline.

    Args:
        image_ids: List of uploaded file IDs (from agent file upload)
        adapter_name: Adapter to use (default: image_variation)
        prompt_name: Prompt variant for generation phase (default: vertical_master_prompt_v2)
        num_rows: Number of variations per image for generation phase (default: 4)
        model: AI model for generation phase only — extraction model is fixed by extract_desc config
        auto_submit: If True, automatically submit all generated prompts as UGC image jobs
        user_id: User ID (auto-injected by Governor)
    """
    from kk_agent_skills._http_client import call_tool

    extract_config = _load_extract_desc_config()

    # Phase 1: extract structured visual descriptions (model fixed, not user-overridable)
    logger.info(f"[csv_generator_v2] Phase 1: extracting descriptions for {len(image_ids)} image(s)")
    desc_result = call_tool("extract-image-desc", {
        "image_ids": image_ids,
        "prompt_name": extract_config["prompt_name"],
        "model": extract_config["model"],
    })

    if not desc_result.get("success"):
        return {
            "success": False,
            "error": f"Description extraction failed: {desc_result.get('error', 'unknown error')}",
        }

    descriptions = desc_result.get("descriptions", [])
    logger.info(f"[csv_generator_v2] Phase 1 complete: {len(descriptions)} description(s) extracted")

    # Phase 2: generate CSV prompts from descriptions — text-only, no images attached
    logger.info(f"[csv_generator_v2] Phase 2: generating {num_rows} variations with enriched context")
    result = call_tool("generate-csv-from-desc", {
        "descriptions": descriptions,
        "adapter_name": adapter_name,
        "prompt_name": prompt_name,
        "num_rows": num_rows,
        "model": model,
    })

    if auto_submit and result.get("success"):
        prompts = _extract_prompts(result)
        if prompts:
            result["image_jobs"] = _submit_prompts(prompts, user_id)

    return result


_auto_register()
