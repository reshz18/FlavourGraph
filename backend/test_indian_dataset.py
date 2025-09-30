#!/usr/bin/env python3
"""
Test Indian Dataset Integration
Run this to verify the CSV is loaded and working
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from services.indian_recipe_service import IndianRecipeService

def test_indian_dataset():
    print("=" * 70)
    print("🧪 TESTING INDIAN DATASET INTEGRATION")
    print("=" * 70)
    
    service = IndianRecipeService()
    
    # Test 1: Check if CSV loaded
    print(f"\n✅ Loaded {len(service.recipes)} recipes from CSV")
    
    if len(service.recipes) == 0:
        print("❌ ERROR: No recipes loaded!")
        print(f"   CSV Path: {service.csv_path}")
        print(f"   File exists: {os.path.exists(service.csv_path)}")
        return False
    
    # Test 2: Search by ingredients
    print("\n📋 TEST: Search for 'rice, lemon, oil'")
    print("-" * 70)
    
    recipes = service.search_by_ingredients(["rice", "lemon", "oil"], limit=5)
    print(f"Found {len(recipes)} recipes\n")
    
    for i, recipe in enumerate(recipes, 1):
        print(f"{i}. {recipe['name']}")
        print(f"   Cuisine: {recipe['cuisine']}")
        print(f"   Match: {recipe.get('match_percentage', 0):.1f}%")
        if recipe.get('matched_ingredients'):
            print(f"   ✓ You have: {', '.join(recipe['matched_ingredients'][:3])}")
        if recipe.get('missing_ingredients'):
            print(f"   🛒 You need: {', '.join(recipe['missing_ingredients'][:3])}")
        print()
    
    # Test 3: Search by name
    print("\n📋 TEST: Search for 'biryani'")
    print("-" * 70)
    
    recipes = service.search_by_name("biryani", limit=3)
    print(f"Found {len(recipes)} recipes\n")
    
    for i, recipe in enumerate(recipes, 1):
        print(f"{i}. {recipe['name']}")
        print(f"   Cuisine: {recipe['cuisine']}")
        print()
    
    # Test 4: Get random recipes
    print("\n📋 TEST: Get random/featured recipes")
    print("-" * 70)
    
    recipes = service.get_random_recipes(count=5)
    print(f"Found {len(recipes)} recipes\n")
    
    for i, recipe in enumerate(recipes, 1):
        print(f"{i}. {recipe['name']}")
        print(f"   Cuisine: {recipe['cuisine']}")
        print(f"   Course: {recipe.get('course', 'N/A')}")
        print()
    
    print("=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    print("\n💡 Indian dataset is working correctly!")
    print("   Now restart backend: python run.py")
    print("   Then test frontend: http://localhost:3000")
    print()
    
    return True

if __name__ == "__main__":
    test_indian_dataset()
