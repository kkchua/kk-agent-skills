#!/usr/bin/env python
"""Test hot_topics skill import and configuration."""

from kk_agent_skills.hot_topics.tools import hot_topics_discovery

print("=" * 50)
print("Hot Topics Skill - Import Test")
print("=" * 50)

# Check function exists
print(f"✓ Function imported: {hot_topics_discovery.__name__}")

# Check tool config
if hasattr(hot_topics_discovery, '_tool_config'):
    config = hot_topics_discovery._tool_config
    print(f"✓ Tool name: {config.get('name', 'N/A')}")
    print(f"✓ Tags: {config.get('tags', [])}")
    print(f"✓ Access level: {config.get('access_level', 'N/A')}")
    print(f"✓ Requires confirmation: {config.get('requires_confirmation', 'N/A')}")
else:
    print("⚠ Tool config not found (may use decorator metadata)")

print("\n✓ Hot topics skill is ready to use!")
print("\nUsage example:")
print('  from kk_agent_skills.hot_topics.tools import hot_topics_discovery')
print('  result = hot_topics_discovery(subject="AI agents", max_topics=10)')
