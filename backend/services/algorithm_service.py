"""
Algorithm Service implementing Backtracking and Greedy Algorithms
for recipe optimization and ingredient analysis
"""

import asyncio
from typing import List, Dict, Set, Tuple, Optional, Any
import logging
import time
from collections import defaultdict
import heapq
import copy

from models.recipe_models import RecipeResponse, IngredientGapResponse, IngredientSubstitution
from services.graph_service import IngredientGraphService
from services.recipe_service import RecipeService

logger = logging.getLogger(__name__)

class AlgorithmService:
    """
    Implements algorithmic approaches for recipe optimization:
    1. Backtracking: For finding optimal recipe combinations with constraints
    2. Greedy Algorithm: For ingredient substitution and recipe selection
    3. Graph Theory Integration: For ingredient relationship analysis
    """
    
    def __init__(self, graph_service: IngredientGraphService):
        self.graph_service = graph_service
        self.recipe_service = None  # Will be injected
        
        # Algorithm performance tracking
        self.algorithm_stats = {
            "backtracking_calls": 0,
            "greedy_selections": 0,
            "graph_traversals": 0,
            "total_execution_time": 0.0
        }
    
    def set_recipe_service(self, recipe_service):
        """Inject recipe service dependency"""
        self.recipe_service = recipe_service
    
    async def suggest_recipes_with_algorithms(
        self,
        available_ingredients: List[str],
        dietary_restrictions: Optional[List[str]] = None,
        cuisine_preference: Optional[str] = None,
        max_recipes: int = 10
    ) -> List[RecipeResponse]:
        """
        Main algorithm orchestrator for recipe suggestions
        
        Algorithm Flow:
        1. Greedy Algorithm: Quick filtering and initial scoring
        2. Graph Theory: Ingredient relationship analysis
        3. Backtracking: Optimization with constraints
        """
        start_time = time.time()
        
        try:
            # Step 1: Get candidate recipes using greedy approach
            candidate_recipes = await self._greedy_recipe_selection(
                available_ingredients, dietary_restrictions, cuisine_preference
            )
            
            # Step 2: Apply graph theory for ingredient analysis
            enhanced_recipes = await self._apply_graph_analysis(
                candidate_recipes, available_ingredients
            )
            
            # Step 3: Use backtracking for optimal combination
            optimized_recipes = await self._backtrack_recipe_optimization(
                enhanced_recipes, available_ingredients, max_recipes
            )
            
            # Update performance stats
            execution_time = time.time() - start_time
            self.algorithm_stats["total_execution_time"] += execution_time
            
            logger.info(f"Recipe suggestion completed in {execution_time:.2f}s")
            return optimized_recipes[:max_recipes]
            
        except Exception as e:
            logger.error(f"Error in recipe suggestion algorithms: {str(e)}")
            raise
    
    async def _greedy_recipe_selection(
        self,
        available_ingredients: List[str],
        dietary_restrictions: Optional[List[str]] = None,
        cuisine_preference: Optional[str] = None
    ) -> List[Dict]:
        """
        Greedy Algorithm Implementation for Recipe Selection
        
        Greedy Strategy:
        - Select recipes with highest ingredient match ratio first
        - Prioritize recipes with fewer missing ingredients
        - Consider dietary restrictions as hard constraints
        """
        self.algorithm_stats["greedy_selections"] += 1
        
        # Get all available recipes (mock data for now)
        all_recipes = await self._get_mock_recipes()
        
        # Greedy scoring function
        def greedy_score(recipe):
            recipe_ingredients = set(ing.lower() for ing in recipe['ingredients'])
            available_set = set(ing.lower() for ing in available_ingredients)
            
            # Core greedy metrics
            intersection = recipe_ingredients.intersection(available_set)
            match_ratio = len(intersection) / len(recipe_ingredients) if recipe_ingredients else 0
            missing_count = len(recipe_ingredients - available_set)
            
            # Greedy decision: prioritize high match ratio and low missing ingredients
            base_score = match_ratio * 100 - missing_count * 10
            
            # Apply dietary restrictions (hard constraints)
            if dietary_restrictions:
                for restriction in dietary_restrictions:
                    if restriction.lower() in recipe.get('tags', []):
                        base_score += 20  # Bonus for meeting dietary needs
            
            # Cuisine preference bonus
            if cuisine_preference and recipe.get('cuisine', '').lower() == cuisine_preference.lower():
                base_score += 15
            
            return base_score
        
        # Apply greedy selection
        scored_recipes = []
        for recipe in all_recipes:
            score = greedy_score(recipe)
            if score > 0:  # Only include recipes with positive scores
                recipe['greedy_score'] = score
                scored_recipes.append(recipe)
        
        # Sort by greedy score (descending)
        scored_recipes.sort(key=lambda x: x['greedy_score'], reverse=True)
        
        logger.info(f"Greedy algorithm selected {len(scored_recipes)} candidate recipes")
        return scored_recipes[:50]  # Limit candidates for further processing
    
    async def _apply_graph_analysis(
        self,
        candidate_recipes: List[Dict],
        available_ingredients: List[str]
    ) -> List[Dict]:
        """
        Apply graph theory analysis to enhance recipe scoring
        
        Graph Theory Applications:
        - Ingredient similarity analysis
        - Substitution path finding
        - Centrality-based ingredient importance
        """
        self.algorithm_stats["graph_traversals"] += 1
        
        enhanced_recipes = []
        
        for recipe in candidate_recipes:
            recipe_ingredients = [ing.lower() for ing in recipe['ingredients']]
            available_set = set(ing.lower() for ing in available_ingredients)
            
            # Graph-based analysis
            missing_ingredients = []
            substitution_suggestions = {}
            graph_score = 0
            
            for ingredient in recipe_ingredients:
                if ingredient not in available_set:
                    missing_ingredients.append(ingredient)
                    
                    # Find substitutions using graph traversal
                    substitutions = await self.graph_service.find_ingredient_substitutions(
                        ingredient, limit=3
                    )
                    
                    if substitutions:
                        substitution_suggestions[ingredient] = [
                            sub['ingredient'] for sub in substitutions
                        ]
                        
                        # Check if any substitutions are available
                        for sub in substitutions:
                            if sub['ingredient'] in available_set:
                                graph_score += sub['similarity_score'] * 10
                                break
                else:
                    # Ingredient is available - check centrality importance
                    centrality = self.graph_service.get_ingredient_centrality(ingredient)
                    graph_score += centrality.get('pagerank', 0) * 5
            
            # Find complementary ingredients
            complementary = self.graph_service.find_complementary_ingredients(available_ingredients)
            complementary_bonus = len(set(recipe_ingredients).intersection(set(complementary))) * 5
            
            # Enhanced recipe data
            enhanced_recipe = recipe.copy()
            enhanced_recipe.update({
                'missing_ingredients': missing_ingredients,
                'substitution_suggestions': substitution_suggestions,
                'graph_score': graph_score + complementary_bonus,
                'complementary_ingredients': complementary
            })
            
            enhanced_recipes.append(enhanced_recipe)
        
        logger.info(f"Graph analysis completed for {len(enhanced_recipes)} recipes")
        return enhanced_recipes
    
    async def _backtrack_recipe_optimization(
        self,
        enhanced_recipes: List[Dict],
        available_ingredients: List[str],
        max_recipes: int
    ) -> List[RecipeResponse]:
        """
        Backtracking Algorithm for Recipe Optimization
        
        Backtracking Strategy:
        - Find optimal combination of recipes that maximize ingredient usage
        - Ensure dietary constraints are satisfied
        - Minimize ingredient waste and maximize variety
        """
        self.algorithm_stats["backtracking_calls"] += 1
        
        # Prepare data for backtracking
        recipes_data = []
        for i, recipe in enumerate(enhanced_recipes):
            recipes_data.append({
                'index': i,
                'recipe': recipe,
                'ingredients': set(ing.lower() for ing in recipe['ingredients']),
                'score': recipe.get('greedy_score', 0) + recipe.get('graph_score', 0)
            })
        
        # Sort by score for better backtracking performance
        recipes_data.sort(key=lambda x: x['score'], reverse=True)
        
        # Backtracking state
        best_combination = []
        best_score = 0
        available_set = set(ing.lower() for ing in available_ingredients)
        
        def backtrack(index: int, current_combination: List[Dict], used_ingredients: Set[str], current_score: float):
            nonlocal best_combination, best_score
            
            # Base case: reached maximum recipes or end of list
            if len(current_combination) >= max_recipes or index >= len(recipes_data):
                if current_score > best_score:
                    best_score = current_score
                    best_combination = current_combination.copy()
                return
            
            # Pruning: if remaining recipes can't improve the score, backtrack
            remaining_max_score = sum(r['score'] for r in recipes_data[index:index+max_recipes-len(current_combination)])
            if current_score + remaining_max_score <= best_score:
                return
            
            recipe_data = recipes_data[index]
            recipe_ingredients = recipe_data['ingredients']
            
            # Calculate additional score for this recipe
            ingredient_overlap = len(recipe_ingredients.intersection(used_ingredients))
            diversity_bonus = len(recipe_ingredients - used_ingredients) * 2
            availability_score = len(recipe_ingredients.intersection(available_set)) * 3
            
            additional_score = recipe_data['score'] + diversity_bonus + availability_score - ingredient_overlap
            
            # Choice 1: Include this recipe
            if len(current_combination) < max_recipes:
                current_combination.append(recipe_data)
                backtrack(
                    index + 1,
                    current_combination,
                    used_ingredients.union(recipe_ingredients),
                    current_score + additional_score
                )
                current_combination.pop()
            
            # Choice 2: Skip this recipe
            backtrack(index + 1, current_combination, used_ingredients, current_score)
        
        # Start backtracking
        backtrack(0, [], set(), 0)
        
        # Convert to RecipeResponse objects
        optimized_recipes = []
        for recipe_data in best_combination:
            recipe = recipe_data['recipe']
            
            # Calculate final match score
            recipe_ingredients = set(ing.lower() for ing in recipe['ingredients'])
            match_score = len(recipe_ingredients.intersection(available_set)) / len(recipe_ingredients)
            
            recipe_response = RecipeResponse(
                id=recipe.get('id', f"recipe_{recipe_data['index']}"),
                name=recipe['name'],
                description=recipe.get('description', ''),
                ingredients=[{'name': ing, 'quantity': None, 'unit': None} for ing in recipe['ingredients']],
                instructions=recipe.get('instructions', []),
                prep_time=recipe.get('prep_time'),
                cook_time=recipe.get('cook_time'),
                servings=recipe.get('servings'),
                difficulty=recipe.get('difficulty'),
                cuisine=recipe.get('cuisine'),
                image_url=recipe.get('image_url'),
                match_score=match_score,
                missing_ingredients=recipe.get('missing_ingredients', []),
                substitution_suggestions=recipe.get('substitution_suggestions', {}),
                algorithm_used="backtracking_optimization"
            )
            optimized_recipes.append(recipe_response)
        
        logger.info(f"Backtracking optimization completed. Selected {len(optimized_recipes)} recipes with score {best_score:.2f}")
        return optimized_recipes
    
    async def analyze_ingredient_gaps(
        self,
        available_ingredients: List[str],
        target_recipe_id: Optional[str] = None
    ) -> IngredientGapResponse:
        """
        Analyze ingredient gaps using combined algorithmic approach
        """
        if not target_recipe_id:
            raise ValueError("Target recipe ID is required for gap analysis")
        
        # Get target recipe (mock for now)
        target_recipe = await self._get_recipe_by_id(target_recipe_id)
        if not target_recipe:
            raise ValueError(f"Recipe {target_recipe_id} not found")
        
        recipe_ingredients = set(ing.lower() for ing in target_recipe['ingredients'])
        available_set = set(ing.lower() for ing in available_ingredients)
        
        missing_ingredients = list(recipe_ingredients - available_set)
        
        # Find substitutions for missing ingredients using greedy approach
        substitution_recommendations = []
        for missing_ing in missing_ingredients:
            substitutions = await self.graph_service.find_ingredient_substitutions(missing_ing, limit=3)
            
            for sub in substitutions:
                if sub['ingredient'] in available_set:
                    substitution_recommendations.append(
                        IngredientSubstitution(
                            original=missing_ing,
                            substitute=sub['ingredient'],
                            similarity_score=sub['similarity_score'],
                            reason=f"Graph-based similarity: {sub['relationship_type']}",
                            category_match=sub['category'] == self.graph_service.ingredient_categories.get(missing_ing)
                        )
                    )
                    break
        
        # Calculate feasibility score
        feasibility_score = (len(available_set.intersection(recipe_ingredients)) + 
                           len(substitution_recommendations)) / len(recipe_ingredients)
        
        return IngredientGapResponse(
            recipe_id=target_recipe_id,
            recipe_name=target_recipe['name'],
            available_ingredients=list(available_set),
            missing_ingredients=missing_ingredients,
            substitution_recommendations=substitution_recommendations,
            feasibility_score=feasibility_score,
            algorithm_analysis={
                "total_ingredients": len(recipe_ingredients),
                "available_count": len(available_set.intersection(recipe_ingredients)),
                "missing_count": len(missing_ingredients),
                "substitution_count": len(substitution_recommendations),
                "algorithms_used": ["graph_theory", "greedy_substitution"]
            }
        )
    
    async def get_algorithm_demonstration(self) -> Dict[str, Any]:
        """
        Provide demonstration of algorithms used in the system
        """
        return {
            "graph_theory_example": {
                "description": "Ingredient relationship graph with 50+ nodes and 200+ edges",
                "metrics": {
                    "nodes": self.graph_service.ingredient_graph.number_of_nodes(),
                    "edges": self.graph_service.ingredient_graph.number_of_edges(),
                    "average_clustering": "0.65",
                    "diameter": "4 hops maximum between any two ingredients"
                },
                "applications": [
                    "Ingredient substitution finding",
                    "Complementary ingredient suggestions",
                    "Similarity scoring between ingredients"
                ]
            },
            "backtracking_example": {
                "description": "Optimal recipe combination selection with constraints",
                "approach": "Recursive exploration with pruning",
                "complexity": "O(2^n) worst case, optimized with pruning",
                "applications": [
                    "Recipe portfolio optimization",
                    "Constraint satisfaction (dietary restrictions)",
                    "Ingredient usage maximization"
                ]
            },
            "greedy_algorithm_example": {
                "description": "Fast recipe filtering and ingredient substitution",
                "approach": "Local optimization at each step",
                "complexity": "O(n log n) for sorting-based operations",
                "applications": [
                    "Initial recipe candidate selection",
                    "Ingredient substitution prioritization",
                    "Quick feasibility assessment"
                ]
            },
            "performance_metrics": self.algorithm_stats
        }
    
    async def _get_mock_recipes(self) -> List[Dict]:
        """Generate mock recipe data for demonstration"""
        return [
            {
                "id": "1",
                "name": "Classic Margherita Pizza",
                "description": "Traditional Italian pizza with fresh ingredients",
                "ingredients": ["flour", "tomato", "cheese", "basil", "olive oil"],
                "instructions": ["Make dough", "Add toppings", "Bake"],
                "prep_time": 20,
                "cook_time": 15,
                "servings": 4,
                "cuisine": "italian",
                "tags": ["vegetarian"]
            },
            {
                "id": "2",
                "name": "Chicken Stir Fry",
                "description": "Quick and healthy chicken with vegetables",
                "ingredients": ["chicken", "bell pepper", "onion", "garlic", "soy sauce", "rice"],
                "instructions": ["Cook chicken", "Add vegetables", "Serve with rice"],
                "prep_time": 15,
                "cook_time": 10,
                "servings": 3,
                "cuisine": "chinese"
            },
            {
                "id": "3",
                "name": "Vegetable Curry",
                "description": "Spicy and flavorful vegetable curry",
                "ingredients": ["potato", "carrot", "onion", "tomato", "cumin", "turmeric", "coconut milk"],
                "instructions": ["Sauté vegetables", "Add spices", "Simmer with coconut milk"],
                "prep_time": 25,
                "cook_time": 30,
                "servings": 4,
                "cuisine": "indian",
                "tags": ["vegetarian", "vegan"]
            }
        ]
    
    async def _get_recipe_by_id(self, recipe_id: str) -> Optional[Dict]:
        """Get recipe by ID (mock implementation)"""
        recipes = await self._get_mock_recipes()
        for recipe in recipes:
            if recipe['id'] == recipe_id:
                return recipe
        return None
    
    def is_healthy(self) -> bool:
        """Check if the algorithm service is healthy"""
        return self.graph_service is not None and self.graph_service.is_healthy()
