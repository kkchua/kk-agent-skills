"""
digital_me — SkillManifest

RAG-powered personal profile skill. Answers career, skills, experience,
education, projects, and certifications questions.
"""
from kk_utils.skill_manifest import SkillManifest

SKILL = SkillManifest(
    name="digital_me",
    display_name="Digital Me",
    description=(
        "RAG-powered personal profile skill. Answers questions about work history, "
        "skills, education, projects, and certifications using ChromaDB vector search "
        "with structured data fallback."
    ),
    version="1.0.0",
    tags=["digital_me", "rag", "resume", "profile"],
    collection="digital_me",
    capabilities=["tool_provider"],
    min_access_level="demo",
)
