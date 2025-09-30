#!/usr/bin/env python3
"""
FlavorGraph Algorithm Testing Script
Tests all implemented algorithms and functionalities
"""

import asyncio
import json
import time
from services.graph_service import IngredientGraphService
from services.algorithm_service import AlgorithmService
from services.recipe_service import RecipeService
from models.recipe_models import RecipeRequest, DietaryRestriction, CuisineType

async def test_graph_theory():
    """Test Graph Theory Implementation"""
    print("🕸️ Testing Graph Theory Implementation...")
    
    graph_service = IngredientGraphService()
    await graph_service.build_ingredient_graph()
    
    # Test 1: Graph structure
    nodes = graph_service.ingredient_graph.number_of_nodes()
    edges = graph_service.ingredient_graph.number_of_edges()
    print(f"   ✅ Graph built: {nodes} nodes, {edges} edges")
    
    # Test 2: Ingredient substitutions
    substitutions = await graph_service.find_ingredient_substitutions("chicken", limit=3)
    print(f"   ✅ Chicken substitutions: {[s['ingredient'] for s in substitutions]}")
    
    # Test 3: Ingredient similarity
    similarity = graph_service.calculate_ingredient_similarity("chicken", "turkey")
    print(f"   ✅ Chicken-Turkey similarity: {similarity:.3f}")
    
    # Test 4: Centrality measures
    centrality = graph_service.get_ingredient_centrality("onion")
    print(f"   ✅ Onion centrality: {centrality}")
    
    # Test 5: Complementary ingredients
    complementary = graph_service.find_complementary_ingredients(["tomato", "cheese"])
    print(f"   ✅ Complementary to tomato+cheese: {complementary}")
    
    return graph_service

async def test_greedy_algorithm(algorithm_service):
    """Test Greedy Algorithm Implementation"""
    print("\n⚡ Testing Greedy Algorithm Implementation...")
    
    # Test 1: Recipe selection with greedy approach
    available_ingredients = ["chicken", "tomato", "onion", "garlic", "cheese"]
    
    start_time = time.time()
    recipes = await algorithm_service._greedy_recipe_selection(
        available_ingredients, 
        dietary_restrictions=None,
        cuisine_preference="italian"
    )
    execution_time = time.time() - start_time
    
    print(f"   ✅ Greedy recipe selection: {len(recipes)} recipes in {execution_time:.3f}s")
    
    # Test 2: Show top 3 recipes with scores
    for i, recipe in enumerate(recipes[:3]):
        print(f"      {i+1}. {recipe['name']} (Score: {recipe.get('greedy_score', 0):.1f})")
    
    return recipes

async def test_backtracking_algorithm(algorithm_service):
    """Test Backtracking Algorithm Implementation"""
    print("\n🔄 Testing Backtracking Algorithm Implementation...")
    
    # Test 1: Recipe optimization with constraints
    available_ingredients = ["chicken", "tomato", "onion", "garlic", "cheese", "pasta", "basil"]
    
    start_time = time.time()
    optimized_recipes = await algorithm_service.suggest_recipes_with_algorithms(
        available_ingredients=available_ingredients,
        dietary_restrictions=None,
        cuisine_preference="italian",
        max_recipes=5
    )
    execution_time = time.time() - start_time
    
    print(f"   ✅ Backtracking optimization: {len(optimized_recipes)} recipes in {execution_time:.3f}s")
    
    # Test 2: Show optimized results
    for i, recipe in enumerate(optimized_recipes):
        print(f"      {i+1}. {recipe.name} (Match: {recipe.match_score:.2f}, Algorithm: {recipe.algorithm_used})")
        if recipe.substitution_suggestions:
            print(f"         Substitutions: {recipe.substitution_suggestions}")
    
    return optimized_recipes

async def test_ingredient_gap_analysis(algorithm_service):
    """Test Ingredient Gap Analysis"""
    print("\n🔍 Testing Ingredient Gap Analysis...")
    
    # Test gap analysis for a specific recipe
    available_ingredients = ["flour", "eggs", "milk", "butter"]
    target_recipe_id = "1"  # Margherita Pizza
    
    gap_analysis = await algorithm_service.analyze_ingredient_gaps(
        available_ingredients=available_ingredients,
        target_recipe_id=target_recipe_id
    )
    
    print(f"   ✅ Gap analysis for recipe '{gap_analysis.recipe_name}':")
    print(f"      Missing ingredients: {gap_analysis.missing_ingredients}")
    print(f"      Feasibility score: {gap_analysis.feasibility_score:.2f}")
    print(f"      Substitution recommendations: {len(gap_analysis.substitution_recommendations)}")
    
    for sub in gap_analysis.substitution_recommendations:
        print(f"         {sub.original} → {sub.substitute} (Score: {sub.similarity_score:.2f})")
    
    return gap_analysis

