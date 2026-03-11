"""
deep_research — agents/planner_agent.py

Factory for the PlannerAgent. Reads instructions from a YAML prompt variant
so the same agent code supports all research flavors.
"""
from agents import Agent

from kk_agent_skills.deep_research.schemas import WebSearchPlan
from kk_agent_skills.deep_research.agents._prompt_loader import get_planner_instruction


def make_planner_agent(variant: str = "general", model: str = "gpt-4o-mini") -> Agent:
    """
    Build a PlannerAgent configured for the given prompt variant.

    Args:
        variant: Prompt variant (general | technical | market | article)
        model: LLM model name

    Returns:
        Configured Agent with WebSearchPlan structured output.
    """
    instruction, _ = get_planner_instruction(variant)
    return Agent(
        name=f"PlannerAgent[{variant}]",
        instructions=instruction,
        model=model,
        output_type=WebSearchPlan,
    )
