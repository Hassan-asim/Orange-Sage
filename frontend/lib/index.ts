/**
 * Central export for all API services
 */

export { apiClient } from './api-client'
export type { ApiResponse } from './api-client'

export { authService } from './auth-service'
export type { RegisterData, LoginData, User, LoginResponse } from './auth-service'

export { projectsService } from './projects-service'
export type { Project, CreateProjectData, UpdateProjectData } from './projects-service'

export { targetsService } from './targets-service'
export type { Target, CreateTargetData, UpdateTargetData } from './targets-service'

export { scansService } from './scans-service'
export type { Scan, CreateScanData, ComprehensiveScanData } from './scans-service'

export { findingsService } from './findings-service'
export type { Finding, UpdateFindingData } from './findings-service'

export { reportsService } from './reports-service'
export type { Report, GenerateReportData } from './reports-service'

export { API_CONFIG, getApiUrl } from './api-config'

