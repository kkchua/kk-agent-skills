# Skill Registration — How It Works

## The Three-Repo Chain

Skill registration currently spans three repositories:

```
kk-utils              ← provides the registry primitives
kk-agent-skills       ← contains the actual skill code
personal-assistant    ← backend that imports and routes skills
```

Here is the full call chain from "skill code on disk" to "LLM can call the tool":

```
1. kk_agent_skills/<skill>/tools.py
       @agent_tool(tags=[...])       ← decorator from kk_utils
       def my_tool(...): ...
       _auto_register()              ← last line, called at import time

2. kk_utils.agent_tools.registry.AgentRegistry   (singleton)
       ← _auto_register() registers every @agent_tool function here

3. personal-assistant/backend/app/services/skills_registry.SkillsRegistry
       ← scans kk_agent_skills/ for every folder with tools.py
       ← imports each tools.py  →  triggers step 1  →  populates step 2

4. kk_utils.agents.master_agent.MasterAgent._load_tools(skill_tags)
       ← queries AgentRegistry.get_tools_for_tags(skill_tags)
       ← returns matching tools to the LLM as callable functions
```

---

## Step-by-Step Detail

### Step 1 — `@agent_tool` decorator (`kk_utils`)

Every tool function in `tools.py` is decorated with `@agent_tool`:

```python
from kk_utils.agent_tools import agent_tool, _auto_register

@agent_tool(
    name="Human-readable name",
    description="What the LLM reads to decide whether to call this tool",
    tags=["skill_name", "other_tag", ...],   # ← see CRITICAL rule below
    access_level="user",
)
def my_tool(param: str, user_id: Optional[str] = None) -> dict:
    ...

_auto_register()   # MUST be the last line
```

The decorator adds `__agent_tool__` and `__openai_schema__` attributes to the
function. `_auto_register()` scans the calling module for all decorated functions
and registers them in `AgentRegistry` using the skill folder name as a namespace
prefix (e.g. `csv_generator_v2__generate_csv_v2`).

### Step 2 — `AgentRegistry` (`kk_utils`)

A process-wide singleton (`kk_utils.agent_tools.registry.AgentRegistry`) stores
all registered tools keyed by their prefixed name. Tools are indexed by tag so
they can be retrieved with `get_tools_for_tags(["tag1", "tag2"])`.

### Step 3 — `SkillsRegistry` (`personal-assistant` backend)

`app/services/skills_registry.py` scans the `kk_agent_skills` package directory
at startup and imports every `<skill>/tools.py` it finds. This import triggers
`_auto_register()` in each file, which populates `AgentRegistry`.

### Step 4 — `MasterAgent._load_tools` (`kk_utils`)

When a chat request arrives with `skill="csv_generator_v2"`, `master_agent.py`
adds `"csv_generator_v2"` to the tag list and calls
`AgentRegistry.get_tools_for_tags(["csv_generator_v2"])`. This returns all tools
whose `tags` list includes `"csv_generator_v2"`.

---

## CRITICAL: The Self-Naming Tag Rule

**Every skill must include its own folder name as the first entry in `tags`.**

```python
# ✓ Correct — skill name is in tags
@agent_tool(
    tags=["csv_generator_v2", "csv", "studio", "image"],
    ...
)

# ✗ Wrong — master_agent sends skill="csv_generator_v2" but finds nothing
@agent_tool(
    tags=["csv", "studio", "image"],
    ...
)
```

Why: `master_agent.py` line 328 does `final_skill_tags += [skill.lower()]` — it
adds the skill name as a tag and then queries the registry. If the tool does not
carry that tag, it will never be returned to the LLM.

---

## What Happens If It Breaks

| Symptom | Likely cause |
|---------|-------------|
| Skill listed in admin panel, `tool_count: 0` | `_auto_register()` missing or tools.py import fails |
| Skill not in admin panel at all | Folder has no `tools.py`, or `SkillsRegistry` could not scan |
| `tools_available: 0` in chat response | Skill name not in `tags` (self-naming tag rule violated) |
| Admin panel shows empty name / description | `SKILL.md` missing YAML frontmatter |
| Changes not picked up by backend | `kk-agent-skills` installed as a frozen copy, not editable — run `pip install -e /path/to/kk-agent-skills` |

