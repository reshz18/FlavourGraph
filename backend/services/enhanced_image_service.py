"""
Enhanced Image Service - Uses TheMealDB + Pexels for accurate food images
100% FREE - No API keys required!
"""

import logging
import hashlib
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class EnhancedImageService:
    """
    Multi-source image service:
    1. TheMealDB - Real food images (free, no API key)
    2. Pexels - High-quality curated images (free, no API key for basic use)
    3. Fallback - Curated direct URLs
    """
    
    def __init__(self):
        self.image_cache = {}
        self.mealdb_images = self._build_mealdb_map()
        self.curated_images = self._build_curated_map()
        logger.info("✅ Enhanced Image Service initialized - Multi-source FREE images!")
    
    def get_recipe_image(self, recipe_name: str, cuisine: str = "", ingredients: str = "") -> str:
        """Get best matching image for recipe"""
        name_lower = recipe_name.lower()
        
        # Check cache first
        cache_key = hashlib.md5(name_lower.encode()).hexdigest()
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        
        # Try TheMealDB images first (most accurate)
        for keyword, image_url in self.mealdb_images.items():
            if keyword in name_lower:
                self.image_cache[cache_key] = image_url
                return image_url
        
        # Try curated Pexels images
        for keyword, image_url in self.curated_images.items():
            if keyword in name_lower:
                self.image_cache[cache_key] = image_url
                return image_url
        
        # Check by cuisine
        if 'indian' in cuisine.lower() or 'indian' in name_lower:
            return self.curated_images['default_indian']
        
        # Default
        return self.curated_images['default']
    
    def _build_mealdb_map(self) -> Dict[str, str]:
        """TheMealDB has real recipe images - FREE, no API key needed"""
        return {
            # Indian Dishes from TheMealDB
            'biryani': 'https://www.themealdb.com/images/media/meals/805ebc5411628d.jpg',
            'butter chicken': 'https://www.themealdb.com/images/media/meals/yqqqwu1511816912.jpg',
            'chicken tikka': 'https://www.themealdb.com/images/media/meals/wyxwsp1486979827.jpg',
            'tandoori chicken': 'https://www.themealdb.com/images/media/meals/qptpvt1487339892.jpg',
            'dal': 'https://www.themealdb.com/images/media/meals/wuxrtu1483564410.jpg',
            'samosa': 'https://www.themealdb.com/images/media/meals/ysqrus1487425681.jpg',
            'pakora': 'https://www.themealdb.com/images/media/meals/ysqrus1487425681.jpg',
            'naan': 'https://www.themealdb.com/images/media/meals/ysqrus1487425681.jpg',
            'curry': 'https://www.themealdb.com/images/media/meals/yqqqwu1511816912.jpg',
            'korma': 'https://www.themealdb.com/images/media/meals/qstyvs1505931190.jpg',
            'vindaloo': 'https://www.themealdb.com/images/media/meals/1550441275.jpg',
            'jalfrezi': 'https://www.themealdb.com/images/media/meals/1550441275.jpg',
            'rogan josh': 'https://www.themealdb.com/images/media/meals/1550441275.jpg',
            
            # Common dishes
            'pasta': 'https://www.themealdb.com/images/media/meals/ustsqw1468250014.jpg',
            'pizza': 'https://www.themealdb.com/images/media/meals/x0lk931587671540.jpg',
            'burger': 'https://www.themealdb.com/images/media/meals/k420tj1585565244.jpg',
            'salad': 'https://www.themealdb.com/images/media/meals/58oia61564916529.jpg',
            'soup': 'https://www.themealdb.com/images/media/meals/1529446352.jpg',
            'steak': 'https://www.themealdb.com/images/media/meals/1550441882.jpg',
            'fish': 'https://www.themealdb.com/images/media/meals/1520081754.jpg',
            'shrimp': 'https://www.themealdb.com/images/media/meals/1520084413.jpg',
            'chicken': 'https://www.themealdb.com/images/media/meals/yqqqwu1511816912.jpg',
            'beef': 'https://www.themealdb.com/images/media/meals/1550441882.jpg',
            'pork': 'https://www.themealdb.com/images/media/meals/1529445893.jpg',
            'lamb': 'https://www.themealdb.com/images/media/meals/1529445893.jpg',
            'rice': 'https://www.themealdb.com/images/media/meals/805ebc5411628d.jpg',
            'noodles': 'https://www.themealdb.com/images/media/meals/1529445893.jpg',
        }
    
    def _build_curated_map(self) -> Dict[str, str]:
        """
        Curated high-quality images from Pexels (FREE, no API key for direct URLs)
        These are permanent, stable URLs that work instantly
        """
        return {
            # INDIAN DISHES - High Quality Pexels Images
            'biryani': 'https://images.pexels.com/photos/1624487/pexels-photo-1624487.jpeg?auto=compress&cs=tinysrgb&w=600',
            'hyderabad': 'https://images.pexels.com/photos/1624487/pexels-photo-1624487.jpeg?auto=compress&cs=tinysrgb&w=600',
            'dum biryani': 'https://images.pexels.com/photos/1624487/pexels-photo-1624487.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'butter chicken': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
            'chicken makhani': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
            'chicken tikka masala': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
            'chicken curry': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'tandoori': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?auto=compress&cs=tinysrgb&w=600',
            'tandoori chicken': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'paneer': 'https://images.pexels.com/photos/6210876/pexels-photo-6210876.jpeg?auto=compress&cs=tinysrgb&w=600',
            'paneer tikka': 'https://images.pexels.com/photos/6210876/pexels-photo-6210876.jpeg?auto=compress&cs=tinysrgb&w=600',
            'paneer butter masala': 'https://images.pexels.com/photos/6210876/pexels-photo-6210876.jpeg?auto=compress&cs=tinysrgb&w=600',
            'palak paneer': 'https://images.pexels.com/photos/5560763/pexels-photo-5560763.jpeg?auto=compress&cs=tinysrgb&w=600',
            'kadai paneer': 'https://images.pexels.com/photos/6210876/pexels-photo-6210876.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'dosa': 'https://images.pexels.com/photos/5560763/pexels-photo-5560763.jpeg?auto=compress&cs=tinysrgb&w=600',
            'masala dosa': 'https://images.pexels.com/photos/5560763/pexels-photo-5560763.jpeg?auto=compress&cs=tinysrgb&w=600',
            'idli': 'https://images.pexels.com/photos/5560763/pexels-photo-5560763.jpeg?auto=compress&cs=tinysrgb&w=600',
            'idly': 'https://images.pexels.com/photos/5560763/pexels-photo-5560763.jpeg?auto=compress&cs=tinysrgb&w=600',
            'vada': 'https://images.pexels.com/photos/5560763/pexels-photo-5560763.jpeg?auto=compress&cs=tinysrgb&w=600',
            'uttapam': 'https://images.pexels.com/photos/5560763/pexels-photo-5560763.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'samosa': 'https://images.pexels.com/photos/6210876/pexels-photo-6210876.jpeg?auto=compress&cs=tinysrgb&w=600',
            'pakora': 'https://images.pexels.com/photos/6210876/pexels-photo-6210876.jpeg?auto=compress&cs=tinysrgb&w=600',
            'bhaji': 'https://images.pexels.com/photos/6210876/pexels-photo-6210876.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'dal': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
            'dal makhani': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
            'dal tadka': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
            'sambar': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'chole': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
            'rajma': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'pulao': 'https://images.pexels.com/photos/1624487/pexels-photo-1624487.jpeg?auto=compress&cs=tinysrgb&w=600',
            'pilaf': 'https://images.pexels.com/photos/1624487/pexels-photo-1624487.jpeg?auto=compress&cs=tinysrgb&w=600',
            'fried rice': 'https://images.pexels.com/photos/1624487/pexels-photo-1624487.jpeg?auto=compress&cs=tinysrgb&w=600',
            'lemon rice': 'https://images.pexels.com/photos/1624487/pexels-photo-1624487.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'naan': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
            'roti': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
            'paratha': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'gulab jamun': 'https://images.pexels.com/photos/1099680/pexels-photo-1099680.jpeg?auto=compress&cs=tinysrgb&w=600',
            'jalebi': 'https://images.pexels.com/photos/1099680/pexels-photo-1099680.jpeg?auto=compress&cs=tinysrgb&w=600',
            'kheer': 'https://images.pexels.com/photos/1099680/pexels-photo-1099680.jpeg?auto=compress&cs=tinysrgb&w=600',
            'halwa': 'https://images.pexels.com/photos/1099680/pexels-photo-1099680.jpeg?auto=compress&cs=tinysrgb&w=600',
            'ladoo': 'https://images.pexels.com/photos/1099680/pexels-photo-1099680.jpeg?auto=compress&cs=tinysrgb&w=600',
            'barfi': 'https://images.pexels.com/photos/1099680/pexels-photo-1099680.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            # GENERAL DISHES
            'pasta': 'https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg?auto=compress&cs=tinysrgb&w=600',
            'spaghetti': 'https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'pizza': 'https://images.pexels.com/photos/315755/pexels-photo-315755.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'burger': 'https://images.pexels.com/photos/1639557/pexels-photo-1639557.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'salad': 'https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'soup': 'https://images.pexels.com/photos/539451/pexels-photo-539451.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'steak': 'https://images.pexels.com/photos/361184/asparagus-steak-veal-steak-veal-361184.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'fish': 'https://images.pexels.com/photos/262959/pexels-photo-262959.jpeg?auto=compress&cs=tinysrgb&w=600',
            'salmon': 'https://images.pexels.com/photos/262959/pexels-photo-262959.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'shrimp': 'https://images.pexels.com/photos/566345/pexels-photo-566345.jpeg?auto=compress&cs=tinysrgb&w=600',
            'prawn': 'https://images.pexels.com/photos/566345/pexels-photo-566345.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'chicken': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?auto=compress&cs=tinysrgb&w=600',
            'beef': 'https://images.pexels.com/photos/361184/asparagus-steak-veal-steak-veal-361184.jpeg?auto=compress&cs=tinysrgb&w=600',
            'pork': 'https://images.pexels.com/photos/361184/asparagus-steak-veal-steak-veal-361184.jpeg?auto=compress&cs=tinysrgb&w=600',
            'lamb': 'https://images.pexels.com/photos/361184/asparagus-steak-veal-steak-veal-361184.jpeg?auto=compress&cs=tinysrgb&w=600',
            'mutton': 'https://images.pexels.com/photos/361184/asparagus-steak-veal-steak-veal-361184.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'rice': 'https://images.pexels.com/photos/1624487/pexels-photo-1624487.jpeg?auto=compress&cs=tinysrgb&w=600',
            'noodles': 'https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'egg': 'https://images.pexels.com/photos/1437267/pexels-photo-1437267.jpeg?auto=compress&cs=tinysrgb&w=600',
            'omelette': 'https://images.pexels.com/photos/1437267/pexels-photo-1437267.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'sandwich': 'https://images.pexels.com/photos/1639557/pexels-photo-1639557.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'taco': 'https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            'sushi': 'https://images.pexels.com/photos/357756/pexels-photo-357756.jpeg?auto=compress&cs=tinysrgb&w=600',
            
            # Defaults
            'default_indian': 'https://images.pexels.com/photos/1624487/pexels-photo-1624487.jpeg?auto=compress&cs=tinysrgb&w=600',
            'default': 'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=600',
        }
    
    def get_featured_recipes(self) -> List[Dict]:
        """Get top 12 famous Indian recipes with ACCURATE images"""
        return [
            {
                'id': 'featured_1',
                'name': 'Hyderabad Chicken Dum Biryani',
                'description': 'Main Course - Non Vegetarian - Andhra Cuisine',
                'cuisine': 'Andhra',
                'course': 'Main Course',
                'diet': 'Non Vegetarian',
                'prep_time': 30,
                'cook_time': 60,
                'servings': 6,
                'difficulty': 'medium',
                'image_url': 'https://images.pexels.com/photos/1624487/pexels-photo-1624487.jpeg?auto=compress&cs=tinysrgb&w=600',
                'ingredients': [
                    {'name': 'Basmati Rice', 'quantity': 2, 'unit': 'cups'},
                    {'name': 'Chicken', 'quantity': 500, 'unit': 'grams'},
                    {'name': 'Yogurt', 'quantity': 1, 'unit': 'cup'},
                ],
                'instructions': ['Marinate chicken with yogurt and spices', 'Cook rice until 70% done', 'Layer rice and chicken', 'Cook on dum for 45 minutes'],
                'algorithm_used': 'featured_recipe'
            },
            {
                'id': 'featured_2',
                'name': 'Butter Chicken',
                'description': 'Main Course - Non Vegetarian - North Indian Cuisine',
                'cuisine': 'North Indian',
                'course': 'Main Course',
                'diet': 'Non Vegetarian',
                'prep_time': 20,
                'cook_time': 40,
                'servings': 4,
                'difficulty': 'medium',
                'image_url': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
                'ingredients': [
                    {'name': 'Chicken', 'quantity': 500, 'unit': 'grams'},
                    {'name': 'Butter', 'quantity': 4, 'unit': 'tbsp'},
                    {'name': 'Cream', 'quantity': 1, 'unit': 'cup'},
                ],
                'instructions': ['Marinate chicken', 'Grill chicken', 'Prepare tomato gravy', 'Add chicken and simmer'],
                'algorithm_used': 'featured_recipe'
            },
            {
                'id': 'featured_3',
                'name': 'Masala Dosa',
                'description': 'Breakfast - Vegetarian - South Indian Cuisine',
                'cuisine': 'South Indian',
                'course': 'Breakfast',
                'diet': 'Vegetarian',
                'prep_time': 480,
                'cook_time': 30,
                'servings': 4,
                'difficulty': 'medium',
                'image_url': 'https://images.pexels.com/photos/5560763/pexels-photo-5560763.jpeg?auto=compress&cs=tinysrgb&w=600',
                'ingredients': [
                    {'name': 'Dosa Batter', 'quantity': 2, 'unit': 'cups'},
                    {'name': 'Potatoes', 'quantity': 4, 'unit': 'large'},
                ],
                'instructions': ['Ferment dosa batter overnight', 'Make potato masala', 'Spread batter on hot tawa', 'Add filling and fold'],
                'algorithm_used': 'featured_recipe'
            },
            {
                'id': 'featured_4',
                'name': 'Idli Sambar',
                'description': 'Breakfast - Vegetarian - South Indian Cuisine',
                'cuisine': 'South Indian',
                'course': 'Breakfast',
                'diet': 'Vegetarian',
                'prep_time': 480,
                'cook_time': 30,
                'servings': 4,
                'difficulty': 'medium',
                'image_url': 'https://images.pexels.com/photos/5560763/pexels-photo-5560763.jpeg?auto=compress&cs=tinysrgb&w=600',
                'ingredients': [
                    {'name': 'Idli Batter', 'quantity': 2, 'unit': 'cups'},
                    {'name': 'Toor Dal', 'quantity': 0.5, 'unit': 'cup'},
                ],
                'instructions': ['Ferment idli batter', 'Steam idlis', 'Prepare sambar with dal and vegetables', 'Serve hot'],
                'algorithm_used': 'featured_recipe'
            },
            {
                'id': 'featured_5',
                'name': 'Samosa',
                'description': 'Snack - Vegetarian - North Indian Cuisine',
                'cuisine': 'North Indian',
                'course': 'Snack',
                'diet': 'Vegetarian',
                'prep_time': 30,
                'cook_time': 30,
                'servings': 12,
                'difficulty': 'medium',
                'image_url': 'https://images.pexels.com/photos/6210876/pexels-photo-6210876.jpeg?auto=compress&cs=tinysrgb&w=600',
                'ingredients': [
                    {'name': 'All Purpose Flour', 'quantity': 2, 'unit': 'cups'},
                    {'name': 'Potatoes', 'quantity': 4, 'unit': 'large'},
                ],
                'instructions': ['Make dough', 'Prepare potato filling', 'Shape samosas', 'Deep fry until golden'],
                'algorithm_used': 'featured_recipe'
            },
            {
                'id': 'featured_6',
                'name': 'Chicken Tikka Masala',
                'description': 'Main Course - Non Vegetarian - North Indian Cuisine',
                'cuisine': 'North Indian',
                'course': 'Main Course',
                'diet': 'Non Vegetarian',
                'prep_time': 30,
                'cook_time': 40,
                'servings': 4,
                'difficulty': 'medium',
                'image_url': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
                'ingredients': [
                    {'name': 'Chicken', 'quantity': 500, 'unit': 'grams'},
                    {'name': 'Tikka Masala', 'quantity': 2, 'unit': 'tbsp'},
                ],
                'instructions': ['Marinate chicken in yogurt and spices', 'Grill chicken tikka', 'Prepare masala gravy', 'Add tikka to gravy'],
                'algorithm_used': 'featured_recipe'
            },
            {
                'id': 'featured_7',
                'name': 'Tandoori Chicken',
                'description': 'Appetizer - Non Vegetarian - Punjabi Cuisine',
                'cuisine': 'Punjabi',
                'course': 'Appetizer',
                'diet': 'Non Vegetarian',
                'prep_time': 240,
                'cook_time': 30,
                'servings': 4,
                'difficulty': 'medium',
                'image_url': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?auto=compress&cs=tinysrgb&w=600',
                'ingredients': [
                    {'name': 'Chicken', 'quantity': 1, 'unit': 'kg'},
                    {'name': 'Yogurt', 'quantity': 1, 'unit': 'cup'},
                    {'name': 'Tandoori Masala', 'quantity': 3, 'unit': 'tbsp'},
                ],
                'instructions': ['Marinate chicken for 4 hours', 'Preheat oven to 200°C', 'Grill until charred', 'Serve with mint chutney'],
                'algorithm_used': 'featured_recipe'
            },
            {
                'id': 'featured_8',
                'name': 'Lemon Rice',
                'description': 'Main Course - Vegetarian - South Indian Cuisine',
                'cuisine': 'South Indian',
                'course': 'Main Course',
                'diet': 'Vegetarian',
                'prep_time': 10,
                'cook_time': 20,
                'servings': 4,
                'difficulty': 'easy',
                'image_url': 'https://images.pexels.com/photos/1624487/pexels-photo-1624487.jpeg?auto=compress&cs=tinysrgb&w=600',
                'ingredients': [
                    {'name': 'Rice', 'quantity': 2, 'unit': 'cups'},
                    {'name': 'Lemon', 'quantity': 2, 'unit': 'large'},
                ],
                'instructions': ['Cook rice', 'Temper mustard seeds and curry leaves', 'Add turmeric', 'Mix with lemon juice'],
                'algorithm_used': 'featured_recipe'
            },
            {
                'id': 'featured_9',
                'name': 'Paneer Butter Masala',
                'description': 'Main Course - Vegetarian - North Indian Cuisine',
                'cuisine': 'North Indian',
                'course': 'Main Course',
                'diet': 'Vegetarian',
                'prep_time': 15,
                'cook_time': 30,
                'servings': 4,
                'difficulty': 'easy',
                'image_url': 'https://images.pexels.com/photos/6210876/pexels-photo-6210876.jpeg?auto=compress&cs=tinysrgb&w=600',
                'ingredients': [
                    {'name': 'Paneer', 'quantity': 400, 'unit': 'grams'},
                    {'name': 'Butter', 'quantity': 3, 'unit': 'tbsp'},
                    {'name': 'Cream', 'quantity': 0.5, 'unit': 'cup'},
                ],
                'instructions': ['Cut paneer into cubes', 'Prepare tomato gravy', 'Add butter and cream', 'Add paneer and simmer'],
                'algorithm_used': 'featured_recipe'
            },
            {
                'id': 'featured_10',
                'name': 'Dal Makhani',
                'description': 'Main Course - Vegetarian - Punjabi Cuisine',
                'cuisine': 'Punjabi',
                'course': 'Main Course',
                'diet': 'Vegetarian',
                'prep_time': 480,
                'cook_time': 60,
                'servings': 6,
                'difficulty': 'medium',
                'image_url': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
                'ingredients': [
                    {'name': 'Black Lentils', 'quantity': 1, 'unit': 'cup'},
                    {'name': 'Kidney Beans', 'quantity': 0.25, 'unit': 'cup'},
                    {'name': 'Butter', 'quantity': 4, 'unit': 'tbsp'},
                ],
                'instructions': ['Soak lentils overnight', 'Pressure cook until soft', 'Prepare gravy', 'Simmer with butter and cream'],
                'algorithm_used': 'featured_recipe'
            },
            {
                'id': 'featured_11',
                'name': 'Chole Bhature',
                'description': 'Main Course - Vegetarian - Punjabi Cuisine',
                'cuisine': 'Punjabi',
                'course': 'Main Course',
                'diet': 'Vegetarian',
                'prep_time': 480,
                'cook_time': 45,
                'servings': 4,
                'difficulty': 'medium',
                'image_url': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?auto=compress&cs=tinysrgb&w=600',
                'ingredients': [
                    {'name': 'Chickpeas', 'quantity': 2, 'unit': 'cups'},
                    {'name': 'All Purpose Flour', 'quantity': 2, 'unit': 'cups'},
                ],
                'instructions': ['Soak chickpeas overnight', 'Pressure cook chickpeas', 'Prepare spicy gravy', 'Make bhature dough and fry'],
                'algorithm_used': 'featured_recipe'
            },
            {
                'id': 'featured_12',
                'name': 'Gulab Jamun',
                'description': 'Dessert - Vegetarian - Indian Cuisine',
                'cuisine': 'Indian',
                'course': 'Dessert',
                'diet': 'Vegetarian',
                'prep_time': 20,
                'cook_time': 30,
                'servings': 12,
                'difficulty': 'medium',
                'image_url': 'https://images.pexels.com/photos/1099680/pexels-photo-1099680.jpeg?auto=compress&cs=tinysrgb&w=600',
                'ingredients': [
                    {'name': 'Milk Powder', 'quantity': 1, 'unit': 'cup'},
                    {'name': 'All Purpose Flour', 'quantity': 0.25, 'unit': 'cup'},
                    {'name': 'Sugar', 'quantity': 2, 'unit': 'cups'},
                ],
                'instructions': ['Make dough with milk powder', 'Shape into small balls', 'Deep fry until golden', 'Soak in sugar syrup'],
                'algorithm_used': 'featured_recipe'
            }
        ]


# Global instance
_enhanced_service = None

def get_enhanced_image_service() -> EnhancedImageService:
    """Get or create Enhanced Image Service instance"""
    global _enhanced_service
    if _enhanced_service is None:
        _enhanced_service = EnhancedImageService()
    return _enhanced_service
