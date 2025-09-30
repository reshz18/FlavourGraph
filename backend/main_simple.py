"""
FlavorGraph: Simple Working Backend
Optimized for deployment - No complex dependencies
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Dict, Any, Optional
import os
import logging
from dotenv import load_dotenv

# Simple imports - only what we need
from services.simple_recipe_service import SimpleRecipeService

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FlavorGraph API",
    description="Recipe Navigator with Intelligent Search",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize simple recipe service
recipe_service = SimpleRecipeService()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("🚀 Starting FlavorGraph API...")
    logger.info("✅ FlavorGraph API started successfully!")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "FlavorGraph API is running!",
        "version": "2.0.0",
        "status": "healthy"
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "recipe_service",
        "ready": True
    }

@app.post("/api/recipes/suggest")
async def suggest_recipes(request: Dict[str, Any]):
    """
    Recipe suggestions based on available ingredients
    """
    try:
        available_ingredients = request.get("available_ingredients", [])
        max_recipes = request.get("max_recipes", 12)
        
        logger.info(f"Recipe suggestion request: {len(available_ingredients)} ingredients")
        
        # Search recipes
        recipes = await recipe_service.search_by_ingredients(
            available_ingredients,
            max_recipes
        )
        
        logger.info(f"Returning {len(recipes)} recipes")
        return recipes
        
    except Exception as e:
        logger.error(f"Error in recipe suggestion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recipes/search")
async def search_recipes(
    query: Optional[str] = None,
    ingredients: Optional[str] = None,
    limit: int = 12
):
    """
    Search recipes by name or ingredients
    """
    try:
        # Search by name if query provided
        if query and query.strip():
            recipes = await recipe_service.search_by_name(query, limit)
            return {"recipes": recipes, "total": len(recipes)}
        
        # Search by ingredients if provided
        if ingredients:
            ingredient_list = [i.strip() for i in ingredients.split(",") if i.strip()]
            recipes = await recipe_service.search_by_ingredients(ingredient_list, limit)
            return {"recipes": recipes, "total": len(recipes)}
        
        # Default: return featured recipes
        recipes = await recipe_service.get_random_recipes(limit)
        return {"recipes": recipes, "total": len(recipes)}
        
    except Exception as e:
        logger.error(f"Error searching recipes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
