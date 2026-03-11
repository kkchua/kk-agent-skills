"""
deep_research — agents/writer_agent.py

Factory for the WriterAgent. Switches between ReportData and ArticleReportData
output types depending on the prompt variant's output_type field.
"""
from agents import Agent

from kk_agent_skills.deep_research.schemas import ArticleReportData, ReportData
from kk_agent_skills.deep_research.agents._prompt_loader import get_writer_instruction


def make_writer_agent(variant: str = "general", model: str = "gpt-4o-mini") -> Agent:
    """
    Build a WriterAgent configured for the given prompt variant.

    Args:
        variant: Prompt variant (general | technical | market | article)
        model: LLM model name

    Returns:
        Configured Agent. Uses ArticleReportData when variant is 'article',
        otherwise uses ReportData.
    """
    instruction, output_type_key = get_writer_instruction(variant)
    output_type = ArticleReportData if output_type_key == "article" else ReportData
    return Agent(
        name=f"WriterAgent[{variant}]",
        instructions=instruction,
        model=model,
        output_type=output_type,
    )
