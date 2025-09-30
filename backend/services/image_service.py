"""
Image Service - Provides accurate, category-based recipe images
Uses multiple free sources for best quality
"""

import logging
import hashlib

logger = logging.getLogger(__name__)

class RecipeImageService:
    """Service to provide accurate recipe images based on main ingredient"""
    
    def __init__(self):
        # High-quality curated images from Unsplash (free, no API key)
        # These are permanent URLs that always work
        self.category_images = {
            # BIRYANI - Beautiful biryani
            'biryani': 'https://source.unsplash.com/400x300/?biryani,indian-food',
            
            # CHICKEN DISHES
            'chicken': 'https://source.unsplash.com/400x300/?indian-chicken,curry',
            
            # PANEER DISHES
            'paneer': 'https://source.unsplash.com/400x300/?paneer,indian-food',
            
            # FISH DISHES
            'fish': 'https://source.unsplash.com/400x300/?fish-curry,indian',
            
            # MUTTON/LAMB
            'mutton': 'https://source.unsplash.com/400x300/?mutton-curry,indian',
            'lamb': 'https://source.unsplash.com/400x300/?lamb-curry,indian',
            
            # PRAWN/SHRIMP
            'prawn': 'https://source.unsplash.com/400x300/?prawn-curry,seafood',
            'shrimp': 'https://source.unsplash.com/400x300/?shrimp-curry,seafood',
            
            # RICE DISHES
            'rice': 'https://source.unsplash.com/400x300/?indian-rice,food',
            
            # DAL/LENTILS
            'dal': 'https://source.unsplash.com/400x300/?dal,lentils,indian',
            'lentil': 'https://source.unsplash.com/400x300/?lentils,curry',
            
            # DOSA
            'dosa': 'https://source.unsplash.com/400x300/?dosa,south-indian',
            
            # IDLI
            'idli': 'https://source.unsplash.com/400x300/?idli,south-indian',
            
            # SAMOSA
            'samosa': 'https://source.unsplash.com/400x300/?samosa,indian-snack',
            
            # PAKORA/BHAJI
            'pakora': 'https://source.unsplash.com/400x300/?pakora,indian-snack',
            'bhaji': 'https://source.unsplash.com/400x300/?bhaji,indian-food',
            
            # NAAN/ROTI
            'naan': 'https://source.unsplash.com/400x300/?naan,indian-bread',
            'roti': 'https://source.unsplash.com/400x300/?roti,indian-bread',
            'paratha': 'https://source.unsplash.com/400x300/?paratha,indian-bread',
            
            # CURRY
            'curry': 'https://source.unsplash.com/400x300/?indian-curry,food',
            
            # VEGETABLE DISHES
            'aloo': 'https://source.unsplash.com/400x300/?potato-curry,indian',
            'potato': 'https://source.unsplash.com/400x300/?potato-curry,indian',
            'gobi': 'https://source.unsplash.com/400x300/?cauliflower-curry,indian',
            'cauliflower': 'https://source.unsplash.com/400x300/?cauliflower-curry,indian',
            
            # CHUTNEY
            'chutney': 'https://source.unsplash.com/400x300/?chutney,indian-condiment',
            
            # DESSERTS
            'kheer': 'https://source.unsplash.com/400x300/?kheer,indian-dessert',
            'halwa': 'https://source.unsplash.com/400x300/?halwa,indian-sweet',
            'ladoo': 'https://source.unsplash.com/400x300/?ladoo,indian-sweet',
            'sweet': 'https://source.unsplash.com/400x300/?indian-dessert,sweet',
            'dessert': 'https://source.unsplash.com/400x300/?indian-dessert',
            
            # SOUP
            'soup': 'https://source.unsplash.com/400x300/?soup,indian',
            
            # SALAD
            'salad': 'https://source.unsplash.com/400x300/?salad,indian',
        }
        
        # Default Indian food image
        self.default_image = 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=500&h=400&fit=crop'
        
        logger.info(f"✅ Image Service initialized with {len(self.category_images)} categories")
    
    def get_recipe_image(self, recipe_name: str, ingredients: str = '') -> str:
        """
        Get accurate image based on recipe name and ingredients
        
        Strategy:
        1. Check recipe name for main ingredient
        2. Check ingredients list for main ingredient
        3. Return category-specific image
        4. All recipes with same main ingredient get same beautiful image
        """
        
        # Combine recipe name and ingredients for better matching
        search_text = f"{recipe_name} {ingredients}".lower()
        
        # Priority order for matching (most specific first)
        
        # BIRYANI (highest priority - very specific)
        if 'biryani' in search_text:
            logger.debug(f"🍚 Biryani image for: {recipe_name}")
            return self.category_images['biryani']
        
        # CHICKEN (all chicken dishes get same image)
        if 'chicken' in search_text or 'murgh' in search_text:
            logger.debug(f"🍗 Chicken image for: {recipe_name}")
            return self.category_images['chicken']
        
        # FISH (all fish dishes get same image)
        if 'fish' in search_text or 'meen' in search_text:
            logger.debug(f"🐟 Fish image for: {recipe_name}")
            return self.category_images['fish']
        
        # MUTTON/LAMB (all mutton dishes get same image)
        if 'mutton' in search_text or 'lamb' in search_text or 'goat' in search_text:
            logger.debug(f"🍖 Mutton image for: {recipe_name}")
            return self.category_images['mutton']
        
        # PRAWN/SHRIMP (all prawn dishes get same image)
        if 'prawn' in search_text or 'shrimp' in search_text:
            logger.debug(f"🦐 Prawn image for: {recipe_name}")
            return self.category_images['prawn']
        
        # PANEER (all paneer dishes get same image)
        if 'paneer' in search_text:
            logger.debug(f"🧀 Paneer image for: {recipe_name}")
            return self.category_images['paneer']
        
        # DOSA (all dosa recipes get same image)
        if 'dosa' in search_text:
            logger.debug(f"🥞 Dosa image for: {recipe_name}")
            return self.category_images['dosa']
        
        # IDLI (all idli recipes get same image)
        if 'idli' in search_text:
            logger.debug(f"⚪ Idli image for: {recipe_name}")
            return self.category_images['idli']
        
        # SAMOSA (all samosa recipes get same image)
        if 'samosa' in search_text:
            logger.debug(f"🥟 Samosa image for: {recipe_name}")
            return self.category_images['samosa']
        
        # PAKORA/BHAJI (all pakora recipes get same image)
        if 'pakora' in search_text or 'bhaji' in search_text or 'bhajji' in search_text:
            logger.debug(f"🍤 Pakora image for: {recipe_name}")
            return self.category_images['pakora']
        
        # RICE (all rice dishes get same image, except biryani)
        if 'rice' in search_text or 'pulao' in search_text or 'pilaf' in search_text:
            logger.debug(f"🍚 Rice image for: {recipe_name}")
            return self.category_images['rice']
        
        # DAL/LENTILS (all dal recipes get same image)
        if 'dal' in search_text or 'lentil' in search_text or 'sambar' in search_text:
            logger.debug(f"🍲 Dal image for: {recipe_name}")
            return self.category_images['dal']
        
        # NAAN/ROTI (all bread recipes get same image)
        if 'naan' in search_text or 'roti' in search_text or 'paratha' in search_text or 'chapati' in search_text:
            logger.debug(f"🫓 Bread image for: {recipe_name}")
            return self.category_images['naan']
        
        # CURRY (all curry recipes get same image)
        if 'curry' in search_text:
            logger.debug(f"🍛 Curry image for: {recipe_name}")
            return self.category_images['curry']
        
        # CHUTNEY (all chutney recipes get same image)
        if 'chutney' in search_text or 'pickle' in search_text:
            logger.debug(f"🥫 Chutney image for: {recipe_name}")
            return self.category_images['chutney']
        
        # DESSERTS (all dessert recipes get same image)
        if any(word in search_text for word in ['kheer', 'halwa', 'ladoo', 'sweet', 'dessert', 'payasam']):
            logger.debug(f"🍮 Dessert image for: {recipe_name}")
            return self.category_images['kheer']
        
        # SOUP (all soup recipes get same image)
        if 'soup' in search_text:
            logger.debug(f"🍜 Soup image for: {recipe_name}")
            return self.category_images['soup']
        
        # SALAD (all salad recipes get same image)
        if 'salad' in search_text:
            logger.debug(f"🥗 Salad image for: {recipe_name}")
            return self.category_images['salad']
        
        # VEGETABLES (all vegetable dishes get same image)
        if any(word in search_text for word in ['aloo', 'potato', 'gobi', 'cauliflower', 'vegetable']):
            logger.debug(f"🥬 Vegetable image for: {recipe_name}")
            return self.category_images['aloo']
        
        # DEFAULT (if no category matches)
        logger.debug(f"🍽️ Default image for: {recipe_name}")
        return self.default_image
    
    def get_category_info(self, recipe_name: str) -> dict:
        """Get category information for a recipe"""
        search_text = recipe_name.lower()
        
        for category, image_url in self.category_images.items():
            if category in search_text:
                return {
                    'category': category,
                    'image_url': image_url,
                    'has_specific_image': True
                }
        
        return {
            'category': 'indian',
            'image_url': self.default_image,
            'has_specific_image': False
        }

# Global instance
_image_service = None

def get_image_service() -> RecipeImageService:
    """Get or create image service instance"""
    global _image_service
    if _image_service is None:
        _image_service = RecipeImageService()
    return _image_service
