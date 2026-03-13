"""
kk-agent-skills — agentskills.io-compatible skill library

Skills for the personal-assistant backend. Each sub-package is a
self-contained skill with SKILL.md, config.json, and tools.py.

Available skills:
  kk_agent_skills.ai_tools            — Summarize, rewrite, extract tasks, classify intent
  kk_agent_skills.article_generation  — Research + AI article drafting (single-shot)
  kk_agent_skills.deep_research       — Multi-agent deep research pipeline (YAML prompt variants)
  kk_agent_skills.digital_me          — RAG-powered personal profile queries
  kk_agent_skills.hot_topics          — Discover trending topics for any subject
  kk_agent_skills.notes               — Full CRUD note management
  kk_agent_skills.portfolio_publisher — Portfolio-01 article CRUD (create/publish/archive)
  kk_agent_skills.web_search          — Tavily real-time web search
"""

__version__ = "1.1.0"
