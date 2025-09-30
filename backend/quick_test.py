import httpx
import asyncio
import json

async def quick_test():
    try:
        # Test health endpoint
        async with httpx.AsyncClient(timeout=5.0) as client:
            print("Testing health endpoint...")
            response = await client.get("http://localhost:8000/api/health")
            print(f"Health status: {response.status_code}")
            
            print("\nTesting recipe search...")
            response = await client.get(
                "http://localhost:8000/api/recipes/search",
                params={"query": "chicken", "limit": 3}
            )
            print(f"Search status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Response keys: {list(data.keys())}")
                recipes = data.get('recipes', [])
                print(f"Found {len(recipes)} recipes")
                if recipes:
                    print(f"First recipe: {recipes[0].get('name', 'Unknown')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(quick_test())
