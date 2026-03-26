from setuptools import setup, find_packages

setup(
    name="kk-agent-skills",
    version="1.0.0",
    packages=find_packages(),
    package_data={
        "kk_agent_skills": [
            "*/config.json",
            "*/adapters/*/adapter_config.json",
            "*/adapters/*/prompts/*.json",
            "*/adapters/*/prompts/*.txt",
            "*/adapters/*/prompts/*.yaml",
        ],
    },
    include_package_data=True,
    install_requires=[
        "kk-utils",
    ],
    extras_require={
        "web_search": ["tavily-python"],
        "ai": ["openai-agents"],
    },
    python_requires=">=3.10",
    description="agentskills.io-compatible skill library for the personal-assistant backend",
    author="KK",
)
