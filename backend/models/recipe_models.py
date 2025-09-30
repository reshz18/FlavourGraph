"""
Pydantic models for FlavorGraph API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class DietaryRestriction(str, Enum):
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten-free"
    DAIRY_FREE = "dairy-free"
    KETO = "keto"
    PALEO = "paleo"
    LOW_CARB = "low-carb"

class CuisineType(str, Enum):
    ITALIAN = "italian"
    CHINESE = "chinese"
    INDIAN = "indian"
    MEXICAN = "mexican"
    AMERICAN = "american"
    FRENCH = "french"
    JAPANESE = "japanese"
    THAI = "thai"
    MEDITERRANEAN = "mediterranean"

class Ingredient(BaseModel):
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    category: Optional[str] = None

class NutritionInfo(BaseModel):
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    fiber: Optional[float] = None

class RecipeResponse(BaseModel):
    id: str
    name: str
    description: str
    ingredients: List[Ingredient]
    instructions: List[str]
    prep_time: Optional[int] = None  # in minutes
    cook_time: Optional[int] = None  # in minutes
    servings: Optional[int] = None
    difficulty: Optional[str] = None
    cuisine: Optional[str] = None
    image_url: Optional[str] = None
    nutrition: Optional[NutritionInfo] = None
    
    # Algorithm-specific fields
    match_score: float = Field(..., description="Algorithm-calculated match score (0-1)")
    missing_ingredients: List[str] = Field(default_factory=list)
    substitution_suggestions: Dict[str, List[str]] = Field(default_factory=dict)
    algorithm_used: str = Field(..., description="Primary algorithm used for suggestion")

class RecipeRequest(BaseModel):
    available_ingredients: List[str] = Field(..., description="List of available ingredients")
    dietary_restrictions: Optional[List[DietaryRestriction]] = None
    cuisine_preference: Optional[CuisineType] = None
    max_recipes: Optional[int] = Field(default=10, ge=1, le=50)
    target_recipe_id: Optional[str] = None  # For gap analysis

class IngredientSubstitution(BaseModel):
    original: str
    substitute: str
    similarity_score: float
    reason: str
    category_match: bool

class IngredientGapResponse(BaseModel):
    recipe_id: str
    recipe_name: str
    available_ingredients: List[str]
    missing_ingredients: List[str]
    substitution_recommendations: List[IngredientSubstitution]
    feasibility_score: float
    estimated_cost_increase: Optional[float] = None
    algorithm_analysis: Dict[str, Any]

class AlgorithmDemonstration(BaseModel):
    graph_theory_example: Dict[str, Any]
    backtracking_example: Dict[str, Any]
    greedy_algorithm_example: Dict[str, Any]
    performance_metrics: Dict[str, float]
