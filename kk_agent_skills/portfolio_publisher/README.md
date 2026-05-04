# `portfolio_publisher`

**Status: ✅ Completed**

CRUD article management for the Portfolio-01 site. Wraps the personal-assistant backend's blog API via an `httpx`-based `PortfolioClient`. Used standalone for manual article management, or automatically as the second stage of the `deep_research → research_to_article` pipeline.

---

## Tools

| Tool | Function | Tags |
|------|----------|------|
| Create Portfolio Article | `create_portfolio_article` | `portfolio`, `article`, `blog`, `create` |
| Publish Portfolio Article | `publish_portfolio_article` | `portfolio`, `article`, `publish` |
| Archive Portfolio Article | `archive_portfolio_article` | `portfolio`, `article`, `archive` |
| List Portfolio Articles | `list_portfolio_articles` | `portfolio`, `article`, `list` |
| Update Portfolio Article | `update_portfolio_article` | `portfolio`, `article`, `update` |

---

## Tool Reference

### `create_portfolio_article`

Create a new article. Defaults to `draft` status.

```python
create_portfolio_article(
    title: str,                          # 5–500 characters
    content: str,                        # Full markdown body (min 50 chars)
    excerpt: Optional[str] = None,       # 1-2 sentence teaser (max 500 chars)
    category: Optional[str] = None,      # e.g. "AI", "Architecture", "Tutorial"
    tags: Optional[list] = None,         # Tag strings
    status: str = "draft",               # draft | published
)
```

**Returns:**
```python
{
    "success": True,
    "id": 42,
    "slug": "understanding-rag-2026-03",
    "title": "Understanding RAG",
    "status": "draft",
    "url": None,    # populated for published articles
    "message": "Article '...' created as draft.",
}
```

---

### `publish_portfolio_article`

Transition an article from `draft` → `published`. Sets `published_at` automatically.

```python
publish_portfolio_article(slug: str)
```

**Returns:**
```python
{
    "success": True,
    "slug": "...",
    "title": "...",
    "status": "published",
    "published_at": "2026-03-10T08:30:00Z",
    "url": "https://portfolio.example.com/blog/...",
    "message": "Article '...' is now published.",
}
```

---

### `archive_portfolio_article`

Remove an article from public view without deleting it.

```python
archive_portfolio_article(slug: str)
```

---

### `list_portfolio_articles`

List all articles. Pass a `status` filter to see only drafts, published, or archived.

```python
list_portfolio_articles(
    status: Optional[str] = None,   # draft | published | archived | None (all)
)
```

**Returns:**
```python
{
    "success": True,
    "total": 12,
    "status_filter": "draft",
    "articles": [
        {
            "id": 42, "slug": "...", "title": "...",
            "status": "draft", "category": "AI",
            "tags": [...], "created_at": "...", "published_at": None,
        }
    ],
}
```

---

### `update_portfolio_article`

Edit an article's content or metadata. Pass only the fields to change.

```python
update_portfolio_article(
    slug: str,
    title: Optional[str] = None,
    content: Optional[str] = None,
    excerpt: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[list] = None,
)
```

---

## Status Transitions

```
draft ──► published ──► archived
  ▲                        │
  └────────────────────────┘   (re-draft by updating status via update_portfolio_article)
```

---

## Schemas

```python
class ArticleStatus(str, Enum):
    draft = "draft"
    published = "published"
    archived = "archived"

class ArticleInput(BaseModel):
    title: str              # min 5, max 500
    content: str            # min 50 (markdown)
    excerpt: Optional[str]  # max 500
    category: Optional[str]
    tags: list[str]
    status: ArticleStatus   # default: draft
    metadata: dict          # stored as metadata_json in DB

class ArticleOutput(BaseModel):
    id: int
    slug: str
    title: str
    status: ArticleStatus
    category: Optional[str]
    tags: list[str]
    created_at: Optional[datetime]
    published_at: Optional[datetime]
    url: Optional[str]      # computed from PORTFOLIO_SITE_URL + slug
```

---

## Backend API Endpoints Used

| Method | Path | Used By |
|--------|------|---------|
| `POST` | `/api/v1/portfolio/blog/posts` | `create_portfolio_article` |
| `GET` | `/api/v1/portfolio/blog/posts/admin/all` | `list_portfolio_articles` |
| `PUT` | `/api/v1/portfolio/blog/posts/{slug}` | `update_portfolio_article` |
| `PATCH` | `/api/v1/portfolio/blog/posts/{slug}/status` | `publish_portfolio_article`, `archive_portfolio_article` |

All requests use the `X-Admin-Key` header for authentication.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PORTFOLIO_API_URL` | Yes | Backend base URL (default: `http://localhost:8000`) |
| `PORTFOLIO_ADMIN_KEY` | Yes | Admin API key for `X-Admin-Key` header |
| `PORTFOLIO_SITE_URL` | No | Public site URL — used to compute article links |

---

## Dependencies

- `httpx` — synchronous HTTP client
- `pydantic` v2 — schema validation

## Config (`config.json`)

| Key | Description |
|-----|-------------|
| `portfolio_api_url_env` | Env var name for the backend URL |
| `portfolio_admin_key_env` | Env var name for the admin key |
| `portfolio_site_url_env` | Env var name for the public site URL |
| `default_status` | Default article status on creation (`"draft"`) |
| `request_timeout_seconds` | HTTP request timeout (30s) |
