# `deep_research`

**Status: ✅ Completed**

Multi-agent deep research pipeline built on the OpenAI Agents SDK. Coordinates three specialised agents — planner, searcher, and writer — running web searches in parallel, then synthesising a comprehensive report. Prompt instructions are fully externalised to YAML files, making research behaviour configurable without touching Python.

---

## Tools

| Tool | Function | Tags |
|------|----------|------|
| Deep Research | `deep_research` | `research`, `web`, `analysis`, `report`, `multi-agent` |
| Research to Article | `research_to_article` | `research`, `article`, `portfolio`, `blog`, `multi-agent` |

---

## Tool Reference

### `deep_research`

Run the full multi-agent pipeline on any topic. Returns a structured markdown report.

```python
deep_research(
    query: str,
    variant: str = "general",              # general | technical | market | article
    send_notification: bool = False,       # Email report via Resend
    notification_recipient: Optional[str] = None,  # Overrides RESEARCH_NOTIFICATION_EMAIL
)
```

**Returns:**
```python
{
    "success": True,
    "variant": "general",
    "query": "...",
    "output_type": "report",    # "report" or "article"
    "content": "# Full markdown report...",
    "status_log": [
        "Starting research (variant: general)...",
        "Trace: https://platform.openai.com/traces/...",
        "Searches planned (5 queries), searching...",
        "Searches complete (5 results), writing report...",
        "Report written.",
        "Research complete.",
    ],
}
```

---

### `research_to_article`

Research a topic and automatically post the result as a portfolio blog draft.
Chains `deep_research` (article variant) → `portfolio_publisher.create_article`.

```python
research_to_article(
    topic: str,
    category: Optional[str] = None,   # e.g. "AI", "Architecture", "Tutorial"
    auto_publish: bool = False,        # True = publish immediately, False = save as draft
)
```

**Returns:**
```python
{
    "success": True,
    "id": 42,
    "slug": "building-rag-pipelines-2026-03",
    "title": "Building RAG Pipelines in 2026",
    "status": "draft",
    "url": None,    # populated when published
    "message": "Article '...' saved as draft. Slug: ...",
}
```

---

## Pipeline Architecture

```
query + variant
    │
    ▼
PlannerAgent ──────────────────────── WebSearchPlan (N queries)
    │                                  structured output
    ▼
SearchAgent × N ──────────────────── parallel execution
    │                                  summaries (< 300-400 words each)
    ▼
WriterAgent ───────────────────────── ReportData | ArticleReportData
    │                                  structured output
    ▼
[Notifier] ────────────────────────── Resend HTML email (optional)
```

All agents are created via factory functions that inject the correct prompt from YAML, so the same Python code handles all variants.

---

## Prompt Variants

| Variant | Searches | Output Type | Writer Target | Best For |
|---------|:--------:|-------------|---------------|----------|
| `general` | 5 | `ReportData` | 1000+ word report | Broad research questions |
| `technical` | 6 | `ReportData` | 1200+ word deep-dive | Architecture, code, internals |
| `market` | 6 | `ReportData` | 1000+ word analysis | Competitive landscape |
| `article` | 4 | `ArticleReportData` | 800–1200 word blog post | Portfolio blog articles |

### Adding a New Variant

Create a YAML file — no Python changes needed:

```bash
# e.g. for legal research
touch kk_agent_skills/deep_research/prompts/legal.yaml
```

```yaml
# prompts/legal.yaml
name: legal
description: "Legal and regulatory research."

planner:
  num_searches: 5
  instruction: |
    You are a legal research assistant. Plan {num_searches} searches to cover
    applicable regulations, case law, and compliance requirements.

search:
  context_size: medium
  instruction: |
    Summarise search results for a legal analyst. Focus on specific rules,
    statutes, and precedents. Under 350 words.

writer:
  min_words: 1000
  format: markdown
  output_type: report
  instruction: |
    You are a legal analyst. Write a clear regulatory overview with sections
    for applicable law, key requirements, and compliance checklist.

notification:
  enabled: true
  subject_template: "Legal Research: {query}"
```

---

## Output Schemas

```python
# Used by general / technical / market variants
class ReportData(BaseModel):
    short_summary: str                     # 2-3 sentences (10–1000 chars)
    markdown_report: str                   # Full report (min 100 chars)
    follow_up_questions: list[str]
    search_queries_used: list[str]
    sources: list[str]

# Used by the article variant
class ArticleReportData(BaseModel):
    title: str                             # Blog post title (5–500 chars)
    excerpt: str                           # 1-2 sentence teaser (10–500 chars)
    markdown_content: str                  # Full article (min 100 chars)
    tags: list[str]
    follow_up_questions: list[str]
```

---

## File Structure

```
deep_research/
├── __init__.py
├── skill.py                  # SkillManifest
├── tools.py                  # @agent_tool: deep_research, research_to_article
├── schemas.py                # Pydantic output models
├── research_manager.py       # Async orchestration engine (ResearchManager)
├── config.json               # Defaults
├── prompts/
│   ├── general.yaml
│   ├── technical.yaml
│   ├── market.yaml
│   └── article.yaml
└── agents/
    ├── __init__.py
    ├── _prompt_loader.py     # Cached YAML loader with typed getters
    ├── planner_agent.py      # make_planner_agent(variant, model)
    ├── search_agent.py       # make_search_agent(variant, model)
    ├── writer_agent.py       # make_writer_agent(variant, model)
    └── notifier.py           # send_research_report() via Resend
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for Agents SDK |
| `RESEND_API_KEY` | For notifications | Resend email delivery key |
| `RESEND_FROM_EMAIL` | For notifications | Verified sender address |
| `RESEARCH_NOTIFICATION_EMAIL` | For notifications | Default recipient (can be overridden per call) |

---

## Dependencies

- `openai-agents` — Agent, Runner, WebSearchTool, trace, gen_trace_id
- `resend` — Email delivery (replaces SendGrid from playground prototype)
- `pyyaml` — YAML prompt loading
- `markdown` — Optional, HTML conversion for email body
- `nest_asyncio` — Async bridge for sync callers

## Config (`config.json`)

| Key | Default | Description |
|-----|---------|-------------|
| `default_model` | `"gpt-4o-mini"` | LLM used by all agents |
| `default_variant` | `"general"` | Variant when none specified |
| `valid_variants` | `[...]` | Allowed variant names |
| `notification_enabled` | `true` | Whether notification is active |
| `notification_recipient` | `""` | Default recipient (blank = use env var) |
