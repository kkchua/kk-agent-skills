"""
deep_research — schemas.py

Pydantic v2 models for the deep research pipeline.
Used as structured outputs for agents and as validation boundaries
between pipeline stages.
"""
from typing import Optional
from pydantic import BaseModel, Field


class WebSearchItem(BaseModel):
    """A single planned search with its reasoning."""
    reason: str = Field(description="Why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    """Structured output from the planner agent."""
    searches: list[WebSearchItem] = Field(
        description="List of web searches to perform to best answer the query."
    )


class ReportData(BaseModel):
    """Structured output from the writer agent — the final research report."""
    short_summary: str = Field(
        description="A short 2-3 sentence summary of the findings.",
        min_length=10,
        max_length=1000,
    )
    markdown_report: str = Field(
        description="The full research report in markdown format.",
        min_length=100,
    )
    follow_up_questions: list[str] = Field(
        default_factory=list,
        description="Suggested topics to research further.",
    )
    search_queries_used: list[str] = Field(
        default_factory=list,
        description="The search queries that were executed.",
    )
    sources: list[str] = Field(
        default_factory=list,
        description="Source URLs or references cited in the report.",
    )


class ArticleReportData(BaseModel):
    """
    Structured output from the writer agent when using the 'article' prompt variant.
    Optimized for direct use as a portfolio blog post.
    """
    title: str = Field(
        description="The blog article title.",
        min_length=5,
        max_length=500,
    )
    excerpt: str = Field(
        description="A 1-2 sentence teaser for the article.",
        min_length=10,
        max_length=500,
    )
    markdown_content: str = Field(
        description="The full article body in markdown format.",
        min_length=100,
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Relevant tags for the article.",
    )
    follow_up_questions: list[str] = Field(
        default_factory=list,
        description="Further research angles.",
    )
