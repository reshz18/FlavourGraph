#!/usr/bin/env python
"""
Complete system test to verify everything works
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import httpx

async def test_everything():
    print("=" * 60)
    print("FLAVORGRAPH COMPLETE SYSTEM TEST")
    print("=" * 60)
    
    # Test 1: Check if backend is running
    print("\n1. Checking backend health...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/api/health")
            if response.status_code == 200:
                print("   ✓ Backend is running")
            else:
                print("   ✗ Backend not responding properly")
                return
    except:
        print("   ✗ Backend is NOT running!")
        print("   Please run: python run.py")
        return
    
    # Test 2: Test recipe search by ingredients
    print("\n2. Testing recipe search by ingredients...")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/recipes/suggest",
            json={
                "available_ingredients": ["chicken", "rice", "tomato"],
                "max_recipes": 5
            }
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            recipes = response.json()
            print(f"   ✓ Found {len(recipes)} recipes")
            if recipes:
                for i, recipe in enumerate(recipes[:3], 1):
                    print(f"      {i}. {recipe.get('name', 'Unknown')}")
        else:
            print(f"   ✗ Error: {response.text}")
    
    # Test 3: Test recipe search by name
    print("\n3. Testing recipe search by name...")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/recipes/search",
            params={"query": "pasta", "limit": 5}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            recipes = data.get('recipes', [])
            print(f"   ✓ Found {len(recipes)} recipes")
            if recipes:
                for i, recipe in enumerate(recipes[:3], 1):
                    print(f"      {i}. {recipe.get('name', 'Unknown')}")
        else:
            print(f"   ✗ Error: {response.text}")
    
    # Test 4: Test TheMealDB directly
    print("\n4. Testing TheMealDB API directly...")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.themealdb.com/api/json/v1/1/search.php",
            params={"s": "chicken"}
        )
        if response.status_code == 200:
            data = response.json()
            meals = data.get("meals", [])
            if meals:
                print(f"   ✓ TheMealDB is working ({len(meals)} recipes found)")
                print(f"      Sample: {meals[0]['strMeal']}")
            else:
                print("   ✗ TheMealDB returned no recipes")
        else:
            print("   ✗ TheMealDB API is down")

if __name__ == "__main__":
    print("\nStarting complete system test...")
    print("Make sure backend is running (python run.py)\n")
    asyncio.run(test_everything())
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
