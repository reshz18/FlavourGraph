"""
PRODUCTION-READY Indian Recipe Service with Unsplash Integration
"""

import csv
import os
import asyncio
from typing import List, Dict, Optional
import logging
from difflib import SequenceMatcher
from services.unsplash_service import get_unsplash_service

logger = logging.getLogger(__name__)

class IndianRecipeService:
    """Production-ready service for Indian recipes with real images"""
    
    def __init__(self):
        self.recipes = []
        self.csv_path = os.path.join(os.path.dirname(__file__), "__pycache__", "IndianFoodDatasetCSV.csv")
        self.unsplash = get_unsplash_service()
        self._load_recipes()
    
    def _load_recipes(self):
        """Load recipes from CSV file"""
        try:
            if not os.path.exists(self.csv_path):
                self.csv_path = os.path.join(os.path.dirname(__file__), "IndianFoodDatasetCSV.csv")
            
            if not os.path.exists(self.csv_path):
                logger.error(f"❌ CSV file not found at {self.csv_path}")
                return
            
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    self.recipes.append(row)
            
            logger.info(f"✅ Loaded {len(self.recipes)} Indian recipes from CSV")
        except Exception as e:
            logger.error(f"❌ Error loading CSV: {e}")
    
    async def search_by_ingredients(self, ingredients: List[str], limit: int = 20) -> List[Dict]:
        """
        PRODUCTION: Accurate ingredient-based search with real images
        """
        if not ingredients or not self.recipes:
            return []
        
        # Clean and normalize ingredients
        cleaned_ingredients = []
        for ing in ingredients:
            if not ing or not ing.strip():
                continue
            ing_lower = ing.strip().lower()
            cleaned_ingredients.append(ing_lower)
            # Add first word for compound ingredients
            words = ing_lower.split()
            if len(words) > 1 and words[0] not in cleaned_ingredients:
                cleaned_ingredients.append(words[0])
        
        if not cleaned_ingredients:
            return []
        
        logger.info(f"🔍 Searching for recipes with: {cleaned_ingredients}")
        
        matched_recipes = []
        
        for recipe in self.recipes:
            # Get recipe ingredients (use TranslatedIngredients for English)
            recipe_ingredients_str = recipe.get('TranslatedIngredients', recipe.get('Ingredients', ''))
            if not recipe_ingredients_str:
                continue
            
            # Parse ingredients - split by comma and clean
            recipe_ingredients = []
            for ing in recipe_ingredients_str.split(','):
                ing_clean = ing.strip().lower()
                if ing_clean:
                    recipe_ingredients.append(ing_clean)
                    # Also add first word
                    first_word = ing_clean.split()[0] if ing_clean.split() else ''
                    if first_word and first_word not in recipe_ingredients:
                        recipe_ingredients.append(first_word)
            
            # ACCURATE MATCHING
            matched_ingredients = []
            matched_count = 0
            
            for user_ing in cleaned_ingredients:
                matched = False
                for recipe_ing in recipe_ingredients:
                    # Direct match or substring match
                    if (user_ing == recipe_ing or 
                        user_ing in recipe_ing or 
                        recipe_ing in user_ing or
                        self._fuzzy_match(user_ing, recipe_ing)):
                        if user_ing not in matched_ingredients:
                            matched_ingredients.append(user_ing)
                            matched_count += 1
                            matched = True
                        break
            
            # Calculate match percentage
            total_user_ingredients = len(set([ing for ing in cleaned_ingredients if len(ing) > 2]))
            match_percentage = (matched_count / total_user_ingredients * 100) if total_user_ingredients > 0 else 0
            
            # FLEXIBLE FILTER
            if total_user_ingredients == 1:
                # Single ingredient: must match
                if matched_count < 1:
                    continue
            else:
                # Multiple ingredients: at least 40% match
                if match_percentage < 40:
                    continue
            
            # Calculate missing ingredients
            missing_ingredients = []
            for recipe_ing in recipe_ingredients[:8]:
                is_covered = False
                for user_ing in cleaned_ingredients:
                    if user_ing in recipe_ing or recipe_ing in user_ing:
                        is_covered = True
                        break
                if not is_covered and recipe_ing and len(recipe_ing) > 2:
                    missing_ingredients.append(recipe_ing)
            
            # Get cuisine
            cuisine = recipe.get('Cuisine', 'Indian')
            is_indian = any(word in cuisine.lower() for word in ['indian', 'south', 'north', 'andhra', 'bengali', 'punjabi', 'gujarati', 'maharashtrian'])
            
            # SCORING with MASSIVE Indian boost
            base_score = match_percentage + (matched_count * 15)
            missing_penalty = len(missing_ingredients) * 0.8
            
            if is_indian:
                # 10x multiplier for Indian recipes!
                final_score = (base_score * 10.0) - missing_penalty + 100
            else:
                final_score = base_score - missing_penalty
            
            # Bonus for high matches
            if match_percentage >= 80:
                final_score += 30
            elif match_percentage >= 60:
                final_score += 15
            
            # Format recipe (will fetch image later)
            formatted = {
                'id': recipe.get('Srno', '0'),
                'name': recipe.get('TranslatedRecipeName', recipe.get('RecipeName', 'Unknown Recipe')),
                'cuisine': cuisine,
                'match_score': final_score,
                'match_percentage': round(match_percentage, 1),
                'matched_ingredients': matched_ingredients[:10],
                'missing_ingredients': missing_ingredients[:5],
                'total_matched': matched_count,
                'total_user_ingredients': total_user_ingredients,
                'recipe_data': recipe  # Store for later formatting
            }
            
            matched_recipes.append(formatted)
        
        # Sort by score
        matched_recipes.sort(
            key=lambda r: (
                r.get('match_score', 0),
                r.get('match_percentage', 0),
                -len(r.get('missing_ingredients', []))
            ),
            reverse=True
        )
        
        # Take top results
        top_recipes = matched_recipes[:limit]
        
        # Format recipes with images (async)
        formatted_recipes = await self._format_recipes_with_images(top_recipes)
        
        logger.info(f"✅ Returning {len(formatted_recipes)} recipes with images")
        return formatted_recipes
    
    def _fuzzy_match(self, str1: str, str2: str, threshold: float = 0.8) -> bool:
        """Check if two strings are similar enough"""
        if len(str1) < 3 or len(str2) < 3:
            return False
        ratio = SequenceMatcher(None, str1, str2).ratio()
        return ratio >= threshold
    
    async def search_by_name(self, query: str, limit: int = 20) -> List[Dict]:
        """Search recipes by name with IMPROVED accuracy and real images"""
        if not query or not self.recipes:
            return []
        
        query_lower = query.strip().lower()
        matched_recipes = []
        
        # IMPROVED SEARCH ALGORITHM for better accuracy
        for recipe in self.recipes:
            recipe_name = recipe.get('TranslatedRecipeName', recipe.get('RecipeName', '')).lower()
            original_recipe_name = recipe.get('TranslatedRecipeName', recipe.get('RecipeName', ''))
            
            # Calculate multiple match scores for better accuracy
            exact_match_score = 0
            partial_match_score = 0
            word_match_score = 0
            fuzzy_match_score = 0
            
            # 1. EXACT MATCH (highest priority)
            if recipe_name == query_lower:
                exact_match_score = 1000
            elif recipe_name.startswith(query_lower):
                exact_match_score = 800
            elif query_lower in recipe_name:
                exact_match_score = 600
            
            # 2. PARTIAL MATCH (recipe contains query)
            if query_lower in recipe_name:
                # Calculate how much of the query is matched
                match_ratio = len(query_lower) / len(recipe_name)
                partial_match_score = int(500 * match_ratio)
            
            # 3. WORD MATCH (individual words)
            query_words = [w for w in query_lower.split() if len(w) > 2]
            recipe_words = recipe_name.split()
            word_matches = 0
            for q_word in query_words:
                for r_word in recipe_words:
                    if q_word in r_word or r_word in q_word:
                        word_matches += 1
                        break
            
            if query_words:
                word_match_score = int(300 * (word_matches / len(query_words)))
            
            # 4. FUZZY MATCH (similarity)
            if len(query_lower) > 3 and len(recipe_name) > 3:
                similarity = self._fuzzy_match(query_lower, recipe_name, 0.6)
                if similarity:
                    fuzzy_match_score = int(200 * self._fuzzy_match_ratio(query_lower, recipe_name))
            
            # Calculate final score
            final_score = max(exact_match_score, partial_match_score, word_match_score, fuzzy_match_score)
            
            # Only include recipes with meaningful matches
            if final_score >= 100:
                # Boost Indian recipes
                cuisine = recipe.get('Cuisine', '')
                if any(word in cuisine.lower() for word in ['indian', 'south', 'north', 'andhra', 'punjabi', 'gujarati']):
                    final_score *= 1.2  # Reduced boost to prevent over-prioritization
                
                formatted = {
                    'id': recipe.get('Srno', '0'),
                    'name': original_recipe_name,
                    'cuisine': cuisine,
                    'match_score': final_score,
                    'recipe_data': recipe,
                    'search_accuracy': 'improved_name_search_v2'
                }
                
                matched_recipes.append(formatted)
        
        # Sort by relevance (exact matches first)
        matched_recipes.sort(key=lambda r: r.get('match_score', 0), reverse=True)
        
        # Take top results
        top_recipes = matched_recipes[:limit]
        
        # Format with images
        formatted_recipes = await self._format_recipes_with_images(top_recipes)
        
        logger.info(f"✅ Found {len(formatted_recipes)} recipes for '{query}' (improved accuracy)")
        return formatted_recipes
    
    def _fuzzy_match_ratio(self, str1: str, str2: str) -> float:
        """Calculate fuzzy match ratio"""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, str1, str2).ratio()
    
    async def get_random_recipes(self, count: int = 20) -> List[Dict]:
        """Get featured recipes with real images"""
        if not self.recipes:
            return []
        
        # Get Indian recipes first
        indian_recipes = [r for r in self.recipes if 'indian' in r.get('Cuisine', '').lower()]
        other_recipes = [r for r in self.recipes if 'indian' not in r.get('Cuisine', '').lower()]
        
        # Mix: 80% Indian, 20% others
        indian_count = int(count * 0.8)
        other_count = count - indian_count
        
        selected = indian_recipes[:indian_count] + other_recipes[:other_count]
        
        # Format for image fetching
        recipes_to_format = []
        for recipe in selected[:count]:
            recipes_to_format.append({
                'id': recipe.get('Srno', '0'),
                'name': recipe.get('TranslatedRecipeName', recipe.get('RecipeName', 'Unknown Recipe')),
                'cuisine': recipe.get('Cuisine', 'Indian'),
                'recipe_data': recipe
            })
        
        # Format with images
        formatted_recipes = await self._format_recipes_with_images(recipes_to_format)
        
        return formatted_recipes
    
    async def _format_recipes_with_images(self, recipes: List[Dict]) -> List[Dict]:
        """Format recipes and fetch images from Unsplash in parallel"""
        
        # Fetch all images in parallel
        image_tasks = []
        for recipe in recipes:
            recipe_name = recipe['name']
            cuisine = recipe['cuisine']
            task = self.unsplash.get_recipe_image(recipe_name, cuisine)
            image_tasks.append(task)
        
        # Wait for all images
        images = await asyncio.gather(*image_tasks)
        
        # Format complete recipes
        formatted_recipes = []
        for i, recipe in enumerate(recipes):
            recipe_data = recipe['recipe_data']
            
            # Parse ingredients
            ingredients_str = recipe_data.get('TranslatedIngredients', recipe_data.get('Ingredients', ''))
            ingredients = []
            for ing in ingredients_str.split(','):
                ing = ing.strip()
                if ing:
                    ingredients.append({
                        'name': ing,
                        'quantity': 1,
                        'unit': ''
                    })
            
            # Parse instructions
            instructions_str = recipe_data.get('TranslatedInstructions', recipe_data.get('Instructions', ''))
            instructions = [s.strip() for s in instructions_str.split('.') if s.strip() and len(s.strip()) > 10][:15]
            
            formatted = {
                'id': recipe['id'],
                'name': recipe['name'],
                'description': f"{recipe_data.get('Course', 'Main Course')} - {recipe_data.get('Diet', 'Vegetarian')} - {recipe['cuisine']} Cuisine",
                'ingredients': ingredients,
                'instructions': instructions,
                'prep_time': int(recipe_data.get('PrepTimeInMins', 15)),
                'cook_time': int(recipe_data.get('CookTimeInMins', 30)),
                'servings': int(recipe_data.get('Servings', 4)),
                'difficulty': 'medium',
                'cuisine': recipe['cuisine'],
                'image_url': images[i],  # Real Unsplash image!
                'course': recipe_data.get('Course', 'Main Course'),
                'diet': recipe_data.get('Diet', 'Vegetarian'),
                'source_url': recipe_data.get('URL', ''),
                'algorithm_used': recipe.get('algorithm_used', 'indian_dataset_production_v3')
            }
            
            # Add matching info if available
            if 'match_score' in recipe:
                formatted['match_score'] = recipe['match_score']
            if 'match_percentage' in recipe:
                formatted['match_percentage'] = recipe['match_percentage']
            if 'matched_ingredients' in recipe:
                formatted['matched_ingredients'] = recipe['matched_ingredients']
            if 'missing_ingredients' in recipe:
                formatted['missing_ingredients'] = recipe['missing_ingredients']
            if 'total_matched' in recipe:
                formatted['total_matched'] = recipe['total_matched']
            if 'total_user_ingredients' in recipe:
                formatted['total_user_ingredients'] = recipe['total_user_ingredients']
            
            formatted_recipes.append(formatted)
        
        return formatted_recipes
