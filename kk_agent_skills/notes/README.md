# `notes`

**Status: ✅ Completed**

Full CRUD note management with group organisation and keyword search. Notes are stored in the personal-assistant PostgreSQL database and support markdown content and custom metadata.

---

## Tools

| Tool | Function | Destructive | Tags |
|------|----------|:-----------:|------|
| Create Note | `create_note` | No | `notes`, `create` |
| Get Note | `get_note` | No | `notes`, `read` |
| Update Note | `update_note` | No | `notes`, `update` |
| Delete Note | `delete_note` | **Yes** | `notes`, `delete` |
| Search Notes | `search_notes` | No | `notes`, `search` |
| List Notes | `list_notes` | No | `notes`, `list` |

---

## Tool Reference

### `create_note`

Create a new note inside a group.

```python
create_note(
    title: str,                          # Max 500 characters
    content: str,                        # Markdown supported
    group_id: int,                       # Group the note belongs to
    metadata: Optional[dict] = None,     # Tags, classification, etc.
)
```

---

### `get_note`

Retrieve a note by its ID.

```python
get_note(note_id: int)
```

---

### `update_note`

Update any combination of title, content, or metadata. Pass only the fields to change.

```python
update_note(
    note_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None,
    metadata: Optional[dict] = None,
)
```

---

### `delete_note`

Permanently delete a note. Requires explicit confirmation.

```python
delete_note(
    note_id: int,
    confirmed: bool = False,    # Must pass True to execute
)
```

> **Sensitivity:** `medium` — requires `confirmed=True` and prompts for user confirmation before execution.

---

### `search_notes`

Full-text keyword search across note titles and content.

```python
search_notes(
    query: str,
    group_id: Optional[int] = None,   # Restrict to a specific group
    limit: int = 20,
)
```

**Returns:**
```python
{
    "notes": [{"id": 1, "title": "...", "excerpt": "...", "group_id": 2}],
    "total": 5,
    "query": "...",
    "success": True,
}
```

---

### `list_notes`

List notes with optional group filter. Returns summaries without full content.

```python
list_notes(
    group_id: Optional[int] = None,   # None = all groups
    limit: int = 50,
)
```

---

## Dependencies

- `app.services.note_service` — backend note service (lazy import)
  - `create_note_service`
  - `get_note_service`
  - `update_note_service`
  - `delete_note_service`
  - `search_notes_service`
  - `list_notes_service`

## Config (`config.json`)

| Key | Default | Description |
|-----|---------|-------------|
| `default_group` | `null` | Default group when none specified |
| `max_content_length` | `50000` | Maximum note content length in characters |
