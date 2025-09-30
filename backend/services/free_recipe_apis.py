"""
Free Recipe API Integration Service
Provides multiple free recipe API options as alternatives to Spoonacular
"""

import os
import httpx
import json
from typing import List, Dict, Optional, Any
from utils.logger import logger

class FreeRecipeAPIs:
    """
    Integration with free recipe APIs that don't require API keys or have generous free tiers
    """
    
    def __init__(self):
        self.apis = {
            "themealdb": {
                "base_url": "https://www.themealdb.com/api/json/v1/1",
                "enabled": True,
                "description": "Free recipe API with 600+ recipes"
            },
            "recipepuppy": {
                "base_url": "http://www.recipepuppy.com/api",
                "enabled": False,  # Often down
                "description": "Simple recipe search API"
            }
        }
        
    async def search_themealdb(self, ingredients: List[str] = None, query: str = "") -> List[Dict]:
        """
        Search TheMealDB API (completely free, no key required)
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                recipes = []
                
                # Search by main ingredient if provided
                if ingredients and len(ingredients) > 0:
                    # Clean the ingredient name
                    main_ingredient = ingredients[0].strip() if hasattr(ingredients[0], 'strip') else str(ingredients[0])
                    response = await client.get(
                        f"{self.apis['themealdb']['base_url']}/filter.php",
                        params={"i": main_ingredient}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        meals = data.get("meals", [])[:10]  # Limit to 10
                        
                        # Get detailed info for each meal
                        for meal in meals:
                            detail_response = await client.get(
                                f"{self.apis['themealdb']['base_url']}/lookup.php",
                                params={"i": meal["idMeal"]}
                            )
                            if detail_response.status_code == 200:
                                detail_data = detail_response.json()
                                if detail_data.get("meals"):
                                    recipes.append(self._format_themealdb_recipe(detail_data["meals"][0]))
                
                # If query provided, search by name
                elif query:
                    response = await client.get(
                        f"{self.apis['themealdb']['base_url']}/search.php",
                        params={"s": query}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        meals = data.get("meals", [])
                        for meal in meals[:10]:
                            recipes.append(self._format_themealdb_recipe(meal))
                
                # Random recipes if no specific search
                else:
                    for _ in range(5):
                        response = await client.get(
                            f"{self.apis['themealdb']['base_url']}/random.php"
                        )
                        if response.status_code == 200:
                            data = response.json()
                            if data.get("meals"):
                                recipes.append(self._format_themealdb_recipe(data["meals"][0]))
                
                logger.info(f"TheMealDB returned {len(recipes)} recipes")
                return recipes
                
        except Exception as e:
            logger.error(f"Error searching TheMealDB: {e}")
            return []
    
    def _format_themealdb_recipe(self, meal: Dict) -> Dict:
        """Format TheMealDB response to our standard format"""
        
        # Extract ingredients and measurements
        ingredients = []
        for i in range(1, 21):
            ingredient = meal.get(f"strIngredient{i}", "").strip()
            measure = meal.get(f"strMeasure{i}", "").strip()
            if ingredient:
                ingredients.append({
                    "name": ingredient.lower(),
                    "quantity": 1,
                    "unit": measure if measure else ""
                })
        
        # Parse instructions
        instructions = []
        if meal.get("strInstructions"):
            # Split by sentences or newlines
            raw_instructions = meal["strInstructions"]
            sentences = raw_instructions.replace("\r\n", "\n").split("\n")
            instructions = [s.strip() for s in sentences if s.strip()]
            if len(instructions) == 1:
                # If it's one long paragraph, split by periods
                instructions = [s.strip() + "." for s in instructions[0].split(".") if s.strip()]
        
        return {
            "id": meal.get("idMeal", ""),
            "name": meal.get("strMeal", "Unknown Recipe"),
            "description": f"{meal.get('strCategory', 'Recipe')} from {meal.get('strArea', 'International')} cuisine",
            "ingredients": ingredients,
            "instructions": instructions[:10],  # Limit instructions
            "prep_time": 15,  # Default estimates
            "cook_time": 30,
            "servings": 4,
            "cuisine": meal.get("strArea", "International").lower(),
            "difficulty": "medium",
            "image_url": meal.get("strMealThumb", ""),
            "source_url": meal.get("strSource", ""),
            "tags": [meal.get("strCategory", "").lower()] if meal.get("strCategory") else [],
            "category": meal.get("strCategory", ""),
            "video_url": meal.get("strYoutube", "")
        }
    
    async def search_edamam_free(self, ingredients: List[str] = None, query: str = "") -> List[Dict]:
        """
        Search Edamam Recipe API (free tier: 10,000 requests/month)
        Requires free registration at https://developer.edamam.com/
        """
        app_id = os.getenv("EDAMAM_APP_ID")
        app_key = os.getenv("EDAMAM_APP_KEY")
        
        if not app_id or not app_key:
            logger.info("Edamam credentials not configured, skipping")
            return []
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                params = {
                    "type": "public",
                    "app_id": app_id,
                    "app_key": app_key,
                    "to": 10  # Limit results
                }
                
                if query:
                    params["q"] = query
                elif ingredients:
                    params["q"] = " ".join(ingredients)
                else:
                    params["q"] = "recipe"  # Generic search
                
                response = await client.get(
                    "https://api.edamam.com/api/recipes/v2",
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    hits = data.get("hits", [])
                    recipes = []
                    
                    for hit in hits:
                        recipe = hit.get("recipe", {})
                        recipes.append({
                            "id": recipe.get("uri", "").split("#")[-1],
                            "name": recipe.get("label", ""),
                            "description": f"Calories: {recipe.get('calories', 0):.0f}, Servings: {recipe.get('yield', 1)}",
                            "ingredients": [
                                {"name": ing.get("food", "").lower(), "quantity": ing.get("quantity", 1), "unit": ing.get("measure", "")}
                                for ing in recipe.get("ingredients", [])
                            ],
                            "instructions": [],  # Edamam doesn't provide instructions
                            "prep_time": recipe.get("totalTime", 30) // 2,
                            "cook_time": recipe.get("totalTime", 30) // 2,
                            "servings": recipe.get("yield", 1),
                            "cuisine": recipe.get("cuisineType", ["international"])[0] if recipe.get("cuisineType") else "international",
                            "difficulty": "medium",
                            "image_url": recipe.get("image", ""),
                            "source_url": recipe.get("url", ""),
                            "tags": recipe.get("dietLabels", []) + recipe.get("healthLabels", [])
                        })
                    
                    return recipes
                    
        except Exception as e:
            logger.error(f"Error searching Edamam: {e}")
            return []
    
    async def get_recipes(self, ingredients: List[str] = None, query: str = "", limit: int = 20) -> List[Dict]:
        """
        Get recipes from all available free APIs
        """
        all_recipes = []
        
        # Try TheMealDB first (completely free)
        themealdb_recipes = await self.search_themealdb(ingredients, query)
        all_recipes.extend(themealdb_recipes)
        
        # If not enough recipes, try other APIs
        if len(all_recipes) < limit:
            edamam_recipes = await self.search_edamam_free(ingredients, query)
            all_recipes.extend(edamam_recipes)
        
        # Remove duplicates by name
        seen_names = set()
        unique_recipes = []
        for recipe in all_recipes:
            if recipe["name"].lower() not in seen_names:
                seen_names.add(recipe["name"].lower())
                unique_recipes.append(recipe)
        
        return unique_recipes[:limit]
