# Repository Guidelines

## Project Structure & Module Organization
This repository is a Python skill library. Each skill lives under `kk_agent_skills/<skill_name>/` and is self-contained.

- `skill.py` declares the `SkillManifest`
- `tools.py` exposes `@agent_tool` functions and ends with `_auto_register()`
- `config.json` stores default settings
- `README.md` documents the skill
- Optional folders include `agents/`, `prompts/`, `adapters/`, and `schemas.py`

Root-level files such as `README.md`, `RELEASE.md`, and `HOT_TOPICS_IMPLEMENTATION.md` document the package and feature history. The main smoke test currently lives in `test_hot_topics.py`.

## Build, Test, and Development Commands

- `pip install -e .` installs the package in editable mode for local development.
- `pip install -e ".[web_search]"` or `pip install -e ".[ai]"` installs optional extras from `setup.py`.
- `python test_hot_topics.py` runs the existing import/config smoke test for the hot topics skill.

There is no dedicated build script in the repo; packaging is driven by `setup.py`.

## Coding Style & Naming Conventions
Use Python 3.10+ and standard 4-space indentation. Keep skill code explicit and small:

- module and function names use `snake_case`
- classes and Pydantic models use `PascalCase`
- tool functions must return `dict`
- `user_id: Optional[str] = None` belongs at the end of each tool signature
- backend imports should be lazy, inside the function body
- keep `_auto_register()` as the last line in `tools.py`

Follow the existing pattern of clear docstrings and minimal module-level logic.

## Testing Guidelines
Current validation is lightweight and script-based. Prefer small smoke tests that verify imports, tool metadata, and default config values, as in `test_hot_topics.py`. Name new tests `test_*.py` and keep them close to the skill they exercise. There is no enforced coverage threshold in the repository.

## Commit & Pull Request Guidelines
Recent history uses short, imperative commit messages, often with a release tag or scope prefix such as `docs:`. Keep commits focused and descriptive.

Pull requests should include:

- a brief summary of the skill or behavior changed
- the affected package paths, such as `kk_agent_skills/deep_research/`
- evidence of validation, for example `python test_hot_topics.py`
- screenshots only when a UI or rendered output changes

## Agent-Specific Notes
Do not move backend imports to module scope, and do not change skill manifests or package data globs without checking how the skill is loaded and packaged.
