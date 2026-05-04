"""
hot_topics skill — tools.py

agentskills.io-compatible tools for discovering trending topics.
Exposes one public tool:
  - hot_topics_discovery: Find top X hot topics for a given subject
"""
import asyncio
import logging
from typing import Optional

from kk_utils.agent_tools import _auto_register, agent_tool

logger = logging.getLogger(__name__)

# Search queries to find trending topics
_TRENDING_SEARCH_TEMPLATES = [
    "{subject} trending topics 2025 2026",
    "{subject} hottest discussions this week",
    "{subject} controversial topics debate",
    "{subject} emerging trends analysis",
    "{subject} most talked about news",
    "{subject} reddit discussions popular",
    "{subject} twitter trending hashtags",
    "{subject} latest breakthrough developments",
]

# AI prompt for analyzing and ranking topics
_TOPIC_ANALYSIS_PROMPT = """
Analyze the following search results about trending topics in "{subject}".
Identify the top {max_topics} hottest/most trending topics.

For each topic, provide:
1. **Topic Name** - Clear, concise title
2. **Why It's Hot** - Explanation of why it's trending now (recent events, controversies, breakthroughs)
3. **Discussion Level** - High/Medium/Low based on how much people are talking about it
4. **Controversy Level** - High/Medium/Low based on debate level
5. **Suggested Angles** - 2-3 specific angles or questions worth exploring

Search Results:
{search_results}

Format your response as a markdown table with columns:
| Rank | Topic | Why It's Hot | Discussion | Controversy | Suggested Angles |

Then provide a brief summary of overall trends in the field.
"""


def _asyncio_run(coroutine):
    """Run async coroutine in sync context (mirrors web_search skill pattern)."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
        return loop.run_until_complete(coroutine)
    except RuntimeError:
        return asyncio.run(coroutine)


async def _search_for_trends(subject: str, max_searches: int = 5) -> list:
    """
    Perform multiple searches to gather trending topic data.
    
    Args:
        subject: The subject/domain to search for
        max_searches: Number of search queries to run
        
    Returns:
        List of search result strings
    """
    from kk_agent_skills.web_search.tools import web_search
    
    all_results = []
    queries_used = []
    
    # Run multiple searches with different templates
    for i, template in enumerate(_TRENDING_SEARCH_TEMPLATES[:max_searches]):
        query = template.format(subject=subject)
        queries_used.append(query)
        logger.info(f"Searching for trends: {query}")
        
        try:
            result = web_search(
                query=query,
                max_results=10,
                search_depth="basic",
            )
            
            if result.get("success"):
                # Format results for analysis
                for r in result.get("results", []):
                    formatted = f"Title: {r.get('title', 'N/A')}\nURL: {r.get('url', 'N/A')}\nSnippet: {r.get('content', 'N/A')[:300]}"
                    all_results.append(formatted)
        except Exception as e:
            logger.warning(f"Search failed for query '{query}': {e}")
    
    logger.info(f"Trend search complete: {len(all_results)} results from {len(queries_used)} queries")
    return all_results


async def _analyze_trends(subject: str, search_results: list, max_topics: int = 10) -> dict:
    """
    Use AI to analyze search results and identify hot topics.
    
    Args:
        subject: The subject/domain
        search_results: List of formatted search result strings
        max_topics: Maximum number of topics to return
        
    Returns:
        Dict with analyzed topics and summary
    """
    from agents import Runner, trace, gen_trace_id
    
    # Prepare search results text
    results_text = "\n\n---\n\n".join(search_results) if search_results else "No search results found."
    
    # Create prompt
    prompt = _TOPIC_ANALYSIS_PROMPT.format(
        subject=subject,
        max_topics=max_topics,
        search_results=results_text,
    )
    
    trace_id = gen_trace_id()
    
    with trace("hot_topics_analysis", trace_id=trace_id):
        logger.info(f"Analyzing trends for '{subject}' (trace: {trace_id})")
        
        try:
            # Use OpenAI Agents SDK to analyze
            result = await Runner.run(
                "gpt-4o-mini",
                prompt,
            )
            
            analysis = result.final_output
            
            return {
                "success": True,
                "subject": subject,
                "max_topics": max_topics,
                "analysis": analysis,
                "sources_count": len(search_results),
                "trace_id": trace_id,
            }
            
        except Exception as e:
            logger.exception(f"Trend analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "subject": subject,
            }


@agent_tool(
    name="Hot Topics Discovery",
    description=(
        "Discover the top X hottest/trending topics for any given subject. "
        "Performs targeted web searches to find what people are discussing, "
        "then uses AI to analyze and rank topics by discussion level and controversy. "
        "Returns a ranked list with explanations of why each topic is trending "
        "and suggested angles for deeper exploration. "
        "Perfect for content planning, research prioritization, or staying current."
    ),
    tags=["hot_topics", "topics", "trending", "research", "analysis", "web", "discovery"],
    access_level="user",
    sensitivity="low",
    requires_confirmation=False,
    is_destructive=False,
)
def hot_topics_discovery(
    subject: str,
    max_topics: int = 10,
    max_searches: int = 5,
    user_id: Optional[str] = None,
) -> dict:
    """
    Discover trending topics for a given subject.
    
    Args:
        subject: The subject/domain to analyze (e.g., "AI agents", "web development", "climate tech")
        max_topics: Maximum number of topics to return (1-20, default 10)
        max_searches: Number of search queries to run (1-8, default 5, more = more comprehensive)
        user_id: Auto-injected by Governor.
        
    Returns:
        Dict with:
        - success: bool
        - subject: str
        - max_topics: int
        - analysis: str (markdown formatted topics table + summary)
        - sources_count: int (number of web sources analyzed)
        - trace_id: str (for debugging)
        - error: str (if failed)
    """
    # Validate inputs
    max_topics = max(1, min(20, max_topics))
    max_searches = max(1, min(8, max_searches))
    
    logger.info(f"Hot topics discovery: subject='{subject}' max_topics={max_topics} max_searches={max_searches} user={user_id}")
    
    try:
        # Step 1: Search for trending topics
        search_results = _asyncio_run(_search_for_trends(subject, max_searches))
        
        if not search_results:
            return {
                "success": False,
                "error": "No search results found. Try a different subject or check web search configuration.",
                "subject": subject,
            }
        
        # Step 2: Analyze and rank topics
        analysis = _asyncio_run(_analyze_trends(subject, search_results, max_topics))
        
        return analysis
        
    except Exception as exc:
        logger.exception(f"Hot topics discovery failed: {exc}")
        return {
            "success": False,
            "error": str(exc),
            "subject": subject,
        }


_auto_register()
