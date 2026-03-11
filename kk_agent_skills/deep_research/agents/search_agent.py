"""
deep_research — agents/search_agent.py

Factory for the SearchAgent. Reads instructions and context size from
a YAML prompt variant.
"""
from agents import Agent, ModelSettings, WebSearchTool

from kk_agent_skills.deep_research.agents._prompt_loader import get_search_instruction


def make_search_agent(variant: str = "general", model: str = "gpt-4o-mini") -> Agent:
    """
    Build a SearchAgent configured for the given prompt variant.

    Args:
        variant: Prompt variant (general | technical | market | article)
        model: LLM model name

    Returns:
        Configured Agent with WebSearchTool (tool_choice=required).
    """
    instruction, context_size = get_search_instruction(variant)
    return Agent(
        name=f"SearchAgent[{variant}]",
        instructions=instruction,
        model=model,
        tools=[WebSearchTool(search_context_size=context_size)],
        model_settings=ModelSettings(tool_choice="required"),
    )
