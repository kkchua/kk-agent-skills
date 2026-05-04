#!/usr/bin/env python3
"""
test_skill_registration.py — Validate that all kk_agent_skills are correctly registered.

What this checks per skill:
  - tools.py can be imported without errors
  - _auto_register() was called (tools appear in AgentRegistry)
  - @agent_tool carries the skill name as a tag (required for master_agent routing)
  - SKILL.md exists with YAML frontmatter (required for admin panel metadata)
  - config.json exists and is valid JSON

Usage:
    python test_skill_registration.py            # all skills
    python test_skill_registration.py csv_generator_v2 extract_desc  # specific skills

Exit codes:
    0 — all skills passed
    1 — one or more skills failed
"""

import importlib
import json
import sys
import traceback
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup — works whether kk_utils is pip-installed or sibling directory
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent
KK_UTILS_SIBLING = REPO_ROOT.parent / "kk-utils"
if KK_UTILS_SIBLING.exists() and str(KK_UTILS_SIBLING) not in sys.path:
    sys.path.insert(0, str(KK_UTILS_SIBLING))

SKILLS_ROOT = REPO_ROOT / "kk_agent_skills"

# ANSI colours (disabled when stdout is not a tty)
_tty = sys.stdout.isatty()
GREEN  = "\033[32m" if _tty else ""
RED    = "\033[31m" if _tty else ""
YELLOW = "\033[33m" if _tty else ""
RESET  = "\033[0m"  if _tty else ""
BOLD   = "\033[1m"  if _tty else ""


def _find_skill_dirs(names: list[str] | None = None) -> list[str]:
    """Return sorted list of skill directory names that contain a tools.py."""
    all_skills = sorted(
        d.name
        for d in SKILLS_ROOT.iterdir()
        if d.is_dir()
        and not d.name.startswith("_")
        and (d / "tools.py").exists()
    )
    if names:
        unknown = set(names) - set(all_skills)
        if unknown:
            print(f"{RED}Unknown skill(s): {', '.join(sorted(unknown))}{RESET}")
            print(f"Available: {', '.join(all_skills)}")
            sys.exit(1)
        return [s for s in all_skills if s in names]
    return all_skills


# ---------------------------------------------------------------------------
# Individual checks (structural, no import needed)
# ---------------------------------------------------------------------------

def _check_skill_md(skill_dir: Path) -> list[str]:
    """Warn if SKILL.md is missing or lacks YAML frontmatter."""
    warnings = []
    md = skill_dir / "SKILL.md"
    if not md.exists():
        warnings.append("SKILL.md not found — admin panel will show empty metadata")
        return warnings
    content = md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        warnings.append(
            "SKILL.md has no YAML frontmatter (must start with ---) — "
            "admin panel metadata will be empty"
        )
    return warnings


def _check_config_json(skill_dir: Path) -> list[str]:
    """Error if config.json exists but is not valid JSON."""
    errors = []
    cfg = skill_dir / "config.json"
    if not cfg.exists():
        return errors  # optional — only warn if you want to require it
    try:
        json.loads(cfg.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"config.json invalid JSON: {exc}")
    return errors


def _check_skill_py(skill_dir: Path) -> list[str]:
    """Warn if skill.py (SkillManifest) is missing."""
    warnings = []
    if not (skill_dir / "skill.py").exists():
        warnings.append(
            "skill.py not found — SkillManifest missing. "
            "Legacy skill; consider adding skill.py for richer metadata."
        )
    return warnings


# ---------------------------------------------------------------------------
# Import + registry check
# ---------------------------------------------------------------------------

def _import_skill(skill_name: str) -> str | None:
    """
    Import kk_agent_skills.<skill>.tools.
    Returns None on success, or an error string on failure.
    """
    module_path = f"kk_agent_skills.{skill_name}.tools"
    # Remove from sys.modules cache so we get a fresh import (important when
    # running individual skills; harmless when running all)
    sys.modules.pop(module_path, None)
    try:
        importlib.import_module(module_path)
        return None
    except ImportError as exc:
        return f"ImportError: {exc}"
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}"


