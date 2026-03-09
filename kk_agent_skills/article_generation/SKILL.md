---
name: article_generation
description: Article generation skill — research a topic using web search (Tavily) and generate a structured technical article, saved as a draft in the portfolio blog for admin review before publishing.
version: 1.0.0
dependencies: tavily-python, openai-agents
capabilities: tool_provider
tags: research, writing, blog, article, portfolio
metadata:
  author: personal-assistant
  access_levels: user
---

# article_generation

Combines Tavily web research with AI generation to produce structured markdown articles.
Articles are saved as drafts in the portfolio blog (requires admin review before publishing).

## Tools

| Tool | Access | Description |
|---|---|---|
| `research_and_write_article` | user | Research topic via web search, generate and save article draft |

## Config (`config.json`)

```json
{
  "default_tone": "technical",
  "default_num_search_results": 4
}
```

## Pipeline

1. Tavily web search → research context
2. Build prompt with research context
3. `AIService.generate_structured()` → typed `GeneratedArticle`
4. Save as `draft` in `blog_posts` table
5. Return title, slug, excerpt, tags

## Environment

Requires `TAVILY_API_KEY` and `API_MODEL` in `.env`.
