#!/usr/bin/env python3
"""
Validation script for LangGraph Business Analysis System
Tests system structure and basic functionality without external dependencies
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path: str, description: str) -> bool:
    """Check if a file exists and report status"""
    exists = os.path.exists(file_path)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {file_path}")
    return exists

def check_directory_structure():
    """Check if all required directories and files exist"""
    print("Checking directory structure...")
    
    required_files = [
        ("README.md", "Main README"),
        ("requirements.txt", "Requirements file"),
        ("setup.py", "Setup script"),
        (".env.example", "Environment template"),
        ("main.py", "Main entry point"),
        ("graph.py", "LangGraph workflow"),
        
        # Agent files
        ("agents/__init__.py", "Agents package"),
        ("agents/base_agent.py", "Base agent class"),
        ("agents/planner.py", "Planner agent"),
        ("agents/research.py", "Research agent"),
        ("agents/swot.py", "SWOT agent"),
        ("agents/strategy.py", "Strategy agent"),
        ("agents/finance.py", "Finance agent"),
        ("agents/writer.py", "Writer agent"),
        
        # Model files
        ("models/__init__.py", "Models package"),
        ("models/schemas.py", "Data schemas"),
        
        # Tool files
        ("tools/__init__.py", "Tools package"),
        ("tools/search.py", "Search tool"),
        ("tools/scraper.py", "Web scraper"),
        ("tools/pdf_generator.py", "PDF generator"),
        
        # Utility files
        ("utils/__init__.py", "Utils package"),
        ("utils/config.py", "Configuration"),
        ("utils/logger.py", "Logging system"),
        
        # Template files
        ("templates/report_template.html", "HTML template"),
        ("templates/styles.css", "CSS styles"),
    ]
    
    all_exist = True
    for file_path, description in required_files:
        exists = check_file_exists(file_path, description)
        all_exist = all_exist and exists
    
    return all_exist

def check_file_sizes():
    """Check if files have reasonable content"""
    print("\nChecking file sizes...")
    
    important_files = [
        "main.py",
        "graph.py",
        "agents/base_agent.py",
        "agents/planner.py",
        "agents/research.py",
        "tools/search.py",
        "models/schemas.py",
        "README.md"
    ]
    
    for file_path in important_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            status = "✓" if size > 100 else "⚠"
            print(f"{status} {file_path}: {size} bytes")
        else:
            print(f"✗ {file_path}: NOT FOUND")

def check_python_syntax():
    """Check basic Python syntax of key files"""
    print("\nChecking Python syntax...")
    
    python_files = [
        "main.py",
        "graph.py",
        "setup.py",
        "agents/base_agent.py",
        "models/schemas.py",
        "utils/config.py",
    ]
    
    for file_path in python_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    compile(f.read(), file_path, 'exec')
                print(f"✓ {file_path}: Syntax OK")
            except SyntaxError as e:
                print(f"✗ {file_path}: Syntax Error - {e}")
            except Exception as e:
                print(f"⚠ {file_path}: {e}")
        else:
            print(f"✗ {file_path}: NOT FOUND")

def check_imports():
    """Check if imports are properly structured"""
    print("\nChecking import structure...")
    
    # Try to check imports without actually importing (to avoid dependency issues)
    import_checks = [
        ("agents/__init__.py", ["BaseAgent", "PlannerAgent"]),
        ("models/__init__.py", ["BusinessAnalysisState"]),
        ("tools/__init__.py", ["SearchTool", "WebScraperTool"]),
        ("utils/__init__.py", ["Config", "logger"]),
    ]
    
    for file_path, expected_exports in import_checks:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                for export in expected_exports:
                    if export in content:
                        print(f"✓ {file_path} exports {export}")
                    else:
                        print(f"✗ {file_path} missing {export}")

def main():
    """Run all validation checks"""
    print("=" * 60)
    print("LangGraph Business Analysis System - Structure Validation")
    print("=" * 60)
    
    # Change to the correct directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    all_good = True
    
    # Run checks
    all_good &= check_directory_structure()
    check_file_sizes()
    check_python_syntax()
    check_imports()
    
    print("\n" + "=" * 60)
    if all_good:
        print("✓ VALIDATION PASSED - System structure looks good!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up Ollama: ollama pull mistral:7b")
        print("3. Configure environment: cp .env.example .env")
        print("4. Test system: python main.py --validate-config")
    else:
        print("✗ VALIDATION FAILED - Some files are missing or have issues")
        return 1
    
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())