# kk-agent-skills

**agentskills.io-compatible skill library for the personal-assistant backend.**

Each skill is a self-contained Python sub-package with its own tools, manifest, config, and README. Skills are auto-registered into the Governor routing layer at import time.

---

## Skills

| Skill | Status | Tools | Min Access | Description |
|-------|--------|------:|------------|-------------|
| [ai_tools](kk_agent_skills/ai_tools/README.md) | ✅ Completed | 4 | `user` | Summarize, rewrite, extract tasks, classify intent |
| [article_generation](kk_agent_skills/article_generation/README.md) | ✅ Completed | 1 | `user` | Single-shot research + article draft via Tavily + AI |
| [deep_research](kk_agent_skills/deep_research/README.md) | ✅ Completed | 2 | `user` | Multi-agent deep research pipeline with YAML prompt variants |
| [digital_me](kk_agent_skills/digital_me/README.md) | ✅ Completed | 7 | `anonymous` | RAG-powered personal profile (experience, skills, projects) |
| [digital_me_rag](kk_agent_skills/digital_me_rag/README.md) | ✅ Completed | — | internal | ChromaDB RAG engine (internal, not a tool provider) |
| [notes](kk_agent_skills/notes/README.md) | ✅ Completed | 6 | `user` | Full CRUD note management with keyword search |
| [portfolio_publisher](kk_agent_skills/portfolio_publisher/README.md) | ✅ Completed | 5 | `user` | Portfolio-01 article CRUD — create, publish, archive |
| [web_search](kk_agent_skills/web_search/README.md) | ✅ Completed | 1 | `user` | Real-time web search via Tavily |

**Status legend:** `📋 Plan` · `⏳ Pending` · `🚧 WIP` · `✅ Completed`

---

## Skill Package Structure

Every skill follows this layout:

```
kk_agent_skills/
└── my_skill/
    ├── __init__.py       # Public exports (SKILL, schemas, key classes)
    ├── skill.py          # SkillManifest declaration
    ├── tools.py          # @agent_tool decorated functions + _auto_register()
    ├── config.json       # Default configuration values
    └── README.md         # Skill documentation (this file per skill)
```

Complex skills (e.g. `deep_research`, `portfolio_publisher`) extend the structure:

```
└── my_skill/
    ├── schemas.py        # Pydantic v2 input/output models
    ├── client.py         # External HTTP/API client (if needed)
    ├── <module>.py       # Core logic (e.g. research_manager.py)
    ├── prompts/          # YAML prompt configs (deep_research)
    │   └── *.yaml
    └── agents/           # Agent factory modules (deep_research)
        └── *.py
```

---

## Common Patterns

### 1. SkillManifest (`skill.py`)

Declares identity, version, tags, capabilities, and minimum access level.

```python
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="my_skill",
    display_name="My Skill",
    description="What this skill does.",
    version="1.0.0",
    tags=["tag1", "tag2"],
    capabilities=["tool_provider"],   # or ["rag_engine"] for internal skills
    min_access_level="user",          # anonymous | demo | user
)
```

### 2. `@agent_tool` Decorator (`tools.py`)

Wraps every public tool function. Generates the JSON schema for the Governor and ToolRegistry.

```python
from kk_utils.agent_tools import agent_tool, _auto_register

@agent_tool(
    name="My Tool",
    description="What the tool does. Be specific — this is shown to the agent.",
    tags=["tag1", "feature"],
    access_level="user",          # anonymous | demo | user
    sensitivity="low",            # low | medium | high
    requires_confirmation=False,  # set True for irreversible actions
    is_destructive=False,         # set True for delete/overwrite operations
)
def my_tool(param: str, optional: int = 5, user_id: Optional[str] = None) -> dict:
    """Docstring used by the tool registry."""
    ...
    return {"result": "...", "success": True}

_auto_register()   # MUST be at the end of every tools.py
```

**Rules:**
- `user_id: Optional[str] = None` is always the **last** parameter — auto-injected by the Governor.
- Return type is always `dict`.
- Backend service imports are **always lazy** (inside the function body), never at module level.
- `_auto_register()` must be called once at the bottom of `tools.py`.

### 3. Lazy Backend Imports

Skills are loaded outside the backend context (e.g. in tests, CLI). Importing `app.*` at module level would fail. Always defer:

```python
# ✅ Correct — lazy import inside function
def my_tool(param: str, user_id=None) -> dict:
    from app.services.my_service import get_my_service
    service = get_my_service()
    return service.do_thing(param)

# ❌ Wrong — module-level backend import
from app.services.my_service import get_my_service
```

