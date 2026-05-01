import axios from 'axios'

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1'

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('❌ API Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor for logging and error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error(`❌ API Response Error: ${error.response?.status} ${error.config?.url}`)
    
    // Handle specific error cases
    if (error.response?.status === 429) {
      error.message = 'Too many requests. Please try again later.'
    } else if (error.response?.status === 413) {
      error.message = 'Request too large. Please reduce input size.'
    } else if (error.response?.status === 400) {
      error.message = error.response.data?.message || 'Invalid request data.'
    } else if (error.response?.status >= 500) {
      error.message = 'Server error. Please try again later.'
    } else if (error.code === 'ECONNABORTED') {
      error.message = 'Request timeout. Please try again.'
    } else if (!error.response) {
      error.message = 'Network error. Please check your connection.'
    }
    
    return Promise.reject(error)
  }
)

// API Service Methods
export const apiService = {
  // Health Check
  async healthCheck() {
    const response = await apiClient.get('/health')
    return response.data
  },

  // Get API Metadata
  async getMeta() {
    const response = await apiClient.get('/meta')
    return response.data
  },

  // Get Available Locations
  async getLocations() {
    const response = await apiClient.get('/locations')
    return response.data
  },

  // Get Available Cuisines
  async getCuisines() {
    const response = await apiClient.get('/cuisines')
    return response.data
  },

  // Get Dataset Statistics
  async getStats() {
    const response = await apiClient.get('/stats')
    return response.data
  },

  // Get Recommendations
  async getRecommendations(preferences) {
    const response = await apiClient.post('/recommendations', preferences)
    return response.data
  },

  // Get Telemetry (for debugging)
  async getTelemetry() {
    const response = await apiClient.get('/monitoring/telemetry')
    return response.data
  },
}

// Utility Functions
export const apiUtils = {
  // Format API error messages
  formatError(error) {
    if (error.response?.data?.message) {
      return error.response.data.message
    }
    return error.message || 'An unexpected error occurred.'
  },

  // Check if API is available
  async isApiAvailable() {
    try {
      await apiService.healthCheck()
      return true
    } catch (error) {
      return false
    }
  },

  // Get API status with details
  async getApiStatus() {
    try {
      const health = await apiService.healthCheck()
      return {
        available: true,
        status: health.status,
        checks: health.checks,
        timestamp: health.timestamp,
      }
    } catch (error) {
      return {
        available: false,
        error: apiUtils.formatError(error),
        timestamp: new Date().toISOString(),
      }
    }
  },
}

export default apiService
