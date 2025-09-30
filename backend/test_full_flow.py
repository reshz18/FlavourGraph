import httpx
import json
import asyncio

async def test_full_flow():
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("Testing complete recipe flow...")
        print("=" * 50)
        
        # Test 1: Direct TheMealDB API
        print("\n1. Testing TheMealDB directly...")
        response = await client.get(
            "https://www.themealdb.com/api/json/v1/1/search.php",
            params={"s": "chicken"}
        )
        if response.status_code == 200:
            data = response.json()
            meals = data.get("meals", [])
            print(f"   TheMealDB returned {len(meals) if meals else 0} recipes")
            if meals:
                print(f"   Sample: {meals[0]['strMeal']}")
        
        # Test 2: Our backend search endpoint
        print("\n2. Testing our backend /api/recipes/search...")
        response = await client.get(
            "http://localhost:8000/api/recipes/search",
            params={"query": "chicken", "limit": 5}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response structure: {list(data.keys())}")
            print(f"   Total recipes: {data.get('total', 0)}")
            if data.get("recipes"):
                print(f"   First recipe: {data['recipes'][0].get('name', 'Unknown')}")
                print(f"   Recipe keys: {list(data['recipes'][0].keys())[:5]}")
        
        # Test 3: Our backend suggest endpoint
        print("\n3. Testing our backend /api/recipes/suggest...")
        response = await client.post(
            "http://localhost:8000/api/recipes/suggest",
            json={
                "available_ingredients": ["chicken", "rice"],
                "max_recipes": 3
            }
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            recipes = response.json()
            print(f"   Returned {len(recipes)} recipes")
            if recipes:
                print(f"   First recipe: {recipes[0].get('name', 'Unknown')}")
        elif response.status_code == 422:
            print(f"   Validation error: {response.json()}")
        else:
            print(f"   Error: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_full_flow())
