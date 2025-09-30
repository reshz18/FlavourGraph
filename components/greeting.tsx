"use client"

import { useState, useEffect } from "react"

interface GreetingProps {
  name?: string
  email?: string
  className?: string
}

export function Greeting({ name, email, className = "" }: GreetingProps) {
  const [greeting, setGreeting] = useState("")

  useEffect(() => {
    const updateGreeting = () => {
      const hour = new Date().getHours()
      let timeGreeting = ""

      if (hour >= 5 && hour < 12) {
        timeGreeting = "Good morning"
      } else if (hour >= 12 && hour < 17) {
        timeGreeting = "Good afternoon"
      } else if (hour >= 17 && hour < 21) {
        timeGreeting = "Good evening"
      } else {
        timeGreeting = "Good night"
      }

      setGreeting(timeGreeting)
    }

    // Update immediately
    updateGreeting()

    // Update every minute to keep greeting current
    const interval = setInterval(updateGreeting, 60000)

    return () => clearInterval(interval)
  }, [])

  const displayName = name || email?.split('@')[0] || "User"

  return (
    <span className={className}>
      {greeting}, {displayName}!
    </span>
  )
}
