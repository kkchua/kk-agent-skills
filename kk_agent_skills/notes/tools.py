"""
notes skill — tools.py

agentskills.io-compatible tool module.
Full CRUD note management with group organisation and keyword search.
Backend service calls are lazy imports — resolved at call time within the backend.
"""
from typing import Optional
import logging

from kk_utils.agent_tools import agent_tool, _auto_register

logger = logging.getLogger(__name__)


@agent_tool(
    name="Create Note",
    description="Create a new note in a specified group",
    tags=["notes", "create"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def create_note(
    title: str,
    content: str,
    group_id: int,
    user_id: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> dict:
    """
    Create a new note.

    Args:
        title: Note title (max 500 characters)
        content: Note content in markdown format
        group_id: ID of the group to add note to
        user_id: User ID (auto-injected by Governor)
        metadata: Optional metadata (tags, classification, etc.)
    """
    from app.services.note_service import create_note_service
    logger.info(f"Creating note: {title} (group_id={group_id})")
    return create_note_service(title=title, content=content, group_id=group_id, user_id=user_id, metadata=metadata)


@agent_tool(
    name="Get Note",
    description="Retrieve a note by ID",
    tags=["notes", "read"],
    access_level="user",
    sensitivity="low",
)
def get_note(
    note_id: int,
    user_id: Optional[str] = None,
) -> dict:
    """
    Get a note by ID.

    Args:
        note_id: Note ID to retrieve
        user_id: User ID for access control (auto-injected)
    """
    from app.services.note_service import get_note_service
    logger.info(f"Retrieving note {note_id}")
    return get_note_service(note_id=note_id, user_id=user_id)


@agent_tool(
    name="Update Note",
    description="Update an existing note",
    tags=["notes", "update"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def update_note(
    note_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None,
    metadata: Optional[dict] = None,
    user_id: Optional[str] = None,
) -> dict:
    """
    Update note title, content or metadata.

    Args:
        note_id: Note ID to update
        title: New title (optional)
        content: New content in markdown (optional)
        metadata: New metadata (optional)
        user_id: User ID for access control (auto-injected)
    """
    from app.services.note_service import update_note_service
    logger.info(f"Updating note {note_id}")
    return update_note_service(note_id=note_id, title=title, content=content, metadata=metadata, user_id=user_id)


@agent_tool(
    name="Delete Note",
    description="Delete a note permanently",
    tags=["notes", "delete"],
    access_level="user",
    sensitivity="medium",
    requires_confirmation=True,
    is_destructive=True,
)
def delete_note(
    note_id: int,
    user_id: Optional[str] = None,
    confirmed: bool = False,
) -> dict:
    """
    Delete a note.

    Args:
        note_id: Note ID to delete
        user_id: User ID for access control (auto-injected)
        confirmed: Confirmation flag (required for destructive actions)
    """
    from app.services.note_service import delete_note_service
    logger.info(f"Deleting note {note_id}")
    return delete_note_service(note_id=note_id, user_id=user_id)


@agent_tool(
    name="Search Notes",
    description="Search notes by keyword in title or content",
    tags=["notes", "search"],
    access_level="user",
    sensitivity="low",
)
def search_notes(
    query: str,
    group_id: Optional[int] = None,
    limit: int = 20,
    user_id: Optional[str] = None,
) -> dict:
    """
    Search notes by keyword.

    Args:
        query: Search query (searches title and content)
        group_id: Optional group filter
        limit: Maximum results to return
        user_id: User ID for filtering results (auto-injected)
    """
    from app.services.note_service import search_notes_service
    logger.info(f"Searching notes: {query}")
    return search_notes_service(query=query, group_id=group_id, limit=limit, user_id=user_id)


@agent_tool(
    name="List Notes",
    description="List notes in a group",
    tags=["notes", "list"],
    access_level="user",
    sensitivity="low",
)
def list_notes(
    group_id: Optional[int] = None,
    limit: int = 50,
    user_id: Optional[str] = None,
) -> dict:
    """
    List notes with optional group filter.

    Args:
        group_id: Optional group filter (None = all groups)
        limit: Maximum results to return
        user_id: User ID for filtering (auto-injected)
    """
    from app.services.note_service import list_notes_service
    logger.info(f"Listing notes (group_id={group_id}, limit={limit})")
    return list_notes_service(group_id=group_id, limit=limit, user_id=user_id)


_auto_register()
