#!/usr/bin/env python
"""
Test script to verify all imports work correctly
"""

print("Testing FlavorGraph Backend Imports...")
print("-" * 40)

try:
    print("✓ Testing utils.logger...")
    from utils.logger import logger, setup_logger
    print("  ✓ Logger imported successfully")
    
    print("✓ Testing models...")
    from models.recipe_models import RecipeRequest, RecipeResponse, Ingredient
    print("  ✓ Models imported successfully")
    
    print("✓ Testing services...")
    from services.recipe_service import RecipeService
    print("  ✓ RecipeService imported successfully")
    
    from services.graph_service import IngredientGraphService
    print("  ✓ GraphService imported successfully")
    
    from services.algorithm_service import AlgorithmService
    print("  ✓ AlgorithmService imported successfully")
    
    print("✓ Testing main app...")
    from main import app
    print("  ✓ FastAPI app imported successfully")
    
    print("-" * 40)
    print("✅ ALL IMPORTS SUCCESSFUL! Backend is ready to run.")
    print("\nYou can now run: python run.py")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("\nPlease run: pip install -r requirements.txt")
    
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
