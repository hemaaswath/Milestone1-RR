import { useMutation, useQuery } from 'react-query'
import { apiService } from '../services/apiService'
import toast from 'react-hot-toast'

export const useRecommendations = () => {
  // Mutation for getting recommendations
  const {
    data,
    error,
    isLoading,
    mutate,
    reset,
  } = useMutation(
    apiService.getRecommendations,
    {
      onSuccess: (data) => {
        console.log('✅ Recommendations received:', data)
        
        // Show success toast
        const recommendations = data.data?.recommendations || []
        if (recommendations.length > 0) {
          toast.success(`Found ${recommendations.length} restaurant${recommendations.length > 1 ? 's' : ''} for you!`)
        } else {
          toast('No restaurants found matching your criteria', {
            icon: '🔍',
          })
        }
      },
      onError: (error) => {
        console.error('❌ Recommendations error:', error)
        
        // Show error toast with specific message
        const errorMessage = error.response?.data?.message || error.message || 'Failed to get recommendations'
        toast.error(errorMessage)
      },
    }
  )

  return {
    data,
    error,
    isLoading,
    mutate,
    reset,
  }
}

// Hook for getting API metadata (locations, cuisines, etc.)
export const useApiMeta = () => {
  return useQuery(
    'apiMeta',
    apiService.getMeta,
    {
      staleTime: 10 * 60 * 1000, // 10 minutes
      cacheTime: 15 * 60 * 1000, // 15 minutes
      retry: 2,
      onError: (error) => {
        console.error('Failed to load API metadata:', error)
        toast.error('Failed to load form options')
      },
    }
  )
}

// Hook for getting locations
export const useLocations = () => {
  return useQuery(
    'locations',
    apiService.getLocations,
    {
      staleTime: 30 * 60 * 1000, // 30 minutes
      cacheTime: 60 * 60 * 1000, // 1 hour
      retry: 2,
      select: (data) => data.data?.locations || [],
    }
  )
}

// Hook for getting cuisines
export const useCuisines = () => {
  return useQuery(
    'cuisines',
    apiService.getCuisines,
    {
      staleTime: 30 * 60 * 1000, // 30 minutes
      cacheTime: 60 * 60 * 1000, // 1 hour
      retry: 2,
      select: (data) => data.data?.cuisines || [],
    }
  )
}
