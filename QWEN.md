# kk-agent-skills Guide

**Version:** v0.2.0  
**Status:** ✅ Active - agentskills.io Compliant  
**Last Updated:** 2026-03-12

---

## 📦 Skills Inventory (8 Skills, 27 Tools)

| Skill                                                                | Tools | Access | Description                                                  |
| -------------------------------------------------------------------- | ----- | ------ | ------------------------------------------------------------ |
| [ai_tools](kk_agent_skills/ai_tools/README.md)                       | 4     | `user` | Summarize, rewrite, extract tasks, classify intent           |
| [article_generation](kk_agent_skills/article_generation/README.md)   | 1     | `user` | Single-shot research + article draft via Tavily + AI         |
| [csv_generator](kk_agent_skills/csv_generator/)                      | —     | —      | CSV data generation (check status)                           |
| [deep_research](kk_agent_skills/deep_research/README.md)             | 3     | `user` | Multi-agent deep research pipeline with YAML prompt variants |
| [hot_topics](kk_agent_skills/hot_topics/README.md)                   | 2     | `user` | Discovers trending topics via web search + AI analysis       |
| [n8n_trigger](kk_agent_skills/n8n_trigger/)                          | —     | —      | n8n workflow trigger (check status)                          |
| [notes](kk_agent_skills/notes/README.md)                             | 6     | `user` | Full CRUD note management with keyword search                |
| [portfolio_publisher](kk_agent_skills/portfolio_publisher/README.md) | 5     | `user` | Portfolio-01 article CRUD — create, publish, archive         |
| [web_search](kk_agent_skills/web_search/README.md)                   | 2     | `user` | Real-time web search via Tavily                              |

**Note:** `csv_generator` and `n8n_trigger` need status verification.

---

## 🚀 Quick Start

### Installation

```bash
cd kk-agent-skills

# Development install (editable)
pip install -e .

# With optional extras
pip install -e ".[web_search,ai]"
```

### Optional Extras

| Extra        | Packages                                |
| ------------ | --------------------------------------- |
| `web_search` | `tavily-python`                         |
| `ai`         | `openai-agents`                         |
| _(implicit)_ | `resend`, `pyyaml`, `httpx`, `markdown` |

### Test Installation

```bash
# Run import test
python test_hot_topics.py

# Or test all skills
python -c "from kk_agent_skills import SKILLS; print(f'{len(SKILLS)} skills loaded')"
```

---

## 📁 Project Structure

```
kk-agent-skills/
├── kk_agent_skills/
│   ├── __init__.py           # Root exports, SKILLS registry
│   ├── _http_client.py       # Shared HTTP client
│   ├── ai_tools/
│   │   ├── __init__.py
│   │   ├── skill.py          # SkillManifest declaration
│   │   ├── tools.py          # @agent_tool decorated functions
│   │   ├── config.json
│   │   └── README.md
│   ├── article_generation/
│   ├── csv_generator/        # ⚠️ Verify status
│   ├── deep_research/
│   │   ├── __init__.py
│   │   ├── skill.py
│   │   ├── tools.py
│   │   ├── schemas.py        # Pydantic models
│   │   ├── client.py         # External API client
│   │   ├── research_manager.py
│   │   ├── prompts/          # YAML prompt configs
│   │   │   └── *.yaml
│   │   └── agents/           # Agent factories
│   │       └── *.py
│   ├── hot_topics/
│   ├── n8n_trigger/          # ⚠️ Verify status
│   ├── notes/
│   ├── portfolio_publisher/
│   │   ├── __init__.py
│   │   ├── skill.py
│   │   ├── tools.py
│   │   ├── schemas.py
│   │   └── client.py         # Portfolio API client
│   └── web_search/
├── setup.py
├── RELEASE.md
├── QWEN.md                   # This file
├── HOT_TOPICS_IMPLEMENTATION.md
├── example_hot_topics.py
├── test_hot_topics.py
└── README.md
```

---

## 🛠️ Creating a New Skill

### Step 1 — Create Package Structure

```bash
mkdir kk_agent_skills/my_new_skill
cd kk_agent_skills/my_new_skill

touch __init__.py skill.py tools.py config.json README.md
```

### Step 2 — Define Manifest (`skill.py`)

```python
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="my_new_skill",
    display_name="My New Skill",
    description="Short description for agent router.",
    version="1.0.0",
    tags=["my_tag"],
    capabilities=["tool_provider"],  # or ["rag_engine"]
    min_access_level="user",         # anonymous | demo | user
)
```

### Step 3 — Implement Tools (`tools.py`)

```python
from typing import Optional
from kk_utils.agent_tools import agent_tool, _auto_register

@agent_tool(
    name="Do Something",
    description="Detailed description shown to the agent.",
    tags=["my_tag"],
    access_level="user",
    sensitivity="low",            # low | medium | high
    requires_confirmation=False,
    is_destructive=False,
)
def do_something(input: str, user_id: Optional[str] = None) -> dict:
    """Docstring used by tool registry."""
    # LAZY IMPORT - always inside function
    from app.services.my_service import get_my_service

    service = get_my_service()
    result = service.run(input)

    return {"result": result, "success": True}

_auto_register()  # MUST be at the end
```

