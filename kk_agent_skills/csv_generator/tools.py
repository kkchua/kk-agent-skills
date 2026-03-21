"""
csv_generator skill — tools.py

Schema-driven image-to-CSV generator.
Uploads images are analyzed by AI vision and structured JSON + CSV output is generated.
Calls personal-assistant API via HTTP client (architecture rule: no direct kk-utils imports).
"""
import logging
from typing import List, Optional

from kk_utils.agent_tools import agent_tool, _auto_register

logger = logging.getLogger(__name__)


@agent_tool(
    name="Generate CSV from Images",
    description=(
        "Analyze uploaded images with AI vision and generate structured JSON + CSV variation "
        "prompts for ComfyUI T2I batch workflows. Returns download links for JSON and CSV files. "
        "Set auto_submit=True to automatically submit all generated prompts as UGC image jobs."
    ),
    tags=["csv", "studio", "image", "generation"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def generate_csv_from_images(
    image_ids: List[str],
    adapter_name: str = "image_variation",
    prompt_name: str = "master_prompt_qwen",
    num_rows: int = 6,
    model: Optional[str] = None,
    auto_submit: bool = False,
    user_id: Optional[str] = None,
) -> dict:
    """
    Generate CSV variation prompts from uploaded images.

    Args:
        image_ids: List of uploaded file IDs (from agent file upload)
        adapter_name: Adapter to use (default: image_variation)
        prompt_name: Prompt variant (master_prompt_qwen or master_prompt_hidream)
        num_rows: Number of variations per image (3-6, default: 6)
        model: AI model override (uses PA default if not specified)
        auto_submit: If True, automatically submit all generated prompts as UGC image jobs
        user_id: User ID (auto-injected by Governor)
    """
    from kk_agent_skills._http_client import call_tool
    result = call_tool("generate-csv", {
        "image_ids": image_ids,
        "adapter_name": adapter_name,
        "prompt_name": prompt_name,
        "num_rows": num_rows,
        "model": model,
    })

    if auto_submit and result.get("success"):
        prompts = _extract_prompts(result)
        if prompts:
            submit_result = _submit_prompts(prompts, user_id)
            result["image_jobs"] = submit_result

    return result


def _extract_prompts(csv_result: dict) -> List[str]:
    """Extract all t2i prompts from a generate-csv result."""
    prompts = []
    for image_data in csv_result.get("images", []):
        for variation in image_data.get("variations", []):
            for key in ("t2i_prompt", "t2i_prompt1", "t2i_prompt2", "prompt"):
                p = variation.get(key, "").strip()
                if p:
                    prompts.append(p)
                    break
    return prompts


def _submit_prompts(prompts: List[str], user_id: Optional[str]) -> dict:
    """Submit a list of prompts as UGC image jobs."""
    from kk_agent_skills._http_client import call_tool
    jobs = []
    failed = []
    for prompt in prompts:
        res = call_tool("submit-ugc-image", {"prompt": prompt, "user_id": user_id})
        if res.get("success"):
            jobs.append({"job_id": res["job_id"], "prompt": prompt[:80]})
        else:
            failed.append({"prompt": prompt[:80], "error": res.get("error", "unknown")})
    return {"submitted": len(jobs), "failed": len(failed), "jobs": jobs, "errors": failed}


@agent_tool(
    name="Submit UGC Image Jobs",
    description=(
        "Submit one or more text-to-image prompts as UGC image generation jobs. "
        "Each prompt is sent to the Wan image workflow — results appear in the Media Gallery."
    ),
    tags=["csv", "studio", "image", "generation"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def submit_ugc_image_jobs(
    prompts: List[str],
    user_id: Optional[str] = None,
) -> dict:
    """
    Submit prompts as UGC image generation jobs.

    Args:
        prompts: List of text-to-image prompts to submit
        user_id: User ID (auto-injected by Governor)
    """
    if not prompts:
        return {"success": False, "error": "No prompts provided"}
    result = _submit_prompts(prompts, user_id)
    result["success"] = result["submitted"] > 0
    return result


@agent_tool(
    name="Dry-Run CSV from Saved Response",
    description=(
        "Re-run the validation and CSV generation pipeline using a previously saved raw LLM response "
        "(.raw.json file in uploads/csv_output/_debug/). Useful for fixing validation bugs without "
        "re-calling the LLM. Provide the raw_response_path from the debug logs."
    ),
    tags=["csv", "studio", "debug", "dry-run"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def dryrun_csv_from_saved_response(
    raw_response_path: str,
    adapter_name: str = "image_variation",
    prompt_name: str = "master_prompt_qwen",
    user_id: Optional[str] = None,
) -> dict:
    """
    Re-run validation + CSV generation from a saved raw LLM response file.

    Args:
        raw_response_path: Absolute path to the .raw.json file saved by a previous run
        adapter_name: Adapter to use (default: image_variation)
        prompt_name: Prompt variant matching the original run
        user_id: User ID (auto-injected by Governor)
    """
    from kk_agent_skills._http_client import call_tool
    return call_tool("dryrun-csv", {
        "raw_response_path": raw_response_path,
        "adapter_name": adapter_name,
        "prompt_name": prompt_name,
    })


_auto_register()
