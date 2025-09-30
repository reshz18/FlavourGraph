#!/usr/bin/env python
"""Test recipe search functionality"""

import asyncio
import httpx
import json

async def test_direct_api():
    """Test TheMealDB API directly"""
    print("Testing TheMealDB API directly...")
    
    async with httpx.AsyncClient() as client:
        # Test 1: Search by ingredient
        print("\n1. Testing search by ingredient (chicken)...")
        response = await client.get(
            "https://www.themealdb.com/api/json/v1/1/filter.php",
            params={"i": "chicken"}
        )
        if response.status_code == 200:
            data = response.json()
            meals = data.get("meals", [])
            print(f"   Found {len(meals)} chicken recipes")
            if meals:
                print(f"   Sample: {meals[0]['strMeal']}")
        else:
            print(f"   Error: {response.status_code}")
            
        # Test 2: Search by name
        print("\n2. Testing search by name (pasta)...")
        response = await client.get(
            "https://www.themealdb.com/api/json/v1/1/search.php",
            params={"s": "pasta"}
        )
        if response.status_code == 200:
            data = response.json()
            meals = data.get("meals", [])
            print(f"   Found {len(meals) if meals else 0} pasta recipes")
            if meals:
                print(f"   Sample: {meals[0]['strMeal']}")
        else:
            print(f"   Error: {response.status_code}")
            
        # Test 3: Get random recipe
        print("\n3. Testing random recipe...")
        response = await client.get(
            "https://www.themealdb.com/api/json/v1/1/random.php"
        )
        if response.status_code == 200:
            data = response.json()
            meals = data.get("meals", [])
            if meals:
                print(f"   Random recipe: {meals[0]['strMeal']}")
        else:
            print(f"   Error: {response.status_code}")

async def test_our_api():
    """Test our FreeRecipeAPIs class"""
    print("\n\nTesting our FreeRecipeAPIs class...")
    
    from services.free_recipe_apis import FreeRecipeAPIs
    api = FreeRecipeAPIs()
    
    # Test with ingredients
    print("\n1. Testing with ingredients...")
    recipes = await api.search_themealdb(ingredients=["chicken", "rice"])
    print(f"   Found {len(recipes)} recipes")
    if recipes:
        print(f"   Sample: {recipes[0]['name']}")
    
    # Test with query
    print("\n2. Testing with query...")
    recipes = await api.search_themealdb(query="pasta")
    print(f"   Found {len(recipes)} recipes")
    if recipes:
        print(f"   Sample: {recipes[0]['name']}")
    
    # Test get_recipes method
    print("\n3. Testing get_recipes method...")
    recipes = await api.get_recipes(ingredients=["chicken"], limit=5)
    print(f"   Found {len(recipes)} recipes")
    for i, recipe in enumerate(recipes[:3]):
        print(f"   {i+1}. {recipe['name']}")

if __name__ == "__main__":
    print("=" * 50)
    print("Recipe API Test")
    print("=" * 50)
    
    asyncio.run(test_direct_api())
    asyncio.run(test_our_api())
    
    print("\n" + "=" * 50)
    print("✓ Tests complete!")
    print("=" * 50)
