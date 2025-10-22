/**
 * API Configuration
 */

export const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  API_VERSION: 'v1',
  ENDPOINTS: {
    // Auth
    REGISTER: '/auth/register',
    LOGIN: '/auth/login',
    ME: '/auth/me',
    
    // Projects
    PROJECTS: '/projects',
    
    // Targets
    TARGETS: '/targets',
    
    // Scans
    SCANS: '/scans',
    COMPREHENSIVE_SCAN: '/comprehensive-scan',
    
    // Findings
    FINDINGS: '/findings',
    
    // Reports
    REPORTS: '/reports',
    
    // Health
    HEALTH: '/health',
  },
  TIMEOUT: 30000, // 30 seconds
}

export const getApiUrl = (endpoint: string) => {
  return `${API_CONFIG.BASE_URL}/api/${API_CONFIG.API_VERSION}${endpoint}`
}

