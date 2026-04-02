# Prompts — Migrated to Database

Prompt text (`.txt` files) have been migrated to the `llm_prompts` database table and are no longer stored here.

The source of truth for prompt text is the DB. Use the admin UI or seed script to manage prompts.

## Schema files (`*_schema.json`)

Still present as reference and for DB seeding. Each schema file defines:

- `_input_schema` — dynamic form fields shown in the AgentPanel UI
- `_comfyui` — workflow mappings for ComfyUI execution
- `_validation_rules` — LLM output validation constraints (counts, uniqueness rules)
- JSON schema — Pydantic model structure for validating LLM output

## Template Variables in Prompt Text

Prompts stored in DB can use `{field_name}` placeholders for any **non-file** field
defined in `_input_schema.fields`. At runtime, values entered by the user are
substituted into the prompt before it is sent to the LLM.

**Example** — if your prompt text in DB contains:

```
Generate {num_rows} variations. Image filenames: image_01 to image_{num_rows}.
```

And the user selects `num_rows = 4`, the LLM receives:

```
Generate 4 variations. Image filenames: image_01 to image_4.
```

The schema injection block (auto-appended after the prompt) also reflects the
dynamic value — e.g. `mode=VARIATION: 4 variations` instead of the static schema default.
