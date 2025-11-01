/**
 * API Configuration
 */

export const API_CONFIG = {
  BASE_URL: (() => {
    // Hardcode HTTPS backend URL for production
    const productionUrl = 'https://orange-sage-backend-cpd4lwaqmq-uc.a.run.app'
    
    // Allow override via env var
    const envUrl = process.env.NEXT_PUBLIC_API_URL
    
    // If env var is provided, use it but force HTTPS
    if (envUrl) {
      return envUrl.startsWith('http://') ? envUrl.replace(/^http:/, 'https:') : envUrl
    }
    
    // In production build or runtime, use hardcoded HTTPS URL
    // For local development, check if we're in browser and on localhost
    if (typeof window !== 'undefined') {
      const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
      if (isLocalhost) {
        return 'http://localhost:8000'
      }
    }
    
    // Default to production HTTPS URL (will be used in Cloud Run)
    return productionUrl
  })(),
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

