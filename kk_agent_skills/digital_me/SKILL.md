---
name: digital_me
description: Personal profile AI skill — answers career, skills, experience, education, projects and certifications questions using RAG-powered search over uploaded documents with structured data fallback.
version: 1.0.0
dependencies: chromadb, sentence-transformers
capabilities: tool_provider
tags: digital_me, rag, resume, profile
metadata:
  author: personal-assistant
  access_levels: anonymous, demo, user
---

# digital_me

RAG-powered personal profile skill. Answers questions about work history, skills, education,
projects and certifications. Uses ChromaDB vector search over uploaded documents with a
structured data fallback when RAG confidence is low.

## Tools

| Tool | Access | Description |
|---|---|---|
| `search_digital_me` | user | Semantic RAG search over all uploaded documents |
| `get_work_experience` | demo | Work history — RAG first, structured fallback |
| `get_skills` | demo | Skills with category/proficiency filters |
| `get_education` | demo | Education records |
| `get_projects` | demo | Projects with technology/role filters |
| `get_certifications` | demo | Certifications with issuer filter |
| `get_digital_me_summary` | anonymous | Brief public-friendly profile summary |

## Config (`config.json`)

```json
{
  "rag_top_k": 5,
  "min_confidence": 0.1,
  "collection_name": "digital_me"
}
```

## RAG Design

1. **Layer 1 — Retrieval Access Control**: `source_type` filter applied before query
2. **Layer 2 — Post-retrieval sanitization**: `sanitize_chunks()` strips sensitive fields
3. **Fallback**: Structured YAML data in `data/digital_me/` when RAG confidence < 0.1
