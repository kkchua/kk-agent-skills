---
name: csv_generator_v2
description: Two-phase image-to-CSV pipeline for ComfyUI T2I batch workflows.
version: 1.0.0
dependencies: openai-agents
capabilities: tool_provider
tags: csv, image, generation
metadata:
  author: personal-assistant
  access_levels: user
---
## Overview

Improves on `csv_generator` by running a dedicated description extraction pass first, then feeding those structured descriptions as context into the prompt generation phase. This gives the generation LLM a richer, pre-analyzed view of each image rather than relying solely on raw vision.

## Pipeline

```
Phase 1 — extract_desc
  call generate-csv (prompt: extract_desc, model: fixed from extract_desc/config.json)
  → structured descriptions per image

Phase 2 — generate CSV
  call generate-csv (prompt: vertical_master_prompt_v2, descriptions injected via {descriptions})
  → JSON + CSV download links
```

Both phases use the same `POST /api/v1/tools/generate-csv` endpoint.

## Tools

### `generate_csv_v2`

```
generate_csv_v2(
    image_ids: List[str],
    adapter_name: str = "image_variation",
    prompt_name: str = "vertical_master_prompt_v2",
    num_rows: int = 4,
    model: Optional[str] = None,
    auto_submit: bool = False,
) -> dict
```

**Parameters:**
- `image_ids` — uploaded file IDs
- `adapter_name` — adapter for generation phase (default: image_variation)
- `prompt_name` — prompt for generation phase (default: vertical_master_prompt_v2)
- `num_rows` — variations per image in generation phase (default: 4)
- `model` — model for generation phase only; extraction model is fixed by `extract_desc/config.json`
- `auto_submit` — submit generated prompts as UGC image jobs automatically

**Returns:** standard `generate-csv` response with `downloads`, `variations`, etc. If `auto_submit=True`, also includes `image_jobs`.

## Config (`config.json`)

| Key | Default | Description |
|-----|---------|-------------|
| `default_num_rows` | `4` | Default variation count for generation phase |
| `default_prompt_name` | `vertical_master_prompt_v2` | Default prompt for generation phase |

Extraction model is configured separately in `extract_desc/config.json`.

## PA Backend dependency

- `generate-csv` endpoint must accept optional `descriptions: str` field
- DB prompt entry `vertical_master_prompt_v2` must include the `{descriptions}` placeholder
- DB prompt entry `extract_desc` must exist (see `extract_desc` skill)
