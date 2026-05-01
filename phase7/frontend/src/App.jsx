import React from 'react'
import { useState } from 'react'
import { Search, Loader2, AlertCircle, CheckCircle } from 'lucide-react'
import PreferenceForm from './components/PreferenceForm/PreferenceForm'
import ResultsDisplay from './components/ResultsDisplay/ResultsDisplay'
import LoadingState from './components/LoadingStates/LoadingState'
import ErrorBoundary from './components/ErrorHandling/ErrorBoundary'
import { useRecommendations } from './hooks/useRecommendations'
import { useApiHealth } from './hooks/useApiHealth'

function App() {
  const [preferences, setPreferences] = useState(null)
  const [showResults, setShowResults] = useState(false)
  
  // API Health Check
  const { data: healthData, isLoading: healthLoading, error: healthError } = useApiHealth()
  
  // Recommendations Hook
  const {
    data: recommendations,
    isLoading: recommendationsLoading,
    error: recommendationsError,
    mutate: getRecommendations,
    reset
  } = useRecommendations()

  const handlePreferencesSubmit = (formData) => {
    setPreferences(formData)
    setShowResults(true)
    reset() // Reset previous recommendations
    getRecommendations(formData)
  }

  const handleNewSearch = () => {
    setPreferences(null)
    setShowResults(false)
    reset()
  }

  // Determine loading state
  const isLoading = healthLoading || recommendationsLoading

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <Search className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-xl font-bold text-slate-900">
                  Restaurant Recommendations
                </h1>
                <p className="text-sm text-slate-600">Phase 7 Frontend Web UI</p>
              </div>
            </div>
            
            {/* API Status */}
            <div className="flex items-center space-x-2">
              {healthLoading ? (
                <div className="flex items-center space-x-2 text-slate-500">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span className="text-sm">Checking API...</span>
                </div>
              ) : healthError ? (
                <div className="flex items-center space-x-2 text-red-600">
                  <AlertCircle className="w-4 h-4" />
                  <span className="text-sm">API Offline</span>
                </div>
              ) : healthData ? (
                <div className="flex items-center space-x-2 text-green-600">
                  <CheckCircle className="w-4 h-4" />
                  <span className="text-sm">API Online</span>
                </div>
              ) : null}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <ErrorBoundary>
          {!showResults ? (
            /* Preference Form View */
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2">
                <PreferenceForm 
                  onSubmit={handlePreferencesSubmit}
                  isLoading={isLoading}
                  apiDisabled={!!healthError}
                />
              </div>
              
              <div className="space-y-6">
                {/* Info Cards */}
                <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
                  <h3 className="text-lg font-semibold text-slate-900 mb-3">
                    How it Works
                  </h3>
                  <ol className="space-y-2 text-sm text-slate-600">
                    <li className="flex items-start">
                      <span className="flex-shrink-0 w-5 h-5 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-medium mr-2 mt-0.5">
                        1
                      </span>
                      <span>Enter your preferences for location, budget, and cuisine</span>
                    </li>
                    <li className="flex items-start">
                      <span className="flex-shrink-0 w-5 h-5 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-medium mr-2 mt-0.5">
                        2
                      </span>
                      <span>Our AI analyzes restaurants matching your criteria</span>
                    </li>
                    <li className="flex items-start">
                      <span className="flex-shrink-0 w-5 h-5 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-medium mr-2 mt-0.5">
                        3
                      </span>
                      <span>Get personalized recommendations with explanations</span>
                    </li>
                  </ol>
                </div>

                {/* Features */}
                <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
                  <h3 className="text-lg font-semibold text-slate-900 mb-3">
                    Features
                  </h3>
                  <ul className="space-y-2 text-sm text-slate-600">
                    <li className="flex items-center">
                      <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                      AI-powered recommendations
                    </li>
                    <li className="flex items-center">
                      <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                      Personalized explanations
                    </li>
                    <li className="flex items-center">
                      <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                      Multiple cuisine options
                    </li>
                    <li className="flex items-center">
                      <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                      Budget-friendly filtering
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          ) : (
            /* Results View */
            <div>
              <div className="mb-6">
                <button
                  onClick={handleNewSearch}
                  className="inline-flex items-center px-4 py-2 border border-slate-300 rounded-lg text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  ← New Search
                </button>
              </div>

              {recommendationsLoading ? (
                <LoadingState message="AI is analyzing restaurants for you..." />
              ) : recommendationsError ? (
                <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                  <div className="flex items-center space-x-3">
                    <AlertCircle className="w-6 h-6 text-red-600" />
                    <div>
                      <h3 className="text-lg font-semibold text-red-900">
                        Unable to Get Recommendations
                      </h3>
                      <p className="text-red-700 mt-1">
                        {recommendationsError.message || 'Please try again later.'}
                      </p>
                    </div>
                  </div>
                </div>
              ) : recommendations ? (
                <ResultsDisplay 
                  recommendations={recommendations}
                  preferences={preferences}
                />
              ) : null}
            </div>
          )}
        </ErrorBoundary>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-sm text-slate-600">
            <p>Phase 7 Frontend Web UI • Restaurant Recommendation System</p>
            <p className="mt-1">Powered by Phase 6 Backend HTTP API</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
