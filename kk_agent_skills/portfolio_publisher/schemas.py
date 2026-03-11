"""
portfolio_publisher — schemas.py

Pydantic v2 models for Portfolio-01 article management.
Mirrors the backend's BlogPost model and schemas.
"""
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field


class ArticleStatus(str, Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class ArticleInput(BaseModel):
    """Input schema for creating or updating a portfolio article."""
    title: str = Field(..., min_length=5, max_length=500)
    content: str = Field(..., min_length=50, description="Full article body in markdown.")
    excerpt: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=100)
    tags: list[str] = Field(default_factory=list)
    status: ArticleStatus = ArticleStatus.draft
    metadata: dict[str, Any] = Field(default_factory=dict)


class ArticleOutput(BaseModel):
    """Returned after creating or updating an article."""
    id: int
    slug: str
    title: str
    status: ArticleStatus
    category: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    excerpt: Optional[str] = None
    created_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    url: Optional[str] = Field(None, description="Computed public URL for published articles.")

    @classmethod
    def from_api_response(cls, data: dict, base_url: str = "") -> "ArticleOutput":
        """Build from the backend API dict response."""
        obj = cls.model_validate(data)
        if obj.status == ArticleStatus.published and obj.slug and base_url:
            obj.url = f"{base_url}/blog/{obj.slug}"
        return obj


class ArticleListItem(BaseModel):
    """Summary row for article listings."""
    id: int
    slug: str
    title: str
    status: ArticleStatus
    category: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    published_at: Optional[datetime] = None


class StatusUpdate(BaseModel):
    """Payload for the PATCH /blog/posts/{slug}/status endpoint."""
    status: ArticleStatus
    published_at: Optional[datetime] = None
