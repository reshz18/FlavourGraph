"""
Simplified Recipe Service - Uses Indian Food Dataset CSV
This ensures recipes are actually returned to users
"""

import os
import time
from typing import List, Dict, Optional, Any, Tuple
import logging
from services.indian_recipe_service import IndianRecipeService

logger = logging.getLogger(__name__)

class SimpleRecipeService:
    """Simple, working recipe service using Indian dataset"""
    
    def __init__(self):
        self.indian_service = IndianRecipeService()
        # Lightweight in-memory caches with TTL
        self._cache_ttl_seconds: int = 300  # 5 minutes
        self._cache_by_ingredients: Dict[str, Tuple[float, List[Dict]]] = {}
        self._cache_by_name: Dict[str, Tuple[float, List[Dict]]] = {}
    
    async def search_by_ingredients(self, ingredients: List[str], limit: int = 10) -> List[Dict]:
        """Search recipes by ingredients using TheMealDB with Indian-first ranking.

        Strategy:
        - Normalize and expand ingredient names (e.g., "lemon juice" -> "lemon")
        - Query filter.php for several ingredients in parallel
        - ALWAYS include Indian area recipes
        - Union results and score by number of matched ingredients
        - Strong boost for Indian recipes (3x multiplier)
        - Fetch details in parallel (bounded concurrency) and return top scored
        """
        if not ingredients:
            return []

        # Normalize and expand ingredients (handle compound names)
        cleaned_ingredients = []
        for ing in ingredients:
            if not ing or not ing.strip():
                continue
            ing_lower = ing.strip().lower()
            # Add the full ingredient
            cleaned_ingredients.append(ing_lower)
            # Also add first word for compound ingredients (e.g., "lemon juice" -> "lemon")
            words = ing_lower.split()
            if len(words) > 1 and words[0] not in cleaned_ingredients:
                cleaned_ingredients.append(words[0])
        
        if not cleaned_ingredients:
            return []

        # Cache check (use sorted unique ingredients as key)
        key = ",".join(sorted(set(cleaned_ingredients)))
        cached = self._cache_by_ingredients.get(key)
        if cached and (time.time() - cached[0]) < self._cache_ttl_seconds:
            return cached[1][:limit]

        # Concurrency control for detail fetches
        semaphore = asyncio.Semaphore(8)

        async def fetch_filter(client: httpx.AsyncClient, ing: str) -> List[Dict]:
            try:
                resp = await client.get(f"{self.themealdb_base}/filter.php", params={"i": ing})
                if resp.status_code == 200:
                    return (resp.json() or {}).get("meals", []) or []
            except Exception as e:
                logger.error(f"Filter fetch failed for {ing}: {e}")
            return []

        async def fetch_area(client: httpx.AsyncClient, area: str) -> List[Dict]:
            try:
                resp = await client.get(f"{self.themealdb_base}/filter.php", params={"a": area})
                if resp.status_code == 200:
                    return (resp.json() or {}).get("meals", []) or []
            except Exception as e:
                logger.error(f"Area fetch failed for {area}: {e}")
            return []

        async def fetch_detail(client: httpx.AsyncClient, meal_id: str) -> Optional[Dict]:
            try:
                async with semaphore:
                    resp = await client.get(f"{self.themealdb_base}/lookup.php", params={"i": meal_id})
                if resp.status_code == 200:
                    data = resp.json() or {}
                    meals = data.get("meals") or []
                    if meals:
                        return meals[0]
            except Exception as e:
                logger.error(f"Detail fetch failed for {meal_id}: {e}")
            return None

        # Collect candidate meals and score
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Fetch by each ingredient in parallel (up to first 8 to widen results)
            ingredient_lists = await asyncio.gather(
                *[fetch_filter(client, ing) for ing in cleaned_ingredients[:8]]
            )

            # ALWAYS fetch Indian-area meals to prioritize (this is critical!)
            indian_list = await fetch_area(client, "Indian")
            logger.info(f"Found {len(indian_list)} Indian recipes")

            # Build score map
            id_to_meal_stub: Dict[str, Dict[str, Any]] = {}
            id_to_score: Dict[str, float] = {}
            id_to_match_count: Dict[str, int] = {}

            # Score by ingredient occurrences
            for meals in ingredient_lists:
                for meal in meals:
                    mid = meal.get("idMeal")
                    if not mid:
                        continue
                    id_to_meal_stub[mid] = meal
                    id_to_match_count[mid] = id_to_match_count.get(mid, 0) + 1

            # STRONG boost for Indian area candidates
            for meal in indian_list:
                mid = meal.get("idMeal")
                if not mid:
                    continue
                id_to_meal_stub[mid] = meal
                # Give Indian recipes a strong base boost (2.0) so they always appear
                id_to_match_count[mid] = id_to_match_count.get(mid, 0)
                id_to_score[mid] = id_to_score.get(mid, 0.0) + 2.0

            # Rank candidates by preliminary score (matches first)
            candidates = list(id_to_meal_stub.keys())
            def prelim_key(mid: str) -> float:
                return id_to_match_count.get(mid, 0) + id_to_score.get(mid, 0.0)
            candidates.sort(key=prelim_key, reverse=True)

            # Fetch more details to ensure we get enough recipes
            max_details = min(80, max(30, limit * 6))
            detail_ids = candidates[:max_details]
            logger.info(f"Fetching details for {len(detail_ids)} candidate recipes")

            details = await asyncio.gather(
                *[fetch_detail(client, mid) for mid in detail_ids]
            )

        # EXPERT-LEVEL ACCURACY: Score meals with strict ingredient matching
        finalized: List[Dict] = []
        cleaned_set = set(cleaned_ingredients)
        
        for meal in details:
            if not meal:
                continue
            
            # Extract all recipe ingredients
            recipe_ingredients = []
            recipe_ingredients_lower = []
            for i in range(1, 21):
                ing = (meal.get(f"strIngredient{i}") or "").strip()
                if ing:
                    recipe_ingredients.append(ing)
                    recipe_ingredients_lower.append(ing.lower())
            
            if not recipe_ingredients:
                continue
            
            # ACCURATE MATCHING: Check which user ingredients are in this recipe
            matched_ingredients = []
            matched_count = 0
            
            for user_ing in cleaned_ingredients:
                # Direct match
                if user_ing in recipe_ingredients_lower:
                    matched_ingredients.append(user_ing)
                    matched_count += 1
                    continue
                
                # Fuzzy match: Check if user ingredient is part of recipe ingredient
                # e.g., "chicken" matches "chicken breast", "lemon" matches "lemon juice"
                for recipe_ing in recipe_ingredients_lower:
                    if user_ing in recipe_ing or recipe_ing in user_ing:
                        matched_ingredients.append(user_ing)
                        matched_count += 1
                        break
            
            # Calculate match percentage
            total_user_ingredients = len(cleaned_ingredients)
            match_percentage = (matched_count / total_user_ingredients * 100) if total_user_ingredients > 0 else 0
            
            # STRICT FILTER: Only include recipes that match at least 40% of user ingredients
            # OR at least 2 ingredients for small searches
            min_matches_required = max(2, int(total_user_ingredients * 0.4))
            if matched_count < min_matches_required:
                continue
            
            # Calculate missing ingredients (what user needs to buy)
            missing_ingredients = []
            for recipe_ing in recipe_ingredients_lower:
                is_covered = False
                for user_ing in cleaned_ingredients:
                    if user_ing in recipe_ing or recipe_ing in user_ing:
                        is_covered = True
                        break
                if not is_covered:
                    # Find the original cased ingredient name
                    idx = recipe_ingredients_lower.index(recipe_ing)
                    missing_ingredients.append(recipe_ingredients[idx])
            
            area = (meal.get("strArea") or "").strip()
            is_indian = area.lower() == "indian"
            
            # SCORING FORMULA:
            # 1. Match percentage (0-100)
            # 2. Matched count bonus (each match = +10 points)
            # 3. Indian multiplier (3x for Indian recipes)
            # 4. Fewer missing ingredients = higher score
            base_score = match_percentage + (matched_count * 10)
            indian_multiplier = 3.0 if is_indian else 1.0
            missing_penalty = len(missing_ingredients) * 0.5
            
            final_score = (base_score * indian_multiplier) - missing_penalty
            
            formatted = self._format_recipe(meal)
            formatted["match_score"] = final_score
            formatted["match_percentage"] = round(match_percentage, 1)
            formatted["matched_ingredients"] = matched_ingredients
            formatted["missing_ingredients"] = missing_ingredients[:5]  # Show top 5 missing
            formatted["total_matched"] = matched_count
            formatted["total_user_ingredients"] = total_user_ingredients
            formatted["algorithm_used"] = "themealdb_accurate_matching"
            
            finalized.append(formatted)
        
        # Log matching statistics
        logger.info(f"Found {len(finalized)} recipes matching at least {min_matches_required} ingredients")

        # Final ranking: 
        # 1. Match score (higher = better)
        # 2. Match percentage (higher = better)
        # 3. Fewer missing ingredients (better)
        finalized.sort(
            key=lambda r: (
                r.get("match_score", 0),
                r.get("match_percentage", 0),
                -len(r.get("missing_ingredients", []))
            ),
            reverse=True
        )
        # Deduplicate by name
        seen = set()
        deduped: List[Dict] = []
        for r in finalized:
            name = r.get("name", "").lower()
            if name and name not in seen:
                seen.add(name)
                deduped.append(r)

        result = deduped[:limit]
        # Update cache
        self._cache_by_ingredients[key] = (time.time(), result)
        return result
    
    async def search_by_name(self, query: str, limit: int = 10) -> List[Dict]:
        """Search recipes by name with Indian-first ranking and multiple fallback strategies."""
        if not query:
            return []

        # Cache check
        qkey = query.strip().lower()
        cached = self._cache_by_name.get(qkey)
        if cached and (time.time() - cached[0]) < self._cache_ttl_seconds:
            return cached[1][:limit]

        recipes: List[Dict] = []
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Strategy 1: Direct search by full query
            try:
                response = await client.get(f"{self.themealdb_base}/search.php", params={"s": query})
                if response.status_code == 200:
                    data = response.json() or {}
                    meals = data.get("meals", []) or []
                    logger.info(f"Direct search for '{query}' found {len(meals)} recipes")
                    for meal in meals:
                        formatted = self._format_recipe(meal)
                        formatted["algorithm_used"] = "themealdb_name_direct"
                        recipes.append(formatted)
            except Exception as e:
                logger.error(f"Error in direct search for {query}: {e}")

            # Strategy 2: If no results, try first-letter search with filtering
            if not recipes and len(query) > 0:
                try:
                    resp = await client.get(f"{self.themealdb_base}/search.php", params={"f": query[0]})
                    if resp.status_code == 200:
                        data = resp.json() or {}
                        meals = data.get("meals", []) or []
                        logger.info(f"First-letter search for '{query[0]}' found {len(meals)} recipes")
                        ql = query.lower()
                        for meal in meals:
                            meal_name = (meal.get("strMeal") or "").lower()
                            # Match if query is in name OR if any word in query matches
                            query_words = ql.split()
                            matches_words = any(word in meal_name for word in query_words if len(word) > 2)
                            if ql in meal_name or matches_words:
                                formatted = self._format_recipe(meal)
                                formatted["algorithm_used"] = "themealdb_name_partial"
                                recipes.append(formatted)
                except Exception as e:
                    logger.error(f"Error in first-letter search: {e}")
            
            # Strategy 3: If still no results, get some Indian recipes as fallback
            if not recipes:
                try:
                    logger.info(f"No matches for '{query}', fetching Indian recipes as fallback")
                    resp = await client.get(f"{self.themealdb_base}/filter.php", params={"a": "Indian"})
                    if resp.status_code == 200:
                        data = resp.json() or {}
                        meals = (data.get("meals") or [])[:limit * 2]
                        # Fetch details for these meals
                        for meal_stub in meals:
                            meal_id = meal_stub.get("idMeal")
                            if meal_id:
                                detail_resp = await client.get(f"{self.themealdb_base}/lookup.php", params={"i": meal_id})
                                if detail_resp.status_code == 200:
                                    detail_data = detail_resp.json() or {}
                                    detail_meals = detail_data.get("meals") or []
                                    if detail_meals:
                                        formatted = self._format_recipe(detail_meals[0])
                                        formatted["algorithm_used"] = "themealdb_indian_fallback"
                                        recipes.append(formatted)
                                        if len(recipes) >= limit:
                                            break
                except Exception as e:
                    logger.error(f"Error in Indian fallback: {e}")

        # Rank: Indian first, then name similarity (starts-with), then length
        ql = query.lower()
        def name_rank(r: Dict) -> float:
            name = r.get("name", "").lower()
            starts = 1.0 if name.startswith(ql) else 0.0
            contains = 0.5 if ql in name else 0.0
            is_indian = 1.0 if (r.get("cuisine", "").lower() == "indian") else 0.0
            return is_indian * 3 + starts * 2 + contains

        recipes.sort(key=name_rank, reverse=True)
        # Deduplicate by name
        seen_names = set()
        deduped: List[Dict] = []
        for r in recipes:
            nm = r.get("name", "").lower()
            if nm and nm not in seen_names:
                seen_names.add(nm)
                deduped.append(r)
        result = deduped[:limit]
        # Update cache
        self._cache_by_name[qkey] = (time.time(), result)
        return result
    
    async def get_random_recipes(self, count: int = 5) -> List[Dict]:
        """Get random recipes with Indian preference, prioritizing famous dishes like Hyderabad Biryani."""
        popular_indian_dishes = [
            "hyderabadi biryani", "biryani", "butter chicken", "paneer tikka masala", "dal makhani",
            "palak paneer", "chole bhature", "rogan josh", "vindaloo", "idli sambar", "masala dosa"
        ]

        # Select a few popular queries randomly
        selected_queries = random.sample(popular_indian_dishes, min(5, count))

        recipes = []

        for q in selected_queries:
            found = await self.search_by_name(q, limit=2)  # Get 1-2 best matches per famous dish
            recipes.extend(found)
            if len(recipes) >= count:
                break

        # Fill remaining with random Indian recipes
        remaining = count - len(recipes)
        if remaining > 0:
            async with httpx.AsyncClient(timeout=15.0) as client:
                try:
                    response = await client.get(f"{self.themealdb_base}/filter.php", params={"a": "Indian"})
                    if response.status_code == 200:
                        data = response.json() or {}
                        indian_meals = (data.get("meals") or [])[:remaining * 2]
                        # Fetch details
                        for meal_stub in indian_meals:
                            meal_id = meal_stub.get("idMeal")
                            if meal_id:
                                detail_resp = await client.get(f"{self.themealdb_base}/lookup.php", params={"i": meal_id})
                                if detail_resp.status_code == 200:
                                    detail_data = detail_resp.json() or {}
                                    detail_meals = detail_data.get("meals") or []
                                    if detail_meals:
                                        recipe = self._format_recipe(detail_meals[0])
                                        recipes.append(recipe)
                                        remaining -= 1
                                        if remaining <= 0:
                                            break
                except Exception as e:
                    logger.error(f"Error fetching additional Indian recipes: {e}")

        # If still needed, fall back to general random
        remaining = count - len(recipes)
        for _ in range(remaining):
            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    response = await client.get(f"{self.themealdb_base}/random.php")
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("meals"):
                            recipe = self._format_recipe(data["meals"][0])
                            recipes.append(recipe)
            except:
                pass
        
        return recipes[:count]
    
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