### 4. Async Bridge

When a tool calls an async service from a synchronous context, use `_asyncio_run()`:

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

### 5. `__init__.py` Exports

Export only what external code needs:

```python
from kk_agent_skills.my_skill.skill import SKILL
from kk_agent_skills.my_skill.schemas import MyInputModel, MyOutputModel

__all__ = ["SKILL", "MyInputModel", "MyOutputModel"]
```

### 6. `config.json`

Stores default values. Keys map to behaviour controlled in `tools.py`. Keep it flat and machine-readable:

```json
{
  "default_max_results": 5,
  "default_tone": "professional",
  "some_feature_enabled": true
}
```

---

## Access Levels

| Level | Audience | Typical Use |
|-------|----------|-------------|
| `anonymous` | Unauthenticated public visitors | Public profile summary |
| `demo` | Demo / guest users | Read-only profile data |
| `user` | Authenticated users | All write and research tools |

---

## How to Add a New Skill

### Step 1 — Create the package

```bash
mkdir kk_agent_skills/my_new_skill
touch kk_agent_skills/my_new_skill/__init__.py
touch kk_agent_skills/my_new_skill/skill.py
touch kk_agent_skills/my_new_skill/tools.py
touch kk_agent_skills/my_new_skill/config.json
touch kk_agent_skills/my_new_skill/README.md
```

### Step 2 — Declare the manifest (`skill.py`)

```python
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="my_new_skill",
    display_name="My New Skill",
    description="Short description for the agent router.",
    version="1.0.0",
    tags=["my_tag"],
    capabilities=["tool_provider"],
    min_access_level="user",
)
```

### Step 3 — Write tools (`tools.py`)

```python
from typing import Optional
from kk_utils.agent_tools import agent_tool, _auto_register

@agent_tool(
    name="Do Something",
    description="...",
    tags=["my_tag"],
    access_level="user",
    sensitivity="low",
)
def do_something(input: str, user_id: Optional[str] = None) -> dict:
    from app.services.my_service import get_my_service
    result = get_my_service().run(input)
    return {"result": result, "success": True}

_auto_register()
```

### Step 4 — Add config defaults (`config.json`)

```json
{ "some_default": "value" }
```

### Step 5 — Register in root `__init__.py`

Add a line to the docstring in [kk_agent_skills/__init__.py](kk_agent_skills/__init__.py):

```python
#   kk_agent_skills.my_new_skill — Short description
```

### Step 6 — Write the README

Create `kk_agent_skills/my_new_skill/README.md` using the template in the section below.

---

## Skill README Template

```markdown
# `my_new_skill`

**Status: 🚧 WIP**

One-paragraph description of what the skill does and when to use it.

## Tools

| Tool | Function | Description |
|------|----------|-------------|
| Tool Name | `function_name` | What it does |

## Key Parameters

\`\`\`python
function_name(required_param, optional_param="default")
\`\`\`

## Return Shape

\`\`\`python
{
    "field": "...",
    "success": True,
}
\`\`\`

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MY_API_KEY` | Yes | ... |

## Dependencies

- `some-package` — why it's needed
- `app.services.my_service` — backend lazy import

## Config (`config.json`)

| Key | Default | Description |
|-----|---------|-------------|
| `some_default` | `"value"` | ... |
```

---

## Installation

```bash
# Editable install (development)
pip install -e ".[web_search,ai]"

# Optional extras
pip install resend pyyaml httpx markdown   # for deep_research + portfolio_publisher
```

**Extras declared in `setup.py`:**

| Extra | Packages Added |
|-------|---------------|
| `web_search` | `tavily-python` |
| `ai` | `openai-agents` |

---

## Environment Variables

| Variable | Skill | Description |
|----------|-------|-------------|
| `OPENAI_API_KEY` | `deep_research` | OpenAI API key for Agents SDK |
| `TAVILY_API_KEY` | `web_search`, `article_generation` | Tavily search API key |
| `RESEND_API_KEY` | `deep_research` | Resend email delivery key |
| `RESEND_FROM_EMAIL` | `deep_research` | Verified sender address |
| `RESEARCH_NOTIFICATION_EMAIL` | `deep_research` | Default notification recipient |
| `PORTFOLIO_API_URL` | `portfolio_publisher` | Backend URL (default: `http://localhost:8000`) |
| `PORTFOLIO_ADMIN_KEY` | `portfolio_publisher` | Admin API key (`X-Admin-Key` header) |
| `PORTFOLIO_SITE_URL` | `portfolio_publisher` | Public site URL for article links |
