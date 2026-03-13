---
name: hot-topics
description: Discovers trending and hot topics for any given subject. Performs targeted web searches to find what people are discussing, then uses AI to analyze and rank topics by discussion level and controversy. Use when planning content, researching market trends, or staying current in a field.
license: MIT
compatibility: Requires OpenAI API key, Tavily API key for web search, and network access
metadata:
  author: kkchua
  version: "1.0.0"
  tags: topics, trending, research, analysis, web, discovery
allowed-tools: Bash(curl:*) Read Write
---

# Hot Topics Discovery Skill

## Overview

Discovers trending and hot topics for any given subject. Uses web search and AI analysis to identify the most discussed, controversial, and emerging topics in a field.

## When to Use

- Planning content calendars and blog topics
- Researching market trends and competitive landscapes
- Staying current in your field or industry
- Finding trending topics for social media
- Identifying emerging technologies or practices
- Content strategy and SEO planning

## What It Does

1. **Performs targeted web searches** - Uses 8 different search templates to find trending discussions (Reddit, Twitter, news, forums)
2. **Analyzes search results** - AI analyzes 30-50+ search results to identify patterns and hot topics
3. **Ranks topics** - Ranks by discussion level (High/Medium/Low) and controversy level
4. **Provides actionable insights** - Returns why each topic is trending and suggested angles for exploration

## Usage

```python
from kk_agent_skills.hot_topics.tools import hot_topics_discovery

# Find top 10 hot topics in AI agents
result = hot_topics_discovery(
    subject="AI agents",
    max_topics=10,
    max_searches=5,
)

if result.get("success"):
    print(result["analysis"])  # Markdown formatted topics
else:
    print(f"Error: {result.get('error')}")
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `subject` | str | required | The subject/domain to analyze (e.g., "AI agents", "web development", "climate tech") |
| `max_topics` | int | 10 | Maximum number of topics to return (1-20) |
| `max_searches` | int | 5 | Number of search queries to run (1-8, more = more comprehensive) |
| `user_id` | str | auto | Auto-injected by Governor |

## Output Format

```python
{
    "success": True,
    "subject": "AI agents",
    "max_topics": 10,
    "analysis": """| Rank | Topic | Why It's Hot | Discussion | Controversy | Suggested Angles |
|------|-------|--------------|------------|-------------|------------------|
| 1 | ... | ... | ... | ... | ... |

## Summary
Overall trends in the field...
""",
    "sources_count": 42,
    "trace_id": "trace_..."
}
```

## Example Output

```markdown
| Rank | Topic | Why It's Hot | Discussion | Controversy | Suggested Angles |
|------|-------|--------------|------------|-------------|------------------|
| 1 | Agentic Workflows in Production | New frameworks making it easier to deploy AI agents | High | Medium | ROI metrics, case studies |
| 2 | Multi-Agent Collaboration Patterns | Growing interest in agent teams | High | Low | Comparison of frameworks |
| 3 | Agent Memory Architectures | Debate over vector vs graph memory | Medium | High | Technical deep-dive |

## Summary
The field is rapidly evolving with focus shifting from single agents to multi-agent systems...
```

## Search Strategy

The skill uses these search templates:

1. `"{subject} trending topics 2025 2026"`
2. `"{subject} hottest discussions this week"`
3. `"{subject} controversial topics debate"`
4. `"{subject} emerging trends analysis"`
5. `"{subject} most talked about news"`
6. `"{subject} reddit discussions popular"`
7. `"{subject} twitter trending hashtags"`
8. `"{subject} latest breakthrough developments"`

By default, runs 5 searches (configurable via `max_searches`).

## Use Cases

### Content Planning
- Find blog post topics that are currently trending
- Identify gaps in content coverage
- Discover controversial topics for thought leadership

### Research Prioritization
- Understand what's hot in a field before starting research
- Identify emerging trends worth investigating
- Find collaboration opportunities

### Market Intelligence
- Track competitor discussions
- Identify market shifts early
- Understand customer pain points

### Learning & Development
- Stay current in your field
- Identify skills worth learning
- Find communities and discussions to join

## Related Skills

- **deep-research** - Deep dive into a specific topic
- **web-search** - Raw web search (used internally)
- **article-generation** - Turn hot topics into articles

## Error Handling

Returns structured error responses:

```python
{
    "success": False,
    "error": "No search results found. Try a different subject...",
    "subject": "..."
}
```

Common errors:
- No search results (subject too niche)
- Web search API not configured
- Rate limiting

## Tips

1. **Be specific with subject** - "AI agent memory architectures" vs "AI"
2. **Increase max_searches** for comprehensive analysis (slower but better)
3. **Use for content calendars** - Run monthly to stay current
4. **Combine with deep-research** - Use hot_topics to pick topics, then deep_research for analysis
