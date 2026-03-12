---
name: portfolio-publisher
description: Manage portfolio articles and blog posts. Create, publish, archive, and update articles with full metadata management. Use when creating content for portfolio sites, managing blog posts, or publishing articles to web applications.
license: MIT
compatibility: Requires PostgreSQL database connection and portfolio site backend API access
metadata:
  author: kkchua
  version: "1.0.0"
  tags: portfolio, article, blog, publishing, content
allowed-tools: Read Write
---

# Portfolio Publisher Skill

## Overview

Manage portfolio articles and blog posts. Create, publish, archive, and update articles in the portfolio site with full metadata management.

## When to Use

- Creating new blog posts or articles
- Publishing draft content
- Managing article lifecycle (draft → published → archived)
- Updating existing articles
- Listing articles with filters
- Assigning articles to specific portfolio apps

## What It Does

1. **Creates articles** - Draft new portfolio articles with title, content, category, tags, and metadata
2. **Publishes content** - Move articles from draft to published status with publish date
3. **Archives old content** - Archive outdated articles without deleting them
4. **Lists articles** - Retrieve articles with filtering by status, category, tag, or app
5. **Updates content** - Edit existing article title, content, metadata, or status

## Usage

```python
from kk_agent_skills.portfolio_publisher.tools import create_portfolio_article

# Create a new article
result = create_portfolio_article(
    title="Building RAG Systems: A Practical Guide",
    content="# Introduction\n\nRAG systems combine...",
    excerpt="Learn how to build production RAG systems...",
    category="AI",
    tags=["rag", "ai", "tutorial"],
    status="draft",
    assigned_apps=["portfolio-01"],
)

if result.get("success"):
    print(f"Created: {result['article']['slug']}")
else:
    print(f"Error: {result.get('error')}")
```

## Tools

| Tool | Access | Description |
|------|--------|-------------|
| `create_portfolio_article` | user | Create new article draft |
| `publish_portfolio_article` | admin | Publish draft article |
| `archive_portfolio_article` | admin | Archive published article |
| `list_portfolio_articles` | user | List articles with filters |
| `update_portfolio_article` | admin | Update article content |

## Article Status Flow

```
draft ──publish──> published ──archive──> archived
  │                    │
  └────update──────────┘
```

## Assignment System

Articles can be assigned to specific apps for targeted visibility:

```python
# Assign to specific app
create_portfolio_article(
    title="AgentMe Guide",
    assigned_apps=["portfolio-01"],  # Only shows on portfolio-01
)

# Public article (no assignment)
create_portfolio_article(
    title="General Post",
    assigned_apps=[],  # Shows on all sites
)
```

## Example Workflow

```python
from kk_agent_skills.portfolio_publisher.tools import (
    create_portfolio_article,
    publish_portfolio_article,
    list_portfolio_articles,
)

# Step 1: Create draft
draft = create_portfolio_article(
    title="My RAG Tutorial",
    content="# RAG Tutorial\n\n...",
    category="Tutorial",
    tags=["rag", "ai"],
    status="draft",
)

# Step 2: Review and edit if needed
update_portfolio_article(
    slug=draft["article"]["slug"],
    content="# RAG Tutorial\n\nUpdated content...",
)

# Step 3: Publish
publish_portfolio_article(slug=draft["article"]["slug"])

# Step 4: Verify published
articles = list_portfolio_articles(status="published")
print(f"Total published: {articles['total']}")
```

## Related Skills

- **article-generation** - AI-assisted article drafting
- **deep-research** - Research topics before writing
- **notes** - Store article ideas and outlines
- **hot-topics** - Find trending topics to write about

## Error Handling

Returns structured error responses:

```python
{
    "success": False,
    "error": "Slug already exists: 'my-article'",
    "detail": "Article with this slug already exists"
}
```

Common errors:
- Duplicate slug - Article with this slug already exists
- Article not found - No article matches the given slug
- Invalid status transition - Cannot transition from X to Y
- Missing required fields - Title or content is required

## Tips

1. **Use descriptive slugs** - Auto-generated from title but can be customized for SEO
2. **Add excerpts** - Helps with article listings and social sharing
3. **Categorize content** - Makes filtering and navigation easier
4. **Tag strategically** - Use consistent tags for related articles
5. **Review before publishing** - Use draft status for review workflow
6. **Archive instead of delete** - Keep historical content accessible via archive filter
