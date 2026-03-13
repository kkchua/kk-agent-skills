#!/usr/bin/env python
"""
Example: Using the Hot Topics Discovery Skill

This script demonstrates how to use the hot_topics_discovery tool
to find trending topics for any subject.
"""

from kk_agent_skills.hot_topics.tools import hot_topics_discovery

# Example 1: Find hot topics in AI agents
print("=" * 60)
print("Example 1: Hot Topics in AI Agents")
print("=" * 60)

result = hot_topics_discovery(
    subject="AI agents",
    max_topics=10,
    max_searches=5,
)

if result.get("success"):
    print(f"\nSubject: {result['subject']}")
    print(f"Sources analyzed: {result['sources_count']}")
    print(f"\n{result['analysis']}")
else:
    print(f"Error: {result.get('error')}")

# Example 2: Find hot topics in Web Development (quick)
print("\n" + "=" * 60)
print("Example 2: Hot Topics in Web Development (Quick)")
print("=" * 60)

result = hot_topics_discovery(
    subject="web development frameworks",
    max_topics=5,
    max_searches=3,  # Faster but less comprehensive
)

if result.get("success"):
    print(f"\nSubject: {result['subject']}")
    print(f"Sources analyzed: {result['sources_count']}")
    print(f"\n{result['analysis']}")
else:
    print(f"Error: {result.get('error')}")
