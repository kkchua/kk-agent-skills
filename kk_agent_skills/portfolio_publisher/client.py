"""
portfolio_publisher — client.py

HTTP client that wraps the personal-assistant backend's Portfolio blog API.

Backend endpoints (personal-assistant/backend/app/api/v1/portfolio.py):
  POST   /api/v1/portfolio/blog/posts              → create post
  GET    /api/v1/portfolio/blog/posts/admin/all    → list all posts (any status)
  GET    /api/v1/portfolio/blog/posts/{slug}       → get single post
  PUT    /api/v1/portfolio/blog/posts/{slug}       → full update
  PATCH  /api/v1/portfolio/blog/posts/{slug}/status → status transition
  DELETE /api/v1/portfolio/blog/posts/{slug}       → delete

Auth: X-Admin-Key header (from PORTFOLIO_ADMIN_KEY env var).
Base URL: PORTFOLIO_API_URL env var (default: http://localhost:8000).
"""
import logging
import os
from typing import Any, Optional

logger = logging.getLogger(__name__)


class PortfolioAPIError(Exception):
    """Raised when the Portfolio backend returns a non-2xx response."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"Portfolio API {status_code}: {message}")


class PortfolioClient:
    """Synchronous HTTP client for the Portfolio blog API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        admin_key: Optional[str] = None,
    ):
        self.base_url = (base_url or os.environ.get("PORTFOLIO_API_URL", "http://localhost:8000")).rstrip("/")
        self.admin_key = admin_key or os.environ.get("PORTFOLIO_ADMIN_KEY", "")
        if not self.admin_key:
            logger.warning("PORTFOLIO_ADMIN_KEY not set — admin endpoints will be rejected.")

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-Admin-Key": self.admin_key,
        }

    def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        """Make an HTTP request and return parsed JSON. Raises PortfolioAPIError on failure."""
        import httpx  # lazy import — only needed at call time

        url = f"{self.base_url}{path}"
        logger.debug(f"Portfolio API {method} {url}")

        response = httpx.request(
            method,
            url,
            headers=self._headers,
            timeout=30.0,
            **kwargs,
        )

        if response.status_code >= 400:
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            raise PortfolioAPIError(response.status_code, detail)

        return response.json()

    # ------------------------------------------------------------------
    # CRUD operations
    # ------------------------------------------------------------------

    def create_post(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Create a new blog post. Returns the created post dict."""
        return self._request("POST", "/api/v1/portfolio/blog/posts", json=payload)

    def get_post(self, slug: str) -> dict[str, Any]:
        """Get a single post by slug (public endpoint, no admin key needed)."""
        return self._request("GET", f"/api/v1/portfolio/blog/posts/{slug}")

    def list_all_posts(self, status: Optional[str] = None) -> list[dict[str, Any]]:
        """List all posts (admin endpoint, any status). Optionally filter by status."""
        data = self._request("GET", "/api/v1/portfolio/blog/posts/admin/all")
        posts = data if isinstance(data, list) else data.get("posts", data.get("items", []))
        if status:
            posts = [p for p in posts if p.get("status") == status]
        return posts

    def update_post(self, slug: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Full update of a post (PUT)."""
        return self._request("PUT", f"/api/v1/portfolio/blog/posts/{slug}", json=payload)

    def update_status(self, slug: str, status: str) -> dict[str, Any]:
        """Transition a post to draft | published | archived."""
        return self._request(
            "PATCH",
            f"/api/v1/portfolio/blog/posts/{slug}/status",
            json={"status": status},
        )

    def delete_post(self, slug: str) -> dict[str, Any]:
        """Delete a post permanently."""
        return self._request("DELETE", f"/api/v1/portfolio/blog/posts/{slug}")


# Module-level singleton (lazy init)
_client: Optional[PortfolioClient] = None


def get_portfolio_client() -> PortfolioClient:
    """Return the shared PortfolioClient instance (created on first call)."""
    global _client
    if _client is None:
        _client = PortfolioClient()
    return _client
