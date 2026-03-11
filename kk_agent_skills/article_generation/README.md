# `article_generation`

**Status: ✅ Completed**

Single-shot research and article generation. Searches the web via Tavily, synthesises the results, and writes a structured markdown article saved as a draft in the Portfolio site.

> **Choosing between skills:**
> Use `article_generation` for quick, single-pass article drafts.
> Use [`deep_research`](../deep_research/README.md) when you need deeper multi-agent research, parallel searches, different research flavours (technical/market/general), or email notification of results.

---

## Tools

| Tool | Function | Tags |
|------|----------|------|
| Research and Write Article | `research_and_write_article` | `research`, `writing`, `blog`, `article` |

---

## Tool Reference

### `research_and_write_article`

Research a topic using Tavily web search, then generate and save a structured article draft.

```python
research_and_write_article(
    topic: str,                          # Article topic or subject
    category: Optional[str] = None,     # e.g. "Architecture", "Tools", "Tutorial"
    tone: str = "technical",            # technical | accessible | reference
    num_search_results: int = 4,        # Number of Tavily results (1–8)
)
```

**Returns:**
```python
{
    "title": "Understanding Vector Databases",
    "slug": "understanding-vector-databases",
    "excerpt": "...",
    "tags": ["vector-db", "rag", "ai"],
    "category": "Architecture",
    "search_results_used": 4,
    "status": "draft",
    "message": "Article '...' has been researched and saved as a draft. Visit /admin to preview and publish it.",
    "success": True,
}
```

---

## Pipeline

```
Tavily web search (num_search_results)
    ↓
ArticleGenerationService.generate()
    ↓
Markdown article (1500 words, structured headings)
    ↓
Saved to blog_posts (status="draft")
```

---

## Dependencies

- `app.services.article_generation_service` — backend article generation (lazy import)
- `app.services.web_search_service` — Tavily search service (lazy import)
- `app.database.session` — database session context (lazy import)
- `TAVILY_API_KEY` env var (set in backend `.env`)

## Config (`config.json`)

| Key | Default | Description |
|-----|---------|-------------|
| `default_max_length` | `1500` | Target article word count |
| `default_tone` | `"technical"` | Default writing tone |
