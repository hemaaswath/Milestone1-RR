import React from 'react'
import { AlertTriangle, RefreshCw, Home } from 'lucide-react'

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null, errorInfo: null }
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    // Catch errors in any components below and re-render with error message
    this.setState({
      error: error,
      errorInfo: errorInfo
    })
    
    // Log error to console
    console.error('ErrorBoundary caught an error:', error, errorInfo)
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null })
  }

  handleGoHome = () => {
    window.location.reload()
  }

  render() {
    if (this.state.hasError) {
      // You can render any custom fallback UI
      return (
        <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
          <div className="max-w-md w-full bg-white rounded-lg shadow-lg border border-slate-200 p-8">
            <div className="text-center">
              {/* Error Icon */}
              <div className="inline-flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mb-4">
                <AlertTriangle className="w-8 h-8 text-red-600" />
              </div>

              {/* Error Title */}
              <h1 className="text-2xl font-bold text-slate-900 mb-2">
                Something went wrong
              </h1>
              
              {/* Error Message */}
              <p className="text-slate-600 mb-6">
                We're sorry, but something unexpected happened. 
                Our team has been notified and we're working to fix this issue.
              </p>

              {/* Error Details (Development Only) */}
              {process.env.NODE_ENV === 'development' && this.state.error && (
                <details className="text-left mb-6 p-4 bg-slate-50 rounded-lg border border-slate-200">
                  <summary className="cursor-pointer font-medium text-slate-700 mb-2">
                    Error Details (Development)
                  </summary>
                  <div className="mt-2 text-xs">
                    <div className="mb-2">
                      <strong>Error:</strong>
                      <pre className="mt-1 p-2 bg-red-50 border border-red-200 rounded text-red-800 overflow-auto">
                        {this.state.error.toString()}
                      </pre>
                    </div>
                    <div>
                      <strong>Component Stack:</strong>
                      <pre className="mt-1 p-2 bg-red-50 border border-red-200 rounded text-red-800 overflow-auto">
                        {this.state.errorInfo.componentStack}
                      </pre>
                    </div>
                  </div>
                </details>
              )}

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-3">
                <button
                  onClick={this.handleReset}
                  className="btn btn-primary flex items-center justify-center"
                >
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Try Again
                </button>
                <button
                  onClick={this.handleGoHome}
                  className="btn btn-outline flex items-center justify-center"
                >
                  <Home className="w-4 h-4 mr-2" />
                  Reload Page
                </button>
              </div>

              {/* Help Text */}
              <p className="text-sm text-slate-500 mt-6">
                If this problem persists, please contact our support team.
              </p>
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
