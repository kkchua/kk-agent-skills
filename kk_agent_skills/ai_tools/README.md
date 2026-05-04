# `ai_tools`

**Status: ✅ Completed**

AI text-processing tools that route through `kk_utils.ai.AIService` (provider-agnostic). Use these tools to summarise content, rewrite it in a different tone, pull out actionable tasks, or classify user intent for downstream routing.

---

## Tools

| Tool | Function | Tags |
|------|----------|------|
| Summarize Text | `summarize_text` | `ai`, `summarize`, `text-processing` |
| Rewrite Text | `rewrite_text` | `ai`, `rewrite`, `text-processing` |
| Extract Tasks | `extract_tasks` | `ai`, `tasks`, `extraction` |
| Classify Intent | `classify_intent` | `ai`, `intent`, `classification` |

---

## Tool Reference

### `summarize_text`

Condense a block of text into a concise summary with optional bullet points.

```python
summarize_text(
    text: str,
    max_length: int = 150,      # Maximum summary length in words
    bullet_points: bool = True,
)
```

**Returns:**
```python
{
    "summary": "...",
    "key_points": ["...", "..."],
    "word_count": 42,
    "success": True,
}
```

---

### `rewrite_text`

Rewrite content with a different tone or style. Common tones: `professional`, `casual`, `friendly`, `formal`, `concise`.

```python
rewrite_text(
    text: str,
    tone: str = "professional",
    style: Optional[str] = None,    # Extra instructions, e.g. "use simple words"
)
```

**Returns:**
```python
{
    "rewritten_text": "...",
    "tone": "professional",
    "changes_made": ["..."],
    "success": True,
}
```

---

### `extract_tasks`

Pull actionable tasks from meeting notes, emails, or any unstructured text.

```python
extract_tasks(text: str)
```

**Returns:**
```python
{
    "tasks": [
        {"task": "...", "priority": "high", "due_date": "..."},
    ],
    "total_tasks": 3,
    "success": True,
}
```

---

### `classify_intent`

Identify the user's intent and extract entities for routing to the right tool or service.

```python
classify_intent(text: str)
```

**Returns:**
```python
{
    "intent": "search_notes",
    "confidence": 0.92,
    "entities": {"query": "meeting recap"},
    "suggested_tools": ["search_notes"],
    "success": True,
}
```

---

## Dependencies

- `kk_utils.ai.AIService` — provider-agnostic AI service (resolved at call time)
- `nest_asyncio` — async bridge for sync callers

## Config (`config.json`)

| Key | Default | Description |
|-----|---------|-------------|
| `default_max_length` | `150` | Default word limit for `summarize_text` |
| `default_tone` | `"professional"` | Default tone for `rewrite_text` |
