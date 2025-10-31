"use client"

import type React from "react"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { Menu, LogOut } from "lucide-react"
import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import Logo from "../Logo"
import { authService } from "@/lib"
import { useToast } from "@/hooks/use-toast"

interface PublicLayoutProps {
  children: React.ReactNode
}

export function PublicLayout({ children }: PublicLayoutProps) {
  const pathname = usePathname()
  const router = useRouter()
  const { toast } = useToast()

  const navItems = [
    { name: "Dashboard", href: "/dashboard" },
    { name: "Projects", href: "/projects" },
    { name: "Scans", href: "/scans" },
    { name: "Findings", href: "/findings" },
    { name: "Reports", href: "/reports" },
    { name: "Settings", href: "/settings" },
  ]

  const isActive = (href: string) => {
    return pathname === href || pathname.startsWith(href + "/")
  }

  const handleLogout = () => {
    authService.logout()
    toast({
      title: "Logged out",
      description: "You have been successfully logged out."
    })
    router.push("/login")
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header/Navbar */}
      <header className="w-full py-4 px-6 border-b border-border">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-6">
            {/* Logo */}
            <Link href="/" className="flex items-center gap-3">
            <Logo />
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-2">
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`px-4 py-2 rounded-full font-medium transition-colors ${
                    isActive(item.href)
                      ? "text-foreground bg-accent"
                      : "text-[#888888] hover:text-foreground"
                  }`}
                >
                  {item.name}
                </Link>
              ))}
            </nav>
          </div>

          {/* Desktop Actions */}
          <div className="hidden md:flex items-center gap-4">
            <Link href="/scans">
              <Button className="bg-primary text-primary-foreground hover:bg-primary/90 px-6 py-2 rounded-full font-medium shadow-sm">
                New Scan
              </Button>
            </Link>
            <Button 
              onClick={handleLogout}
              variant="outline" 
              className="border-border text-foreground hover:bg-accent px-6 py-2 rounded-full font-medium"
            >
              <LogOut className="h-4 w-4 mr-2" />
              Logout
            </Button>
          </div>

          {/* Mobile Menu */}
          <Sheet>
            <SheetTrigger asChild className="md:hidden">
              <Button variant="ghost" size="icon" className="text-foreground">
                <Menu className="h-7 w-7" />
                <span className="sr-only">Toggle navigation menu</span>
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="bg-background border-l border-border text-foreground">
              <SheetHeader>
                <SheetTitle className="text-left text-xl font-semibold text-foreground">Navigation</SheetTitle>
              </SheetHeader>
              <nav className="flex flex-col gap-4 mt-6">
                {navItems.map((item) => (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`text-lg py-2 transition-colors ${
                      isActive(item.href)
                        ? "text-foreground font-medium"
                        : "text-[#888888] hover:text-foreground"
                    }`}
                  >
                    {item.name}
                  </Link>
                ))}
                <div className="flex flex-col gap-3 mt-6 pt-6 border-t border-border">
                  <Link href="/scans" className="w-full">
                    <Button className="bg-primary text-primary-foreground hover:bg-primary/90 w-full rounded-full font-medium shadow-sm">
                      New Scan
                    </Button>
                  </Link>
                  <Button 
                    onClick={handleLogout}
                    variant="outline" 
                    className="w-full border-border text-foreground hover:bg-accent rounded-full font-medium"
                  >
                    <LogOut className="h-4 w-4 mr-2" />
                    Logout
                  </Button>
                </div>
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>
    </div>
  )
}
