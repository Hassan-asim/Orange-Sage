/**
 * Reports Service
 */

import { apiClient, ApiResponse } from './api-client'
import { API_CONFIG } from './api-config'

export interface Report {
  id: number
  scan_id: number
  report_type: string
  format: 'pdf' | 'html' | 'json'
  file_path?: string
  created_at: string
  metadata?: any
}

export interface GenerateReportData {
  scan_id: number
  format: 'pdf' | 'html' | 'json'
  include_details?: boolean
}

class ReportsService {
  async getReports(): Promise<ApiResponse<Report[]>> {
    return await apiClient.get<Report[]>(API_CONFIG.ENDPOINTS.REPORTS)
  }

  async getReport(id: number): Promise<ApiResponse<Report>> {
    return await apiClient.get<Report>(`${API_CONFIG.ENDPOINTS.REPORTS}/${id}`)
  }

  async generateReport(data: GenerateReportData): Promise<ApiResponse<Report>> {
    return await apiClient.post<Report>(`${API_CONFIG.ENDPOINTS.REPORTS}/generate`, data)
  }

  async downloadReport(id: number): Promise<void> {
    const response = await apiClient.get<Blob>(`${API_CONFIG.ENDPOINTS.REPORTS}/${id}/download`)
    
    if (response.data) {
      // Create download link
      const url = window.URL.createObjectURL(response.data as any)
      const link = document.createElement('a')
      link.href = url
      link.download = `report_${id}.pdf`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    }
  }

  async deleteReport(id: number): Promise<ApiResponse<void>> {
    return await apiClient.delete<void>(`${API_CONFIG.ENDPOINTS.REPORTS}/${id}`)
  }
}

export const reportsService = new ReportsService()

