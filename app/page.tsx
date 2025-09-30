import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function Index() {
  return (
    <div className="w-full min-h-screen flex flex-col items-center justify-center text-center p-6 bg-background">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="space-y-6">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-primary tracking-tight">
            Welcome to FlavorGraph
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto">
            Your intelligent recipe navigator. Discover amazing recipes, manage your pantry, and explore new flavors.
          </p>
        </div>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/dashboard">
            <Button size="lg" className="text-lg px-8 py-3">
              Start Cooking
            </Button>
          </Link>
          <Link href="/about">
            <Button variant="outline" size="lg" className="text-lg px-8 py-3">
              Learn More
            </Button>
          </Link>
        </div>
      </div>
    </div>
  )
}
