import { useQuery } from 'react-query'
import { apiService } from '../services/apiService'

export const useApiHealth = () => {
  return useQuery(
    'apiHealth',
    apiService.healthCheck,
    {
      refetchInterval: 30000, // Refetch every 30 seconds
      retry: 2,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 5000),
      onError: (error) => {
        console.error('API Health Check Failed:', error)
      },
    }
  )
}
