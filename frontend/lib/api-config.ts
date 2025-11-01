/**
 * API Configuration
 */

export const API_CONFIG = {
  BASE_URL: (() => {
    // Hardcode HTTPS backend URL for production
    const productionUrl = 'https://orange-sage-backend-cpd4lwaqmq-uc.a.run.app'
    
    // Check if we're in browser runtime
    if (typeof window !== 'undefined') {
      // Runtime: check if we're on localhost for local dev
      const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
      if (isLocalhost) {
        return 'http://localhost:8000'
      }
      // Runtime: we're in production (Cloud Run), always use HTTPS
      return productionUrl
    }
    
    // Build-time: Check environment variable
    const envUrl = process.env.NEXT_PUBLIC_API_URL
    
    // If env var is provided, force HTTPS (never allow HTTP in production builds)
    if (envUrl) {
      // If it's HTTP, convert to HTTPS
      if (envUrl.startsWith('http://')) {
        // Check if it's localhost (ok to keep HTTP for local dev builds)
        if (envUrl.includes('localhost') || envUrl.includes('127.0.0.1')) {
          return envUrl
        }
        // Otherwise, convert to HTTPS
        return envUrl.replace(/^http:/, 'https:')
      }
      return envUrl
    }
    
    // Build-time default: Use production HTTPS URL
    // This will be used when building for Cloud Run
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

