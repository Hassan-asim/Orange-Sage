/**
 * Scans Service
 */

import { apiClient, ApiResponse } from './api-client'
import { API_CONFIG } from './api-config'

export interface Scan {
  id: number
  target_id: number
  scan_type: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  progress: number
  started_at?: string
  completed_at?: string
  created_at: string
  result?: any
}

export interface CreateScanData {
  target_id: number
  scan_type: string
  config?: any
}

export interface ComprehensiveScanData {
  target_url: string
  project_id?: number
  scan_types?: string[]
}

class ScansService {
  async getScans(): Promise<ApiResponse<Scan[]>> {
    return await apiClient.get<Scan[]>(API_CONFIG.ENDPOINTS.SCANS)
  }

  async getScan(id: number): Promise<ApiResponse<Scan>> {
    return await apiClient.get<Scan>(`${API_CONFIG.ENDPOINTS.SCANS}/${id}`)
  }

  async createScan(data: CreateScanData): Promise<ApiResponse<Scan>> {
    return await apiClient.post<Scan>(API_CONFIG.ENDPOINTS.SCANS, data)
  }

  async startComprehensiveScan(data: ComprehensiveScanData): Promise<ApiResponse<any>> {
    return await apiClient.post<any>(`${API_CONFIG.ENDPOINTS.COMPREHENSIVE_SCAN}/start`, data)
  }

  async getScanStatus(scanId: string): Promise<ApiResponse<any>> {
    return await apiClient.get<any>(`${API_CONFIG.ENDPOINTS.COMPREHENSIVE_SCAN}/status/${scanId}`)
  }

  async cancelScan(id: number): Promise<ApiResponse<void>> {
    return await apiClient.delete<void>(`${API_CONFIG.ENDPOINTS.SCANS}/${id}`)
  }
}

export const scansService = new ScansService()

