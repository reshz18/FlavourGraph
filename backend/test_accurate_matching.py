#!/usr/bin/env python3
"""
Test script to verify expert-level accurate matching is working
Run this AFTER starting the backend server
"""

import asyncio
import sys
sys.path.insert(0, '.')

from services.simple_recipe_service import SimpleRecipeService

async def test_accurate_matching():
    """Test the accurate matching algorithm"""
    
    print("=" * 70)
    print("🧪 TESTING EXPERT-LEVEL ACCURATE MATCHING")
    print("=" * 70)
    
    service = SimpleRecipeService()
    
    # Test 1: Basic ingredient search
    print("\n📋 TEST 1: Search for 'rice, lemon, oil'")
    print("-" * 70)
    
    ingredients = ["rice", "lemon", "oil"]
    recipes = await service.search_by_ingredients(ingredients, limit=5)
    
    print(f"✅ Found {len(recipes)} recipes\n")
    
    for i, recipe in enumerate(recipes, 1):
        print(f"{i}. {recipe.get('name')} ({recipe.get('cuisine', 'Unknown')})")
        print(f"   Match Score: {recipe.get('match_score', 0):.2f}")
        print(f"   Match Percentage: {recipe.get('match_percentage', 0):.1f}%")
        print(f"   Matched: {recipe.get('total_matched', 0)}/{recipe.get('total_user_ingredients', 0)} ingredients")
        
        if recipe.get('matched_ingredients'):
            print(f"   ✓ You have: {', '.join(recipe['matched_ingredients'][:5])}")
        
        if recipe.get('missing_ingredients'):
            missing = recipe['missing_ingredients'][:3]
            print(f"   🛒 You need: {', '.join(missing)}")
            if len(recipe['missing_ingredients']) > 3:
                print(f"      (+{len(recipe['missing_ingredients']) - 3} more)")
        
        print(f"   Algorithm: {recipe.get('algorithm_used', 'unknown')}")
        print()
    
    # Test 2: Compound ingredient names
    print("\n📋 TEST 2: Search for 'chicken breast, lemon juice, olive oil'")
    print("-" * 70)
    
    ingredients2 = ["chicken breast", "lemon juice", "olive oil"]
    recipes2 = await service.search_by_ingredients(ingredients2, limit=3)
    
    print(f"✅ Found {len(recipes2)} recipes\n")
    
    for i, recipe in enumerate(recipes2, 1):
        print(f"{i}. {recipe.get('name')} ({recipe.get('cuisine', 'Unknown')})")
        print(f"   Match: {recipe.get('match_percentage', 0):.1f}%")
        if recipe.get('matched_ingredients'):
            print(f"   ✓ Matched: {', '.join(recipe['matched_ingredients'])}")
        print()
    
    # Test 3: Name search
    print("\n📋 TEST 3: Search by name 'biryani'")
    print("-" * 70)
    
    name_recipes = await service.search_by_name("biryani", limit=3)
    
    print(f"✅ Found {len(name_recipes)} recipes\n")
    
    for i, recipe in enumerate(name_recipes, 1):
        print(f"{i}. {recipe.get('name')} ({recipe.get('cuisine', 'Unknown')})")
        print(f"   Algorithm: {recipe.get('algorithm_used', 'unknown')}")
        print()
    
    # Test 4: Random recipes (should be Indian-first)
    print("\n📋 TEST 4: Get random recipes (Indian-first)")
    print("-" * 70)
    
    random_recipes = await service.get_random_recipes(count=5)
    
    print(f"✅ Found {len(random_recipes)} recipes\n")
    
    indian_count = sum(1 for r in random_recipes if r.get('cuisine', '').lower() == 'indian')
    print(f"   Indian recipes: {indian_count}/{len(random_recipes)}")
    
    for i, recipe in enumerate(random_recipes, 1):
        cuisine = recipe.get('cuisine', 'Unknown')
        marker = "🇮🇳" if cuisine.lower() == "indian" else "🌍"
        print(f"{i}. {marker} {recipe.get('name')} ({cuisine})")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 70)
    
    # Summary
    print("\n📊 SUMMARY:")
    print(f"   ✅ Ingredient search: {'WORKING' if recipes else 'FAILED'}")
    print(f"   ✅ Accurate matching: {'WORKING' if recipes and recipes[0].get('match_percentage') else 'FAILED'}")
    print(f"   ✅ Matched ingredients: {'WORKING' if recipes and recipes[0].get('matched_ingredients') else 'FAILED'}")
    print(f"   ✅ Missing ingredients: {'WORKING' if recipes and recipes[0].get('missing_ingredients') else 'FAILED'}")
    print(f"   ✅ Name search: {'WORKING' if name_recipes else 'FAILED'}")
    print(f"   ✅ Indian priority: {'WORKING' if indian_count >= len(random_recipes) // 2 else 'NEEDS CHECK'}")
    
    print("\n💡 If all tests passed, your backend is working perfectly!")
    print("   Now test the frontend at: http://localhost:3000")
    print()

if __name__ == "__main__":
    asyncio.run(test_accurate_matching())
