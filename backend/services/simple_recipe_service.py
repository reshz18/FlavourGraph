"""
Simplified Recipe Service - Direct API calls without complex algorithms
This ensures recipes are actually returned to users
"""

import os
import httpx
import asyncio
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class SimpleRecipeService:
    """Simple, working recipe service using free APIs"""
    
    def __init__(self):
        self.themealdb_base = "https://www.themealdb.com/api/json/v1/1"
        self.spoonacular_key = os.getenv("SPOONACULAR_API_KEY", "")
    
    async def search_by_ingredients(self, ingredients: List[str], limit: int = 10) -> List[Dict]:
        """Search recipes by ingredients"""
        recipes = []
        
        # Try searching for each main ingredient
        async with httpx.AsyncClient(timeout=10.0) as client:
            for ingredient in ingredients[:3]:  # Use first 3 ingredients
                try:
                    # Search by ingredient in TheMealDB
                    response = await client.get(
                        f"{self.themealdb_base}/filter.php",
                        params={"i": ingredient.strip()}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        meals = data.get("meals", [])
                        
                        # Get detailed info for each meal
                        for meal in meals[:5]:  # Limit per ingredient
                            detail_response = await client.get(
                                f"{self.themealdb_base}/lookup.php",
                                params={"i": meal["idMeal"]}
                            )
                            if detail_response.status_code == 200:
                                detail_data = detail_response.json()
                                if detail_data.get("meals"):
                                    recipe = self._format_recipe(detail_data["meals"][0])
                                    if recipe not in recipes:
                                        recipes.append(recipe)
                except Exception as e:
                    logger.error(f"Error searching for {ingredient}: {e}")
        
        return recipes[:limit]
    
    async def search_by_name(self, query: str, limit: int = 10) -> List[Dict]:
        """Search recipes by name"""
        recipes = []
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                # Search by name in TheMealDB
                response = await client.get(
                    f"{self.themealdb_base}/search.php",
                    params={"s": query}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    meals = data.get("meals", [])
                    
                    for meal in meals[:limit]:
                        recipe = self._format_recipe(meal)
                        recipes.append(recipe)
            except Exception as e:
                logger.error(f"Error searching for {query}: {e}")
        
        # If no results, try partial match
        if not recipes and len(query) > 2:
            try:
                # Search by first letter as fallback
                response = await client.get(
                    f"{self.themealdb_base}/search.php",
                    params={"f": query[0]}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    meals = data.get("meals", [])
                    
                    # Filter by query
                    for meal in meals:
                        if query.lower() in meal.get("strMeal", "").lower():
                            recipe = self._format_recipe(meal)
                            recipes.append(recipe)
                            if len(recipes) >= limit:
                                break
            except:
                pass
        
        return recipes[:limit]
    
    async def get_random_recipes(self, count: int = 5) -> List[Dict]:
        """Get random recipes"""
        recipes = []
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            for _ in range(count):
                try:
                    response = await client.get(f"{self.themealdb_base}/random.php")
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("meals"):
                            recipe = self._format_recipe(data["meals"][0])
                            recipes.append(recipe)
                except:
                    pass
        
        return recipes
    
    def _format_recipe(self, meal: Dict) -> Dict:
        """Format TheMealDB recipe to our standard format"""
        
        # Extract ingredients
        ingredients = []
        for i in range(1, 21):
            ingredient = meal.get(f"strIngredient{i}", "").strip()
            measure = meal.get(f"strMeasure{i}", "").strip()
            if ingredient:
                ingredients.append({
                    "name": ingredient,
                    "quantity": 1,
                    "unit": measure
                })
        
        # Parse instructions
        instructions = []
        if meal.get("strInstructions"):
            raw_instructions = meal["strInstructions"].replace("\r\n", "\n")
            sentences = [s.strip() for s in raw_instructions.split("\n") if s.strip()]
            instructions = sentences[:10]  # Limit instructions
        
        return {
            "id": meal.get("idMeal", ""),
            "name": meal.get("strMeal", "Unknown Recipe"),
            "description": f"{meal.get('strCategory', 'Recipe')} from {meal.get('strArea', 'International')} cuisine",
            "ingredients": ingredients,
            "instructions": instructions,
            "prep_time": 15,
            "cook_time": 30,
            "servings": 4,
            "cuisine": meal.get("strArea", "International").lower(),
            "difficulty": "medium",
            "image_url": meal.get("strMealThumb", ""),
            "tags": [meal.get("strCategory", "").lower()] if meal.get("strCategory") else [],
            "source_url": meal.get("strSource", ""),
            "video_url": meal.get("strYoutube", "")
        }
