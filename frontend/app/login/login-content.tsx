"use client"

import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ArrowLeft } from "lucide-react"

export function LoginContent() {
  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Background gradient - matching landing page */}
      <div className="absolute inset-0 bg-gradient-to-br from-background via-background to-muted/50" />
      
      {/* Back to home link */}
      <div className="absolute top-6 left-6 z-20">
        <Link href="/" className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
          <ArrowLeft className="h-4 w-4" />
          <span>Back to home</span>
        </Link>
      </div>

      {/* Main content */}
      <div className="relative z-10 flex min-h-screen items-center justify-center p-6">
        <Card className="w-full max-w-md bg-card/95 backdrop-blur-sm border-border shadow-2xl rounded-2xl">
          <CardHeader className="space-y-2 text-center">
            <div className="flex items-center gap-3 justify-center mb-2">
              <div className="w-8 h-8 bg-secondary rounded-lg flex items-center justify-center">
                <span className="text-secondary-foreground font-bold text-sm">OS</span>
              </div>
              <span className="text-xl font-bold text-foreground">Orange Sage</span>
            </div>
            <CardTitle className="text-2xl font-bold text-foreground">
              Welcome back
            </CardTitle>
            <p className="text-muted-foreground">
              Sign in to your account to continue
            </p>
          </CardHeader>
          
          <CardContent className="space-y-6">
            <form className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email" className="text-foreground font-medium">
                  Email
                </Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="Enter your email"
                  className="bg-background border-border text-foreground placeholder:text-muted-foreground focus:border-ring focus:ring-ring h-11"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="password" className="text-foreground font-medium">
                  Password
                </Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  className="bg-background border-border text-foreground placeholder:text-muted-foreground focus:border-ring focus:ring-ring h-11"
                />
              </div>
              
              <div className="flex items-center justify-between text-sm">
                <label className="flex items-center space-x-2 text-muted-foreground">
                  <input type="checkbox" className="rounded border-border" />
                  <span>Remember me</span>
                </label>
                <Link 
                  href="/forgot-password" 
                  className="text-secondary hover:text-secondary/90 font-medium"
                >
                  Forgot password?
                </Link>
              </div>
              
              <Button 
                type="submit"
                className="w-full bg-secondary text-secondary-foreground hover:bg-secondary/90 font-medium text-base h-11 rounded-lg shadow-lg ring-1 ring-white/10"
              >
                Sign In
              </Button>
            </form>
            
            <div className="text-center">
              <p className="text-sm text-muted-foreground">
                Don't have an account?{" "}
                <Link 
                  href="/register" 
                  className="text-secondary hover:text-secondary/90 font-medium underline underline-offset-4"
                >
                  Sign up
                </Link>
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
