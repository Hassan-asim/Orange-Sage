/**
 * Targets Service
 */

import { apiClient, ApiResponse } from './api-client'
import { API_CONFIG } from './api-config'

export interface Target {
  id: number
  project_id: number
  url: string
  name?: string
  description?: string
  target_type: string
  created_at: string
  updated_at?: string
  is_active: boolean
}

export interface CreateTargetData {
  project_id: number
  url: string
  name?: string
  description?: string
  target_type?: string
}

export interface UpdateTargetData {
  url?: string
  name?: string
  description?: string
  is_active?: boolean
}

class TargetsService {
  async getTargets(projectId?: number): Promise<ApiResponse<Target[]>> {
    const endpoint = projectId
      ? `${API_CONFIG.ENDPOINTS.TARGETS}?project_id=${projectId}`
      : API_CONFIG.ENDPOINTS.TARGETS
    return await apiClient.get<Target[]>(endpoint)
  }

  async getTarget(id: number): Promise<ApiResponse<Target>> {
    return await apiClient.get<Target>(`${API_CONFIG.ENDPOINTS.TARGETS}/${id}`)
  }

  async createTarget(data: CreateTargetData): Promise<ApiResponse<Target>> {
    // Transform data to match backend schema
    const backendData = {
      name: data.name || 'Target',
      type: data.target_type || 'url',
      value: data.url,
      description: data.description || '',
      project_id: data.project_id,
      config: {}
    }
    return await apiClient.post<Target>(API_CONFIG.ENDPOINTS.TARGETS, backendData)
  }

  async updateTarget(id: number, data: UpdateTargetData): Promise<ApiResponse<Target>> {
    return await apiClient.put<Target>(`${API_CONFIG.ENDPOINTS.TARGETS}/${id}`, data)
  }

  async deleteTarget(id: number): Promise<ApiResponse<void>> {
    return await apiClient.delete<void>(`${API_CONFIG.ENDPOINTS.TARGETS}/${id}`)
  }
}

export const targetsService = new TargetsService()

