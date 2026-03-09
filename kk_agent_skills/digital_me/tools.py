"""
digital_me skill — tools.py

agentskills.io-compatible tool module.
RAG-powered personal profile tools with structured data fallback.
Backend service calls are lazy imports — resolved at call time within the backend.
"""
from typing import Optional
import logging

from kk_utils.agent_tools import agent_tool, _auto_register

logger = logging.getLogger(__name__)


@agent_tool(
    name="Search Digital Me Knowledge",
    description="Search Digital Me knowledge base using RAG (resume, projects, documents)",
    tags=["digital_me", "rag", "search"],
    access_level="user",
    sensitivity="medium",
    input_schema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Natural language question or search query"
            },
            "top_k": {
                "type": "integer",
                "description": "Number of results to return",
                "default": 3,
                "minimum": 1,
                "maximum": 10
            },
            "source_type": {
                "type": "string",
                "enum": ["resume", "projects", "skills", "all"],
                "description": "Filter by document type"
            }
        },
        "required": ["query"]
    },
)
def search_digital_me(
    query: str,
    top_k: int = 3,
    source_type: Optional[str] = None,
    user_id: Optional[str] = None,
) -> dict:
    """
    Search Digital Me knowledge base using RAG.

    Args:
        query: Natural language question
        top_k: Number of chunks to retrieve
        source_type: Optional filter (resume, projects, skills, or all)
        user_id: User ID for access control (auto-injected by Governor)
    """
    from kk_agent_skills.digital_me_rag import get_digital_me_rag
    from kk_utils.rag.context_builder import sanitize_chunks

    rag = get_digital_me_rag()

    filter_metadata = {}
    if source_type and source_type != "all":
        filter_metadata["type"] = source_type

    result = rag.query(
        question=query,
        top_k=top_k * 2,
        filter_metadata=filter_metadata,
        min_confidence=0.1,
    )

    sanitized_chunks = sanitize_chunks(result.chunks if result.has_results else [])

    return {
        "query": query,
        "chunks": sanitized_chunks[:top_k],
        "confidence": result.confidence if result.has_results else 0.0,
        "sources": result.sources if result.has_results else [],
        "security_filter_applied": True,
        "filtered_count": len(result.chunks if result.has_results else []) - len(sanitized_chunks),
        "message": result.message,
    }


@agent_tool(
    name="Get Work Experience",
    description="Get work experience from Digital Me (structured data or RAG)",
    tags=["digital_me", "experience", "resume"],
    access_level="demo",
    sensitivity="low",
)
def get_work_experience(
    company: Optional[str] = None,
    search_query: Optional[str] = None,
    user_id: Optional[str] = None,
) -> dict:
    """
    Get work experience — RAG first, structured fallback.

    Args:
        company: Filter by company name
        search_query: Natural language query (uses RAG)
        user_id: User ID (auto-injected)
    """
    rag_query = search_query or (f"work experience at {company}" if company else "work experience and employment history")
    rag_result = search_digital_me(query=rag_query, top_k=5, source_type=None, user_id=user_id)

    if rag_result.get("confidence", 0.0) > 0.1:
        return {
            "source": "rag",
            "confidence": rag_result["confidence"],
            "chunks": rag_result["chunks"],
            "sources": rag_result["sources"],
        }

    from app.services.digital_me_service import get_work_experience_service
    experiences = get_work_experience_service(company=company)
    return {"source": "structured", "experiences": experiences, "count": len(experiences)}


@agent_tool(
    name="Get Skills",
    description="Get skills from Digital Me profile",
    tags=["digital_me", "skills"],
    access_level="demo",
    sensitivity="low",
)
def get_skills(
    category: Optional[str] = None,
    min_proficiency: int = 1,
    search_query: Optional[str] = None,
    user_id: Optional[str] = None,
) -> dict:
    """
    Get skills — RAG first, structured fallback.

    Args:
        category: Filter by category (technical, soft, languages)
        min_proficiency: Minimum proficiency level (1-5)
        search_query: Natural language query (uses RAG)
        user_id: User ID (auto-injected)
    """
    rag_query = search_query or (f"{category} skills" if category else "technical skills and expertise")
    rag_result = search_digital_me(query=rag_query, top_k=5, source_type=None, user_id=user_id)

    if rag_result.get("confidence", 0.0) > 0.1:
        return {"source": "rag", "confidence": rag_result["confidence"], "chunks": rag_result["chunks"]}

    from app.services.digital_me_service import get_skills_service
    skills = get_skills_service(category=category, min_proficiency=min_proficiency)
    return {"source": "structured", "skills": skills, "count": len(skills)}


@agent_tool(
    name="Get Education",
    description="Get education history from Digital Me profile",
    tags=["digital_me", "education", "resume"],
    access_level="demo",
    sensitivity="low",
)
def get_education(
    degree_level: Optional[str] = None,
    field_of_study: Optional[str] = None,
    user_id: Optional[str] = None,
) -> dict:
    """
    Get education history.

    Args:
        degree_level: Filter by degree (bachelor, master, phd)
        field_of_study: Filter by field
        user_id: User ID (auto-injected)
    """
    from app.services.digital_me_service import get_education_service
    education = get_education_service(degree_level=degree_level, field_of_study=field_of_study)
    return {"source": "structured", "education": education, "count": len(education)}


@agent_tool(
    name="Get Projects",
    description="Get projects from Digital Me profile",
    tags=["digital_me", "projects"],
    access_level="demo",
    sensitivity="low",
)
def get_projects(
    technology: Optional[str] = None,
    role: Optional[str] = None,
    search_query: Optional[str] = None,
    user_id: Optional[str] = None,
) -> dict:
    """
    Get projects — RAG first, structured fallback.

    Args:
        technology: Filter by technology
        role: Filter by role
        search_query: Natural language query (uses RAG)
        user_id: User ID (auto-injected)
    """
    rag_query = search_query or (
        f"{technology} projects" if technology else
        f"{role} role projects" if role else
        "projects and accomplishments"
    )
    rag_result = search_digital_me(query=rag_query, top_k=5, source_type=None, user_id=user_id)

    if rag_result.get("confidence", 0.0) > 0.1:
        return {"source": "rag", "confidence": rag_result["confidence"], "chunks": rag_result["chunks"]}

    from app.services.digital_me_service import get_projects_service
    projects = get_projects_service(technology=technology, role=role)
    return {"source": "structured", "projects": projects, "count": len(projects)}


@agent_tool(
    name="Get Certifications",
    description="Get certifications from Digital Me profile",
    tags=["digital_me", "certifications", "resume"],
    access_level="demo",
    sensitivity="low",
)
def get_certifications(
    issuer: Optional[str] = None,
    include_expired: bool = False,
    user_id: Optional[str] = None,
) -> dict:
    """
    Get certifications.

    Args:
        issuer: Filter by issuer
        include_expired: Include expired certifications
        user_id: User ID (auto-injected)
    """
    from app.services.digital_me_service import get_certifications_service
    certs = get_certifications_service(issuer=issuer, include_expired=include_expired)
    return {"source": "structured", "certifications": certs, "count": len(certs)}


@agent_tool(
    name="Get Digital Me Summary",
    description="Get a brief summary of Digital Me profile",
    tags=["digital_me", "summary"],
    access_level="anonymous",
    sensitivity="low",
)
def get_digital_me_summary(user_id: Optional[str] = None) -> dict:
    """
    Get public-friendly Digital Me summary.

    Args:
        user_id: User ID (auto-injected)
    """
    from app.services.digital_me_service import get_digital_me_summary_service
    return get_digital_me_summary_service()


_auto_register()
