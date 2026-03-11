# `digital_me`

**Status: ✅ Completed**

RAG-powered personal profile skill. Answers questions about career history, technical skills, education, projects, and certifications. Uses ChromaDB vector search as the primary source, with structured database fallback when RAG confidence is below threshold.

---

## Tools

| Tool | Function | Access | Tags |
|------|----------|--------|------|
| Search Digital Me Knowledge | `search_digital_me` | `user` | `digital_me`, `rag`, `search` |
| Get Work Experience | `get_work_experience` | `demo` | `digital_me`, `experience`, `resume` |
| Get Skills | `get_skills` | `demo` | `digital_me`, `skills` |
| Get Education | `get_education` | `demo` | `digital_me`, `education`, `resume` |
| Get Projects | `get_projects` | `demo` | `digital_me`, `projects` |
| Get Certifications | `get_certifications` | `demo` | `digital_me`, `certifications`, `resume` |
| Get Digital Me Summary | `get_digital_me_summary` | `anonymous` | `digital_me`, `summary` |

---

## RAG + Structured Fallback Pattern

Profile tools first try RAG (ChromaDB vector search). If confidence is too low they fall back to the structured database service:

```
RAG query (ChromaDB)
    ├── confidence > 0.1  →  return RAG chunks + sources
    └── confidence ≤ 0.1  →  return structured DB result
```

`search_digital_me` is the raw RAG entry point. All other tools call it internally before falling back.

---

## Tool Reference

### `search_digital_me`

Full-text RAG search across all profile documents.

```python
search_digital_me(
    query: str,
    top_k: int = 3,                     # 1–10 results
    source_type: Optional[str] = None,  # resume | projects | skills | all
)
```

**Returns:**
```python
{
    "query": "...",
    "chunks": [{"text": "...", "score": 0.85, "source": "..."}],
    "confidence": 0.85,
    "sources": ["resume.pdf"],
    "security_filter_applied": True,
    "filtered_count": 0,
    "message": "...",
}
```

---

### `get_work_experience`

Employment history — RAG first, structured fallback.

```python
get_work_experience(
    company: Optional[str] = None,        # Filter by company name
    search_query: Optional[str] = None,   # Natural language query
)
```

---

### `get_skills`

Technical and soft skills — RAG first, structured fallback.

```python
get_skills(
    category: Optional[str] = None,       # technical | soft | languages
    min_proficiency: int = 1,             # 1–5
    search_query: Optional[str] = None,
)
```

---

### `get_education`

Education history (structured DB only — no RAG for education).

```python
get_education(
    degree_level: Optional[str] = None,   # bachelor | master | phd
    field_of_study: Optional[str] = None,
)
```

---

### `get_projects`

Projects and accomplishments — RAG first, structured fallback.

```python
get_projects(
    technology: Optional[str] = None,
    role: Optional[str] = None,
    search_query: Optional[str] = None,
)
```

---

### `get_certifications`

Certifications — structured DB with filters.

```python
get_certifications(
    issuer: Optional[str] = None,
    include_expired: bool = False,
)
```

---

### `get_digital_me_summary`

Public-safe profile summary. Available to unauthenticated visitors.

```python
get_digital_me_summary()
```

---

## Dependencies

- [`digital_me_rag`](../digital_me_rag/README.md) — internal ChromaDB RAG engine
- `kk_utils.rag.context_builder.sanitize_chunks` — security filtering on retrieved chunks
- `app.services.digital_me_service` — structured data fallback (lazy import)

## Config (`config.json`)

| Key | Default | Description |
|-----|---------|-------------|
| `rag_top_k` | `3` | Default number of RAG chunks to retrieve |
| `min_confidence` | `0.1` | Confidence threshold for RAG vs. structured fallback |
| `collection_name` | `"digital_me"` | ChromaDB collection name |
