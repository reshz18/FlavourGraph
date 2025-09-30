"""
Unsplash Image Service - Fetches real recipe images from Unsplash API
"""

import os
import httpx
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class UnsplashService:
    """Service to fetch recipe images from Unsplash"""
    
    def __init__(self):
        self.access_key = os.getenv('UNSPLASH_ACCESS_KEY', '')
        self.base_url = "https://api.unsplash.com"
        self.cache = {}  # Simple in-memory cache
        
        if not self.access_key:
            logger.warning("⚠️ UNSPLASH_ACCESS_KEY not found in .env file")
        else:
            logger.info("✅ Unsplash API initialized")
    
    async def get_recipe_image(self, recipe_name: str, cuisine: str = "Indian") -> str:
        """
        Fetch recipe image from Unsplash based on recipe name
        Returns image URL or fallback placeholder
        """
        if not self.access_key:
            return self._get_fallback_image(recipe_name)
        
        # Check cache first
        cache_key = f"{recipe_name}_{cuisine}".lower()
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            # Build search query
            search_query = self._build_search_query(recipe_name, cuisine)
            
            # Call Unsplash API
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{self.base_url}/search/photos",
                    params={
                        "query": search_query,
                        "per_page": 1,
                        "orientation": "landscape"
                    },
                    headers={
                        "Authorization": f"Client-ID {self.access_key}"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('results') and len(data['results']) > 0:
                        image_url = data['results'][0]['urls']['regular']
                        # Cache the result
                        self.cache[cache_key] = image_url
                        logger.info(f"✅ Found Unsplash image for: {recipe_name}")
                        return image_url
                    else:
                        logger.info(f"ℹ️ No Unsplash results for: {recipe_name}, using fallback")
                        return self._get_fallback_image(recipe_name)
                else:
                    logger.warning(f"⚠️ Unsplash API error: {response.status_code}")
                    return self._get_fallback_image(recipe_name)
                    
        except Exception as e:
            logger.error(f"❌ Error fetching Unsplash image: {e}")
            return self._get_fallback_image(recipe_name)
    
    def _build_search_query(self, recipe_name: str, cuisine: str) -> str:
        """Build optimized search query for Unsplash"""
        name_lower = recipe_name.lower()
        
        # Extract key dish name
        if 'biryani' in name_lower:
            return "indian biryani rice food"
        elif 'butter chicken' in name_lower:
            return "butter chicken indian curry"
        elif 'tandoori' in name_lower:
            return "tandoori chicken indian food"
        elif 'paneer tikka' in name_lower:
            return "paneer tikka indian appetizer"
        elif 'paneer' in name_lower:
            return "paneer indian curry food"
        elif 'dosa' in name_lower:
            return "dosa south indian food"
        elif 'idli' in name_lower:
            return "idli south indian breakfast"
        elif 'samosa' in name_lower:
            return "samosa indian snack"
        elif 'dal' in name_lower:
            return "dal indian lentils curry"
        elif 'naan' in name_lower or 'roti' in name_lower:
            return "indian bread naan roti"
        elif 'curry' in name_lower:
            return f"indian curry {cuisine} food"
        elif 'rice' in name_lower:
            return "indian rice dish food"
        elif 'chicken' in name_lower:
            return "indian chicken curry food"
        elif 'fish' in name_lower:
            return "indian fish curry food"
        else:
            # Generic Indian food search
            return f"indian food {cuisine} cuisine"
    
    def _get_fallback_image(self, recipe_name: str) -> str:
        """Get fallback placeholder image if Unsplash fails"""
        name_lower = recipe_name.lower()
        
        # Color-coded placeholders
        if 'biryani' in name_lower:
            color, text = "FF6B35", "Biryani"
        elif 'chicken' in name_lower:
            color, text = "F7931E", "Chicken"
        elif 'paneer' in name_lower:
            color, text = "FFC857", "Paneer"
        elif 'dosa' in name_lower or 'idli' in name_lower:
            color, text = "C1A57B", "South+Indian"
        elif 'rice' in name_lower:
            color, text = "E8B4B8", "Rice"
        elif 'dal' in name_lower:
            color, text = "F4A460", "Dal"
        elif 'curry' in name_lower:
            color, text = "FF8C42", "Curry"
        else:
            color, text = "FF6B6B", "Indian+Food"
        
        return f"https://via.placeholder.com/400x300/{color}/FFFFFF?text={text}"

# Global instance
_unsplash_service = None

def get_unsplash_service() -> UnsplashService:
    """Get or create Unsplash service instance"""
    global _unsplash_service
    if _unsplash_service is None:
        _unsplash_service = UnsplashService()
    return _unsplash_service
