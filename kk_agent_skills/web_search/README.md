# `web_search`

**Status: ✅ Completed**

Real-time web search powered by [Tavily](https://tavily.com). Returns titles, URLs, and content snippets from the most relevant pages. Used directly by agents needing up-to-date information, and internally by `article_generation`.

---

## Tools

| Tool | Function | Tags |
|------|----------|------|
| Web Search | `web_search` | `search`, `research`, `web` |

---

## Tool Reference

### `web_search`

Search the web and return structured results.

```python
web_search(
    query: str,
    max_results: int = 5,          # 1–10
    search_depth: str = "basic",   # basic (fast) | advanced (higher quality)
)
```

**Returns:**
```python
{
    "results": [
        {
            "title": "Understanding Vector Databases",
            "url": "https://example.com/vector-dbs",
            "content": "Vector databases store embeddings...",
        },
    ],
    "total": 5,
    "query": "vector databases overview",
    "success": True,
}
```

On failure:
```python
{
    "results": [],
    "total": 0,
    "query": "...",
    "success": False,
    "error": "Tavily API error: ...",
}
```

---

## Search Depth

| Value | Speed | Quality | Use When |
|-------|-------|---------|----------|
| `basic` | Fast | Good | Quick lookups, factual questions |
| `advanced` | Slower | Higher | Deep research, complex topics |

---

## Dependencies

- `app.services.web_search_service` — Tavily service wrapper (lazy import)
- `nest_asyncio` — async bridge for sync context
- `TAVILY_API_KEY` env var (configured in backend `.env`)

## Config (`config.json`)

| Key | Default | Description |
|-----|---------|-------------|
| `default_max_results` | `5` | Default number of search results |
| `default_search_depth` | `"basic"` | Default search depth |
