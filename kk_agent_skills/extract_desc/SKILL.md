---
name: extract_desc
description: Structured visual description extraction from uploaded images using a fixed vision model.
version: 1.0.0
dependencies: openai-agents
capabilities: tool_provider
metadata:
  author: personal-assistant
  version: "1.0.0"
  tags: extract_desc, vision, image, description, csv
  access_levels: user
---
# extract_desc

Structured visual description extraction from uploaded images using a fixed vision model.

## Overview

Analyzes each uploaded image and produces a structured JSON description covering:
- **subject**: main visual elements, focal points, recognizable identity
- **mood**: emotional tone, atmosphere, cinematic feeling
- **composition**: framing, depth layers, vertical flow
- **lighting**: quality, direction, color temperature
- **style**: artistic style, texture, rendering approach
- **color_palette**: dominant and accent colors
- **animatable_elements**: objects/effects that could move in video

## Tools

### `extract_image_descriptions`

```
extract_image_descriptions(image_ids: List[str]) -> dict
```

**Parameters:**
- `image_ids` — list of uploaded file IDs

**Returns:** standard `generate-csv` response with `variations` containing one description object per image.

**Note:** The vision model is fixed by `config.json` (`qwen/qwen3.6-plus` by default) and cannot be overridden by the caller.

## Config (`config.json`)

| Key | Default | Description |
|-----|---------|-------------|
| `model` | `qwen/qwen3.6-plus` | Vision model used for extraction — change here to update globally |
| `adapter_name` | `image_variation` | PA adapter |
| `prompt_name` | `extract_desc` | DB prompt entry (namespace: csv_generator) |

## Usage

Standalone:
```
extract_image_descriptions(image_ids=["file-id-1", "file-id-2"])
```

Or used internally by `csv_generator_v2` as Phase 1 of its pipeline.

## PA Backend dependency

Requires a `llm_prompts` DB entry:
- `namespace = "csv_generator"`
- `adapter = "image_variation"`
- `name = "extract_desc"`
- `prompt_text` = adapted 01_extract_desc.txt content
- `schema_json` = schema with fields: `image_filename`, `subject`, `mood`, `composition`, `lighting`, `style`, `color_palette`, `animatable_elements`
