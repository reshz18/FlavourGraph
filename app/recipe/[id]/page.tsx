"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Clock, Users, ChefHat } from "lucide-react"

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
  match_percentage?: number
  matched_ingredients?: string[]
  missing_ingredients?: string[]
  total_matched?: number
  total_user_ingredients?: number
  course?: string
  diet?: string
}

export default function RecipeDetailPage() {
  const params = useParams()
  const router = useRouter()
  const [recipe, setRecipe] = useState<Recipe | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Get recipe from localStorage (passed from dashboard)
    const storedRecipe = localStorage.getItem(`recipe_${params.id}`)
    if (storedRecipe) {
      setRecipe(JSON.parse(storedRecipe))
    }
    setLoading(false)
  }, [params.id])

  if (loading) {
    return (
      <div className="container mx-auto py-8">
        <div className="text-center">Loading recipe...</div>
      </div>
    )
  }

  if (!recipe) {
    return (
      <div className="container mx-auto py-8">
        <Card className="p-8 text-center">
          <p className="text-lg mb-4">Recipe not found</p>
          <Button onClick={() => router.push('/dashboard')}>
            Back to Dashboard
          </Button>
        </Card>
      </div>
    )
  }

  const totalTime = (recipe.prep_time || 0) + (recipe.cook_time || 0)

  return (
    <div className="container mx-auto py-8 px-4">
      {/* Back Button */}
      <Button
        variant="ghost"
        onClick={() => router.push('/dashboard')}
        className="mb-6"
      >
        <ArrowLeft className="mr-2 h-4 w-4" />
        Back to Recipes
      </Button>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Header */}
          <Card>
            <CardHeader>
              {recipe.image_url && (
                <div className="relative w-full h-64 md:h-96 rounded-lg overflow-hidden mb-4">
                  <img
                    src={recipe.image_url}
                    alt={recipe.name}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.currentTarget.src = 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800&h=600&fit=crop'
                    }}
                  />
                  {recipe.match_percentage !== undefined && (
                    <Badge 
                      className="absolute top-4 right-4 text-lg px-4 py-2"
                      variant={recipe.match_percentage >= 80 ? "default" : recipe.match_percentage >= 50 ? "secondary" : "outline"}
                    >
                      {recipe.match_percentage.toFixed(0)}% Match
                    </Badge>
                  )}
                </div>
              )}
              
              <CardTitle className="text-3xl md:text-4xl">{recipe.name}</CardTitle>
              <CardDescription className="text-lg">{recipe.description}</CardDescription>
              
              <div className="flex flex-wrap gap-2 mt-4">
                {recipe.cuisine && (
                  <Badge variant="outline">{recipe.cuisine}</Badge>
                )}
                {recipe.course && (
                  <Badge variant="outline">{recipe.course}</Badge>
                )}
                {recipe.diet && (
                  <Badge variant="secondary">{recipe.diet}</Badge>
                )}
                {recipe.difficulty && (
                  <Badge variant="outline">{recipe.difficulty}</Badge>
                )}
              </div>
            </CardHeader>
          </Card>

          {/* Ingredients */}
          <Card>
            <CardHeader>
              <CardTitle className="text-2xl">Ingredients</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {recipe.ingredients.map((ingredient, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-primary mr-3">•</span>
                    <span className="flex-1">
                      <span className="font-medium">{ingredient.name}</span>
                      {ingredient.quantity && ingredient.unit && (
                        <span className="text-muted-foreground ml-2">
                          ({ingredient.quantity} {ingredient.unit})
                        </span>
                      )}
                    </span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Instructions */}
          <Card>
            <CardHeader>
              <CardTitle className="text-2xl">Instructions</CardTitle>
            </CardHeader>
            <CardContent>
              <ol className="space-y-4">
                {recipe.instructions.map((instruction, index) => (
                  <li key={index} className="flex items-start">
                    <span className="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center mr-4 font-bold">
                      {index + 1}
                    </span>
                    <p className="flex-1 pt-1">{instruction}</p>
                  </li>
                ))}
              </ol>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Recipe Info */}
          <Card>
            <CardHeader>
              <CardTitle>Recipe Info</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {recipe.prep_time && (
                <div className="flex items-center gap-3">
                  <Clock className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm text-muted-foreground">Prep Time</p>
                    <p className="font-medium">{recipe.prep_time} mins</p>
                  </div>
                </div>
              )}
              
              {recipe.cook_time && (
                <div className="flex items-center gap-3">
                  <ChefHat className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm text-muted-foreground">Cook Time</p>
                    <p className="font-medium">{recipe.cook_time} mins</p>
                  </div>
                </div>
              )}
              
              {totalTime > 0 && (
                <div className="flex items-center gap-3">
                  <Clock className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm text-muted-foreground">Total Time</p>
                    <p className="font-medium">{totalTime} mins</p>
                  </div>
                </div>
              )}
              
              {recipe.servings && (
                <div className="flex items-center gap-3">
                  <Users className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm text-muted-foreground">Servings</p>
                    <p className="font-medium">{recipe.servings} people</p>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Match Information */}
          {recipe.total_matched !== undefined && recipe.total_user_ingredients !== undefined && (
            <Card>
              <CardHeader>
                <CardTitle>Your Ingredients</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center">
                  <div className="text-4xl font-bold text-primary">
                    {recipe.total_matched}/{recipe.total_user_ingredients}
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">
                    Ingredients you have
                  </p>
                </div>

                {recipe.matched_ingredients && recipe.matched_ingredients.length > 0 && (
                  <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                    <p className="font-semibold text-green-700 mb-2">✓ You have:</p>
                    <div className="flex flex-wrap gap-2">
                      {recipe.matched_ingredients.map((ing, idx) => (
                        <Badge key={idx} variant="outline" className="bg-white">
                          {ing}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {recipe.missing_ingredients && recipe.missing_ingredients.length > 0 && (
                  <div className="p-3 bg-orange-50 border border-orange-200 rounded-lg">
                    <p className="font-semibold text-orange-700 mb-2">🛒 You need:</p>
                    <div className="flex flex-wrap gap-2">
                      {recipe.missing_ingredients.map((ing, idx) => (
                        <Badge key={idx} variant="outline" className="bg-white">
                          {ing}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
