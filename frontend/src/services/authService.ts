import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authService = {
  async login(email: string, password: string) {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    
    const response = await api.post('/api/v1/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    
    // Get user info after successful login
    const userResponse = await this.getCurrentUser()
    
    return {
      access_token: response.data.access_token,
      token_type: response.data.token_type,
      expires_in: response.data.expires_in,
      user: userResponse,
    }
  },

  async register(userData: {
    email: string
    username: string
    password: string
    full_name?: string
  }) {
    const response = await api.post('/api/v1/auth/register', userData)
    return response.data
  },

  async getCurrentUser() {
    const response = await api.get('/api/v1/auth/me')
    return response.data
  },

  async logout() {
    localStorage.removeItem('access_token')
  },
}
