# kk-agent-skills - Project Index

**Version:** v0.2.0  
**Last Updated:** 2026-03-12  
**Status:** Phase 1 Complete - agentskills.io Compliant

---

## 📦 Current Version: v0.2.0

**Release Date:** 2026-03-12  
**Release Notes:** [RELEASE.md](RELEASE.md)

### What's New in v0.2.0

- ✅ **New Skill:** hot-topics (2 tools)
- ✅ **agentskills.io Compliance:** All SKILL.md files updated
- ✅ **8 Skills Total:** 30 tools available
- ✅ **Backend Integration:** Auto-discovery in personal-assistant

---

## 📚 Available Skills (8 total, 30 tools)

| Skill | Tools | Description | Status |
|-------|-------|-------------|--------|
| ai_tools | 4 | Summarize, rewrite, extract tasks, classify intent | ✅ |
| article_generation | 1 | Research + AI article drafting | ✅ |
| deep_research | 3 | Multi-agent deep research pipeline | ✅ |
| digital_me | 7 | RAG-powered personal profile queries | ✅ |
| hot_topics | 2 | Trending topics discovery | ✅ NEW |
| notes | 6 | Full CRUD note management | ✅ |
| portfolio_publisher | 5 | Portfolio article CRUD | ✅ |
| web_search | 2 | Tavily real-time web search | ✅ |

---

## 🚀 Quick Start

```python
from kk_agent_skills.hot_topics.tools import hot_topics_discovery

# Find trending topics
result = hot_topics_discovery(
    subject="AI agents",
    max_topics=10,
)
print(result["analysis"])
```

---

## 📋 Version History

| Version | Date | Highlights |
|---------|------|------------|
| v0.2.0 | 2026-03-12 | hot-topics skill, agentskills.io compliance |
| v0.1.0 | Previous | Initial 7 skills release |

---

## 🔗 Related Projects

| Project | Version | Description |
|---------|---------|-------------|
| kk-utils | v0.8.0 | Core utilities, RAG engine, agent factory |
| personal-assistant | v0.58.0 | Backend API with skill discovery |
| pa-admin | v0.3.0 | Admin UI (Phase 1 backend ready) |
| portfolio-01 | v0.11.0 | Portfolio frontend |
| gradio-apps | v0.5.0 | Gradio UI apps |

---

## 📝 Development

### Adding a New Skill

1. Create skill directory: `kk_agent_skills/my-skill/`
2. Create `SKILL.md` with YAML frontmatter:
```yaml
---
name: my-skill
description: What it does and when to use it
license: MIT
metadata:
  version: "1.0.0"
  tags: tag1, tag2
---
```
3. Create `tools.py` with `@agent_tool` decorated functions
4. Create `skill.py` with SkillManifest
5. Update `__init__.py` exports

### SKILL.md Format (agentskills.io)

```yaml
---
name: skill-name
description: Description and when to use it
license: MIT
compatibility: Requirements
metadata:
  author: name
  version: "1.0.0"
  tags: comma,separated,tags
---

# Skill Instructions
[Markdown content...]
```

---

## ✅ Testing

```bash
# Run import test
python test_hot_topics.py

# Run example
python example_hot_topics.py
```

---

**Status:** ✅ Production Ready  
**Next Release:** v0.3.0 - Additional skills + enhanced tool schemas
