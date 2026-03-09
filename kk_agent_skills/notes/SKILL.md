---
name: notes
description: Note management skill — create, read, update, delete, search and list notes organised in groups. All operations are user-scoped and Governor-validated.
version: 1.0.0
dependencies: sqlalchemy
capabilities: tool_provider
tags: notes, crud, productivity
metadata:
  author: personal-assistant
  access_levels: user
---

# notes

Full CRUD note management skill with group organisation and keyword search.

## Tools

| Tool | Access | Description |
|---|---|---|
| `create_note` | user | Create a new note in a group |
| `get_note` | user | Retrieve a note by ID |
| `update_note` | user | Update title, content or metadata |
| `delete_note` | user | Delete a note (destructive, requires confirmation) |
| `search_notes` | user | Keyword search across title and content |
| `list_notes` | user | List notes with optional group filter |

## Config (`config.json`)

```json
{
  "default_limit": 50,
  "max_limit": 200
}
```
