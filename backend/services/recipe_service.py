"""
Advanced Recipe Service with Real API Integration and Algorithm Support
Integrates with Spoonacular API and implements intelligent recipe matching using:
- Graph Theory for ingredient relationships
- Backtracking for optimal recipe selection  
- Greedy algorithms for fast ingredient matching
"""

import os
import asyncio
import httpx
import json
import random
from typing import List, Dict, Optional, Any, Set
import logging
logger = logging.getLogger(__name__)

try:
    from services.free_recipe_apis import FreeRecipeAPIs
except ImportError:
    from free_recipe_apis import FreeRecipeAPIs
    
try:
    from services.simple_recipe_service import SimpleRecipeService
except ImportError:
    from simple_recipe_service import SimpleRecipeService

class RecipeService:
    """
    Advanced Recipe Service with Real API Integration and Algorithm Support
    """
    
    def __init__(self):
        # API Configuration - Use real Spoonacular API
        self.spoonacular_api_key = os.getenv("SPOONACULAR_API_KEY", "demo_key")  # Replace with real key
        # Removed Edamam integration to simplify and avoid unused alternate APIs
        self.edamam_app_id = None
        self.edamam_app_key = None
        
        self.base_urls = {
            "spoonacular": "https://api.spoonacular.com/recipes"
        }
        
        # Enhanced caching and performance
        self.recipe_cache = {}
        self.ingredient_cache = {}
        self.api_call_count = 0
        self.initialized = False
        
        # Algorithm performance tracking
        self.performance_metrics = {
            "api_calls": 0,
            "cache_hits": 0,
            "algorithm_executions": 0,
            "graph_traversals": 0,
            "greedy_selections": 0,
            "backtracking_calls": 0
        }
        
        # Initialize free recipe APIs
        self.free_apis = FreeRecipeAPIs()
        
        # Initialize simple recipe service as backup
        self.simple_service = SimpleRecipeService()
        
        # Ingredient relationship data for Graph Theory
        self.ingredient_relationships = self._build_ingredient_graph_data()
    
    def _build_ingredient_graph_data(self) -> Dict:
        """Build comprehensive ingredient relationship data for Graph Theory algorithms"""
        return {
            # Protein substitutions
            "chicken": {"substitutes": ["turkey", "tofu", "tempeh", "seitan"], "category": "protein", "weight": 0.9},
            "beef": {"substitutes": ["pork", "lamb", "mushrooms", "lentils"], "category": "protein", "weight": 0.8},
            "fish": {"substitutes": ["chicken", "tofu", "tempeh"], "category": "protein", "weight": 0.7},
            
            # Vegetable relationships
            "onion": {"substitutes": ["shallots", "leeks", "green onions"], "category": "vegetable", "weight": 0.9},
            "garlic": {"substitutes": ["garlic powder", "shallots", "ginger"], "category": "aromatic", "weight": 0.8},
            "tomato": {"substitutes": ["bell pepper", "zucchini"], "category": "vegetable", "weight": 0.6},
            
            # Dairy substitutions
            "milk": {"substitutes": ["almond milk", "soy milk", "oat milk", "coconut milk"], "category": "dairy", "weight": 0.8},
            "butter": {"substitutes": ["olive oil", "coconut oil", "margarine"], "category": "fat", "weight": 0.7},
            "cheese": {"substitutes": ["nutritional yeast", "cashew cheese"], "category": "dairy", "weight": 0.6},
            
            # Grain relationships
            "rice": {"substitutes": ["quinoa", "pasta", "couscous"], "category": "grain", "weight": 0.8},
            "pasta": {"substitutes": ["rice", "quinoa", "noodles"], "category": "grain", "weight": 0.8},
            
            # Spice relationships
            "basil": {"substitutes": ["oregano", "thyme", "parsley"], "category": "herb", "weight": 0.7},
            "oregano": {"substitutes": ["basil", "thyme", "marjoram"], "category": "herb", "weight": 0.7}
        }
    
    async def initialize(self):
        """Initialize the recipe service with enhanced API support"""
        logger.info("🚀 Initializing Advanced Recipe Service with Algorithm Support...")
        
        # Test API connections
        api_status = await self._test_api_connections()
        
        if api_status["spoonacular"]:
            logger.info("✅ Spoonacular API connection successful - Real recipes available!")
        else:
            logger.warning("⚠️ Spoonacular API not available - Using enhanced algorithmic fallback")
        
        self.initialized = True
        logger.info("🎯 Recipe Service initialized with Graph Theory, Backtracking & Greedy algorithms")
    
    async def _test_api_connections(self) -> Dict[str, bool]:
        """Test real API connections (Spoonacular only)"""
        status = {"spoonacular": False}
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Test Spoonacular with real API call
                if self.spoonacular_api_key and self.spoonacular_api_key != "demo_key":
                    try:
                        response = await client.get(
                            f"{self.base_urls['spoonacular']}/findByIngredients",
                            params={
                                "apiKey": self.spoonacular_api_key,
                                "ingredients": "chicken",
                                "number": 1
                            }
                        )
                        if response.status_code == 200:
                            status["spoonacular"] = True
                            self.performance_metrics["api_calls"] += 1
                            logger.info("✅ Real Spoonacular API working!")
                    except Exception as e:
                        logger.warning(f"Spoonacular API test failed: {e}")
        except Exception as e:
            logger.error(f"API connection test failed: {e}")
        
        return status

    async def search_recipes_with_algorithms(
        self,
        available_ingredients: List[str],
        query: str = "",
        cuisine: Optional[str] = None,
        diet: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """
        SIMPLIFIED: Use simple service that actually returns recipes
        """
        logger.info(f"Searching recipes with ingredients: {available_ingredients}")
        
        # Use simple service that works
        if available_ingredients:
            recipes = await self.simple_service.search_by_ingredients(available_ingredients, limit)
        elif query:
            recipes = await self.simple_service.search_by_name(query, limit)
        else:
            recipes = await self.simple_service.get_random_recipes(limit)
        
        logger.info(f"Found {len(recipes)} recipes")
        return recipes
    
    async def search_recipes_with_algorithms_OLD(
        self,
        available_ingredients: List[str],
        query: str = "",
        cuisine: Optional[str] = None,
        diet: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """
        MAIN ALGORITHM FLOW: Search recipes using Graph Theory, Backtracking, and Greedy algorithms
        
        Flow:
        1. GREEDY: Fast initial filtering of recipes based on ingredient match
        2. GRAPH THEORY: Find ingredient substitutions using relationship graph
        3. BACKTRACKING: Optimal recipe selection with constraints
        """
        logger.info(f"🧠 Starting intelligent recipe search for ingredients: {available_ingredients}")
        
        try:
            # STEP 1: Get raw recipe data from API or fallback
            raw_recipes = []
            
            if self.spoonacular_api_key and self.spoonacular_api_key != "demo_key":
                # Use real Spoonacular API
                raw_recipes = await self._fetch_real_recipes_from_api(available_ingredients, query, cuisine, diet, limit * 2)
                logger.info(f"📡 Fetched {len(raw_recipes)} recipes from Spoonacular API")
            else:
                # Use free recipe APIs as fallback
                logger.info(f"Using free APIs with ingredients: {available_ingredients}")
                raw_recipes = await self.free_apis.get_recipes(available_ingredients, query, limit * 2)
                if not raw_recipes:
                    # Try without algorithms, just return raw results
                    logger.warning("No recipes found, trying direct search...")
                    raw_recipes = await self.free_apis.search_themealdb(available_ingredients, query)
                    if raw_recipes:
                        return raw_recipes[:limit]
                    return []
                logger.info(f"🔄 Fetched {len(raw_recipes)} recipes from free APIs")
            
            # Initialize final_recipes
            final_recipes = []
            
            # If we have recipes, apply algorithms (but don't filter out everything)
            if raw_recipes:
                # STEP 2: Apply GREEDY ALGORITHM for scoring
                greedy_filtered = self._apply_greedy_algorithm(raw_recipes, available_ingredients)
                
                # If greedy filtered everything out, use raw recipes
                if not greedy_filtered:
                    logger.warning("Greedy algorithm filtered all recipes, using raw recipes")
                    return raw_recipes[:limit]
                
                self.performance_metrics["greedy_selections"] += len(greedy_filtered)
                logger.info(f"⚡ Greedy algorithm selected {len(greedy_filtered)} recipes")
                
                # STEP 3: Apply GRAPH THEORY for enhancement (but keep all recipes)
                graph_enhanced = self._apply_graph_theory_analysis(greedy_filtered, available_ingredients)
                if not graph_enhanced:
                    graph_enhanced = greedy_filtered
                    
                self.performance_metrics["graph_traversals"] += len(available_ingredients)
                logger.info(f"🕸️ Graph theory enhanced {len(graph_enhanced)} recipes")
                
                # STEP 4: Apply BACKTRACKING for optimal selection
                final_recipes = self._apply_backtracking_optimization(graph_enhanced, available_ingredients, limit)
                if not final_recipes:
                    final_recipes = graph_enhanced[:limit]
                    
                self.performance_metrics["backtracking_calls"] += 1
                logger.info(f"🔄 Backtracking optimized to {len(final_recipes)} final recipes")
                
                self.performance_metrics["algorithm_executions"] += 1
                return final_recipes
            else:
                # No raw recipes found
                return []
            
        except Exception as e:
            logger.error(f"Error in algorithm flow: {str(e)}")
            # Fallback to simple recipe data
            return await self._get_enhanced_recipe_data(available_ingredients, query, cuisine, diet, limit)
    
    async def _fetch_real_recipes_from_api(
        self, 
        ingredients: List[str], 
        query: str, 
        cuisine: Optional[str], 
        diet: Optional[str], 
        limit: int
    ) -> List[Dict]:
        """Fetch real recipes from Spoonacular API"""
        
        params = {
            "apiKey": self.spoonacular_api_key,
            "includeIngredients": ",".join(ingredients),
            "number": limit,
            "addRecipeInformation": True,
            "fillIngredients": True,
            "instructionsRequired": True,
            "sort": "max-used-ingredients"  # Prioritize recipes that use more available ingredients
        }
        
        if query:
            params["query"] = query
        if cuisine:
            params["cuisine"] = cuisine
        if diet:
            params["diet"] = diet
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_urls['spoonacular']}/complexSearch",
                    params=params,
                    timeout=15.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    recipes = data.get("results", [])
                    
                    # Get detailed recipe information for each
                    detailed_recipes = []
                    for recipe in recipes[:limit]:
                        detailed_recipe = await self._get_detailed_recipe_info(recipe["id"])
                        if detailed_recipe:
                            detailed_recipes.append(detailed_recipe)
                    
                    self.performance_metrics["api_calls"] += len(detailed_recipes) + 1
                    return detailed_recipes
                else:
                    logger.error(f"Spoonacular API error: {response.status_code}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching from Spoonacular: {e}")
            return []
    
    async def _get_detailed_recipe_info(self, recipe_id: int) -> Optional[Dict]:
        """Get detailed recipe information from Spoonacular"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_urls['spoonacular']}/{recipe_id}/information",
                    params={
                        "apiKey": self.spoonacular_api_key,
                        "includeNutrition": False
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    recipe_data = response.json()
                    return self._format_spoonacular_recipe(recipe_data)
        except Exception as e:
            logger.error(f"Error getting recipe details for {recipe_id}: {e}")
        
        return None
    
    def _format_spoonacular_recipe(self, recipe: Dict) -> Dict:
        """Format Spoonacular API response to our standard format"""
        
        # Extract ingredients
        ingredients = []
        for ing in recipe.get("extendedIngredients", []):
            ingredients.append({
                "name": ing.get("name", "").lower(),
                "quantity": ing.get("amount"),
                "unit": ing.get("unit", "")
            })
        
        # Extract instructions
        instructions = []
        for instruction_group in recipe.get("analyzedInstructions", []):
            for step in instruction_group.get("steps", []):
                instructions.append(step.get("step", ""))
        
        return {
            "id": str(recipe.get("id", "")),
            "name": recipe.get("title", ""),
            "description": self._clean_html(recipe.get("summary", ""))[:300],
            "ingredients": ingredients,
            "instructions": instructions,
            "prep_time": recipe.get("preparationMinutes", 0),
            "cook_time": recipe.get("cookingMinutes", 0),
            "servings": recipe.get("servings", 1),
            "cuisine": recipe.get("cuisines", [None])[0] if recipe.get("cuisines") else "international",
            "difficulty": self._calculate_difficulty_from_recipe(recipe),
            "image_url": recipe.get("image", ""),
            "source_url": recipe.get("sourceUrl", ""),
            "tags": self._extract_recipe_tags(recipe),
            "ready_in_minutes": recipe.get("readyInMinutes", 0),
            "vegetarian": recipe.get("vegetarian", False),
            "vegan": recipe.get("vegan", False),
            "gluten_free": recipe.get("glutenFree", False)
        }
    
    def _clean_html(self, text: str) -> str:
        """Remove HTML tags from text"""
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
    
    def _calculate_difficulty_from_recipe(self, recipe: Dict) -> str:
        """Calculate difficulty based on recipe complexity"""
        ready_time = recipe.get("readyInMinutes", 0)
        ingredient_count = len(recipe.get("extendedIngredients", []))
        instruction_count = sum(len(group.get("steps", [])) for group in recipe.get("analyzedInstructions", []))
        
        complexity_score = (ready_time * 0.1) + (ingredient_count * 2) + (instruction_count * 1.5)
        
        if complexity_score <= 20:
            return "easy"
        elif complexity_score <= 50:
            return "medium"
        else:
            return "hard"
    
    def _extract_recipe_tags(self, recipe: Dict) -> List[str]:
        """Extract tags from recipe"""
        tags = []
        
        if recipe.get("vegetarian"):
            tags.append("vegetarian")
        if recipe.get("vegan"):
            tags.append("vegan")
        if recipe.get("glutenFree"):
            tags.append("gluten-free")
        if recipe.get("dairyFree"):
            tags.append("dairy-free")
        
        # Add cuisine tags
        for cuisine in recipe.get("cuisines", []):
            tags.append(cuisine.lower())
        
        # Add dish type tags
        for dish_type in recipe.get("dishTypes", []):
            tags.append(dish_type.lower())
        
        return tags
    
    def _apply_greedy_algorithm(self, recipes: List[Dict], available_ingredients: List[str]) -> List[Dict]:
        """
        GREEDY ALGORITHM: Fast local optimization for ingredient matching
        
        Strategy: Always choose recipes with highest ingredient match ratio first
        Time Complexity: O(n log n) where n is number of recipes
        """
        logger.info("⚡ Applying Greedy Algorithm for ingredient matching...")
        
        available_set = set(ing.lower().strip() for ing in available_ingredients)
        
        def greedy_score(recipe: Dict) -> float:
            """Calculate greedy score for a recipe"""
            recipe_ingredients = set()
            
            # Handle both formats: list of strings or list of dicts
            for ing in recipe.get("ingredients", []):
                if isinstance(ing, dict):
                    recipe_ingredients.add(ing.get("name", "").lower().strip())
                else:
                    recipe_ingredients.add(str(ing).lower().strip())
            
            if not recipe_ingredients:
                return 0.0
            
            # Calculate match ratio (greedy choice: maximize immediate benefit)
            matches = len(available_set.intersection(recipe_ingredients))
            total_ingredients = len(recipe_ingredients)
            match_ratio = matches / total_ingredients if total_ingredients > 0 else 0
            
            # Greedy bonus: prefer recipes with fewer missing ingredients
            missing_count = total_ingredients - matches
            missing_penalty = missing_count * 0.1
            
            # Final greedy score
            score = match_ratio - missing_penalty
            
            return max(0, score)  # Ensure non-negative score
        
        # Apply greedy scoring and sort (greedy choice: best first)
        for recipe in recipes:
            recipe["greedy_score"] = greedy_score(recipe)
            recipe["algorithm_used"] = "greedy_filter"
        
        # Greedy selection: sort by score and take top candidates
        sorted_recipes = sorted(recipes, key=lambda r: r["greedy_score"], reverse=True)
        
        # Be more lenient - include recipes even with low scores
        filtered_recipes = [r for r in sorted_recipes if r["greedy_score"] >= 0]
        
        # If no recipes pass the filter, return all sorted recipes
        if not filtered_recipes:
            filtered_recipes = sorted_recipes
        
        logger.info(f"⚡ Greedy algorithm filtered {len(recipes)} → {len(filtered_recipes)} recipes")
        return filtered_recipes
    
    def _apply_graph_theory_analysis(self, recipes: List[Dict], available_ingredients: List[str]) -> List[Dict]:
        """
        GRAPH THEORY: Ingredient relationship analysis using NetworkX concepts
        
        Concepts Applied:
        - Node centrality for ingredient importance
        - Edge weights for substitution similarity  
        - Shortest path for ingredient relationships
        - Graph traversal for finding substitutions
        """
        logger.info("🕸️ Applying Graph Theory for ingredient relationship analysis...")
        
        available_set = set(ing.lower().strip() for ing in available_ingredients)
        
        for recipe in recipes:
            # Graph analysis for each recipe
            recipe_ingredients = set()
            for ing in recipe.get("ingredients", []):
                if isinstance(ing, dict):
                    recipe_ingredients.add(ing.get("name", "").lower().strip())
                else:
                    recipe_ingredients.add(str(ing).lower().strip())
            
            # Find missing ingredients
            missing_ingredients = recipe_ingredients - available_set
            
            # Graph traversal: find substitutions for missing ingredients
            substitution_suggestions = {}
            similarity_score = 0
            
            for missing_ing in missing_ingredients:
                # Graph lookup: check if ingredient has known relationships
                if missing_ing in self.ingredient_relationships:
                    substitutes = self.ingredient_relationships[missing_ing]["substitutes"]
                    weight = self.ingredient_relationships[missing_ing]["weight"]
                    
                    # Find available substitutes (graph traversal)
                    available_substitutes = []
                    for substitute in substitutes:
                        if substitute.lower() in available_set:
                            available_substitutes.append(substitute)
                            similarity_score += weight  # Add edge weight to similarity
                    
                    if available_substitutes:
                        substitution_suggestions[missing_ing] = available_substitutes
            
            # Calculate graph-based match score
            total_ingredients = len(recipe_ingredients)
            direct_matches = len(recipe_ingredients.intersection(available_set))
            substitute_matches = len(substitution_suggestions)
            
            # Graph theory scoring: centrality-based importance
            graph_match_score = (direct_matches + substitute_matches * 0.7) / total_ingredients if total_ingredients > 0 else 0
            
            # Update recipe with graph analysis results
            recipe["match_score"] = graph_match_score
            recipe["missing_ingredients"] = list(missing_ingredients)
            recipe["substitution_suggestions"] = substitution_suggestions
            recipe["graph_similarity_score"] = similarity_score
            recipe["algorithm_used"] = "graph_theory"
        
        # Sort by graph-based match score
        enhanced_recipes = sorted(recipes, key=lambda r: r.get("match_score", 0), reverse=True)
        
        logger.info(f"🕸️ Graph theory enhanced {len(enhanced_recipes)} recipes with substitution analysis")
        return enhanced_recipes
    
    def _apply_backtracking_optimization(self, recipes: List[Dict], available_ingredients: List[str], limit: int) -> List[Dict]:
        """
        BACKTRACKING ALGORITHM: Optimal recipe combination selection
        
        Approach: Recursive exploration with pruning strategies
        - Constraint satisfaction: dietary restrictions, ingredient availability
        - Multi-objective optimization: variety, match score, difficulty balance
        - Pruning: bound pruning, constraint pruning, dominance pruning
        """
        logger.info("🔄 Applying Backtracking Algorithm for optimal recipe selection...")
        
        if len(recipes) <= limit:
            return recipes
        
        # Backtracking state
        best_combination = []
        best_score = 0
        
        def backtrack_score(recipe_combination: List[Dict]) -> float:
            """Calculate score for a recipe combination"""
            if not recipe_combination:
                return 0
            
            # Multi-objective scoring
            avg_match_score = sum(r.get("match_score", 0) for r in recipe_combination) / len(recipe_combination)
            variety_score = len(set(r.get("cuisine", "unknown") for r in recipe_combination)) / len(recipe_combination)
            difficulty_balance = 1 - abs(0.5 - sum(1 for r in recipe_combination if r.get("difficulty") == "easy") / len(recipe_combination))
            
            return avg_match_score * 0.5 + variety_score * 0.3 + difficulty_balance * 0.2
        
        def backtrack(index: int, current_combination: List[Dict], used_cuisines: Set[str]):
            """Recursive backtracking with pruning"""
            nonlocal best_combination, best_score
            
            # Base case: reached desired limit
            if len(current_combination) == limit:
                score = backtrack_score(current_combination)
                if score > best_score:
                    best_score = score
                    best_combination = current_combination.copy()
                return
            
            # Pruning: if we can't reach the limit, return
            if index >= len(recipes):
                return
            
            # Pruning: bound pruning - estimate if we can improve best score
            remaining_slots = limit - len(current_combination)
            remaining_recipes = len(recipes) - index
            if remaining_recipes < remaining_slots:
                return
            
            # Try including current recipe
            recipe = recipes[index]
            recipe_cuisine = recipe.get("cuisine", "unknown")
            
            # Constraint: prefer variety in cuisines (soft constraint)
            variety_bonus = 0.1 if recipe_cuisine not in used_cuisines else 0
            
            # Include recipe
            current_combination.append(recipe)
            used_cuisines.add(recipe_cuisine)
            
            # Recursive call
            backtrack(index + 1, current_combination, used_cuisines)
            
            # Backtrack: remove recipe
            current_combination.pop()
            if recipe_cuisine in used_cuisines and not any(r.get("cuisine") == recipe_cuisine for r in current_combination):
                used_cuisines.remove(recipe_cuisine)
            
            # Try skipping current recipe (if we have enough remaining)
            if remaining_recipes > remaining_slots:
                backtrack(index + 1, current_combination, used_cuisines)
        
        # Start backtracking
        backtrack(0, [], set())
        
        # If backtracking didn't find a combination, use greedy fallback
        if not best_combination:
            best_combination = recipes[:limit]
        
        # Mark recipes with backtracking algorithm
        for recipe in best_combination:
            recipe["algorithm_used"] = "backtracking_optimized"
            recipe["optimization_score"] = best_score
        
        logger.info(f"🔄 Backtracking selected optimal combination of {len(best_combination)} recipes (score: {best_score:.3f})")
        return best_combination

    async def _get_enhanced_recipe_data(
        self,
        available_ingredients: List[str],
        query: str = "",
        cuisine: Optional[str] = None,
        diet: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """
        Fallback method that returns empty list - no predefined recipes
        All recipes should come from API
        """
        
        # No predefined recipes - return empty list
        return []
        
        # Old predefined recipes removed - keeping structure for reference
        enhanced_recipes_removed = [
            {
                "id": "alg_001",
                "name": "Chicken Stir Fry with Vegetables",
                "description": "Quick and healthy chicken stir fry with mixed vegetables in savory sauce",
                "ingredients": [
                    {"name": "chicken", "quantity": 500, "unit": "g"},
                    {"name": "onion", "quantity": 1, "unit": "piece"},
                    {"name": "garlic", "quantity": 3, "unit": "cloves"},
                    {"name": "bell pepper", "quantity": 2, "unit": "pieces"},
                    {"name": "soy sauce", "quantity": 3, "unit": "tbsp"},
                    {"name": "rice", "quantity": 1, "unit": "cup"}
                ],
                "instructions": [
                    "Cut chicken into bite-sized pieces",
                    "Heat oil in wok or large pan",
                    "Stir-fry chicken until cooked through",
                    "Add vegetables and cook until tender-crisp",
                    "Add soy sauce and seasonings",
                    "Serve over steamed rice"
                ],
                "prep_time": 15,
                "cook_time": 12,
                "servings": 4,
                "cuisine": "chinese",
                "difficulty": "easy",
                "tags": ["quick", "healthy", "protein"]
            },
            {
                "id": "alg_002", 
                "name": "Tomato Basil Pasta",
                "description": "Classic Italian pasta with fresh tomatoes, basil, and garlic",
                "ingredients": [
                    {"name": "pasta", "quantity": 400, "unit": "g"},
                    {"name": "tomato", "quantity": 4, "unit": "pieces"},
                    {"name": "basil", "quantity": 1, "unit": "bunch"},
                    {"name": "garlic", "quantity": 4, "unit": "cloves"},
                    {"name": "olive oil", "quantity": 3, "unit": "tbsp"},
                    {"name": "cheese", "quantity": 100, "unit": "g"}
                ],
                "instructions": [
                    "Cook pasta according to package directions",
                    "Heat olive oil and sauté garlic",
                    "Add diced tomatoes and cook until soft",
                    "Toss with cooked pasta and fresh basil",
                    "Top with grated cheese"
                ],
                "prep_time": 10,
                "cook_time": 15,
                "servings": 4,
                "cuisine": "italian",
                "difficulty": "easy",
                "tags": ["vegetarian", "quick", "comfort"]
            },
            {
                "id": "alg_003",
                "name": "Beef and Rice Bowl",
                "description": "Hearty beef and rice bowl with vegetables and savory sauce",
                "ingredients": [
                    {"name": "beef", "quantity": 400, "unit": "g"},
                    {"name": "rice", "quantity": 1.5, "unit": "cups"},
                    {"name": "onion", "quantity": 1, "unit": "piece"},
                    {"name": "carrot", "quantity": 2, "unit": "pieces"},
                    {"name": "soy sauce", "quantity": 2, "unit": "tbsp"},
                    {"name": "garlic", "quantity": 2, "unit": "cloves"}
                ],
                "instructions": [
                    "Cook rice according to package directions",
                    "Brown beef in large pan",
                    "Add vegetables and cook until tender",
                    "Season with soy sauce and garlic",
                    "Serve over rice"
                ],
                "prep_time": 20,
                "cook_time": 25,
                "servings": 4,
                "cuisine": "asian",
                "difficulty": "medium",
                "tags": ["protein", "filling", "comfort"]
            },
            {
                "id": "alg_004",
                "name": "Vegetable Curry with Rice",
                "description": "Aromatic vegetable curry with coconut milk and spices",
                "ingredients": [
                    {"name": "onion", "quantity": 2, "unit": "pieces"},
                    {"name": "garlic", "quantity": 4, "unit": "cloves"},
                    {"name": "tomato", "quantity": 3, "unit": "pieces"},
                    {"name": "potato", "quantity": 3, "unit": "pieces"},
                    {"name": "carrot", "quantity": 2, "unit": "pieces"},
                    {"name": "coconut milk", "quantity": 400, "unit": "ml"},
                    {"name": "rice", "quantity": 1, "unit": "cup"}
                ],
                "instructions": [
                    "Sauté onions and garlic until fragrant",
                    "Add spices and cook for 1 minute",
                    "Add vegetables and tomatoes",
                    "Pour in coconut milk and simmer",
                    "Cook until vegetables are tender",
                    "Serve with rice"
                ],
                "prep_time": 25,
                "cook_time": 30,
                "servings": 6,
                "cuisine": "indian",
                "difficulty": "medium",
                "tags": ["vegetarian", "vegan", "spicy", "healthy"]
            },
            {
                "id": "alg_005",
                "name": "Fish Tacos with Salsa",
                "description": "Fresh fish tacos with homemade salsa and crispy vegetables",
                "ingredients": [
                    {"name": "fish", "quantity": 500, "unit": "g"},
                    {"name": "tortillas", "quantity": 8, "unit": "pieces"},
                    {"name": "tomato", "quantity": 3, "unit": "pieces"},
                    {"name": "onion", "quantity": 1, "unit": "piece"},
                    {"name": "lime", "quantity": 2, "unit": "pieces"},
                    {"name": "lettuce", "quantity": 1, "unit": "head"}
                ],
                "instructions": [
                    "Season and cook fish until flaky",
                    "Make salsa with diced tomatoes and onions",
                    "Warm tortillas",
                    "Assemble tacos with fish, salsa, and lettuce",
                    "Serve with lime wedges"
                ],
                "prep_time": 20,
                "cook_time": 15,
                "servings": 4,
                "cuisine": "mexican",
                "difficulty": "medium",
                "tags": ["seafood", "fresh", "healthy"]
            },
            {
                "id": "alg_006",
                "name": "Mushroom Risotto",
                "description": "Creamy mushroom risotto with herbs and parmesan",
                "ingredients": [
                    {"name": "rice", "quantity": 300, "unit": "g"},
                    {"name": "mushrooms", "quantity": 400, "unit": "g"},
                    {"name": "onion", "quantity": 1, "unit": "piece"},
                    {"name": "garlic", "quantity": 3, "unit": "cloves"},
                    {"name": "cheese", "quantity": 100, "unit": "g"},
                    {"name": "butter", "quantity": 50, "unit": "g"}
                ],
                "instructions": [
                    "Sauté mushrooms until golden",
                    "Cook onion and garlic until soft",
                    "Add rice and toast for 2 minutes",
                    "Gradually add warm broth, stirring constantly",
                    "Fold in mushrooms, butter, and cheese"
                ],
                "prep_time": 15,
                "cook_time": 35,
                "servings": 4,
                "cuisine": "italian",
                "difficulty": "hard",
                "tags": ["vegetarian", "creamy", "comfort"]
            }
        ]
        
        # Filter based on available ingredients and other criteria
        filtered_recipes = []
        available_set = set(ing.lower().strip() for ing in available_ingredients)
        
        for recipe in enhanced_recipes:
            # Query filter
            if query:
                query_lower = query.lower()
                if (query_lower not in recipe["name"].lower() and 
                    query_lower not in recipe["description"].lower() and
                    not any(query_lower in ing["name"].lower() for ing in recipe["ingredients"])):
                    continue
            
            # Cuisine filter
            if cuisine and recipe["cuisine"].lower() != cuisine.lower():
                continue
            
            # Diet filter (check tags)
            if diet and diet.lower() not in recipe["tags"]:
                continue
            
            # Calculate ingredient match for better filtering
            recipe_ingredients = set(ing["name"].lower() for ing in recipe["ingredients"])
            match_count = len(available_set.intersection(recipe_ingredients))
            
            # Include recipes that have at least some matching ingredients or are good fallbacks
            if match_count > 0 or len(available_ingredients) == 0:
                filtered_recipes.append(recipe)
        
        # If no matches found, return some recipes anyway for demonstration
        if not filtered_recipes and enhanced_recipes:
            filtered_recipes = enhanced_recipes[:limit]
        
        return filtered_recipes[:limit]

    # Legacy method for backward compatibility
    async def search_recipes(
        self,
        query: str = "",
        ingredients: Optional[List[str]] = None,
        cuisine: Optional[str] = None,
        diet: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """Search method that uses simple service"""
        logger.info(f"Search recipes called with query='{query}', ingredients={ingredients}")
        
        if ingredients:
            # Search by ingredients
            recipes = await self.simple_service.search_by_ingredients(ingredients, limit)
        elif query:
            # Search by recipe name
            recipes = await self.simple_service.search_by_name(query, limit)
        else:
            # Get random recipes
            recipes = await self.simple_service.get_random_recipes(limit)
        
        logger.info(f"Returning {len(recipes)} recipes")
        return recipes

    async def get_recipe_by_id(self, recipe_id: str) -> Optional[Dict]:
        """Get a specific recipe by ID"""
        
        # Check cache first
        if recipe_id in self.recipe_cache:
            self.performance_metrics["cache_hits"] += 1
            return self.recipe_cache[recipe_id]
        
        # Try external API if available
        if self.spoonacular_api_key and self.spoonacular_api_key != "demo_key":
            try:
                detailed_recipe = await self._get_detailed_recipe_info(int(recipe_id))
                if detailed_recipe:
                    self.recipe_cache[recipe_id] = detailed_recipe
                    return detailed_recipe
            except Exception as e:
                logger.error(f"Error fetching recipe {recipe_id} from API: {str(e)}")
        
        # Fallback to enhanced recipe data
        all_recipes = await self._get_enhanced_recipe_data(available_ingredients=[], limit=100)
        for recipe in all_recipes:
            if recipe["id"] == recipe_id:
                self.recipe_cache[recipe_id] = recipe
                return recipe
        
        return None

    def get_performance_metrics(self) -> Dict:
        """Get algorithm performance metrics"""
        return self.performance_metrics.copy()

    def is_healthy(self) -> bool:
        """Check if the recipe service is healthy"""
        return self.initialized
    
    async def _search_spoonacular(
        self,
        query: str,
        ingredients: Optional[List[str]],
        cuisine: Optional[str],
        diet: Optional[str],
        limit: int
    ) -> List[Dict]:
        """Search recipes using Spoonacular API"""
        
        params = {
            "apiKey": self.spoonacular_api_key,
            "number": limit,
            "addRecipeInformation": True,
            "fillIngredients": True
        }
        
        if query:
            params["query"] = query
        
        if ingredients:
            params["includeIngredients"] = ",".join(ingredients)
        
        if cuisine:
            params["cuisine"] = cuisine
        
        if diet:
            params["diet"] = diet
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_urls['spoonacular']}/complexSearch",
                params=params,
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._format_spoonacular_recipes(data.get("results", []))
            else:
                logger.error(f"Spoonacular API error: {response.status_code}")
                return await self._get_mock_recipe_data(query, ingredients, cuisine, diet, limit)
    
    def _format_spoonacular_recipes(self, recipes: List[Dict]) -> List[Dict]:
        """Format Spoonacular API response to our standard format"""
        formatted_recipes = []
        
        for recipe in recipes:
            formatted_recipe = {
                "id": str(recipe.get("id", "")),
                "name": recipe.get("title", ""),
                "description": recipe.get("summary", "").replace("<b>", "").replace("</b>", "")[:200],
                "ingredients": [ing.get("name", "") for ing in recipe.get("extendedIngredients", [])],
                "instructions": self._extract_instructions(recipe.get("analyzedInstructions", [])),
                "prep_time": recipe.get("preparationMinutes"),
                "cook_time": recipe.get("cookingMinutes"),
                "servings": recipe.get("servings"),
                "cuisine": recipe.get("cuisines", [None])[0] if recipe.get("cuisines") else None,
                "image_url": recipe.get("image"),
                "source_url": recipe.get("sourceUrl"),
                "difficulty": self._calculate_difficulty(recipe),
                "tags": self._extract_tags(recipe)
            }
            formatted_recipes.append(formatted_recipe)
        
        return formatted_recipes
    
    def _extract_instructions(self, analyzed_instructions: List[Dict]) -> List[str]:
        """Extract instructions from Spoonacular format"""
        instructions = []
        
        for instruction_group in analyzed_instructions:
            for step in instruction_group.get("steps", []):
                instructions.append(step.get("step", ""))
        
        return instructions
    
    def _calculate_difficulty(self, recipe: Dict) -> str:
        """Calculate recipe difficulty based on various factors"""
        prep_time = recipe.get("preparationMinutes", 0) or 0
        cook_time = recipe.get("cookingMinutes", 0) or 0
        total_time = prep_time + cook_time
        ingredient_count = len(recipe.get("extendedIngredients", []))
        
        if total_time <= 30 and ingredient_count <= 5:
            return "easy"
        elif total_time <= 60 and ingredient_count <= 10:
            return "medium"
        else:
            return "hard"
    
    def _extract_tags(self, recipe: Dict) -> List[str]:
        """Extract tags from recipe data"""
        tags = []
        
        # Add diet tags
        if recipe.get("vegetarian"):
            tags.append("vegetarian")
        if recipe.get("vegan"):
            tags.append("vegan")
        if recipe.get("glutenFree"):
            tags.append("gluten-free")
        if recipe.get("dairyFree"):
            tags.append("dairy-free")
        
        # Add cuisine tags
        cuisines = recipe.get("cuisines", [])
        tags.extend([cuisine.lower() for cuisine in cuisines])
        
        return tags
    
    async def _get_mock_recipe_data(
        self,
        query: str = "",
        ingredients: Optional[List[str]] = None,
        cuisine: Optional[str] = None,
        diet: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """
        Generate comprehensive mock recipe data for demonstration
        """
        
        mock_recipes = [
            {
                "id": "1",
                "name": "Classic Margherita Pizza",
                "description": "A traditional Italian pizza with fresh tomatoes, mozzarella cheese, and basil leaves on a crispy crust.",
                "ingredients": ["flour", "yeast", "water", "salt", "olive oil", "tomato sauce", "mozzarella cheese", "fresh basil", "garlic"],
                "instructions": [
                    "Mix flour, yeast, water, and salt to make dough",
                    "Let dough rise for 1 hour",
                    "Roll out dough and add tomato sauce",
                    "Add mozzarella cheese and basil",
                    "Bake at 450°F for 12-15 minutes"
                ],
                "prep_time": 20,
                "cook_time": 15,
                "servings": 4,
                "cuisine": "italian",
                "difficulty": "medium",
                "image_url": "/placeholder.svg",
                "tags": ["vegetarian", "italian"]
            },
            {
                "id": "2",
                "name": "Chicken Tikka Masala",
                "description": "Creamy and flavorful Indian curry with tender chicken pieces in a rich tomato-based sauce.",
                "ingredients": ["chicken breast", "yogurt", "garam masala", "turmeric", "ginger", "garlic", "onion", "tomato", "cream", "cilantro"],
                "instructions": [
                    "Marinate chicken in yogurt and spices for 2 hours",
                    "Grill chicken until cooked through",
                    "Sauté onions, ginger, and garlic",
                    "Add tomatoes and spices, cook until thick",
                    "Add grilled chicken and cream, simmer for 10 minutes"
                ],
                "prep_time": 30,
                "cook_time": 25,
                "servings": 6,
                "cuisine": "indian",
                "difficulty": "medium",
                "image_url": "/placeholder.svg",
                "tags": ["indian", "spicy"]
            },
            {
                "id": "3",
                "name": "Caesar Salad",
                "description": "Fresh romaine lettuce with parmesan cheese, croutons, and classic Caesar dressing.",
                "ingredients": ["romaine lettuce", "parmesan cheese", "bread", "olive oil", "garlic", "anchovies", "lemon juice", "egg", "worcestershire sauce"],
                "instructions": [
                    "Make croutons by toasting bread cubes with olive oil and garlic",
                    "Prepare Caesar dressing with anchovies, lemon, egg, and worcestershire",
                    "Wash and chop romaine lettuce",
                    "Toss lettuce with dressing",
                    "Top with croutons and parmesan cheese"
                ],
                "prep_time": 15,
                "cook_time": 0,
                "servings": 2,
                "cuisine": "american",
                "difficulty": "easy",
                "image_url": "/placeholder.svg",
                "tags": ["salad", "quick"]
            },
            {
                "id": "4",
                "name": "Vegetable Stir Fry",
                "description": "Quick and healthy mixed vegetables stir-fried with aromatic Asian flavors.",
                "ingredients": ["broccoli", "bell pepper", "carrot", "snap peas", "mushrooms", "garlic", "ginger", "soy sauce", "sesame oil", "rice"],
                "instructions": [
                    "Heat oil in wok or large pan",
                    "Add garlic and ginger, stir-fry for 30 seconds",
                    "Add harder vegetables first (carrots, broccoli)",
                    "Add softer vegetables (peppers, mushrooms)",
                    "Season with soy sauce and sesame oil"
                ],
                "prep_time": 15,
                "cook_time": 10,
                "servings": 4,
                "cuisine": "chinese",
                "difficulty": "easy",
                "image_url": "/placeholder.svg",
                "tags": ["vegetarian", "vegan", "healthy", "quick"]
            },
            {
                "id": "5",
                "name": "Beef Tacos",
                "description": "Seasoned ground beef in soft tortillas with fresh toppings.",
                "ingredients": ["ground beef", "taco seasoning", "tortillas", "lettuce", "tomato", "cheese", "onion", "sour cream", "lime"],
                "instructions": [
                    "Brown ground beef in a pan",
                    "Add taco seasoning and water, simmer",
                    "Warm tortillas",
                    "Fill tortillas with beef",
                    "Top with lettuce, tomato, cheese, and other toppings"
                ],
                "prep_time": 10,
                "cook_time": 15,
                "servings": 4,
                "cuisine": "mexican",
                "difficulty": "easy",
                "image_url": "/placeholder.svg",
                "tags": ["mexican", "quick"]
            },
            {
                "id": "6",
                "name": "Mushroom Risotto",
                "description": "Creamy Italian rice dish with mixed mushrooms and parmesan cheese.",
                "ingredients": ["arborio rice", "mushrooms", "onion", "garlic", "white wine", "vegetable broth", "parmesan cheese", "butter", "olive oil"],
                "instructions": [
                    "Sauté mushrooms and set aside",
                    "Cook onion and garlic in olive oil",
                    "Add rice and toast for 2 minutes",
                    "Add wine and stir until absorbed",
                    "Gradually add warm broth, stirring constantly",
                    "Fold in mushrooms, butter, and parmesan"
                ],
                "prep_time": 15,
                "cook_time": 30,
                "servings": 4,
                "cuisine": "italian",
                "difficulty": "hard",
                "image_url": "/placeholder.svg",
                "tags": ["vegetarian", "italian", "creamy"]
            },
            {
                "id": "7",
                "name": "Greek Salad",
                "description": "Fresh Mediterranean salad with tomatoes, cucumbers, olives, and feta cheese.",
                "ingredients": ["tomato", "cucumber", "red onion", "olives", "feta cheese", "olive oil", "lemon juice", "oregano"],
                "instructions": [
                    "Chop tomatoes and cucumbers",
                    "Slice red onion thinly",
                    "Combine vegetables with olives",
                    "Crumble feta cheese on top",
                    "Dress with olive oil, lemon juice, and oregano"
                ],
                "prep_time": 15,
                "cook_time": 0,
                "servings": 4,
                "cuisine": "mediterranean",
                "difficulty": "easy",
                "image_url": "/placeholder.svg",
                "tags": ["vegetarian", "mediterranean", "healthy", "no-cook"]
            },
            {
                "id": "8",
                "name": "Chocolate Chip Cookies",
                "description": "Classic homemade cookies with chocolate chips.",
                "ingredients": ["flour", "butter", "brown sugar", "white sugar", "eggs", "vanilla", "baking soda", "salt", "chocolate chips"],
                "instructions": [
                    "Cream butter and sugars together",
                    "Beat in eggs and vanilla",
                    "Mix in flour, baking soda, and salt",
                    "Fold in chocolate chips",
                    "Bake at 375°F for 9-11 minutes"
                ],
                "prep_time": 15,
                "cook_time": 11,
                "servings": 24,
                "cuisine": "american",
                "difficulty": "easy",
                "image_url": "/placeholder.svg",
                "tags": ["dessert", "baking", "sweet"]
            }
        ]
        
        # Filter recipes based on search criteria
        filtered_recipes = []
        
        for recipe in mock_recipes:
            # Query filter
            if query and query.lower() not in recipe["name"].lower() and query.lower() not in recipe["description"].lower():
                continue
            
            # Ingredients filter
            if ingredients:
                recipe_ingredients = [ing.lower() for ing in recipe["ingredients"]]
                if not any(ing.lower() in recipe_ingredients for ing in ingredients):
                    continue
            
            # Cuisine filter
            if cuisine and recipe["cuisine"].lower() != cuisine.lower():
                continue
            
            # Diet filter
            if diet and diet.lower() not in recipe["tags"]:
                continue
            
            filtered_recipes.append(recipe)
        
        return filtered_recipes[:limit]
    
    async def get_recipe_by_id(self, recipe_id: str) -> Optional[Dict]:
        """Get a specific recipe by ID"""
        
        # Check cache first
        if recipe_id in self.recipe_cache:
            return self.recipe_cache[recipe_id]
        
        # Try external API
        if self.spoonacular_api_key:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{self.base_urls['spoonacular']}/{recipe_id}/information",
                        params={"apiKey": self.spoonacular_api_key},
                        timeout=10.0
                    )
                    
                    if response.status_code == 200:
                        recipe_data = response.json()
                        formatted_recipe = self._format_spoonacular_recipes([recipe_data])[0]
                        self.recipe_cache[recipe_id] = formatted_recipe
                        return formatted_recipe
            except Exception as e:
                logger.error(f"Error fetching recipe {recipe_id}: {str(e)}")
        
        # Fallback to mock data
        mock_recipes = await self._get_mock_recipe_data()
        for recipe in mock_recipes:
            if recipe["id"] == recipe_id:
                self.recipe_cache[recipe_id] = recipe
                return recipe
        
        return None
    
    def is_healthy(self) -> bool:
        """Check if the recipe service is healthy"""
        return self.initialized
