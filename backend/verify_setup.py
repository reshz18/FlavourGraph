#!/usr/bin/env python
"""
Quick verification that all required modules are installed
"""

import sys

def check_import(module_name, display_name=None):
    """Check if a module can be imported"""
    if display_name is None:
        display_name = module_name
    
    try:
        __import__(module_name)
        print(f"✅ {display_name:20} - OK")
        return True
    except ImportError as e:
        print(f"❌ {display_name:20} - MISSING ({e})")
        return False

print("=" * 50)
print("  FlavorGraph Backend - Dependency Check")
print("=" * 50)
print()

# List of required modules
required_modules = [
    ("fastapi", "FastAPI"),
    ("uvicorn", "Uvicorn"),
    ("pydantic", "Pydantic"),
    ("networkx", "NetworkX"),
    ("httpx", "HTTPX"),
    ("dotenv", "Python-Dotenv"),
    ("fuzzywuzzy", "FuzzyWuzzy"),
]

all_ok = True
for module, name in required_modules:
    if not check_import(module, name):
        all_ok = False

print()
print("=" * 50)

if all_ok:
    print("✅ All dependencies are installed!")
    print()
    print("You can now run: python run.py")
else:
    print("❌ Some dependencies are missing!")
    print()
    print("Please run: pip install -r requirements.txt")
    print("Or run: fix_and_run.bat")

print("=" * 50)
