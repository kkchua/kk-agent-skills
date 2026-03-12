---
name: deep-research
description: Multi-agent deep research pipeline for comprehensive topic analysis. Plans targeted web searches, executes them in parallel, and synthesizes structured reports. Use when researching complex topics, analyzing markets, or creating in-depth technical reports.
license: MIT
compatibility: Requires OpenAI API key, Tavily API key for web search, and network access
metadata:
  author: kkchua
  version: "1.0.0"
  tags: research, web, analysis, report, multi-agent
allowed-tools: Bash(curl:*) Read Write
---

# Deep Research Skill

## Overview

Multi-agent deep research pipeline for comprehensive topic analysis. Uses targeted web searches, parallel execution, and AI synthesis to produce structured reports.

## When to Use

- Researching complex technical topics
- Analyzing market trends and competitive landscapes
- Creating comprehensive reports with multiple sources
- Gathering information for blog posts or articles
- Deep dives into unfamiliar domains

## What It Does

1. **Plans targeted searches** - Creates a search plan with multiple queries based on the research topic
2. **Executes searches in parallel** - Runs all searches concurrently for speed (5-10 queries at once)
3. **Synthesizes findings** - AI analyzes all results and combines them into coherent insights
4. **Produces structured output** - Returns comprehensive markdown report with sections, summaries, and follow-up questions

## Usage

```python
from kk_agent_skills.deep_research.tools import deep_research

# Run full research pipeline
result = deep_research(
    query="AI agent memory architectures",
    variant="technical",  # general, technical, market, article
    send_notification=False,
)

if result.get("success"):
    print(result["content"])  # Markdown report
else:
    print(f"Error: {result.get('error')}")
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | str | required | Research topic or question |
| `variant` | str | "general" | Prompt variant: general, technical, market, article |
| `send_notification` | bool | False | Email report via Resend when done |
| `notification_recipient` | str | None | Override recipient email |
| `user_id` | str | auto | Auto-injected by Governor |

## Variant Types

### general (default)
Broad research suitable for most topics. Balanced depth and breadth.

### technical
Focused on architecture, implementation details, code patterns, and technical trade-offs. Best for engineering research.

### market
Analyzes competitive landscape, market trends, positioning, and business implications. Best for business research.

### article
Optimized for blog-ready output with introduction, sections, and conclusion. Best for content creation.

## Output Format

```python
{
    "success": True,
    "variant": "technical",
    "query": "AI agent memory architectures",
    "output_type": "report",
    "content": "# Technical Report: AI Agent Memory...\n\n...",
    "status_log": [
        "Starting research (variant: technical)...",
        "Searches planned (5 queries), searching...",
        "Searches complete (42 results), writing report...",
        "Report written."
    ]
}
```

## Pipeline Stages

```
1. Plan Searches → Generate 5-10 targeted queries
2. Execute Searches (Parallel) → Run all queries concurrently
3. Synthesize Report → AI analyzes and combines results
4. Notify (Optional) → Email report via Resend
```

## Related Skills

- **hot-topics** - Discover trending topics to research
- **article-generation** - Single-shot article drafting
- **web-search** - Raw web search (used internally)
- **portfolio-publisher** - Publish research as portfolio article

## Error Handling

Returns structured error responses:

```python
{
    "success": False,
    "error": "Search failed: API rate limit exceeded",
    "query": "...",
    "variant": "technical"
}
```

## Tips

1. **Choose the right variant** - Match variant to your use case (technical vs market vs article)
2. **Use specific queries** - "AI agent memory architectures" is better than "AI"
3. **Enable notifications** - Get email when long research completes (2-5 minutes)
4. **Combine with article generation** - Use `research_to_article` tool to convert research into blog posts
