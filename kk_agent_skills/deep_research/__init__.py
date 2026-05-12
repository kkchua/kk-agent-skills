"""
deep_research skill

Multi-agent deep research pipeline with YAML-configurable prompt variants.
Supports general, technical, market, and article research modes.
"""
from kk_agent_skills.deep_research.skill import SKILL
from kk_agent_skills.deep_research.research_manager import ResearchManager
from kk_agent_skills.deep_research.schemas import ReportData, ArticleReportData, WebSearchPlan

__all__ = ["SKILL", "ResearchManager", "ReportData", "ArticleReportData", "WebSearchPlan"]
