import asyncio
from services.free_recipe_apis import FreeRecipeAPIs
from services.recipe_service import RecipeService

async def debug():
    # Test FreeRecipeAPIs directly
    print("1. Testing FreeRecipeAPIs directly...")
    api = FreeRecipeAPIs()
    
    # Test search
    recipes = await api.search_themealdb(ingredients=["chicken"])
    print(f"   Direct API returned {len(recipes)} recipes")
    if recipes:
        print(f"   First recipe: {recipes[0]['name']}")
        print(f"   Ingredients: {[ing['name'] for ing in recipes[0]['ingredients'][:3]]}")
    
    # Test get_recipes
    print("\n2. Testing get_recipes method...")
    recipes2 = await api.get_recipes(ingredients=["chicken"], limit=5)
    print(f"   get_recipes returned {len(recipes2)} recipes")
    
    # Test RecipeService
    print("\n3. Testing RecipeService...")
    service = RecipeService()
    await service.initialize()
    
    # Test search with algorithms
    recipes3 = await service.search_recipes_with_algorithms(
        available_ingredients=["chicken", "rice"],
        limit=5
    )
    print(f"   RecipeService returned {len(recipes3)} recipes")
    if recipes3:
        print(f"   First recipe: {recipes3[0].get('name', 'Unknown')}")
    
    # Test without algorithms
    print("\n4. Testing direct search without algorithms...")
    recipes4 = await service.search_recipes(query="chicken", limit=5)
    print(f"   Direct search returned {len(recipes4)} recipes")

if __name__ == "__main__":
    asyncio.run(debug())
