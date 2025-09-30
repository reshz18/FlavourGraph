import { createClient } from "@/lib/supabase/server"
import { NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  const { searchParams, origin } = new URL(request.url)
  const code = searchParams.get("code")
  const error = searchParams.get("error")
  const error_description = searchParams.get("error_description")
  
  // if "next" is in param, use it as the redirect URL
  const next = searchParams.get("next") ?? "/dashboard"

  // Handle OAuth errors
  if (error) {
    console.error("OAuth error:", error, error_description)
    return NextResponse.redirect(`${origin}/auth/auth-code-error?error=${encodeURIComponent(error_description || error)}`)
  }

  if (code) {
    const supabase = await createClient()
    
    try {
      const { data, error: exchangeError } = await supabase.auth.exchangeCodeForSession(code)
      
      if (exchangeError) {
        console.error("Session exchange error:", exchangeError)
        return NextResponse.redirect(`${origin}/auth/auth-code-error?error=${encodeURIComponent(exchangeError.message)}`)
      }

      if (data.user) {
        // Successfully authenticated
        const forwardedHost = request.headers.get("x-forwarded-host")
        const isLocalEnv = process.env.NODE_ENV === "development"
        
        if (isLocalEnv) {
          return NextResponse.redirect(`${origin}${next}`)
        } else if (forwardedHost) {
          return NextResponse.redirect(`https://${forwardedHost}${next}`)
        } else {
          return NextResponse.redirect(`${origin}${next}`)
        }
      }
    } catch (err) {
      console.error("Unexpected error during authentication:", err)
      return NextResponse.redirect(`${origin}/auth/auth-code-error?error=${encodeURIComponent("An unexpected error occurred")}`)
    }
  }

  // No code provided or other issues
  return NextResponse.redirect(`${origin}/auth/auth-code-error?error=${encodeURIComponent("No authentication code provided")}`)
}