---

## Running the Registration Validator

```bash
cd /path/to/kk-agent-skills

# Check all skills
python test_skill_registration.py

# Check specific skills
python test_skill_registration.py csv_generator_v2 extract_desc
```

The script checks:
- `tools.py` imports without errors
- All tools are registered in `AgentRegistry`
- Each tool carries the skill name as a tag
- `SKILL.md` has YAML frontmatter
- `config.json` is valid JSON

---

## Checklist for Adding a New Skill

```
kk_agent_skills/
└── my_skill/
    ├── __init__.py          # one line: # my_skill skill
    ├── skill.py             # SkillManifest (see existing skills for template)
    ├── SKILL.md             # must start with YAML frontmatter (--- ... ---)
    ├── config.json          # default settings
    └── tools.py             # @agent_tool functions + _auto_register()
```

**`tools.py` minimum template:**
```python
from typing import Optional
from kk_utils.agent_tools import agent_tool, _auto_register

@agent_tool(
    name="My Tool",
    description="What this tool does.",
    tags=["my_skill"],      # ← MUST include the folder name
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def my_tool(param: str, user_id: Optional[str] = None) -> dict:
    """..."""
    ...

_auto_register()   # always last
```

**`skill.py` template:**
```python
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="my_skill",
    display_name="My Skill",
    description="One-line description.",
    version="1.0.0",
    tags=["my_skill"],
    capabilities=["tool_provider"],
    min_access_level="user",
)
```

**`SKILL.md` required frontmatter:**
```yaml
---
name: my_skill
description: One-line description shown in the admin panel.
version: 1.0.0
dependencies: openai-agents
capabilities: tool_provider
metadata:
  author: personal-assistant
  version: "1.0.0"
  tags: my_skill, tag2, tag3
  access_levels: user
---
```

After adding the skill, run `python test_skill_registration.py my_skill` to
verify it registers correctly before committing.

---

## Simplification Proposal

The current flow requires understanding three separate repos to add or debug a
skill. The main friction points are:

1. A new skill in `kk_agent_skills` is invisible to the backend until
   `SkillsRegistry` scans it (requires backend awareness).
2. The self-naming tag rule is not enforced at authoring time.
3. Installing as a non-editable package silently uses a stale snapshot.

### Proposed fix: `register_all()` in `kk_agent_skills`

Add a single function to `kk_agent_skills/__init__.py` that imports every
skill's `tools.py`. The backend calls this once at startup instead of scanning:

```python
# kk_agent_skills/__init__.py  (proposed addition)

def register_all(skip_errors: bool = True) -> dict:
    """
    Import every skill's tools.py, triggering _auto_register() for each.

    Returns {"loaded": [...], "failed": {...skill: error...}}.
    Call once at backend startup:
        import kk_agent_skills
        kk_agent_skills.register_all()
    """
    import importlib, logging
    from pathlib import Path

    logger = logging.getLogger(__name__)
    loaded, failed = [], {}
    skills_root = Path(__file__).parent

    for skill_dir in sorted(skills_root.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
            continue
        if not (skill_dir / "tools.py").exists():
            continue
        module_path = f"kk_agent_skills.{skill_dir.name}.tools"
        try:
            importlib.import_module(module_path)
            loaded.append(skill_dir.name)
        except Exception as exc:
            logger.error(f"Failed to load skill '{skill_dir.name}': {exc}")
            failed[skill_dir.name] = str(exc)
            if not skip_errors:
                raise

    logger.info(f"register_all: loaded={loaded} failed={list(failed)}")
    return {"loaded": loaded, "failed": failed}
```

**Backend startup change** (`orchestrator_service.py` or `main.py`):
```python
# Instead of relying on SkillsRegistry lazy scan:
import kk_agent_skills
kk_agent_skills.register_all()
```

**Benefits:**
- Adding a skill to `kk_agent_skills` is all that's needed — no backend change required
- Failed imports are logged clearly with the skill name
- The backend no longer needs filesystem-scan logic
- `register_all()` is testable in isolation (no backend dependency)

**The self-naming tag rule** can be enforced inside `_auto_register()` in
`kk_utils` by checking each registered tool's tags and warning (or raising) if
the skill name is missing.
