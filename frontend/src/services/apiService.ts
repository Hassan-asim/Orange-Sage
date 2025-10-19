/**
 * API Service for Orange Sage Frontend
 * Handles all API communication with the backend
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

class ApiService {
  private baseURL: string;
  private token: string | null = null;

  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('auth_token');
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(this.token && { Authorization: `Bearer ${this.token}` }),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  // Authentication
  async login(email: string, password: string) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await fetch(`${this.baseURL}/auth/login`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const data = await response.json();
    this.token = data.access_token;
    localStorage.setItem('auth_token', this.token);
    return data;
  }

  async register(userData: { email: string; password: string; name: string }) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async getCurrentUser() {
    return this.request('/auth/me');
  }

  logout() {
    this.token = null;
    localStorage.removeItem('auth_token');
  }

  // Projects
  async getProjects() {
    return this.request('/projects');
  }

  async createProject(projectData: { name: string; description?: string }) {
    return this.request('/projects', {
      method: 'POST',
      body: JSON.stringify(projectData),
    });
  }

  async getProject(projectId: string) {
    return this.request(`/projects/${projectId}`);
  }

  async updateProject(projectId: string, projectData: any) {
    return this.request(`/projects/${projectId}`, {
      method: 'PUT',
      body: JSON.stringify(projectData),
    });
  }

  async deleteProject(projectId: string) {
    return this.request(`/projects/${projectId}`, {
      method: 'DELETE',
    });
  }

  // Targets
  async getTargets(projectId: string) {
    return this.request(`/projects/${projectId}/targets`);
  }

  async createTarget(projectId: string, targetData: any) {
    return this.request(`/projects/${projectId}/targets`, {
      method: 'POST',
      body: JSON.stringify(targetData),
    });
  }

  async getTarget(targetId: string) {
    return this.request(`/targets/${targetId}`);
  }

  async updateTarget(targetId: string, targetData: any) {
    return this.request(`/targets/${targetId}`, {
      method: 'PUT',
      body: JSON.stringify(targetData),
    });
  }

  async deleteTarget(targetId: string) {
    return this.request(`/targets/${targetId}`, {
      method: 'DELETE',
    });
  }

  // Scans
  async getScans(projectId: string) {
    return this.request(`/projects/${projectId}/scans`);
  }

  async createScan(projectId: string, targetId: string, scanData: any) {
    return this.request(`/projects/${projectId}/targets/${targetId}/comprehensive-scan`, {
      method: 'POST',
      body: JSON.stringify(scanData),
    });
  }

  async getScan(scanId: string) {
    return this.request(`/scans/${scanId}/comprehensive-status`);
  }

  async getScanStatus(scanId: string) {
    return this.request(`/scans/${scanId}/comprehensive-status`);
  }

  // Findings
  async getFindings(scanId: string) {
    return this.request(`/scans/${scanId}/findings`);
  }

  async getFinding(findingId: string) {
    return this.request(`/findings/${findingId}`);
  }

  async updateFinding(findingId: string, findingData: any) {
    return this.request(`/findings/${findingId}`, {
      method: 'PUT',
      body: JSON.stringify(findingData),
    });
  }

  // Reports
  async getReports(scanId: string) {
    return this.request(`/scans/${scanId}/reports`);
  }

  async generateReport(scanId: string, reportData: any) {
    return this.request(`/scans/${scanId}/reports`, {
      method: 'POST',
      body: JSON.stringify(reportData),
    });
  }

  async downloadReport(scanId: string, format: string = 'pdf') {
    const response = await fetch(`${this.baseURL}/scans/${scanId}/comprehensive-report?format=${format}`, {
      headers: {
        ...(this.token && { Authorization: `Bearer ${this.token}` }),
      },
    });

    if (!response.ok) {
      throw new Error('Failed to download report');
    }

    return response;
  }

  // Health check
  async healthCheck() {
    return this.request('/health');
  }
}

export const apiService = new ApiService();
export default apiService;