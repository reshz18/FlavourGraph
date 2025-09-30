"""
FlavorGraph: Intelligent Recipe Navigator with Algorithmic Insights
Main FastAPI application entry point
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Dict, Any, Optional
import os
import time
from dotenv import load_dotenv

from models.recipe_models import RecipeRequest, RecipeResponse, IngredientGapResponse, Ingredient
from services.recipe_service import RecipeService
from services.graph_service import IngredientGraphService
from services.algorithm_service import AlgorithmService
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FlavorGraph API",
    description="Intelligent Recipe Navigator with Algorithmic Insights",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
recipe_service = RecipeService()
graph_service = IngredientGraphService()
algorithm_service = AlgorithmService(graph_service)

# Inject dependencies
algorithm_service.set_recipe_service(recipe_service)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting FlavorGraph API...")
    await recipe_service.initialize()
    await graph_service.build_ingredient_graph()
    logger.info("FlavorGraph API started successfully!")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "FlavorGraph API is running!", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "recipe_service": recipe_service.is_healthy(),
            "graph_service": graph_service.is_healthy(),
            "algorithm_service": algorithm_service.is_healthy()
        }
    }

@app.post("/api/recipes/suggest", response_model=List[RecipeResponse])
async def suggest_recipes(request: RecipeRequest) -> List[RecipeResponse]:
    """
    INTELLIGENT RECIPE SUGGESTIONS using Graph Theory, Backtracking & Greedy Algorithms
    
    This endpoint demonstrates:
    - GREEDY ALGORITHM: Fast ingredient matching and initial filtering
    - GRAPH THEORY: ingredient relationship analysis and substitution finding
    - BACK TRACKING: Optimal recipe combination selection with constraints
    """
    try:
        logger.info(f"Recipe suggestion request: {len(request.available_ingredients)} ingredients")
        
        # Use the enhanced recipe service with integrated algorithms
        raw_recipes = await recipe_service.search_recipes_with_algorithms(
            available_ingredients=request.available_ingredients,
            cuisine=request.cuisine_preference.value if request.cuisine_preference else None,
            diet=request.dietary_restrictions[0].value if request.dietary_restrictions else None,
            limit=request.max_recipes
        )
        
        # Convert to RecipeResponse format
        recipe_responses = []
        for i, recipe in enumerate(raw_recipes):
            # Handle ingredient format conversion
            ingredients_list = []
            for ing in recipe.get("ingredients", []):
                if isinstance(ing, dict):
                    ingredients_list.append(Ingredient(
                        name=ing.get("name", ""),
                        quantity=ing.get("quantity", 0),
                        unit=ing.get("unit", "")
                    ))
                else:
                    ingredients_list.append(Ingredient(
                        name=str(ing),
                        quantity=0,
                        unit=""
                    ))
            
            recipe_response = RecipeResponse(
                id=recipe.get("id", f"recipe_{i}"),
                name=recipe.get("name", ""),
                description=recipe.get("description", ""),
                ingredients=ingredients_list,
                instructions=recipe.get("instructions", []),
                prep_time=recipe.get("prep_time", 0),
                cook_time=recipe.get("cook_time", 0),
                servings=recipe.get("servings", 1),
                difficulty=recipe.get("difficulty", "medium"),
                cuisine=recipe.get("cuisine", "international"),
                image_url=recipe.get("image_url", ""),
                match_score=recipe.get("match_score", recipe.get("greedy_score", 0.0)),
                missing_ingredients=recipe.get("missing_ingredients", []),
                substitution_suggestions=recipe.get("substitution_suggestions", {}),
                algorithm_used=recipe.get("algorithm_used", "integrated_algorithms")
            )
            recipe_responses.append(recipe_response)
        
        logger.info(f"Returning {len(recipe_responses)} algorithm-optimized recipes")
        return recipe_responses
        
    except Exception as e:
        logger.error(f"Error in recipe suggestion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Algorithm processing failed: {str(e)}")

@app.post("/api/ingredients/gap-analysis", response_model=IngredientGapResponse)
async def analyze_ingredient_gap(request: RecipeRequest):
    """
    Analyze ingredient gaps and provide substitution recommendations
    Uses:
    - Graph Theory: For ingredient similarity analysis
    - Greedy Algorithm: For optimal substitution selection
    """
    try:
        logger.info(f"Gap analysis request: {request.available_ingredients}")
        
        gap_analysis = await algorithm_service.analyze_ingredient_gaps(
            available_ingredients=request.available_ingredients,
            target_recipe_id=request.target_recipe_id
        )
        
        return gap_analysis
        
    except Exception as e:
        logger.error(f"Error in gap analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ingredients/substitutions/{ingredient}")
async def get_ingredient_substitutions(ingredient: str, limit: int = 5):
    """
    Get ingredient substitutions using graph-based similarity
    """
    try:
        substitutions = await graph_service.find_ingredient_substitutions(
            ingredient, limit
        )
        return {"ingredient": ingredient, "substitutions": substitutions}
        
    except Exception as e:
        logger.error(f"Error finding substitutions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recipes/search")
async def search_recipes(
    query: Optional[str] = None,
    ingredients: Optional[str] = None,
    cuisine: Optional[str] = None,
    diet: Optional[str] = None,
    limit: int = 20
):
    """
    Search recipes with various filters
    - If only ingredients are provided (no query), uses algorithmic flow powered by Spoonacular.
    - If query is provided, uses text-based search with optional filters.
    """
    try:
        ingredient_list = ingredients.split(",") if ingredients else None

        # Ingredients-only search -> use algorithmic flow
        if (not query or query.strip() == "") and ingredient_list:
            algo_results = await recipe_service.search_recipes_with_algorithms(
                available_ingredients=[i.strip() for i in ingredient_list if i.strip()],
                cuisine=cuisine,
                diet=diet,
                limit=limit
            )
            return {"recipes": algo_results, "total": len(algo_results)}

        # Fallback to legacy text search (query may be empty which returns defaults)
        recipes = await recipe_service.search_recipes(
            query=query or "",
            ingredients=ingredient_list,
            cuisine=cuisine,
            diet=diet,
            limit=limit
        )
        return {"recipes": recipes, "total": len(recipes)}
        
    except Exception as e:
        logger.error(f"Error searching recipes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/algorithms/demo")
async def get_algorithm_demonstration():
    """
    ALGORITHM DEMONSTRATION for Academic Presentation
    
    Shows real-time performance metrics of:
    - Graph Theory: NetworkX-based ingredient relationships
    - Backtracking: Recursive optimization with pruning
    - Greedy Algorithm: Local optimization strategies
    """
    try:
        # Get performance metrics from services
        recipe_metrics = recipe_service.get_performance_metrics() if hasattr(recipe_service, 'get_performance_metrics') else {}
        
        # Combine with algorithm service metrics
        algorithm_demo = await algorithm_service.get_algorithm_demonstration()
        
        # Enhanced demo data for judge presentation
        enhanced_demo = {
            **algorithm_demo,
            "performance_metrics": {
                **algorithm_demo.get("performance_metrics", {}),
                **recipe_metrics,
                "timestamp": time.time(),
                "system_status": "algorithms_active"
            },
            "algorithm_explanations": {
                "graph_theory": {
                    "description": "NetworkX-based ingredient relationship modeling",
                    "complexity": "O(V + E) for traversal, O(V²) for shortest path",
                    "applications": ["Ingredient substitution", "Similarity calculation", "Centrality analysis"]
                },
                "backtracking": {
                    "description": "Recursive optimization with constraint satisfaction",
                    "complexity": "O(2^n) worst case, O(n!) with pruning optimizations",
                    "applications": ["Optimal recipe selection", "Multi-objective optimization", "Constraint satisfaction"]
                },
                "greedy_algorithm": {
                    "description": "Local optimization for fast decision making",
                    "complexity": "O(n log n) for sorting-based operations",
                    "applications": ["Fast recipe filtering", "Ingredient matching", "Priority-based selection"]
                }
            },
            "real_time_stats": {
                "total_recipes_processed": recipe_metrics.get("algorithm_executions", 0),
                "api_calls_made": recipe_metrics.get("api_calls", 0),
                "cache_efficiency": f"{(recipe_metrics.get('cache_hits', 0) / max(recipe_metrics.get('api_calls', 1), 1) * 100):.1f}%"
            }
        }
        
        logger.info(" ALGORITHM DEMONSTRATION data prepared for presentation")
        return enhanced_demo
        
    except Exception as e:
        logger.error(f" Error in algorithm demonstration: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Algorithm demo failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
