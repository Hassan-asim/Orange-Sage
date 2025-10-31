/**
 * Findings Service
 */

import { apiClient, ApiResponse } from './api-client'
import { API_CONFIG } from './api-config'

export interface Finding {
  id: number
  scan_id: number
  title: string
  description: string
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info'
  category: string
  remediation?: string
  affected_url?: string
  evidence?: any
  status: 'open' | 'in_progress' | 'resolved' | 'false_positive'
  created_at: string
  updated_at?: string
}

export interface UpdateFindingData {
  status?: 'open' | 'in_progress' | 'resolved' | 'false_positive'
  notes?: string
}

class FindingsService {
  async getFindings(scanId?: number): Promise<ApiResponse<Finding[]>> {
    const endpoint = scanId 
      ? `${API_CONFIG.ENDPOINTS.FINDINGS}?scan_id=${scanId}`
      : API_CONFIG.ENDPOINTS.FINDINGS
    return await apiClient.get<Finding[]>(endpoint)
  }

  async getFinding(id: number): Promise<ApiResponse<Finding>> {
    return await apiClient.get<Finding>(`${API_CONFIG.ENDPOINTS.FINDINGS}/${id}`)
  }

  async updateFinding(id: number, data: UpdateFindingData): Promise<ApiResponse<Finding>> {
    return await apiClient.put<Finding>(`${API_CONFIG.ENDPOINTS.FINDINGS}/${id}`, data)
  }

  async deleteFinding(id: number): Promise<ApiResponse<void>> {
    return await apiClient.delete<void>(`${API_CONFIG.ENDPOINTS.FINDINGS}/${id}`)
  }
}

export const findingsService = new FindingsService()

