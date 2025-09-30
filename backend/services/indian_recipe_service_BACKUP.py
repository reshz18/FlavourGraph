"""
IMPROVED Indian Recipe Service - Better accuracy and image handling
"""

import csv
import os
from typing import List, Dict, Optional
import logging
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

class IndianRecipeService:
    """Improved service for Indian recipes with better accuracy"""
    
    def __init__(self):
        self.recipes = []
        self.csv_path = os.path.join(os.path.dirname(__file__), "__pycache__", "IndianFoodDatasetCSV.csv")
        self._load_recipes()
    
    def _load_recipes(self):
        """Load recipes from CSV file"""
        try:
            if not os.path.exists(self.csv_path):
                self.csv_path = os.path.join(os.path.dirname(__file__), "IndianFoodDatasetCSV.csv")
            
            if not os.path.exists(self.csv_path):
                logger.error(f"CSV file not found at {self.csv_path}")
                return
            
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    self.recipes.append(row)
            
            logger.info(f"✅ Loaded {len(self.recipes)} Indian recipes from CSV")
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
    
    def search_by_ingredients(self, ingredients: List[str], limit: int = 20) -> List[Dict]:
        """
        IMPROVED: More accurate ingredient-based search
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
            
            # IMPROVED MATCHING: Check each user ingredient
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
            is_indian = any(word in cuisine.lower() for word in ['indian', 'south', 'north', 'andhra', 'bengali', 'punjabi', 'gujarati'])
            
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
            
            # Format recipe
            formatted = self._format_recipe(recipe)
            formatted['match_score'] = final_score
            formatted['match_percentage'] = round(match_percentage, 1)
            formatted['matched_ingredients'] = matched_ingredients[:10]
            formatted['missing_ingredients'] = missing_ingredients[:5]
            formatted['total_matched'] = matched_count
            formatted['total_user_ingredients'] = total_user_ingredients
            formatted['algorithm_used'] = 'indian_dataset_improved_v2'
            
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
        
        logger.info(f"✅ Found {len(matched_recipes)} matching recipes (returning top {limit})")
        return matched_recipes[:limit]
    
    def _fuzzy_match(self, str1: str, str2: str, threshold: float = 0.8) -> bool:
        """Check if two strings are similar enough"""
        if len(str1) < 3 or len(str2) < 3:
            return False
        ratio = SequenceMatcher(None, str1, str2).ratio()
        return ratio >= threshold
    
    def search_by_name(self, query: str, limit: int = 20) -> List[Dict]:
        """Search recipes by name"""
        if not query or not self.recipes:
            return []
        
        query_lower = query.strip().lower()
        matched_recipes = []
        
        for recipe in self.recipes:
            recipe_name = recipe.get('TranslatedRecipeName', recipe.get('RecipeName', '')).lower()
            
            # Check if query matches recipe name
            if (query_lower in recipe_name or 
                any(word in recipe_name for word in query_lower.split() if len(word) > 2)):
                formatted = self._format_recipe(recipe)
                formatted['algorithm_used'] = 'indian_dataset_name_search'
                
                # Calculate relevance score
                if recipe_name.startswith(query_lower):
                    formatted['match_score'] = 100
                elif query_lower in recipe_name:
                    formatted['match_score'] = 80
                else:
                    formatted['match_score'] = 60
                
                # Boost Indian recipes
                cuisine = recipe.get('Cuisine', '')
                if any(word in cuisine.lower() for word in ['indian', 'south', 'north']):
                    formatted['match_score'] *= 5
                
                matched_recipes.append(formatted)
        
        # Sort by relevance
        matched_recipes.sort(key=lambda r: r.get('match_score', 0), reverse=True)
        
        logger.info(f"✅ Found {len(matched_recipes)} recipes for '{query}' (returning top {limit})")
        return matched_recipes[:limit]
    
    def get_random_recipes(self, count: int = 20) -> List[Dict]:
        """Get featured recipes (prioritize Indian)"""
        if not self.recipes:
            return []
        
        # Get Indian recipes first
        indian_recipes = [r for r in self.recipes if 'indian' in r.get('Cuisine', '').lower()]
        other_recipes = [r for r in self.recipes if 'indian' not in r.get('Cuisine', '').lower()]
        
        # Mix: 80% Indian, 20% others
        indian_count = int(count * 0.8)
        other_count = count - indian_count
        
        selected = indian_recipes[:indian_count] + other_recipes[:other_count]
        
        formatted_recipes = []
        for recipe in selected[:count]:
            formatted = self._format_recipe(recipe)
            formatted['algorithm_used'] = 'indian_dataset_featured'
            formatted_recipes.append(formatted)
        
        return formatted_recipes
    
    def _format_recipe(self, recipe: Dict) -> Dict:
        """Format recipe to standard format"""
        
        # Parse ingredients
        ingredients_str = recipe.get('TranslatedIngredients', recipe.get('Ingredients', ''))
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
        instructions_str = recipe.get('TranslatedInstructions', recipe.get('Instructions', ''))
        instructions = [s.strip() for s in instructions_str.split('.') if s.strip() and len(s.strip()) > 10][:15]
        
        # Get cuisine
        cuisine = recipe.get('Cuisine', 'Indian')
        
        # Get recipe name
        recipe_name = recipe.get('TranslatedRecipeName', recipe.get('RecipeName', 'Unknown Recipe'))
        
        return {
            'id': recipe.get('Srno', '0'),
            'name': recipe_name,
            'description': f"{recipe.get('Course', 'Main Course')} - {recipe.get('Diet', 'Vegetarian')} - {cuisine} Cuisine",
            'ingredients': ingredients,
            'instructions': instructions,
            'prep_time': int(recipe.get('PrepTimeInMins', 15)),
            'cook_time': int(recipe.get('CookTimeInMins', 30)),
            'servings': int(recipe.get('Servings', 4)),
            'difficulty': 'medium',
            'cuisine': cuisine,
            'image_url': self._get_recipe_image(recipe_name, cuisine),
            'course': recipe.get('Course', 'Main Course'),
            'diet': recipe.get('Diet', 'Vegetarian'),
            'source_url': recipe.get('URL', '')
        }
    
    def _get_recipe_image(self, recipe_name: str, cuisine: str) -> str:
        """Get recipe image using placeholder service with Indian food images"""
        name_lower = recipe_name.lower()
        
        # Use a placeholder service that works reliably
        # Format: https://via.placeholder.com/400x300/COLOR/FFFFFF?text=Recipe+Name
        
        # Determine color based on dish type
        if 'biryani' in name_lower:
            color = "FF6B35"  # Orange for biryani
            text = "Biryani"
        elif 'chicken' in name_lower:
            color = "F7931E"  # Orange for chicken
            text = "Chicken+Dish"
        elif 'paneer' in name_lower:
            color = "FFC857"  # Yellow for paneer
            text = "Paneer+Dish"
        elif 'dosa' in name_lower or 'idli' in name_lower:
            color = "C1A57B"  # Beige for South Indian
            text = "South+Indian"
        elif 'rice' in name_lower:
            color = "E8B4B8"  # Light pink for rice
            text = "Rice+Dish"
        elif 'dal' in name_lower or 'lentil' in name_lower:
            color = "F4A460"  # Sandy brown for dal
            text = "Dal"
        elif 'curry' in name_lower:
            color = "FF8C42"  # Orange for curry
            text = "Curry"
        elif 'sweet' in name_lower or 'dessert' in name_lower:
            color = "FFB6C1"  # Light pink for sweets
            text = "Dessert"
        else:
            color = "FF6B6B"  # Default red
            text = "Indian+Food"
        
        # Return placeholder URL
        return f"https://via.placeholder.com/400x300/{color}/FFFFFF?text={text}"
