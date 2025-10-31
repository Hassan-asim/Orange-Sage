"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ArrowLeft } from "lucide-react"
import Logo from "@/components/Logo"
import { authService } from "@/lib/auth-service"
import { useToast } from "@/hooks/use-toast"

export function RegisterContent() {
  const router = useRouter()
  const { toast } = useToast()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    fullName: "",
    userName: "",
    email: "",
    password: "",
    confirmPassword: "",
    cnic: "",
    phoneNumber: ""
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    // Validate passwords match
    if (formData.password !== formData.confirmPassword) {
      toast({
        title: "Password Mismatch",
        description: "Passwords do not match. Please try again.",
        variant: "destructive",
      })
      setLoading(false)
      return
    }

    // Validate password length
    if (formData.password.length < 6) {
      toast({
        title: "Invalid Password",
        description: "Password must be at least 6 characters long.",
        variant: "destructive",
      })
      setLoading(false)
      return
    }

    try {
      const response = await authService.register({
        email: formData.email,
        username: formData.userName,
        password: formData.password,
        full_name: formData.fullName,
        cnic: formData.cnic,
        phone_number: formData.phoneNumber
      })

      if (response.error) {
        toast({
          title: "Registration Failed",
          description: response.error,
          variant: "destructive",
        })
      } else {
        toast({
          title: "Success!",
          description: "Account created successfully. Please log in.",
        })
        router.push("/login")
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "An unexpected error occurred. Please try again.",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    })
  }

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
              <div className="w-8 h-8 rounded-lg flex items-center justify-center">
                <Logo />
              </div>
            </div>
            <CardTitle className="text-2xl font-bold text-foreground">
              Create your account
            </CardTitle>
            <p className="text-muted-foreground">
              Start securing your code with AI-powered vulnerability detection
            </p>
          </CardHeader>

          <CardContent className="space-y-6">
            <form className="space-y-4" onSubmit={handleSubmit}>
              <div className="space-y-2">
                <Label htmlFor="fullName" className="text-foreground font-medium">
                  Full Name
                </Label>
                <Input
                  id="fullName"
                  type="text"
                  placeholder="Enter your full name"
                  value={formData.fullName}
                  onChange={handleChange}
                  disabled={loading}
                  className="bg-background border-border text-foreground placeholder:text-muted-foreground focus:border-ring focus:ring-ring h-11"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="userName" className="text-foreground font-medium">
                  User Name
                </Label>
                <Input
                  id="userName"
                  type="text"
                  placeholder="Enter your user name"
                  value={formData.userName}
                  onChange={handleChange}
                  required
                  disabled={loading}
                  className="bg-background border-border text-foreground placeholder:text-muted-foreground focus:border-ring focus:ring-ring h-11"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email" className="text-foreground font-medium">
                  Email
                </Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="Enter your email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  disabled={loading}
                  className="bg-background border-border text-foreground placeholder:text-muted-foreground focus:border-ring focus:ring-ring h-11"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="cnic" className="text-foreground font-medium">CNIC</Label>
                <Input
                  id="cnic"
                  type="text"
                  placeholder="Enter your CNIC (e.g. 12345-1234567-1)"
                  value={formData.cnic}
                  onChange={handleChange}
                  disabled={loading}
                  className="bg-background border-border text-foreground placeholder:text-muted-foreground focus:border-ring focus:ring-ring h-11"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="phoneNumber" className="text-foreground font-medium">Phone Number</Label>
                <Input
                  id="phoneNumber"
                  type="tel"
                  placeholder="Enter your phone number"
                  value={formData.phoneNumber}
                  onChange={handleChange}
                  disabled={loading}
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
                  placeholder="Create a password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  disabled={loading}
                  className="bg-background border-border text-foreground placeholder:text-muted-foreground focus:border-ring focus:ring-ring h-11"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="confirmPassword" className="text-foreground font-medium">
                  Confirm Password
                </Label>
                <Input
                  id="confirmPassword"
                  type="password"
                  placeholder="Confirm your password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                  disabled={loading}
                  className="bg-background border-border text-foreground placeholder:text-muted-foreground focus:border-ring focus:ring-ring h-11"
                />
              </div>

              <Button
                type="submit"
                disabled={loading}
                className="w-full bg-secondary text-secondary-foreground hover:bg-secondary/90 font-medium text-base h-11 rounded-lg shadow-lg ring-1 ring-white/10"
              >
                {loading ? "Creating Account..." : "Create Account"}
              </Button>
            </form>

            <div className="text-center">
              <p className="text-sm text-muted-foreground">
                Already have an account?{" "}
                <Link
                  href="/login"
                  className="text-secondary hover:text-secondary/90 font-medium underline underline-offset-4"
                >
                  Sign in
                </Link>
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
