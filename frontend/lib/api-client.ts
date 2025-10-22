/**
 * API Client for making HTTP requests
 */

import { getApiUrl } from './api-config'

export interface ApiResponse<T = any> {
  data?: T
  error?: string
  status: number
}

// Helper function to format validation errors
function formatValidationError(detail: any): string {
  // If detail is a string, return it
  if (typeof detail === 'string') {
    return detail
  }
  
  // If detail is an array of validation errors (FastAPI format)
  if (Array.isArray(detail)) {
    return detail
      .map(err => {
        const field = err.loc ? err.loc.join('.') : 'field'
        return `${field}: ${err.msg || 'validation error'}`
      })
      .join(', ')
  }
  
  // If detail is an object, try to extract a message
  if (typeof detail === 'object' && detail !== null) {
    return detail.message || detail.msg || JSON.stringify(detail)
  }
  
  return 'Request failed'
}

class ApiClient {
  private getAuthHeader(): HeadersInit {
    const token = this.getToken()
    return token
      ? {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        }
      : {
          'Content-Type': 'application/json',
        }
  }

  private getToken(): string | null {
    if (typeof window === 'undefined') return null
    return localStorage.getItem('access_token')
  }

  setToken(token: string): void {
    if (typeof window === 'undefined') return
    localStorage.setItem('access_token', token)
  }

  removeToken(): void {
    if (typeof window === 'undefined') return
    localStorage.removeItem('access_token')
  }

  async get<T = any>(endpoint: string): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(getApiUrl(endpoint), {
        method: 'GET',
        headers: this.getAuthHeader(),
      })

      const data = await response.json()

      if (!response.ok) {
        return {
          error: formatValidationError(data.detail || data.error || data),
          status: response.status,
        }
      }

      return {
        data,
        status: response.status,
      }
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Network error',
        status: 0,
      }
    }
  }

  async post<T = any>(endpoint: string, body?: any): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(getApiUrl(endpoint), {
        method: 'POST',
        headers: this.getAuthHeader(),
        body: body ? JSON.stringify(body) : undefined,
      })

      const data = await response.json()

      if (!response.ok) {
        return {
          error: formatValidationError(data.detail || data.error || data),
          status: response.status,
        }
      }

      return {
        data,
        status: response.status,
      }
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Network error',
        status: 0,
      }
    }
  }

  async put<T = any>(endpoint: string, body?: any): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(getApiUrl(endpoint), {
        method: 'PUT',
        headers: this.getAuthHeader(),
        body: body ? JSON.stringify(body) : undefined,
      })

      const data = await response.json()

      if (!response.ok) {
        return {
          error: formatValidationError(data.detail || data.error || data),
          status: response.status,
        }
      }

      return {
        data,
        status: response.status,
      }
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Network error',
        status: 0,
      }
    }
  }

  async delete<T = any>(endpoint: string): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(getApiUrl(endpoint), {
        method: 'DELETE',
        headers: this.getAuthHeader(),
      })

      const data = await response.json()

      if (!response.ok) {
        return {
          error: formatValidationError(data.detail || data.error || data),
          status: response.status,
        }
      }

      return {
        data,
        status: response.status,
      }
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Network error',
        status: 0,
      }
    }
  }
}

export const apiClient = new ApiClient()

