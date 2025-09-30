"""
Graph Theory Implementation for Ingredient Relationships
Uses NetworkX for graph operations and analysis
"""

import networkx as nx
import numpy as np
from typing import List, Dict, Tuple, Set, Optional
import json
import os
from collections import defaultdict
import logging
from fuzzywuzzy import fuzz

logger = logging.getLogger(__name__)

class IngredientGraphService:
    """
    Implements graph theory for ingredient relationship analysis
    
    Graph Structure:
    - Nodes: Ingredients
    - Edges: Relationships (substitution, complementary, category-based)
    - Weights: Similarity scores, substitution viability
    """
    
    def __init__(self):
        self.ingredient_graph = nx.Graph()
        self.category_graph = nx.Graph()
        self.substitution_graph = nx.DiGraph()  # Directed for substitution relationships
        
        # Ingredient categories and relationships
        self.ingredient_categories = {}
        self.substitution_rules = {}
        self.complementary_pairs = set()
        
        self._initialize_base_data()
    
    def _initialize_base_data(self):
        """Initialize base ingredient data and relationships"""
        
        # Base ingredient categories
        self.base_categories = {
            "proteins": ["chicken", "beef", "pork", "fish", "tofu", "eggs", "beans", "lentils"],
            "vegetables": ["onion", "garlic", "tomato", "carrot", "potato", "bell pepper", "broccoli"],
            "grains": ["rice", "pasta", "bread", "quinoa", "oats", "flour"],
            "dairy": ["milk", "cheese", "butter", "yogurt", "cream"],
            "spices": ["salt", "pepper", "cumin", "paprika", "oregano", "basil", "thyme"],
            "oils": ["olive oil", "vegetable oil", "coconut oil", "butter"],
            "herbs": ["parsley", "cilantro", "mint", "rosemary", "sage", "dill"]
        }
        
        # Substitution rules with similarity scores
        self.base_substitutions = {
            "chicken": [("turkey", 0.9), ("tofu", 0.6), ("mushrooms", 0.4)],
            "beef": [("pork", 0.8), ("lamb", 0.8), ("mushrooms", 0.5)],
            "milk": [("almond milk", 0.8), ("soy milk", 0.8), ("coconut milk", 0.7)],
            "butter": [("olive oil", 0.7), ("coconut oil", 0.7), ("margarine", 0.9)],
            "onion": [("shallot", 0.9), ("leek", 0.7), ("garlic", 0.6)],
            "garlic": [("garlic powder", 0.8), ("onion", 0.6), ("shallot", 0.7)]
        }
        
        # Complementary ingredient pairs
        self.base_complementary = [
            ("tomato", "basil"), ("garlic", "onion"), ("lemon", "herbs"),
            ("cheese", "pasta"), ("rice", "beans"), ("chicken", "herbs")
        ]
    
    async def build_ingredient_graph(self):
        """
        Build the ingredient relationship graph using graph theory principles
        """
        logger.info("Building ingredient relationship graph...")
        
        # Clear existing graphs
        self.ingredient_graph.clear()
        self.category_graph.clear()
        self.substitution_graph.clear()
        
        # Add ingredient nodes with categories
        for category, ingredients in self.base_categories.items():
            for ingredient in ingredients:
                self.ingredient_graph.add_node(
                    ingredient,
                    category=category,
                    centrality=0.0,
                    substitution_score=0.0
                )
                self.ingredient_categories[ingredient] = category
        
        # Add substitution edges (directed graph)
        for ingredient, substitutions in self.base_substitutions.items():
            for substitute, score in substitutions:
                if ingredient in self.ingredient_graph and substitute in self.ingredient_graph:
                    self.substitution_graph.add_edge(
                        ingredient, substitute,
                        weight=score,
                        relationship_type="substitution"
                    )
                    
                    # Add bidirectional edge in main graph with lower weight
                    self.ingredient_graph.add_edge(
                        ingredient, substitute,
                        weight=score * 0.8,  # Slightly lower for reverse substitution
                        relationship_type="substitution"
                    )
        
        # Add complementary edges
        for ing1, ing2 in self.base_complementary:
            if ing1 in self.ingredient_graph and ing2 in self.ingredient_graph:
                self.ingredient_graph.add_edge(
                    ing1, ing2,
                    weight=0.8,
                    relationship_type="complementary"
                )
        
        # Add category-based edges (ingredients in same category)
        for category, ingredients in self.base_categories.items():
            for i, ing1 in enumerate(ingredients):
                for ing2 in ingredients[i+1:]:
                    if not self.ingredient_graph.has_edge(ing1, ing2):
                        self.ingredient_graph.add_edge(
                            ing1, ing2,
                            weight=0.5,  # Lower weight for category similarity
                            relationship_type="category"
                        )
        
        # Calculate centrality measures
        self._calculate_graph_metrics()
        
        logger.info(f"Graph built with {self.ingredient_graph.number_of_nodes()} nodes and {self.ingredient_graph.number_of_edges()} edges")
    
    def _calculate_graph_metrics(self):
        """Calculate graph theory metrics for ingredients"""
        
        # Betweenness centrality - ingredients that connect different groups
        betweenness = nx.betweenness_centrality(self.ingredient_graph, weight='weight')
        
        # Degree centrality - how connected an ingredient is
        degree = nx.degree_centrality(self.ingredient_graph)
        
        # PageRank - importance based on connections
        pagerank = nx.pagerank(self.ingredient_graph, weight='weight')
        
        # Update node attributes
        for node in self.ingredient_graph.nodes():
            self.ingredient_graph.nodes[node]['betweenness_centrality'] = betweenness.get(node, 0)
            self.ingredient_graph.nodes[node]['degree_centrality'] = degree.get(node, 0)
            self.ingredient_graph.nodes[node]['pagerank'] = pagerank.get(node, 0)
    
    async def find_ingredient_substitutions(self, ingredient: str, limit: int = 5) -> List[Dict]:
        """
        Find ingredient substitutions using graph traversal
        
        Uses:
        - Shortest path algorithms
        - Weighted edge traversal
        - Similarity scoring
        """
        ingredient = ingredient.lower()
        substitutions = []
        
        if ingredient not in self.ingredient_graph:
            # Try fuzzy matching
            best_match = self._fuzzy_match_ingredient(ingredient)
            if best_match:
                ingredient = best_match
            else:
                return []
        
        # Direct substitutions from substitution graph
        if ingredient in self.substitution_graph:
            for neighbor in self.substitution_graph.neighbors(ingredient):
                edge_data = self.substitution_graph[ingredient][neighbor]
                substitutions.append({
                    "ingredient": neighbor,
                    "similarity_score": edge_data['weight'],
                    "relationship_type": "direct_substitution",
                    "category": self.ingredient_categories.get(neighbor, "unknown")
                })
        
        # Find substitutions through graph traversal (2-hop neighbors)
        for neighbor in self.ingredient_graph.neighbors(ingredient):
            if len(substitutions) >= limit:
                break
                
            edge_data = self.ingredient_graph[ingredient][neighbor]
            if edge_data['relationship_type'] == 'substitution':
                continue  # Already added above
            
            # Check second-degree connections
            for second_neighbor in self.ingredient_graph.neighbors(neighbor):
                if second_neighbor != ingredient and len(substitutions) < limit:
                    # Calculate path-based similarity
                    path_weight = (
                        self.ingredient_graph[ingredient][neighbor]['weight'] *
                        self.ingredient_graph[neighbor][second_neighbor]['weight']
                    )
                    
                    substitutions.append({
                        "ingredient": second_neighbor,
                        "similarity_score": path_weight * 0.7,  # Reduce for indirect
                        "relationship_type": "indirect_substitution",
                        "category": self.ingredient_categories.get(second_neighbor, "unknown"),
                        "path": [ingredient, neighbor, second_neighbor]
                    })
        
        # Sort by similarity score and return top results
        substitutions.sort(key=lambda x: x['similarity_score'], reverse=True)
        return substitutions[:limit]
    
    def _fuzzy_match_ingredient(self, ingredient: str) -> Optional[str]:
        """Find closest matching ingredient using fuzzy string matching"""
        best_match = None
        best_score = 0
        
        for graph_ingredient in self.ingredient_graph.nodes():
            score = fuzz.ratio(ingredient.lower(), graph_ingredient.lower())
            if score > best_score and score > 70:  # Threshold for acceptable match
                best_score = score
                best_match = graph_ingredient
        
        return best_match
    
    def find_complementary_ingredients(self, ingredients: List[str]) -> List[str]:
        """
        Find ingredients that complement the given ingredients
        Uses graph traversal to find highly connected ingredients
        """
        complementary = set()
        
        for ingredient in ingredients:
            ingredient = ingredient.lower()
            if ingredient in self.ingredient_graph:
                # Find neighbors with complementary relationships
                for neighbor in self.ingredient_graph.neighbors(ingredient):
                    edge_data = self.ingredient_graph[ingredient][neighbor]
                    if edge_data['relationship_type'] == 'complementary':
                        complementary.add(neighbor)
        
        return list(complementary)
    
    def calculate_ingredient_similarity(self, ing1: str, ing2: str) -> float:
        """
        Calculate similarity between two ingredients using graph metrics
        """
        ing1, ing2 = ing1.lower(), ing2.lower()
        
        if ing1 not in self.ingredient_graph or ing2 not in self.ingredient_graph:
            return 0.0
        
        # Direct edge weight
        if self.ingredient_graph.has_edge(ing1, ing2):
            return self.ingredient_graph[ing1][ing2]['weight']
        
        # Shortest path similarity
        try:
            path_length = nx.shortest_path_length(
                self.ingredient_graph, ing1, ing2, weight='weight'
            )
            # Convert path length to similarity (shorter path = higher similarity)
            similarity = 1.0 / (1.0 + path_length)
            return similarity
        except nx.NetworkXNoPath:
            return 0.0
    
    def get_ingredient_centrality(self, ingredient: str) -> Dict[str, float]:
        """Get centrality metrics for an ingredient"""
        ingredient = ingredient.lower()
        
        if ingredient not in self.ingredient_graph:
            return {}
        
        node_data = self.ingredient_graph.nodes[ingredient]
        return {
            "betweenness_centrality": node_data.get('betweenness_centrality', 0),
            "degree_centrality": node_data.get('degree_centrality', 0),
            "pagerank": node_data.get('pagerank', 0)
        }
    
    def is_healthy(self) -> bool:
        """Check if the graph service is healthy"""
        return (
            self.ingredient_graph.number_of_nodes() > 0 and
            self.ingredient_graph.number_of_edges() > 0
        )
