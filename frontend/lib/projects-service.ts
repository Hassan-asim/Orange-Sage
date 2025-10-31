/**
 * Projects Service
 */

import { apiClient, ApiResponse } from './api-client'
import { API_CONFIG } from './api-config'

export interface Project {
  id: number
  name: string
  description?: string
  owner_id: number
  created_at: string
  updated_at?: string
  is_active: boolean
}

export interface CreateProjectData {
  name: string
  description?: string
}

export interface UpdateProjectData {
  name?: string
  description?: string
  is_active?: boolean
}

class ProjectsService {
  async getProjects(): Promise<ApiResponse<Project[]>> {
    return await apiClient.get<Project[]>(API_CONFIG.ENDPOINTS.PROJECTS)
  }

  async getProject(id: number): Promise<ApiResponse<Project>> {
    return await apiClient.get<Project>(`${API_CONFIG.ENDPOINTS.PROJECTS}/${id}`)
  }

  async createProject(data: CreateProjectData): Promise<ApiResponse<Project>> {
    return await apiClient.post<Project>(API_CONFIG.ENDPOINTS.PROJECTS, data)
  }

  async updateProject(id: number, data: UpdateProjectData): Promise<ApiResponse<Project>> {
    return await apiClient.put<Project>(`${API_CONFIG.ENDPOINTS.PROJECTS}/${id}`, data)
  }

  async deleteProject(id: number): Promise<ApiResponse<void>> {
    return await apiClient.delete<void>(`${API_CONFIG.ENDPOINTS.PROJECTS}/${id}`)
  }
}

export const projectsService = new ProjectsService()

