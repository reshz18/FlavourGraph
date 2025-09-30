'use client'

import { useState, useEffect } from "react"
import { createClient } from "@/lib/supabase/client"
import { useRouter } from "next/navigation"
import { RecipeCard } from "@/components/recipe-card"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
// Using emoji alternatives to avoid Lucide React TypeScript issues
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { useToast } from "@/hooks/use-toast"

interface Recipe {
  id: string
  name: string
  description: string
  ingredients: Array<{ name: string; quantity?: number; unit?: string }>
  instructions: string[]
  prep_time?: number
  cook_time?: number
  servings?: number
  difficulty?: string
  cuisine?: string
  image_url?: string
  match_score?: number
  missing_ingredients?: string[]
  substitution_suggestions?: Record<string, string[]>
  algorithm_used?: string
}

interface AlgorithmStats {
  graph_traversals: number
  greedy_selections: number
  backtracking_calls: number
  total_execution_time: number
}

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null)
  const [recipes, setRecipes] = useState<Recipe[]>([])
  const [loading, setLoading] = useState(true)
  const [searching, setSearching] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [ingredients, setIngredients] = useState("")
  const [algorithmStats, setAlgorithmStats] = useState<AlgorithmStats | null>(null)
  const [backendConnected, setBackendConnected] = useState(false)
  
  const router = useRouter()
  const { toast } = useToast()
  const supabase = createClient()

  // Check authentication and load initial data
  useEffect(() => {
    checkAuth()
    checkBackendConnection()
    loadInitialRecipes()
  }, [])

  const checkAuth = async () => {
    const { data: { user }, error } = await supabase.auth.getUser()
    if (error || !user) {
      router.push("/auth/login")
      return
    }
    setUser(user)
  }

  const checkBackendConnection = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/health', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      })
      if (response.ok) {
        setBackendConnected(true)
      } else {
        throw new Error('Backend not responding')
      }
    } catch (error) {
      console.log('Backend not available')
      setBackendConnected(false)
    }
  }

  const loadInitialRecipes = async () => {
    setLoading(true)
    try {
      // Always try backend first
      const response = await fetch('http://localhost:8000/api/recipes/search?limit=12')
      if (response.ok) {
        const data = await response.json()
        console.log('Initial recipes loaded:', data)
        setRecipes(data.recipes || [])
        setBackendConnected(true)
      } else {
        throw new Error('Backend request failed')
      }
    } catch (error) {
      console.error('Error loading recipes:', error)
      setRecipes([])  // No fallback recipes
      setBackendConnected(false)
    } finally {
      setLoading(false)
    }
  }

  const getSampleRecipes = (): Recipe[] => []

  const searchRecipesByIngredients = async () => {
    if (!ingredients.trim()) {
      toast({
        title: "Please enter ingredients",
        description: "Add some ingredients to find matching recipes!",
        variant: "destructive"
      })
      return
    }

    setSearching(true)
    try {
      const ingredientList = ingredients.split(',').map(i => i.trim()).filter(i => i)
      
      if (backendConnected) {
        // Use Python backend with algorithms
        const recipesResponse = await fetch('http://localhost:8000/api/recipes/suggest', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            available_ingredients: ingredientList,
            max_recipes: 12
          })
        })

        if (recipesResponse.ok) {
          const recipesData = await recipesResponse.json()
          console.log('Recipes received:', recipesData)
          setRecipes(recipesData)
          
          if (recipesData.length > 0) {
            toast({
              title: "Recipes Found",
              description: `Found ${recipesData.length} recipes`,
            })
          } else {
            toast({
              title: "No Recipes Found",
              description: "Try different ingredients or check backend connection",
              variant: "destructive"
            })
          }
        }

        // Algorithm stats removed - no longer needed
      } else {
        // Fallback search
        const filtered = getSampleRecipes().filter(recipe =>
          recipe.ingredients.some(ing =>
            ingredientList.some(searchIng =>
              ing.name.toLowerCase().includes(searchIng.toLowerCase())
            )
          )
        )
        setRecipes(filtered)
        
        toast({
          title: "Search Results",
          description: `Found ${filtered.length} matching recipes`,
        })
      }
    } catch (error) {
      console.error('Search error:', error)
      toast({
        title: "Search Error",
        description: "Failed to search recipes. Please try again.",
        variant: "destructive"
      })
    } finally {
      setSearching(false)
    }
  }

  const searchRecipesByQuery = async () => {
    if (!searchQuery.trim()) return

    setSearching(true)
    try {
      const response = await fetch(`http://localhost:8000/api/recipes/search?query=${encodeURIComponent(searchQuery)}&limit=12`)
      if (response.ok) {
        const data = await response.json()
        console.log('Query search results:', data)
        setRecipes(data.recipes || [])
        
        if (data.recipes && data.recipes.length > 0) {
          toast({
            title: "Recipes Found",
            description: `Found ${data.recipes.length} recipes`,
          })
        } else {
          toast({
            title: "No Recipes Found",
            description: "Try a different search term",
            variant: "destructive"
          })
        }
      } else {
        setRecipes([])
        toast({
          title: "Search Failed",
          description: "Backend connection error",
          variant: "destructive"
        })
      }
    } catch (error) {
      console.error('Query search error:', error)
      setRecipes([])
    } finally {
      setSearching(false)
    }
  }

  if (loading) {
    return (
      <div className="flex-1 w-full max-w-6xl mx-auto p-6 flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <p className="text-lg">Loading your recipe dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 w-full max-w-6xl mx-auto p-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            FlavorGraph Dashboard
          </h1>
          <p className="text-muted-foreground">
            Welcome back, {user?.email}! Discover recipes with AI-powered algorithms.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant={backendConnected ? "default" : "secondary"}>
            {backendConnected ? "API Connected" : "Offline Mode"}
          </Badge>
          <Button 
            className="w-fit"
            onClick={() => {
              toast({
                title: "Add Recipe Feature",
                description: "Start by entering ingredients in the search box below to discover recipes!",
              })
              // Focus on the ingredients input
              const input = document.querySelector('input[placeholder*="Enter ingredients"]') as HTMLInputElement
              if (input) input.focus()
            }}
          >
            Add Recipe
          </Button>
        </div>
      </div>


      {/* Ingredient Search */}
      <Card>
        <CardHeader>
          <CardTitle>
            Recipe Search
          </CardTitle>
          <CardDescription>
            Search by ingredients or recipe name to find matching recipes
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-2">
            <Input 
              placeholder="Enter ingredients (comma-separated): chicken, tomato, onion..." 
              className="flex-1"
              value={ingredients}
              onChange={(e) => setIngredients(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && searchRecipesByIngredients()}
            />
            <Button onClick={searchRecipesByIngredients} disabled={searching}>
              {searching ? 'Searching...' : 'Find Recipes'}
            </Button>
          </div>
          
          <div className="flex gap-2">
            <Input 
              placeholder="Or search by recipe name..." 
              className="flex-1"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && searchRecipesByQuery()}
            />
            <Button variant="outline" onClick={searchRecipesByQuery} disabled={searching}>
              Search
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Recipe Grid */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-semibold">
            {ingredients ? 'Recommended Recipes' : 'Featured Recipes'} ({recipes.length})
          </h2>
          {recipes.length > 0 && (
            <Button variant="outline" onClick={loadInitialRecipes}>
              Reset
            </Button>
          )}
        </div>
        
        {recipes.length === 0 ? (
          <Card className="p-8 text-center">
            <div className="text-muted-foreground">
              <p className="text-lg mb-2">No recipes found</p>
              <p>Try searching with different ingredients or recipe names</p>
            </div>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recipes.map((recipe) => (
              <div key={recipe.id} className="relative">
                <RecipeCard recipe={recipe} />
                
                {/* Algorithm Badges */}
                {recipe.match_score !== undefined && (
                  <div className="absolute top-2 right-2 flex flex-col gap-1">
                    <Badge variant="secondary" className="text-xs">
                      Match: {(recipe.match_score * 100).toFixed(0)}%
                    </Badge>
                    {recipe.algorithm_used && (
                      <Badge variant="outline" className="text-xs">
                        {recipe.algorithm_used}
                      </Badge>
                    )}
                  </div>
                )}
                
                {/* Substitution Suggestions */}
                {recipe.substitution_suggestions && Object.keys(recipe.substitution_suggestions).length > 0 && (
                  <div className="mt-2 p-2 bg-yellow-50 rounded text-xs">
                    <strong>💡 Substitutions:</strong>
                    {Object.entries(recipe.substitution_suggestions).slice(0, 2).map(([ingredient, subs]) => (
                      <div key={ingredient} className="truncate">
                        {ingredient} → {subs.slice(0, 2).join(', ')}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
