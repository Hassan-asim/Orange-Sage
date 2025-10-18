import { useState, useEffect, createContext, useContext } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import { authService } from '../services/authService'
import toast from 'react-hot-toast'

interface User {
  id: number
  email: string
  username: string
  full_name?: string
  is_active: boolean
  created_at: string
}

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (userData: RegisterData) => Promise<void>
  logout: () => void
}

interface RegisterData {
  email: string
  username: string
  password: string
  full_name?: string
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const queryClient = useQueryClient()

  // Check if user is logged in on mount
  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      // Verify token and get user info
      authService.getCurrentUser()
        .then((userData) => {
          setUser(userData)
        })
        .catch(() => {
          localStorage.removeItem('access_token')
        })
        .finally(() => {
          setIsLoading(false)
        })
    } else {
      setIsLoading(false)
    }
  }, [])

  const login = async (email: string, password: string) => {
    try {
      const response = await authService.login(email, password)
      localStorage.setItem('access_token', response.access_token)
      setUser(response.user)
      toast.success('Login successful!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Login failed')
      throw error
    }
  }

  const register = async (userData: RegisterData) => {
    try {
      const response = await authService.register(userData)
      toast.success('Registration successful! Please login.')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Registration failed')
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    setUser(null)
    queryClient.clear()
    toast.success('Logged out successfully')
  }

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
