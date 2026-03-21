---
name: csv_generator
description: Schema-driven CSV generator — analyzes images with AI vision and generates structured JSON + CSV variation prompts for ComfyUI batch workflows.
version: 1.0.0
dependencies: openai-agents
capabilities: tool_provider
tags: csv, studio, image, generation
metadata:
  author: personal-assistant
  access_levels: user
---

# csv_generator

AI-powered image-to-CSV generator. Analyzes uploaded images using AI vision and generates
structured variation prompts (JSON + CSV) for downstream ComfyUI T2I batch workflows.

## Adapters

| Adapter | Description |
|---|---|
| `image_variation` | Generate VARIATION or STORYLINE mode prompts from images |

## Prompts (per adapter)

| Prompt | Model Target | Description |
|---|---|---|
| `master_prompt_qwen` | Qwen VL | Optimized for Qwen vision model |
| `master_prompt_hidream` | HiDream | Optimized for HiDream model |

## Output

- JSON: structured variation data with mode, subject, camera directions, prompts
- CSV: `||` delimited file with image_filename, t2i_prompt1, t2i_prompt2, negative_prompt columns

## Validation

AI output is validated against the prompt's schema (Pydantic model built dynamically):
- VARIATION mode: exactly 6 variations, all camera_direction values must be unique
- STORYLINE mode: 3–4 variations
- Field length checks (CJK-aware weighted length)
