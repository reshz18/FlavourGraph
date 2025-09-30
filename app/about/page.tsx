import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import Link from "next/link"
import { ChefHatIcon, SearchIcon, BookOpenIcon, UsersIcon, StarIcon, TrendingUpIcon } from "lucide-react"

export default function AboutPage() {
  const features = [
    {
      icon: <SearchIcon className="h-6 w-6" />,
      title: "Smart Recipe Search",
      description: "Find recipes using natural language queries and ingredient-based searches"
    },
    {
      icon: <BookOpenIcon className="h-6 w-6" />,
      title: "Recipe Management",
      description: "Save, organize, and manage your favorite recipes in one place"
    },
    {
      icon: <UsersIcon className="h-6 w-6" />,
      title: "Community Driven",
      description: "Share recipes with the community and discover new favorites"
    },
    {
      icon: <StarIcon className="h-6 w-6" />,
      title: "Personalized Recommendations",
      description: "Get recipe suggestions based on your preferences and dietary needs"
    },
    {
      icon: <TrendingUpIcon className="h-6 w-6" />,
      title: "Trending Recipes",
      description: "Stay up-to-date with the latest trending recipes and cooking techniques"
    },
    {
      icon: <ChefHatIcon className="h-6 w-6" />,
      title: "Chef-Curated Content",
      description: "Access recipes and tips from professional chefs and cooking experts"
    }
  ]

  return (
    <div className="flex-1 w-full max-w-6xl mx-auto p-6 space-y-12">
      {/* Hero Section */}
      <div className="text-center space-y-6">
        <div className="space-y-4">
          <Badge variant="secondary" className="text-sm px-3 py-1">
            About FlavorGraph
          </Badge>
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
            Your Intelligent Recipe Navigator
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            FlavorGraph revolutionizes how you discover, organize, and enjoy cooking. 
            Our intelligent platform connects you with recipes that match your taste, 
            dietary preferences, and cooking skill level.
          </p>
        </div>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/auth/sign-up">
            <Button size="lg" className="text-lg px-8 py-6">
              Get Started Free
            </Button>
          </Link>
          <Link href="/dashboard">
            <Button variant="outline" size="lg" className="text-lg px-8 py-6">
              Explore Recipes
            </Button>
          </Link>
        </div>
      </div>

      {/* Features Grid */}
      <div className="space-y-8">
        <div className="text-center space-y-4">
          <h2 className="text-3xl font-bold tracking-tight">Why Choose FlavorGraph?</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            We've built the most comprehensive recipe platform with features designed 
            to make cooking more enjoyable and accessible for everyone.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card key={index} className="h-full">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-primary/10 rounded-lg text-primary">
                    {feature.icon}
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Mission Statement */}
      <Card className="bg-gradient-to-r from-primary/5 to-secondary/5 border-0">
        <CardHeader className="text-center pb-4">
          <CardTitle className="text-2xl">Our Mission</CardTitle>
        </CardHeader>
        <CardContent className="text-center space-y-4">
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
            At FlavorGraph, we believe that great food brings people together. Our mission is to 
            make cooking accessible, enjoyable, and inspiring for home cooks of all skill levels. 
            We're building a community where food lovers can discover new flavors, share their 
            culinary creations, and connect through the universal language of food.
          </p>
          <div className="flex flex-wrap justify-center gap-2 pt-4">
            <Badge variant="outline">Community Driven</Badge>
            <Badge variant="outline">AI Powered</Badge>
            <Badge variant="outline">Chef Approved</Badge>
            <Badge variant="outline">Always Free</Badge>
          </div>
        </CardContent>
      </Card>

      {/* Stats Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
        <Card>
          <CardContent className="pt-6">
            <div className="text-3xl font-bold text-primary">10+</div>
            <p className="text-muted-foreground">Curated Recipes</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-3xl font-bold text-primary">10+</div>
            <p className="text-muted-foreground">Happy Cooks</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-3xl font-bold text-primary">5+</div>
            <p className="text-muted-foreground">Meals Prepared</p>
          </CardContent>
        </Card>
      </div>

      {/* CTA Section */}
      <Card className="text-center">
        <CardContent className="pt-8 pb-8 space-y-4">
          <h3 className="text-2xl font-bold">Ready to Start Cooking?</h3>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Join thousands of home cooks who have already discovered their new favorite recipes on FlavorGraph.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <Link href="/auth/sign-up">
              <Button size="lg">Create Free Account</Button>
            </Link>
            <Link href="/dashboard">
              <Button variant="outline" size="lg">Browse Recipes</Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
