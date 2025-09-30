#!/usr/bin/env python
"""Test backend imports and basic functionality"""

import sys
print("Testing backend components...")

try:
    # Test basic imports
    print("1. Testing imports...")
    from services.recipe_service import RecipeService
    from services.free_recipe_apis import FreeRecipeAPIs
    print("✓ Imports successful")
    
    # Test free recipe API
    print("\n2. Testing free recipe API...")
    import asyncio
    
    async def test_api():
        api = FreeRecipeAPIs()
        # Test with simple ingredients
        recipes = await api.search_themealdb(ingredients=["chicken"])
        print(f"✓ Found {len(recipes)} recipes from TheMealDB")
        if recipes:
            print(f"  Sample: {recipes[0]['name']}")
        return recipes
    
    # Run the test
    recipes = asyncio.run(test_api())
    
    print("\n✓ All tests passed!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
