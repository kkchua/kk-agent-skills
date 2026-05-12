"""
portfolio_publisher skill — tools.py

agentskills.io-compatible tools for Portfolio-01 article management.
Wraps the personal-assistant backend's blog API via PortfolioClient.
"""
import logging
from typing import Optional

from kk_utils.agent_tools import _auto_register, agent_tool

from kk_agent_skills.portfolio_publisher.schemas import (
    ArticleInput,
    ArticleOutput,
    ArticleStatus,
)

logger = logging.getLogger(__name__)


def _client():
    from kk_agent_skills.portfolio_publisher.client import get_portfolio_client
    return get_portfolio_client()


def _base_url() -> str:
    import os
    return os.environ.get("PORTFOLIO_SITE_URL", "")


@agent_tool(
    name="Create Portfolio Article",
    description=(
        "Create a new blog article on the Portfolio site. "
        "Defaults to 'draft' status — use publish_portfolio_article to make it live. "
        "Returns the slug and article ID for follow-up operations."
    ),
    tags=["portfolio_publisher", "portfolio", "article", "blog", "create"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def create_portfolio_article(
    title: str,
    content: str,
    excerpt: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[list[str]] = None,
    status: str = "draft",
    user_id: Optional[str] = None,
) -> dict:
    """
    Create a new portfolio blog article.

    Args:
        title: Article title.
        content: Full article body in markdown.
        excerpt: Short teaser (1-2 sentences).
        category: Category label (e.g. "AI", "Architecture").
        tags: List of tag strings.
        status: "draft" (default) or "published".
        user_id: Auto-injected by Governor.
    """
    try:
        article_in = ArticleInput(
            title=title,
            content=content,
            excerpt=excerpt,
            category=category,
            tags=tags or [],
            status=ArticleStatus(status),
        )
    except Exception as exc:
        return {"success": False, "error": f"Invalid input: {exc}"}

    payload = article_in.model_dump(mode="json")
    payload.pop("metadata", None)  # backend uses metadata_json
    payload["metadata_json"] = article_in.metadata

    try:
        data = _client().create_post(payload)
        out = ArticleOutput.from_api_response(data, base_url=_base_url())
        logger.info(f"Article created: slug={out.slug} status={out.status}")
        return {
            "success": True,
            "id": out.id,
            "slug": out.slug,
            "title": out.title,
            "status": out.status,
            "url": out.url,
            "message": f"Article '{out.title}' created as {out.status}.",
        }
    except Exception as exc:
        logger.exception(f"Create article failed: {exc}")
        return {"success": False, "error": str(exc)}


@agent_tool(
    name="Publish Portfolio Article",
    description=(
        "Change a portfolio article's status to 'published', making it visible on the site. "
        "Pass the article slug (returned when the article was created)."
    ),
    tags=["portfolio_publisher", "portfolio", "article", "publish"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def publish_portfolio_article(
    slug: str,
    user_id: Optional[str] = None,
) -> dict:
    """
    Publish a portfolio article (draft → published).

    Args:
        slug: The article slug identifier.
        user_id: Auto-injected by Governor.
    """
    try:
        data = _client().update_status(slug, "published")
        out = ArticleOutput.from_api_response(data, base_url=_base_url())
        logger.info(f"Article published: slug={slug}")
        return {
            "success": True,
            "slug": out.slug,
            "title": out.title,
            "status": out.status,
            "published_at": out.published_at.isoformat() if out.published_at else None,
            "url": out.url,
            "message": f"Article '{out.title}' is now published.",
        }
    except Exception as exc:
        logger.exception(f"Publish article failed: {exc}")
        return {"success": False, "error": str(exc), "slug": slug}


@agent_tool(
    name="Archive Portfolio Article",
    description=(
        "Archive a portfolio article, removing it from public view without deleting it. "
        "Pass the article slug."
    ),
    tags=["portfolio_publisher", "portfolio", "article", "archive"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def archive_portfolio_article(
    slug: str,
    user_id: Optional[str] = None,
) -> dict:
    """
    Archive a portfolio article (published/draft → archived).

    Args:
        slug: The article slug identifier.
        user_id: Auto-injected by Governor.
    """
    try:
        data = _client().update_status(slug, "archived")
        out = ArticleOutput.from_api_response(data, base_url=_base_url())
        logger.info(f"Article archived: slug={slug}")
        return {
            "success": True,
            "slug": out.slug,
            "title": out.title,
            "status": out.status,
            "message": f"Article '{out.title}' has been archived.",
        }
    except Exception as exc:
        logger.exception(f"Archive article failed: {exc}")
        return {"success": False, "error": str(exc), "slug": slug}


@agent_tool(
    name="List Portfolio Articles",
    description=(
        "List portfolio blog articles. Optionally filter by status: "
        "'draft', 'published', or 'archived'. Returns id, slug, title, status, and dates."
    ),
    tags=["portfolio_publisher", "portfolio", "article", "list"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def list_portfolio_articles(
    status: Optional[str] = None,
    user_id: Optional[str] = None,
) -> dict:
    """
    List portfolio articles, optionally filtered by status.

    Args:
        status: Filter by "draft" | "published" | "archived". None returns all.
        user_id: Auto-injected by Governor.
    """
    try:
        posts = _client().list_all_posts(status=status)
        return {
            "success": True,
            "total": len(posts),
            "status_filter": status,
            "articles": [
                {
                    "id": p.get("id"),
                    "slug": p.get("slug"),
                    "title": p.get("title"),
                    "status": p.get("status"),
                    "category": p.get("category"),
                    "tags": p.get("tags", []),
                    "created_at": p.get("created_at"),
                    "published_at": p.get("published_at"),
                }
                for p in posts
            ],
        }
    except Exception as exc:
        logger.exception(f"List articles failed: {exc}")
        return {"success": False, "error": str(exc)}


@agent_tool(
    name="Update Portfolio Article",
    description=(
        "Update the content or metadata of an existing portfolio article. "
        "Pass the slug and only the fields you want to change."
    ),
    tags=["portfolio_publisher", "portfolio", "article", "update"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def update_portfolio_article(
    slug: str,
    title: Optional[str] = None,
    content: Optional[str] = None,
    excerpt: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[list[str]] = None,
    user_id: Optional[str] = None,
) -> dict:
    """
    Update an existing portfolio article's content or metadata.

    Args:
        slug: The article slug identifier.
        title: New title (optional).
        content: New markdown content (optional).
        excerpt: New excerpt (optional).
        category: New category (optional).
        tags: New tags list (optional).
        user_id: Auto-injected by Governor.
    """
    payload = {}
    if title is not None:
        payload["title"] = title
    if content is not None:
        payload["content"] = content
    if excerpt is not None:
        payload["excerpt"] = excerpt
    if category is not None:
        payload["category"] = category
    if tags is not None:
        payload["tags"] = tags

    if not payload:
        return {"success": False, "error": "No fields provided to update."}

    try:
        data = _client().update_post(slug, payload)
        out = ArticleOutput.from_api_response(data, base_url=_base_url())
        logger.info(f"Article updated: slug={slug} fields={list(payload.keys())}")
        return {
            "success": True,
            "slug": out.slug,
            "title": out.title,
            "status": out.status,
            "message": f"Article '{out.title}' updated.",
        }
    except Exception as exc:
        logger.exception(f"Update article failed: {exc}")
        return {"success": False, "error": str(exc), "slug": slug}


# ------------------------------------------------------------------
# Internal helper — called by deep_research.tools.research_to_article
# ------------------------------------------------------------------

def create_article_from_research(
    research_result: dict,
    category: Optional[str],
    auto_publish: bool,
    user_id: Optional[str],
) -> dict:
    """
    Convert a deep_research result (article variant) into a portfolio post.
    Called internally by deep_research.tools.research_to_article.
    """
    content = research_result.get("content", "")
    query = research_result.get("query", "Untitled")

    # Extract title from the first H1 in the markdown if present
    title = query
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            break

    # Build excerpt from first non-heading paragraph
    excerpt = ""
    in_content = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            in_content = True
            continue
        if in_content and stripped:
            excerpt = stripped[:300]
            break

    status = "published" if auto_publish else "draft"

    try:
        article_in = ArticleInput(
            title=title,
            content=content,
            excerpt=excerpt or None,
            category=category,
            status=ArticleStatus(status),
            metadata={"generated_by": "deep_research", "source_query": query},
        )
    except Exception as exc:
        return {"success": False, "error": f"Article schema validation failed: {exc}"}

    payload = article_in.model_dump(mode="json")
    payload["metadata_json"] = payload.pop("metadata", {})

    try:
        data = _client().create_post(payload)
        out = ArticleOutput.from_api_response(data, base_url=_base_url())
        logger.info(f"Research→article created: slug={out.slug} status={out.status}")
        return {
            "success": True,
            "id": out.id,
            "slug": out.slug,
            "title": out.title,
            "status": out.status,
            "url": out.url,
            "message": (
                f"Article '{out.title}' saved as {out.status}. "
                + (f"View at: {out.url}" if out.url else f"Slug: {out.slug}")
            ),
        }
    except Exception as exc:
        logger.exception(f"Research→article post failed: {exc}")
        return {"success": False, "error": str(exc), "topic": query}


_auto_register()
