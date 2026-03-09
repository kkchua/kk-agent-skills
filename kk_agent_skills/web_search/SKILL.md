---
name: web_search
description: Web search skill — search the internet for current information using the Tavily API. Returns titles, URLs, and content snippets. Supports basic and advanced search depth.
version: 1.0.0
dependencies: tavily-python
capabilities: tool_provider
tags: search, research, web, tavily
metadata:
  author: personal-assistant
  access_levels: user
---

# web_search

Tavily-powered web search skill for retrieving up-to-date information from the internet.

## Tools

| Tool | Access | Description |
|---|---|---|
| `web_search` | user | Search the web, returns titles, URLs and content snippets |

## Config (`config.json`)

```json
{
  "default_max_results": 5,
  "default_search_depth": "basic"
}
```

## Environment

Requires `TAVILY_API_KEY` in `.env`.
