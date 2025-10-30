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

  async downloadReport(id: number, format: 'pdf' | 'html' = 'pdf'): Promise<void> {
    const url = `${API_CONFIG.ENDPOINTS.REPORTS}/${id}/download?format=${format}`
    const token = localStorage.getItem('access_token');
    const response = await fetch(getApiUrl(url), {
      method: 'GET',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {},
    });
    if (!response.ok) {
      throw new Error('Failed to download report');
    }
    const blob = await response.blob();
    const fileExtension = format === 'pdf' ? 'pdf' : 'html';
    const fileName = `report_${id}.${fileExtension}`;
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(downloadUrl);
  }

  async deleteReport(id: number): Promise<ApiResponse<void>> {
    return await apiClient.delete<void>(`${API_CONFIG.ENDPOINTS.REPORTS}/${id}`)
  }
}

export const reportsService = new ReportsService()

