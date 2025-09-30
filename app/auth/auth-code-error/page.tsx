import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

interface AuthCodeErrorProps {
  searchParams: {
    error?: string
  }
}

export default function AuthCodeError({ searchParams }: AuthCodeErrorProps) {
  const errorMessage = searchParams.error ? decodeURIComponent(searchParams.error) : "Unknown error occurred"

  return (
    <div className="flex min-h-svh w-full items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-md">
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl text-destructive">Authentication Error</CardTitle>
            <CardDescription>
              Sorry, we couldn't complete your authentication request.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-md">
                <p className="text-sm text-destructive font-medium">Error Details:</p>
                <p className="text-sm text-destructive/80 mt-1">{errorMessage}</p>
              </div>
              <p className="text-sm text-muted-foreground">
                This could be due to an expired or invalid authentication code, 
                or a configuration issue. Please try signing in again.
              </p>
              <div className="flex flex-col gap-2">
                <Link href="/auth/login">
                  <Button className="w-full">Try Again</Button>
                </Link>
                <Link href="/">
                  <Button variant="outline" className="w-full">Go Home</Button>
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
