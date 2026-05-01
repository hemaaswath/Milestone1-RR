import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from 'react-query'
import { useApiHealth, useRecommendations, useApiMeta } from '../src/hooks/useRecommendations'
import apiService from '../src/services/apiService'

// Mock API service
vi.mock('../src/services/apiService')

describe('Phase 7 API Integration Tests', () => {
  let queryClient

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
        mutations: { retry: false },
      },
    })
    vi.clearAllMocks()
  })

  afterEach(() => {
    queryClient.clear()
  })

  const wrapper = ({ children }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  )

  describe('useApiHealth Hook', () => {
    it('should successfully fetch API health status', async () => {
      const mockHealthData = {
        status: 'healthy',
        timestamp: '2025-01-01T12:00:00Z',
        phase: '6',
        checks: {
          api: 'healthy',
          data_source: 'healthy',
          groq_api: 'configured'
        }
      }

      apiService.healthCheck.mockResolvedValue(mockHealthData)

      const { result } = renderHook(() => useApiHealth(), { wrapper })

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true)
        expect(result.current.data).toEqual(mockHealthData)
      })

      expect(apiService.healthCheck).toHaveBeenCalledTimes(1)
    })

    it('should handle API health check errors', async () => {
      const mockError = new Error('API unavailable')
      apiService.healthCheck.mockRejectedValue(mockError)

      const { result } = renderHook(() => useApiHealth(), { wrapper })

      await waitFor(() => {
        expect(result.current.isError).toBe(true)
      })

      expect(result.current.error).toEqual(mockError)
    })
  })

  describe('useRecommendations Hook', () => {
    it('should successfully get recommendations', async () => {
      const mockPreferences = {
        location: 'Bellandur',
        budget: 'medium',
        cuisine: 'North Indian',
        minRating: 3.5,
        topK: 5
      }

      const mockRecommendations = {
        status: 'success',
        timestamp: '2025-01-01T12:00:00Z',
        data: {
          recommendations: [
            {
              restaurant_name: 'Test Restaurant',
              rank: 1,
              score: 0.95,
              explanation: 'Great match for your preferences',
              location: 'Bellandur',
              cuisines: 'North Indian',
              rating: 4.5,
              cost_for_two: 800
            }
          ],
          summary: {
            total_candidates: 10,
            filtered_candidates: 5,
            final_recommendations: 1,
            avg_rating: 4.5
          }
        },
        metadata: {
          pipeline_performance: {
            total_duration_ms: 2700
          }
        }
      }

      apiService.getRecommendations.mockResolvedValue(mockRecommendations)

      const { result } = renderHook(() => useRecommendations(), { wrapper })

      // Call the mutation
      result.current.mutate(mockPreferences)

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true)
        expect(result.current.data).toEqual(mockRecommendations)
      })

      expect(apiService.getRecommendations).toHaveBeenCalledWith(mockPreferences)
    })

    it('should handle recommendation errors', async () => {
      const mockPreferences = {
        location: 'Bellandur',
        budget: 'medium'
      }

      const mockError = {
        response: {
          status: 400,
          data: {
            message: 'Invalid preferences'
          }
        }
      }

      apiService.getRecommendations.mockRejectedValue(mockError)

      const { result } = renderHook(() => useRecommendations(), { wrapper })

      result.current.mutate(mockPreferences)

      await waitFor(() => {
        expect(result.current.isError).toBe(true)
      })

      expect(result.current.error).toEqual(mockError)
    })
  })

  describe('useApiMeta Hook', () => {
    it('should successfully fetch API metadata', async () => {
      const mockMeta = {
        status: 'success',
        data: {
          api_version: '1.0.0',
          phase: '6',
          supported_formats: ['json', 'html', 'cards'],
          available_locations: ['Bellandur', 'Delhi'],
          available_cuisines: ['North Indian', 'Chinese'],
          budget_options: ['low', 'medium', 'high'],
          validation: {
            max_text_length: 1000,
            required_fields: ['location', 'budget']
          }
        }
      }

      apiService.getMeta.mockResolvedValue(mockMeta)

      const { result } = renderHook(() => useApiMeta(), { wrapper })

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true)
        expect(result.current.data).toEqual(mockMeta)
      })

      expect(apiService.getMeta).toHaveBeenCalledTimes(1)
    })
  })

  describe('API Service Direct Tests', () => {
    it('should format error messages correctly', () => {
      const apiUtils = require('../src/services/apiService').apiUtils

      // Test API response error
      const apiError = {
        response: {
          data: {
            message: 'Custom API error message'
          }
        }
      }
      expect(apiUtils.formatError(apiError)).toBe('Custom API error message')

      // Test generic error
      const genericError = new Error('Generic error message')
      expect(apiUtils.formatError(genericError)).toBe('Generic error message')

      // Test no message
      const noMessageError = new Error()
      expect(apiUtils.formatError(noMessageError)).toBe('An unexpected error occurred.')
    })

    it('should check API availability', async () => {
      const apiUtils = require('../src/services/apiService').apiUtils

      // Test successful health check
      apiService.healthCheck.mockResolvedValue({ status: 'healthy' })
      const isAvailable = await apiUtils.isApiAvailable()
      expect(isAvailable).toBe(true)

      // Test failed health check
      apiService.healthCheck.mockRejectedValue(new Error('API down'))
      const notAvailable = await apiUtils.isApiAvailable()
      expect(notAvailable).toBe(false)
    })
  })
})
