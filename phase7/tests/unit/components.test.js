import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { QueryClient, QueryClientProvider } from 'react-query'
import { BrowserRouter } from 'react-router-dom'
import PreferenceForm from '../../src/components/PreferenceForm/PreferenceForm'
import ResultsDisplay from '../../src/components/ResultsDisplay/ResultsDisplay'
import LoadingState from '../../src/components/LoadingStates/LoadingState'
import ErrorBoundary from '../../src/components/ErrorHandling/ErrorBoundary'

// Mock react-hot-toast
vi.mock('react-hot-toast', () => ({
  default: vi.fn(),
}))

// Mock hooks
vi.mock('../../src/hooks/useRecommendations', () => ({
  useApiHealth: () => ({ data: { status: 'healthy' }, isLoading: false, error: null }),
  useApiMeta: () => ({ 
    data: { 
      data: { 
        budget_options: ['low', 'medium', 'high'],
        rating_range: { min: 1.0, max: 5.0, step: 0.5 }
      }
    }, 
    isLoading: false 
  }),
  useLocations: () => ({ 
    data: ['Bellandur', 'Delhi', 'Mumbai'], 
    isLoading: false 
  }),
  useCuisines: () => ({ 
    data: ['North Indian', 'Chinese', 'Italian'], 
    isLoading: false 
  }),
}))

