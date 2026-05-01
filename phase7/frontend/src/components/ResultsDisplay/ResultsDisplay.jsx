import React, { useState } from 'react'
import { 
  MapPin, 
  DollarSign, 
  Star, 
  Clock, 
  Copy, 
  Download,
  TrendingUp,
  Award,
  Info
} from 'lucide-react'
import toast from 'react-hot-toast'

const ResultsDisplay = ({ recommendations, preferences }) => {
  const [expandedCard, setExpandedCard] = useState(null)
  
  const recommendationList = recommendations?.data?.recommendations || []
  const summary = recommendations?.data?.summary || {}
  const metadata = recommendations?.metadata || {}

  // Copy results as Markdown
  const copyAsMarkdown = () => {
    const markdown = generateMarkdownResults()
    navigator.clipboard.writeText(markdown)
    toast.success('Results copied to clipboard!')
  }

  // Download results as JSON
  const downloadAsJSON = () => {
    const dataStr = JSON.stringify(recommendations, null, 2)
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)
    
    const exportFileDefaultName = `restaurant-recommendations-${new Date().toISOString().split('T')[0]}.json`
    
    const linkElement = document.createElement('a')
    linkElement.setAttribute('href', dataUri)
    linkElement.setAttribute('download', exportFileDefaultName)
    linkElement.click()
    
    toast.success('Results downloaded!')
  }

  // Generate Markdown format
  const generateMarkdownResults = () => {
    let markdown = `# Restaurant Recommendations\n\n`
    markdown += `**Generated:** ${new Date().toLocaleString()}\n\n`
    
    if (preferences) {
      markdown += `## Your Preferences\n`
      markdown += `- **Location:** ${preferences.location}\n`
      markdown += `- **Budget:** ${preferences.budget}\n`
      if (preferences.cuisine) markdown += `- **Cuisine:** ${preferences.cuisine}\n`
      markdown += `- **Min Rating:** ${preferences.minRating}/5\n`
      markdown += `- **Results:** ${preferences.topK} recommendations\n\n`
    }

    markdown += `## Recommendations\n\n`
    
    recommendationList.forEach((restaurant, index) => {
      markdown += `### ${index + 1}. ${restaurant.restaurant_name}\n\n`
      markdown += `**Rank:** #${restaurant.rank} (Score: ${(restaurant.score * 100).toFixed(1)}%)\n\n`
      markdown += `**Location:** ${restaurant.location}\n`
      markdown += `**Cuisines:** ${restaurant.cuisines}\n`
      markdown += `**Rating:** ${restaurant.rating}/5 ⭐\n`
      markdown += `**Cost for Two:** ₹${restaurant.cost_for_two}\n\n`
      markdown += `**Why we recommend it:**\n> ${restaurant.explanation}\n\n`
      markdown += `---\n\n`
    })

    if (summary) {
      markdown += `## Summary\n\n`
      markdown += `- **Total Candidates:** ${summary.total_candidates}\n`
      markdown += `- **Filtered Candidates:** ${summary.filtered_candidates}\n`
      markdown += `- **Final Recommendations:** ${summary.final_recommendations}\n`
      if (summary.avg_rating) markdown += `- **Average Rating:** ${summary.avg_rating.toFixed(1)}/5\n`
    }

    return markdown
  }

  // Format currency
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(amount)
  }

  // Get rating color
  const getRatingColor = (rating) => {
    if (rating >= 4.5) return 'text-green-600'
    if (rating >= 4.0) return 'text-blue-600'
    if (rating >= 3.5) return 'text-yellow-600'
    return 'text-red-600'
  }

  // Get budget color
  const getBudgetColor = (budget) => {
    switch (budget?.toLowerCase()) {
      case 'low': return 'text-green-600 bg-green-50'
      case 'medium': return 'text-yellow-600 bg-yellow-50'
      case 'high': return 'text-red-600 bg-red-50'
      default: return 'text-slate-600 bg-slate-50'
    }
  }

  if (recommendationList.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-slate-100 rounded-full mb-4">
          <MapPin className="w-8 h-8 text-slate-600" />
        </div>
        <h3 className="text-lg font-semibold text-slate-900 mb-2">
          No Restaurants Found
        </h3>
        <p className="text-slate-600 max-w-md mx-auto">
          We couldn't find any restaurants matching your criteria. Try adjusting your preferences or expanding your search area.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Results Header */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-slate-900 mb-2">
              Your Restaurant Recommendations
            </h2>
            <p className="text-slate-600">
              Found {recommendationList.length} perfect match{recommendationList.length > 1 ? 'es' : ''} for you
            </p>
          </div>
          
          {/* Action Buttons */}
          <div className="flex space-x-2">
            <button
              onClick={copyAsMarkdown}
              className="btn btn-outline"
              title="Copy as Markdown"
            >
              <Copy className="w-4 h-4 mr-2" />
              Copy
            </button>
            <button
              onClick={downloadAsJSON}
              className="btn btn-outline"
              title="Download as JSON"
            >
              <Download className="w-4 h-4 mr-2" />
              Download
            </button>
          </div>
        </div>

        {/* Summary Stats */}
        {summary && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-6 border-t border-slate-200">
            <div className="text-center">
              <div className="text-2xl font-bold text-slate-900">{summary.total_candidates}</div>
              <div className="text-sm text-slate-600">Total Candidates</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-slate-900">{summary.filtered_candidates}</div>
              <div className="text-sm text-slate-600">Filtered</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{summary.final_recommendations}</div>
              <div className="text-sm text-slate-600">Recommended</div>
            </div>
            {summary.avg_rating && (
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-600">{summary.avg_rating.toFixed(1)}</div>
                <div className="text-sm text-slate-600">Avg Rating</div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Recommendation Cards */}
      <div className="space-y-4">
        {recommendationList.map((restaurant, index) => (
          <div
            key={index}
            className="card hover-lift hover-shadow transition-all duration-200"
          >
            <div className="card-body">
              {/* Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <div className="flex items-center justify-center w-8 h-8 bg-blue-100 text-blue-600 rounded-full font-bold text-sm">
                      {restaurant.rank}
                    </div>
                    <h3 className="text-xl font-bold text-slate-900">
                      {restaurant.restaurant_name}
                    </h3>
                    <div className="flex items-center space-x-2">
                      <span className={`badge ${getBudgetColor(preferences?.budget)}`}>
                        {preferences?.budget?.charAt(0).toUpperCase() + preferences?.budget?.slice(1)}
                      </span>
                      <span className="badge badge-primary">
                        {(restaurant.score * 100).toFixed(1)}% Match
                      </span>
                    </div>
                  </div>
                  
                  {/* Location and Cuisine */}
                  <div className="flex items-center space-x-4 text-sm text-slate-600 mb-3">
                    <div className="flex items-center">
                      <MapPin className="w-4 h-4 mr-1" />
                      {restaurant.location}
                    </div>
                    <div className="flex items-center">
                      <Utensils className="w-4 h-4 mr-1" />
                      {restaurant.cuisines}
                    </div>
                  </div>
                </div>
              </div>

              {/* Rating and Cost */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center">
                    <Star className="w-5 h-5 text-yellow-500 mr-1" />
                    <span className={`font-semibold ${getRatingColor(restaurant.rating)}`}>
                      {restaurant.rating}
                    </span>
                    <span className="text-slate-500 ml-1">/5</span>
                  </div>
                  <div className="flex items-center">
                    <DollarSign className="w-5 h-5 text-green-600 mr-1" />
                    <span className="font-semibold text-slate-900">
                      {formatCurrency(restaurant.cost_for_two)}
                    </span>
                    <span className="text-slate-500 ml-1">for two</span>
                  </div>
                </div>
              </div>

              {/* AI Explanation */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-start space-x-3">
                  <Award className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <h4 className="font-semibold text-blue-900 mb-1">
                      Why we recommend this restaurant
                    </h4>
                    <p className="text-blue-800 text-sm leading-relaxed">
                      {restaurant.explanation}
                    </p>
                  </div>
                </div>
              </div>

              {/* Expand/Collapse Details */}
              <div className="mt-4 pt-4 border-t border-slate-200">
                <button
                  onClick={() => setExpandedCard(expandedCard === index ? null : index)}
                  className="flex items-center text-sm text-blue-600 hover:text-blue-700 font-medium"
                >
                  <Info className="w-4 h-4 mr-1" />
                  {expandedCard === index ? 'Hide' : 'Show'} Details
                </button>
                
                {expandedCard === index && (
                  <div className="mt-4 space-y-3 text-sm">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <span className="font-medium text-slate-700">Match Score:</span>
                        <div className="flex items-center mt-1">
                          <div className="flex-1 bg-slate-200 rounded-full h-2 mr-2">
                            <div 
                              className="bg-blue-600 h-2 rounded-full"
                              style={{ width: `${restaurant.score * 100}%` }}
                            ></div>
                          </div>
                          <span className="text-slate-600">
                            {(restaurant.score * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>
                      <div>
                        <span className="font-medium text-slate-700">Rank:</span>
                        <div className="flex items-center mt-1">
                          <TrendingUp className="w-4 h-4 text-green-600 mr-1" />
                          <span className="text-slate-600">#{restaurant.rank} recommendation</span>
                        </div>
                      </div>
                    </div>
                    
                    {/* Performance Metadata */}
                    {metadata?.pipeline_performance && (
                      <div className="bg-slate-50 rounded-lg p-3">
                        <h5 className="font-medium text-slate-700 mb-2">Processing Info</h5>
                        <div className="grid grid-cols-2 gap-2 text-xs text-slate-600">
                          <div>Analysis time: {metadata.pipeline_performance.total_duration_ms}ms</div>
                          <div>AI model: {metadata.model_info?.model}</div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ResultsDisplay