### Step 4 — Create Config (`config.json`)

```json
{
  "default_max_results": 5,
  "some_feature_enabled": true
}
```

### Step 5 — Update Root `__init__.py`

Add to docstring in `kk_agent_skills/__init__.py`:

```python
#   kk_agent_skills.my_new_skill — Short description
```

### Step 6 — Write README

Use the template in [README.md](README.md#skill-readme-template).

---

## 🔑 Key Patterns

### 1. Lazy Backend Imports

Skills load outside backend context. **Always** import backend services inside functions:

```python
# ✅ Correct
def my_tool(param: str, user_id=None) -> dict:
    from app.services.my_service import get_my_service
    service = get_my_service()
    return service.do_thing(param)

# ❌ Wrong - will fail in tests/CLI
from app.services.my_service import get_my_service
```

### 2. Async Bridge

Call async services from sync context:

```python
import asyncio

def _asyncio_run(coroutine):
    """Run async coroutine in sync context."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
        return loop.run_until_complete(coroutine)
    except RuntimeError:
        return asyncio.run(coroutine)

def my_tool(query: str, user_id=None) -> dict:
    from app.services.async_service import get_service
    return _asyncio_run(get_service().search(query))
```

### 3. Tool Function Signature

```python
def my_tool(
    required_param: str,
    optional_param: int = 5,
    user_id: Optional[str] = None  # ALWAYS last, auto-injected
) -> dict:
```

### 4. Return Shape

Always return `dict`:

```python
{
    "result": "...",
    "success": True,
    "error": None  # Optional
}
```

---

## 🔐 Access Levels

| Level       | Audience                 | Example Tools            |
| ----------- | ------------------------ | ------------------------ |
| `anonymous` | Unauthenticated visitors | Profile data (read-only) |
| `demo`      | Demo/guest users         | Read-only profile data   |
| `user`      | Authenticated users      | All write/research tools |

---

## 🧪 Testing

```bash
# Import test
python test_hot_topics.py

# Test specific skill
python -c "from kk_agent_skills.hot_topics import SKILL; print(SKILL)"

# Test all skills
python -c "from kk_agent_skills import SKILLS; [print(s.name) for s in SKILLS]"
```

---

## 🌍 Environment Variables

| Variable                      | Skill                              | Required | Description                                    |
| ----------------------------- | ---------------------------------- | -------- | ---------------------------------------------- |
| `OPENAI_API_KEY`              | `deep_research`                    | Yes      | OpenAI API key for Agents SDK                  |
| `TAVILY_API_KEY`              | `web_search`, `article_generation` | Yes      | Tavily search API key                          |
| `RESEND_API_KEY`              | `deep_research`                    | Yes      | Resend email delivery key                      |
| `RESEND_FROM_EMAIL`           | `deep_research`                    | Yes      | Verified sender address                        |
| `RESEARCH_NOTIFICATION_EMAIL` | `deep_research`                    | No       | Default notification recipient                 |
| `PORTFOLIO_API_URL`           | `portfolio_publisher`              | No       | Backend URL (default: `http://localhost:8000`) |
| `PORTFOLIO_ADMIN_KEY`         | `portfolio_publisher`              | Yes      | Admin API key (`X-Admin-Key` header)           |
| `PORTFOLIO_SITE_URL`          | `portfolio_publisher`              | No       | Public site URL for article links              |

---

## 📚 Documentation

| File                                                         | Purpose                                 |
| ------------------------------------------------------------ | --------------------------------------- |
| [README.md](README.md)                                       | Skill patterns, templates, installation |
| [RELEASE.md](RELEASE.md)                                     | Version history, changelog              |
| [HOT_TOPICS_IMPLEMENTATION.md](HOT_TOPICS_IMPLEMENTATION.md) | Hot topics skill design                 |
| [example_hot_topics.py](example_hot_topics.py)               | Usage example                           |

---

## 🔗 Integration with personal-assistant

Skills are auto-discovered by the backend:

```python
# personal-assistant backend auto-discovers
from kk_agent_skills import SKILLS

for skill in SKILLS:
    print(f"{skill.name}: {len(skill.tools)} tools")
```

**API Endpoints:**

- `GET /api/v1/agent/skills` - List all skills
- `GET /api/v1/agent/skills/{name}` - Get skill details
- `GET /api/v1/agent/skills/health` - Health check

---

## ✅ TODO Items

- [ ] Verify `csv_generator` skill status (tools implemented?)
- [ ] Verify `n8n_trigger` skill status (tools implemented?)
- [ ] Create README for `hot_topics` skill
- [ ] Add SKILL.md files for all skills (agentskills.io compliance)

---

## 📊 Version History

| Version | Date       | Changes                                     |
| ------- | ---------- | ------------------------------------------- |
| v0.2.0  | 2026-03-12 | Hot topics skill, agentskills.io compliance |
| v0.1.0  | Previous   | Initial release with 7 core skills          |
