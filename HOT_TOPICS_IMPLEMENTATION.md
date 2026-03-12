# Hot Topics Discovery Skill - Implementation Summary

**Date:** 2026-03-12  
**Skill Name:** `hot_topics`  
**Version:** 1.0.0

## Overview

Created a new agent skill that discovers trending/hot topics for any given subject. The skill performs targeted web searches and uses AI analysis to identify and rank the most discussed, controversial, and emerging topics in a field.

## Files Created

```
kk-agent-skills/kk_agent_skills/hot_topics/
├── __init__.py          # Package initialization
├── skill.py             # Skill manifest (metadata)
├── tools.py             # Main tool implementation
├── SKILL.md             # Documentation
```

## Key Features

### 1. **Multi-Query Search Strategy**
Uses 8 different search templates to comprehensively gather trending topic data:
- "trending topics 2025 2026"
- "hottest discussions this week"
- "controversial topics debate"
- "emerging trends analysis"
- "most talked about news"
- "reddit discussions popular"
- "twitter trending hashtags"
- "latest breakthrough developments"

### 2. **AI-Powered Analysis**
- Uses OpenAI Agents SDK (`agents.Runner`) to analyze search results
- Identifies patterns and ranks topics by:
  - Discussion level (High/Medium/Low)
  - Controversy level (High/Medium/Low)
  - Why it's trending now
  - Suggested angles for exploration

### 3. **Structured Output**
Returns markdown-formatted table with:
```markdown
| Rank | Topic | Why It's Hot | Discussion | Controversy | Suggested Angles |
|------|-------|--------------|------------|-------------|------------------|
| 1 | ... | ... | ... | ... | ... |
```

Plus a summary of overall trends in the field.

## Usage

```python
from kk_agent_skills.hot_topics.tools import hot_topics_discovery

# Find top 10 hot topics in AI agents
result = hot_topics_discovery(
    subject="AI agents",
    max_topics=10,        # 1-20 topics
    max_searches=5,       # 1-8 searches
)

if result.get("success"):
    print(result["analysis"])  # Markdown formatted output
```

## Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `subject` | str | required | - | Subject/domain to analyze |
| `max_topics` | int | 10 | 1-20 | Max topics to return |
| `max_searches` | int | 5 | 1-8 | Search queries to run |
| `user_id` | str | auto | - | Auto-injected by Governor |

## Integration

### Dependencies
- **Web Search Skill** (`kk_agent_skills.web_search`) - For gathering data
- **OpenAI Agents SDK** (`agents.Runner`) - For AI analysis
- **Tavily API** - Web search backend (configured in web_search skill)

### Agent Tool Registration
Uses `@agent_tool` decorator from `kk_utils.agent_tools`:
- Name: "Hot Topics Discovery"
- Access level: User
- Requires confirmation: No
- Destructive: No
- Sensitivity: Low

## Use Cases

### 1. Content Planning
- Find blog post topics that are currently trending
- Identify content gaps
- Discover controversial topics for thought leadership

### 2. Research Prioritization
- Understand what's hot before starting research
- Identify emerging trends worth investigating
- Find collaboration opportunities

### 3. Market Intelligence
- Track competitor discussions
- Identify market shifts early
- Understand customer pain points

### 4. Learning & Development
- Stay current in your field
- Identify skills worth learning
- Find communities and discussions

## Example Output

```
Subject: AI agents
Sources analyzed: 42

| Rank | Topic | Why It's Hot | Discussion | Controversy | Suggested Angles |
|------|-------|--------------|------------|-------------|------------------|
| 1 | Agentic Workflows in Production | New frameworks making deployment easier | High | Medium | ROI metrics, case studies |
| 2 | Multi-Agent Collaboration | Growing interest in agent teams | High | Low | Framework comparison |
| 3 | Agent Memory Architectures | Debate over vector vs graph memory | Medium | High | Technical deep-dive |

## Summary
The field is rapidly evolving with focus shifting from single agents to multi-agent systems. 
Key themes include productionization, collaboration patterns, and memory management...
```

## Testing

### Import Test
```bash
cd kk-agent-skills
python test_hot_topics.py
```

### Usage Example
```bash
cd kk-agent-skills
python example_hot_topics.py
```

## Comparison with Deep Research

| Feature | Hot Topics | Deep Research |
|---------|-----------|---------------|
| **Purpose** | Discover what's trending | Deep dive into specific topic |
| **Depth** | Broad overview | Comprehensive analysis |
| **Output** | Ranked topics table | Full research report |
| **Time** | Fast (30-60s) | Slow (2-5 min) |
| **Searches** | 5-8 queries | 10-20+ queries |
| **Best For** | Content planning, trend spotting | Research papers, detailed reports |

## Recommended Workflow

1. **Use `hot_topics_discovery`** to find trending topics in a field
2. **Pick an interesting topic** from the ranked list
3. **Use `deep_research`** to do a comprehensive analysis of that topic
4. **Use `research_to_article`** to create a blog post from the research

## Next Steps (Optional Enhancements)

1. **Time-based filtering** - "trending this week" vs "trending this month"
2. **Source filtering** - Focus on specific platforms (Reddit, Twitter, news)
3. **Geographic filtering** - Trending in specific regions
4. **Historical comparison** - Compare current trends vs past months
5. **Export formats** - JSON, CSV, or direct portfolio article creation

## Files Modified

- `kk_agent_skills/__init__.py` - Added hot_topics to available skills list

## Documentation

- `SKILL.md` - Complete skill documentation with examples
- `test_hot_topics.py` - Import test script
- `example_hot_topics.py` - Usage example script

---

**Status:** ✅ Complete and ready to use  
**Tested:** Import test passed  
**Integration:** Ready for use in agent personas