def _check_registry(skill_name: str) -> tuple[list[str], list[str], list[str]]:
    """
    After the tools module is imported, check AgentRegistry state.
    Returns (tools_found, errors, warnings).
    """
    try:
        from kk_utils.agent_tools import get_registry
    except ImportError:
        return [], ["Cannot import kk_utils.agent_tools — is kk_utils installed?"], []

    registry = get_registry()
    all_tools = registry.get_all_tools()

    # Tools registered under this skill's prefix  (e.g. csv_generator_v2__*)
    prefixed = [
        t["function"]["name"]
        for t in all_tools
        if t["function"]["name"].startswith(f"{skill_name}__")
    ]

    # Tools accessible via the skill-name tag (what master_agent uses)
    tagged = [
        t["function"]["name"]
        for t in registry.get_tools_for_tags([skill_name])
    ]

    errors: list[str] = []
    warnings: list[str] = []

    if not prefixed:
        errors.append(
            f"No tools registered with prefix '{skill_name}__'. "
            "Ensure _auto_register() is the last line in tools.py."
        )

    if prefixed and not tagged:
        # Tools exist but can't be found by master_agent
        # Find the actual tags so we can show a helpful message
        tag_sets = set()
        for t in all_tools:
            if t["function"]["name"].startswith(f"{skill_name}__"):
                func = t.get("function_ref")
                if func and hasattr(func, "__agent_tool__"):
                    tag_sets.update(func.__agent_tool__.get("tags", []))
        errors.append(
            f"Tools are registered (prefix OK) but tag '{skill_name}' is missing. "
            f"master_agent.py looks for tools tagged '{skill_name}' when skill='{skill_name}' "
            f"is selected — it will find nothing.\n"
            f"          Current tags: {sorted(tag_sets)}\n"
            f"          Fix: add '{skill_name}' as the first entry in "
            f"tags=[...] inside @agent_tool in tools.py"
        )

    return tagged, errors, warnings


# ---------------------------------------------------------------------------
# Per-skill report
# ---------------------------------------------------------------------------

def check_skill(skill_name: str) -> bool:
    """Run all checks for one skill. Prints results. Returns True if all passed."""
    skill_dir = SKILLS_ROOT / skill_name
    errors: list[str] = []
    warnings: list[str] = []

    # --- Structural checks (no import) ---
    warnings += _check_skill_md(skill_dir)
    errors   += _check_config_json(skill_dir)
    warnings += _check_skill_py(skill_dir)

    # --- Import check ---
    import_error = _import_skill(skill_name)
    if import_error:
        errors.append(f"tools.py failed to import:\n          {import_error}")

    # --- Registry check (only if import succeeded) ---
    tools_found: list[str] = []
    if not import_error:
        tools_found, reg_errors, reg_warnings = _check_registry(skill_name)
        errors   += reg_errors
        warnings += reg_warnings

    # --- Print result ---
    ok = len(errors) == 0
    badge = f"{GREEN}✓ PASS{RESET}" if ok else f"{RED}✗ FAIL{RESET}"
    print(f"  {badge}  {BOLD}{skill_name}{RESET}")

    if tools_found:
        print(f"         tools : {', '.join(tools_found)}")
    elif not import_error:
        print(f"         tools : {YELLOW}(none found){RESET}")

    for w in warnings:
        print(f"         {YELLOW}WARN{RESET}  : {w}")
    for e in errors:
        print(f"         {RED}ERROR{RESET} : {e}")

    return ok


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    requested = sys.argv[1:] if len(sys.argv) > 1 else None
    skill_names = _find_skill_dirs(requested)

    print(f"\n{BOLD}kk_agent_skills — Registration Check{RESET}")
    print(f"Skills to check: {len(skill_names)}  ({', '.join(skill_names)})\n")

    try:
        from kk_utils.agent_tools import get_registry  # noqa: F401
    except ImportError:
        print(
            f"{RED}ERROR: kk_utils not found.{RESET}\n"
            "Install it first:\n"
            "  pip install -e ../kk-utils\n"
            "or make sure it is on sys.path."
        )
        sys.exit(1)

    passed, failed = [], []
    for name in skill_names:
        if check_skill(name):
            passed.append(name)
        else:
            failed.append(name)
        print()

    print("─" * 60)
    print(f"  {GREEN}{len(passed)} passed{RESET}  |  {RED}{len(failed)} failed{RESET}")
    if failed:
        print(f"\n  Failed: {', '.join(failed)}")
    else:
        print(f"\n  {GREEN}All skills registered correctly.{RESET}")

    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
