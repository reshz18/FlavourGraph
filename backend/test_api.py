import httpx
import json
import asyncio

async def test_endpoints():
    async with httpx.AsyncClient() as client:
        # Test health endpoint
        print("1. Testing health endpoint...")
        response = await client.get("http://localhost:8000/api/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test recipe search with query
        print("\n2. Testing recipe search with query...")
        response = await client.get("http://localhost:8000/api/recipes/search?query=chicken&limit=5")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Found {data.get('total', 0)} recipes")
        if data.get("recipes"):
            print(f"   Sample: {data['recipes'][0].get('name', 'Unknown')}")
        
        # Test recipe suggestion with ingredients
        print("\n3. Testing recipe suggestion with ingredients...")
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
            print(f"   Found {len(recipes)} recipes")
            if recipes:
                print(f"   Sample: {recipes[0].get('name', 'Unknown')}")

if __name__ == "__main__":
    print("Testing FlavorGraph API endpoints...")
    print("=" * 50)
    asyncio.run(test_endpoints())
