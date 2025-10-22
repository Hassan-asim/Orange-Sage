/**
 * Authentication Service
 */

import { apiClient, ApiResponse } from './api-client'
import { API_CONFIG } from './api-config'

export interface RegisterData {
  email: string
  username: string
  password: string
  full_name?: string
}

export interface LoginData {
  email: string
  password: string
}

export interface User {
  id: number
  email: string
  username: string
  full_name?: string
  is_active: boolean
  created_at: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  expires_in: number
}

class AuthService {
  async register(data: RegisterData): Promise<ApiResponse<User>> {
    const response = await apiClient.post<User>(
      API_CONFIG.ENDPOINTS.REGISTER,
      data
    )
    return response
  }

  async login(data: LoginData): Promise<ApiResponse<LoginResponse>> {
    const response = await apiClient.post<LoginResponse>(
      API_CONFIG.ENDPOINTS.LOGIN,
      data
    )

    if (response.data) {
      // Store token
      apiClient.setToken(response.data.access_token)
    }

    return response
  }

  async getCurrentUser(): Promise<ApiResponse<User>> {
    return await apiClient.get<User>(API_CONFIG.ENDPOINTS.ME)
  }

  logout(): void {
    apiClient.removeToken()
  }

  isAuthenticated(): boolean {
    if (typeof window === 'undefined') return false
    return !!localStorage.getItem('access_token')
  }

  getToken(): string | null {
    if (typeof window === 'undefined') return null
    return localStorage.getItem('access_token')
  }
}

export const authService = new AuthService()

