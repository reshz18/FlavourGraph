import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { CheckCircleIcon, MailIcon } from "lucide-react"
import Link from "next/link"

export default function Page() {
  return (
    <div className="flex min-h-svh w-full items-center justify-center p-6 md:p-10 bg-gradient-to-br from-background to-muted/20">
      <div className="w-full max-w-md">
        <div className="flex flex-col gap-8">
          <div className="text-center space-y-2">
            <h1 className="text-4xl font-bold text-primary tracking-tight">FlavorGraph</h1>
            <p className="text-muted-foreground text-lg">Recipe Navigator</p>
          </div>

          <Card className="shadow-lg border-0 bg-card/80 backdrop-blur-sm">
            <CardHeader className="text-center space-y-4">
              <div className="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
                <CheckCircleIcon className="h-8 w-8 text-green-600" />
              </div>
              <CardTitle className="text-2xl font-semibold">Welcome to FlavorGraph!</CardTitle>
              <CardDescription className="text-base">
                Your account has been created successfully
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="text-center space-y-4">
                <div className="flex items-center justify-center gap-2 text-muted-foreground">
                  <MailIcon className="h-5 w-5" />
                  <span>Check your email to verify your account</span>
                </div>
                <p className="text-sm text-muted-foreground">
                  We&apos;ve sent a confirmation email to your inbox. Please click the verification link 
                  to activate your account and start discovering amazing recipes.
                </p>
              </div>
              
              <div className="space-y-3">
                <Link href="/auth/login" className="block">
                  <Button className="w-full">
                    Continue to Login
                  </Button>
                </Link>
                <Link href="/" className="block">
                  <Button variant="outline" className="w-full">
                    Back to Home
                  </Button>
                </Link>
              </div>

              <div className="text-center">
                <p className="text-xs text-muted-foreground">
                  Didn&apos;t receive the email? Check your spam folder or{" "}
                  <button className="text-primary hover:underline">
                    resend verification email
                  </button>
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