describe('Phase 7 Component Tests', () => {
  let queryClient
  let user

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
        mutations: { retry: false },
      },
    })
    user = userEvent.setup()
    vi.clearAllMocks()
  })

  const wrapper = ({ children }) => (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{children}</BrowserRouter>
    </QueryClientProvider>
  )

  describe('PreferenceForm Component', () => {
    it('should render preference form correctly', () => {
      const mockOnSubmit = vi.fn()
      render(<PreferenceForm onSubmit={mockOnSubmit} />, { wrapper })

      expect(screen.getByText('Find Your Perfect Restaurant')).toBeInTheDocument()
      expect(screen.getByLabelText(/location/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/budget/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/cuisine/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/minimum rating/i)).toBeInTheDocument()
    })

    it('should validate required fields', async () => {
      const mockOnSubmit = vi.fn()
      render(<PreferenceForm onSubmit={mockOnSubmit} />, { wrapper })

      const submitButton = screen.getByRole('button', { name: /get recommendations/i })
      await user.click(submitButton)

      // Should not call onSubmit due to validation
      expect(mockOnSubmit).not.toHaveBeenCalled()

      // Should show validation errors
      expect(screen.getByText(/location is required/i)).toBeInTheDocument()
      expect(screen.getByText(/budget is required/i)).toBeInTheDocument()
    })

    it('should submit form with valid data', async () => {
      const mockOnSubmit = vi.fn()
      render(<PreferenceForm onSubmit={mockOnSubmit} />, { wrapper })

      // Fill in required fields
      await user.selectOptions(screen.getByLabelText(/location/i), 'Bellandur')
      
      // Select budget
      const budgetButtons = screen.getAllByRole('radio')
      await user.click(budgetButtons[1]) // Medium budget

      const submitButton = screen.getByRole('button', { name: /get recommendations/i })
      await user.click(submitButton)

      await waitFor(() => {
        expect(mockOnSubmit).toHaveBeenCalledWith({
          location: 'Bellandur',
          budget: 'medium',
          cuisine: '',
          minRating: 3.0,
          topK: 5,
          additionalPreferences: ''
        })
      })
    })

    it('should handle additional preferences', async () => {
      const mockOnSubmit = vi.fn()
      render(<PreferenceForm onSubmit={mockOnSubmit} />, { wrapper })

      // Fill in required fields first
      await user.selectOptions(screen.getByLabelText(/location/i), 'Bellandur')
      const budgetButtons = screen.getAllByRole('radio')
      await user.click(budgetButtons[1])

      // Add additional preferences
      const preferenceInput = screen.getByPlaceholderText(/e.g., family-friendly/i)
      await user.type(preferenceInput, 'family-friendly')
      
      const addButton = screen.getByRole('button', { name: /add/i })
      await user.click(addButton)

      expect(screen.getByText('family-friendly')).toBeInTheDocument()

      // Submit form
      const submitButton = screen.getByRole('button', { name: /get recommendations/i })
      await user.click(submitButton)

      await waitFor(() => {
        expect(mockOnSubmit).toHaveBeenCalledWith(
          expect.objectContaining({
            additionalPreferences: 'family-friendly'
          })
        )
      })
    })

    it('should show API disabled state', () => {
      const mockOnSubmit = vi.fn()
      render(<PreferenceForm onSubmit={mockOnSubmit} apiDisabled={true} />, { wrapper })

      expect(screen.getByText(/api unavailable/i)).toBeInTheDocument()
      expect(screen.getByText(/please start the phase 6 backend api/i)).toBeInTheDocument()
    })
  })

  describe('ResultsDisplay Component', () => {
    const mockRecommendations = {
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

    const mockPreferences = {
      location: 'Bellandur',
      budget: 'medium',
      cuisine: 'North Indian',
      minRating: 3.5,
      topK: 5
    }

    it('should display recommendations correctly', () => {
      render(
        <ResultsDisplay 
          recommendations={mockRecommendations} 
          preferences={mockPreferences} 
        />, 
        { wrapper }
      )

      expect(screen.getByText(/your restaurant recommendations/i)).toBeInTheDocument()
      expect(screen.getByText('Test Restaurant')).toBeInTheDocument()
      expect(screen.getByText(/great match for your preferences/i)).toBeInTheDocument()
      expect(screen.getByText('Bellandur')).toBeInTheDocument()
      expect(screen.getByText('North Indian')).toBeInTheDocument()
      expect(screen.getByText('4.5')).toBeInTheDocument()
      expect(screen.getByText('₹800')).toBeInTheDocument()
    })

    it('should show empty state when no recommendations', () => {
      const emptyRecommendations = { data: { recommendations: [] } }
      
      render(
        <ResultsDisplay 
          recommendations={emptyRecommendations} 
          preferences={mockPreferences} 
        />, 
        { wrapper }
      )

      expect(screen.getByText(/no restaurants found/i)).toBeInTheDocument()
      expect(screen.getByText(/try adjusting your preferences/i)).toBeInTheDocument()
    })

    it('should expand and collapse details', async () => {
      render(
        <ResultsDisplay 
          recommendations={mockRecommendations} 
          preferences={mockPreferences} 
        />, 
        { wrapper }
      )

      const showDetailsButton = screen.getByRole('button', { name: /show details/i })
      await user.click(showDetailsButton)

      expect(screen.getByText(/hide details/i)).toBeInTheDocument()
      expect(screen.getByText(/match score/i)).toBeInTheDocument()
      expect(screen.getByText(/95.0%/i)).toBeInTheDocument()

      // Collapse details
      await user.click(screen.getByRole('button', { name: /hide details/i }))
      expect(screen.getByRole('button', { name: /show details/i })).toBeInTheDocument()
    })

    it('should copy as markdown', async () => {
      // Mock clipboard
      const mockWriteText = vi.fn().mockResolvedValue()
      Object.defineProperty(navigator, 'clipboard', {
        writable: true,
        value: {
          writeText: mockWriteText,
        },
      })

      render(
        <ResultsDisplay 
          recommendations={mockRecommendations} 
          preferences={mockPreferences} 
        />, 
        { wrapper }
      )

      const copyButton = screen.getByRole('button', { name: /copy/i })
      await user.click(copyButton)

      expect(mockWriteText).toHaveBeenCalledWith(
        expect.stringContaining('# Restaurant Recommendations')
      )
    })
  })

  describe('LoadingState Component', () => {
    it('should render default loading state', () => {
      render(<LoadingState />, { wrapper })

      expect(screen.getByText(/loading/i)).toBeInTheDocument()
      expect(screen.getByRole('status')).toBeInTheDocument()
    })

    it('should render searching loading state', () => {
      render(<LoadingState type="searching" />, { wrapper })

      expect(screen.getByText(/searching restaurants/i)).toBeInTheDocument()
      expect(screen.getByText(/scanning through thousands of restaurants/i)).toBeInTheDocument()
      expect(screen.getByText(/filtering by your preferences/i)).toBeInTheDocument()
    })

    it('should render analyzing loading state', () => {
      render(<LoadingState type="analyzing" />, { wrapper })

      expect(screen.getByText(/ai analysis/i)).toBeInTheDocument()
      expect(screen.getByText(/our ai is analyzing restaurants/i)).toBeInTheDocument()
    })
  })

  describe('ErrorBoundary Component', () => {
    it('should render error boundary when error occurs', () => {
      const ThrowError = () => {
        throw new Error('Test error')
      }

      render(
        <ErrorBoundary>
          <ThrowError />
        </ErrorBoundary>,
        { wrapper }
      )

      expect(screen.getByText(/something went wrong/i)).toBeInTheDocument()
      expect(screen.getByText(/we're sorry, but something unexpected happened/i)).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /reload page/i })).toBeInTheDocument()
    })

    it('should render children when no error', () => {
      render(
        <ErrorBoundary>
          <div>No error here</div>
        </ErrorBoundary>,
        { wrapper }
      )

      expect(screen.getByText('No error here')).toBeInTheDocument()
    })
  })
})
