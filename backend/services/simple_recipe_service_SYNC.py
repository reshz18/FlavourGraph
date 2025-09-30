"""
FAST Simplified Recipe Service - Synchronous, no API calls
"""

import time
from typing import List, Dict, Optional, Tuple
import logging
from services.indian_recipe_service import IndianRecipeService

logger = logging.getLogger(__name__)

class SimpleRecipeService:
    """Fast, synchronous recipe service"""
    
    def __init__(self):
        self.indian_service = IndianRecipeService()
        # Lightweight in-memory caches with TTL
        self._cache_ttl_seconds: int = 300  # 5 minutes
        self._cache_by_ingredients: Dict[str, Tuple[float, List[Dict]]] = {}
        self._cache_by_name: Dict[str, Tuple[float, List[Dict]]] = {}
    
    async def search_by_ingredients(self, ingredients: List[str], limit: int = 10) -> List[Dict]:
        """Search recipes by ingredients - FAST (no API calls)"""
        if not ingredients:
            return []
        
        # Cache check
        key = ",".join(sorted(set([i.strip().lower() for i in ingredients if i])))
        cached = self._cache_by_ingredients.get(key)
        if cached and (time.time() - cached[0]) < self._cache_ttl_seconds:
            logger.info(f"⚡ Returning {len(cached[1])} cached recipes")
            return cached[1][:limit]
        
        # Use Indian dataset service (synchronous - no await needed)
        result = self.indian_service.search_by_ingredients(ingredients, limit)
        
        # Update cache
        self._cache_by_ingredients[key] = (time.time(), result)
        
        logger.info(f"⚡ Returning {len(result)} recipes (instant)")
        return result
    
    async def search_by_name(self, query: str, limit: int = 10) -> List[Dict]:
        """Search recipes by name - FAST"""
        if not query:
            return []
        
        # Cache check
        qkey = query.strip().lower()
        cached = self._cache_by_name.get(qkey)
        if cached and (time.time() - cached[0]) < self._cache_ttl_seconds:
            logger.info(f"⚡ Returning {len(cached[1])} cached recipes")
            return cached[1][:limit]
        
        # Use Indian dataset service (synchronous)
        result = self.indian_service.search_by_name(query, limit)
        
        # Update cache
        self._cache_by_name[qkey] = (time.time(), result)
        
        logger.info(f"⚡ Returning {len(result)} recipes for '{query}' (instant)")
        return result
    
    async def get_random_recipes(self, count: int = 10) -> List[Dict]:
        """Get random/featured recipes - FAST"""
        result = self.indian_service.get_random_recipes(count)
        logger.info(f"⚡ Returning {len(result)} featured recipes (instant)")
        return result
