import { createServerClient } from "@supabase/ssr"
import { NextResponse, type NextRequest } from "next/server"

export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({
    request,
  })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) => request.cookies.set(name, value))
          supabaseResponse = NextResponse.next({
            request,
          })
          cookiesToSet.forEach(({ name, value, options }) => supabaseResponse.cookies.set(name, value, options))
        },
      },
    },
  )

  // Refresh session if expired - required for Server Components
  await supabase.auth.getUser()

  const {
    data: { user },
  } = await supabase.auth.getUser()

  const { pathname } = request.nextUrl

  // Define protected routes
  const protectedRoutes = ['/dashboard', '/protected']
  const authRoutes = ['/auth/login', '/auth/sign-up', '/auth/sign-up-success', '/auth/callback', '/auth/auth-code-error']
  const publicRoutes = ['/', '/about']

  // Allow access to auth routes and public routes
  if (authRoutes.some(route => pathname.startsWith(route)) || publicRoutes.includes(pathname)) {
    return supabaseResponse
  }

  // Redirect unauthenticated users from protected routes
  if (protectedRoutes.some(route => pathname.startsWith(route)) && !user) {
    const url = request.nextUrl.clone()
    url.pathname = "/auth/login"
    url.searchParams.set("redirectedFrom", pathname)
    return NextResponse.redirect(url)
  }

  return supabaseResponse
}