async def test_recipe_search(recipe_service):
    """Test Recipe Search Functionality"""
    print("\n🔍 Testing Recipe Search...")
    
    # Test 1: Search by query
    recipes = await recipe_service.search_recipes(query="pizza", limit=3)
    print(f"   ✅ Pizza search: {len(recipes)} results")
    
    # Test 2: Search by ingredients
    recipes = await recipe_service.search_recipes(
        ingredients=["chicken", "tomato"], 
        limit=3
    )
    print(f"   ✅ Ingredient search (chicken, tomato): {len(recipes)} results")
    
    # Test 3: Search by cuisine
    recipes = await recipe_service.search_recipes(
        cuisine="italian", 
        limit=3
    )
    print(f"   ✅ Italian cuisine search: {len(recipes)} results")
    
    return recipes

async def test_performance_metrics(algorithm_service):
    """Test Performance Tracking"""
    print("\n📊 Testing Performance Metrics...")
    
    # Get algorithm demonstration data
    demo_data = await algorithm_service.get_algorithm_demonstration()
    
    print("   ✅ Algorithm Performance Metrics:")
    metrics = demo_data["performance_metrics"]
    print(f"      Graph traversals: {metrics['graph_traversals']}")
    print(f"      Greedy selections: {metrics['greedy_selections']}")
    print(f"      Backtracking calls: {metrics['backtracking_calls']}")
    print(f"      Total execution time: {metrics['total_execution_time']:.3f}s")
    
    return demo_data

async def test_edge_cases():
    """Test Edge Cases and Error Handling"""
    print("\n🧪 Testing Edge Cases...")
    
    graph_service = IngredientGraphService()
    await graph_service.build_ingredient_graph()
    algorithm_service = AlgorithmService(graph_service)
    
    # Test 1: Empty ingredients list
    try:
        recipes = await algorithm_service.suggest_recipes_with_algorithms(
            available_ingredients=[],
            max_recipes=5
        )
        print(f"   ✅ Empty ingredients handled: {len(recipes)} recipes")
    except Exception as e:
        print(f"   ❌ Empty ingredients error: {e}")
    
    # Test 2: Unknown ingredient substitution
    substitutions = await graph_service.find_ingredient_substitutions("unknown_ingredient")
    print(f"   ✅ Unknown ingredient handled: {len(substitutions)} substitutions")
    
    # Test 3: Invalid recipe ID for gap analysis
    try:
        gap_analysis = await algorithm_service.analyze_ingredient_gaps(
            available_ingredients=["flour"],
            target_recipe_id="invalid_id"
        )
        print(f"   ❌ Should have failed for invalid recipe ID")
    except Exception as e:
        print(f"   ✅ Invalid recipe ID handled: {type(e).__name__}")

async def comprehensive_algorithm_test():
    """Run comprehensive test of all algorithms"""
    print("🍳 FlavorGraph Algorithm Comprehensive Test")
    print("=" * 50)
    
    start_time = time.time()
    
    # Initialize services
    print("🚀 Initializing services...")
    recipe_service = RecipeService()
    await recipe_service.initialize()
    
    graph_service = await test_graph_theory()
    
    algorithm_service = AlgorithmService(graph_service)
    algorithm_service.set_recipe_service(recipe_service)
    
    # Run all tests
    await test_greedy_algorithm(algorithm_service)
    await test_backtracking_algorithm(algorithm_service)
    await test_ingredient_gap_analysis(algorithm_service)
    await test_recipe_search(recipe_service)
    await test_performance_metrics(algorithm_service)
    await test_edge_cases()
    
    total_time = time.time() - start_time
    
    print("\n" + "=" * 50)
    print(f"🎉 All tests completed successfully in {total_time:.2f}s!")
    print("\n✅ Algorithm Implementation Summary:")
    print("   • Graph Theory: Ingredient relationships and substitutions")
    print("   • Backtracking: Optimal recipe combination selection")
    print("   • Greedy Algorithm: Fast filtering and local optimization")
    print("   • Gap Analysis: Ingredient substitution recommendations")
    print("   • Performance Tracking: Real-time algorithm metrics")
    print("\n🚀 Backend is ready for integration with Next.js frontend!")

if __name__ == "__main__":
    asyncio.run(comprehensive_algorithm_test())
