"""
portfolio_publisher skill

CRUD tools for Portfolio-01 article management. Wraps the personal-assistant
backend's blog API. Used standalone or chained with deep_research.
"""
from kk_agent_skills.portfolio_publisher.skill import SKILL
from kk_agent_skills.portfolio_publisher.schemas import (
    ArticleInput,
    ArticleOutput,
    ArticleStatus,
)
from kk_agent_skills.portfolio_publisher.client import PortfolioClient, get_portfolio_client

__all__ = [
    "SKILL",
    "ArticleInput",
    "ArticleOutput",
    "ArticleStatus",
    "PortfolioClient",
    "get_portfolio_client",
]
