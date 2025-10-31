/**
 * API Configuration
 */

// Make BASE_URL a function that calculates at runtime instead of at module load
const getBaseUrl = (): string => {
  const raw = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  
  // In browser environment, always use HTTPS if the page is served over HTTPS
  if (typeof window !== 'undefined') {
    if (window.location.protocol === 'https:' && raw.startsWith('http://')) {
      return raw.replace(/^http:/, 'https:')
    }
  }
  
  return raw
}

export const API_CONFIG = {
  get BASE_URL() {
    return getBaseUrl()
  },
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
  // Ensure trailing slash for FastAPI compatibility
  const normalizedEndpoint = endpoint.endsWith('/') ? endpoint : `${endpoint}/`
  return `${API_CONFIG.BASE_URL}/api/${API_CONFIG.API_VERSION}${normalizedEndpoint}`
}

