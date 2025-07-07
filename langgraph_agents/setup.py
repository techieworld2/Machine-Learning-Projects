from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Read README content
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "LangGraph Multi-Agent Business Analysis System"

setup(
    name="langgraph-business-analysis",
    version="1.0.0",
    author="LangGraph Business Analysis Team",
    author_email="support@business-analysis.ai",
    description="Multi-agent LangGraph system for comprehensive business analysis and report generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/techieworld2/Machine-Learning-Projects",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "langgraph-analysis=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/*.html", "templates/*.css", "*.env.example"]
    },
    keywords=[
        "langraph",
        "business analysis", 
        "multi-agent",
        "ai",
        "market research",
        "swot analysis",
        "financial analysis",
        "strategic planning",
        "pdf generation",
        "ollama",
        "llm"
    ],
    project_urls={
        "Bug Reports": "https://github.com/techieworld2/Machine-Learning-Projects/issues",
        "Source": "https://github.com/techieworld2/Machine-Learning-Projects",
        "Documentation": "https://github.com/techieworld2/Machine-Learning-Projects/blob/main/langgraph_agents/README.md",
    },
)