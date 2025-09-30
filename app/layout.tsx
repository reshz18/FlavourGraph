import type React from "react"
import { GeistSans } from "geist/font/sans"
import { GeistMono } from "geist/font/mono"
import "./globals.css"
import { createClient } from "@/lib/supabase/server"
import { redirect } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ThemeProvider } from "@/components/theme-provider"
import { Toaster } from "@/components/ui/toaster"

export const metadata = {
  title: "FlavorGraph Recipe Navigator",
  description: "Intelligent Recipe Navigator",
    generator: 'v0.app'
}

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const supabase = await createClient()

  const {
    data: { user },
    error,
  } = await supabase.auth.getUser()

  const signOut = async () => {
    "use server"
    const supabase = await createClient()
    await supabase.auth.signOut()
    return redirect("/auth/login")
  }

  return (
    <html lang="en" className={`${GeistSans.variable} ${GeistMono.variable} antialiased`} suppressHydrationWarning>
      <body className="min-h-screen bg-background text-foreground">
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <header className="w-full border-b border-b-foreground/10 h-16 flex items-center">
            <div className="w-full max-w-6xl mx-auto flex justify-between items-center px-4">
              <Link href="/">
                <h1 className="font-bold text-lg">FlavorGraph</h1>
              </Link>
              {user ? (
                <div className="flex items-center gap-4 text-sm">
                  <span>Hey, {user.email}!</span>
                  <Link href="/dashboard">
                    <Button variant="ghost" size="sm">Dashboard</Button>
                  </Link>
                  <form action={signOut}>
                    <Button variant="outline" size="sm">Logout</Button>
                  </form>
                </div>
              ) : (
                <Link href="/auth/login">
                  <Button variant="outline" size="sm">Login</Button>
                </Link>
              )}
            </div>
          </header>
          <main className="flex-1">{children}</main>
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  )
}
