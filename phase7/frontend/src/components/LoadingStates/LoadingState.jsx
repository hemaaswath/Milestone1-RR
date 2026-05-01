import React from 'react'
import { Loader2, Search, Brain, MapPin } from 'lucide-react'

const LoadingState = ({ message = 'Loading...', type = 'default' }) => {
  const getLoadingContent = () => {
    switch (type) {
      case 'searching':
        return {
          icon: <Search className="w-8 h-8" />,
          title: 'Searching Restaurants',
          message: message || 'Scanning through thousands of restaurants...',
          steps: [
            'Filtering by your preferences',
            'Checking availability',
            'Preparing recommendations'
          ]
        }
      case 'analyzing':
        return {
          icon: <Brain className="w-8 h-8" />,
          title: 'AI Analysis',
          message: message || 'Our AI is analyzing restaurants for you...',
          steps: [
            'Processing restaurant data',
            'Running preference matching',
            'Generating personalized recommendations'
          ]
        }
      case 'location':
        return {
          icon: <MapPin className="w-8 h-8" />,
          title: 'Finding Locations',
          message: message || 'Discovering restaurants in your area...',
          steps: [
            'Loading restaurant database',
            'Filtering by location',
            'Preparing options'
          ]
        }
      default:
        return {
          icon: <Loader2 className="w-8 h-8" />,
          title: 'Loading',
          message: message,
          steps: []
        }
    }
  }

  const content = getLoadingContent()

  return (
    <div className="flex flex-col items-center justify-center py-12">
      {/* Animated Icon */}
      <div className="relative mb-6">
        <div className="absolute inset-0 bg-blue-100 rounded-full animate-ping"></div>
        <div className="relative flex items-center justify-center w-16 h-16 bg-blue-600 text-white rounded-full">
          {React.cloneElement(content.icon, { className: 'w-8 h-8 loading-spinner' })}
        </div>
      </div>

      {/* Title and Message */}
      <h3 className="text-xl font-semibold text-slate-900 mb-2">
        {content.title}
      </h3>
      <p className="text-slate-600 text-center max-w-md mb-6">
        {content.message}
      </p>

      {/* Progress Steps */}
      {content.steps.length > 0 && (
        <div className="w-full max-w-md">
          <div className="space-y-3">
            {content.steps.map((step, index) => (
              <div key={index} className="flex items-center space-x-3">
                <div className="relative">
                  <div className="w-8 h-8 bg-slate-200 rounded-full flex items-center justify-center">
                    <Loader2 className="w-4 h-4 text-slate-600 loading-spinner" />
                  </div>
                  {index < content.steps.length - 1 && (
                    <div className="absolute top-8 left-4 w-0.5 h-6 bg-slate-200"></div>
                  )}
                </div>
                <div className="flex-1">
                  <p className="text-sm text-slate-600">{step}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Loading Dots */}
      <div className="flex items-center space-x-2 mt-8">
        <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
        <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
        <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
      </div>
    </div>
  )
}

// Skeleton Loading Components
export const SkeletonCard = () => (
  <div className="card">
    <div className="card-body space-y-4">
      <div className="flex items-center space-x-3">
        <div className="skeleton-avatar"></div>
        <div className="flex-1 space-y-2">
          <div className="skeleton-text h-4 w-3/4"></div>
          <div className="skeleton-text-sm h-3 w-1/2"></div>
        </div>
      </div>
      <div className="space-y-2">
        <div className="skeleton-text h-3 w-full"></div>
        <div className="skeleton-text h-3 w-5/6"></div>
      </div>
    </div>
  </div>
)

export const SkeletonForm = () => (
  <div className="card">
    <div className="card-body space-y-6">
      <div className="space-y-2">
        <div className="skeleton-text h-4 w-1/4"></div>
        <div className="skeleton-text h-10 w-full"></div>
      </div>
      <div className="space-y-2">
        <div className="skeleton-text h-4 w-1/4"></div>
        <div className="grid grid-cols-3 gap-3">
          <div className="skeleton-text h-10"></div>
          <div className="skeleton-text h-10"></div>
          <div className="skeleton-text h-10"></div>
        </div>
      </div>
      <div className="space-y-2">
        <div className="skeleton-text h-4 w-1/4"></div>
        <div className="skeleton-text h-10 w-full"></div>
      </div>
      <div className="skeleton-text h-12 w-full"></div>
    </div>
  </div>
)

export const SkeletonResults = () => (
  <div className="space-y-4">
    {[1, 2, 3].map((i) => (
      <SkeletonCard key={i} />
    ))}
  </div>
)

// Inline Loading Spinner
export const InlineSpinner = ({ size = 'sm', className = '' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
  }

  return (
    <Loader2 className={`loading-spinner ${sizeClasses[size]} ${className}`} />
  )
}

// Progress Bar
export const ProgressBar = ({ progress = 0, showPercentage = true, className = '' }) => (
  <div className={`w-full ${className}`}>
    <div className="flex items-center justify-between mb-2">
      <span className="text-sm text-slate-600">Progress</span>
      {showPercentage && (
        <span className="text-sm font-medium text-slate-900">{progress}%</span>
      )}
    </div>
    <div className="w-full bg-slate-200 rounded-full h-2">
      <div 
        className="bg-blue-600 h-2 rounded-full transition-all duration-300 ease-out"
        style={{ width: `${progress}%` }}
      ></div>
    </div>
  </div>
)

// Full Page Loading
export const FullPageLoading = ({ message = 'Loading...' }) => (
  <div className="fixed inset-0 bg-white bg-opacity-90 flex items-center justify-center z-50">
    <div className="text-center">
      <div className="relative mb-6">
        <div className="absolute inset-0 bg-blue-100 rounded-full animate-ping"></div>
        <div className="relative flex items-center justify-center w-16 h-16 bg-blue-600 text-white rounded-full">
          <Loader2 className="w-8 h-8 loading-spinner" />
        </div>
      </div>
      <h3 className="text-xl font-semibold text-slate-900 mb-2">
        {message}
      </h3>
      <div className="flex items-center space-x-2">
        <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
        <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
        <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
      </div>
    </div>
  </div>
)

export default LoadingState
