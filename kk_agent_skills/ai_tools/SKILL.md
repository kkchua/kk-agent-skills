---
name: ai_tools
description: AI text processing skill — summarize, rewrite, extract tasks, and classify intent using the configured AI provider via AIService.
version: 1.0.0
dependencies: openai-agents
capabilities: tool_provider
tags: ai, text-processing, summarize, rewrite, tasks, intent
metadata:
  author: personal-assistant
  access_levels: user
---

# ai_tools

AI-powered text processing skill. All tools route through `AIService` which reads the model
and provider from `API_MODEL` in `.env`, supporting OpenAI, Qwen, Ollama and other providers.

## Tools

| Tool | Access | Description |
|---|---|---|
| `summarize_text` | user | Summarize text with key bullet points |
| `rewrite_text` | user | Rewrite text with a different tone or style |
| `extract_tasks` | user | Extract actionable tasks with priority and due dates |
| `classify_intent` | user | Classify user intent and extract entities for tool routing |

## Config (`config.json`)

```json
{
  "agent_name": "personal_assistant"
}
```

## Environment

Reads `API_MODEL` from `.env` via `AIService`. No separate key needed.
