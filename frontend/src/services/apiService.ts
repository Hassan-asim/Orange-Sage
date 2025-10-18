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

export const apiService = {
  // Health check
  async getHealth() {
    const response = await api.get('/health')
    return response.data
  },

  // Projects
  async getProjects() {
    const response = await api.get('/api/v1/projects')
    return response.data
  },

  async getProject(projectId: number) {
    const response = await api.get(`/api/v1/projects/${projectId}`)
    return response.data
  },

  // Targets
  async getTargets(projectId?: number) {
    const params = projectId ? { project_id: projectId } : {}
    const response = await api.get('/api/v1/targets', { params })
    return response.data
  },

  async getTarget(targetId: number) {
    const response = await api.get(`/api/v1/targets/${targetId}`)
    return response.data
  },

  // Scans
  async getScans(projectId?: number, status?: string) {
    const params: any = {}
    if (projectId) params.project_id = projectId
    if (status) params.status = status
    
    const response = await api.get('/api/v1/scans', { params })
    return response.data
  },

  async getScan(scanId: number) {
    const response = await api.get(`/api/v1/scans/${scanId}`)
    return response.data
  },

  async createScan(scanData: {
    name: string
    description?: string
    project_id: number
    target_id: number
    scan_config?: any
    agent_config?: any
  }) {
    const response = await api.post('/api/v1/scans', scanData)
    return response.data
  },

  async cancelScan(scanId: number) {
    const response = await api.post(`/api/v1/scans/${scanId}/cancel`)
    return response.data
  },

  async getScanAgents(scanId: number) {
    const response = await api.get(`/api/v1/scans/${scanId}/agents`)
    return response.data
  },

  // Findings
  async getFindings(scanId?: number, severity?: string, status?: string) {
    const params: any = {}
    if (scanId) params.scan_id = scanId
    if (severity) params.severity = severity
    if (status) params.status = status
    
    const response = await api.get('/api/v1/findings', { params })
    return response.data
  },

  async getFinding(findingId: number) {
    const response = await api.get(`/api/v1/findings/${findingId}`)
    return response.data
  },

  // Reports
  async generateReport(scanId: number, options: {
    format: string
    include_charts?: boolean
    include_pocs?: boolean
    branding?: string
  }) {
    const response = await api.post('/api/v1/reports/generate', {
      scan_id: scanId,
      ...options,
    })
    return response.data
  },

  async getReportStatus(reportId: number) {
    const response = await api.get(`/api/v1/reports/${reportId}/status`)
    return response.data
  },

  async downloadReport(reportId: number) {
    const response = await api.get(`/api/v1/reports/${reportId}/download`, {
      responseType: 'blob',
    })
    return response.data
  },
}
