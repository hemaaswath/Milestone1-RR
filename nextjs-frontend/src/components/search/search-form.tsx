"use client"

import { useState } from 'react'
import { Search, MapPin, DollarSign, Star, ArrowRight } from 'lucide-react'
import { useRouter } from 'next/navigation'

export function SearchForm() {
  const [formData, setFormData] = useState({
    location: '',
    budget: 'medium',
    cuisine: '',
    min_rating: 3,
    additional_preferences: '',
  })
  
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    
    // Navigate to search results page with query parameters
    const params = new URLSearchParams({
      location: formData.location,
      budget: formData.budget,
      ...(formData.cuisine && { cuisine: formData.cuisine }),
      ...(formData.min_rating && { min_rating: formData.min_rating.toString() }),
      ...(formData.additional_preferences && { additional_preferences: formData.additional_preferences }),
    })
    
    router.push(`/search?${params.toString()}`)
    setIsLoading(false)
  }

  const handleInputChange = (field: string, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  return (
    <div className="bg-white rounded-2xl shadow-lg p-8">
      <h3 className="text-2xl font-bold text-gray-900 mb-6">
        Find Your Perfect Restaurant
      </h3>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Location Input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <MapPin className="w-4 h-4 inline mr-1" />
            Location
          </label>
          <input
            type="text"
            value={formData.location}
            onChange={(e) => handleInputChange('location', e.target.value)}
            placeholder="Enter location (e.g., Bellandur, Delhi)"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-restaurant-primary focus:border-transparent"
            required
          />
        </div>

        {/* Budget Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <DollarSign className="w-4 h-4 inline mr-1" />
            Budget Range
          </label>
          <div className="grid grid-cols-3 gap-3">
            {[
              { value: 'low', label: 'Low (Under ₹600)' },
              { value: 'medium', label: 'Medium (₹600-1500)' },
              { value: 'high', label: 'High (Above ₹1500)' },
            ].map((budget) => (
              <button
                key={budget.value}
                type="button"
                onClick={() => handleInputChange('budget', budget.value)}
                className={`px-4 py-2 rounded-lg border transition-colors duration-200 ${
                  formData.budget === budget.value
                    ? 'border-restaurant-primary bg-restaurant-primary/10 text-restaurant-primary'
                    : 'border-gray-300 hover:border-gray-400'
                }`}
              >
                {budget.label}
              </button>
            ))}
          </div>
        </div>

        {/* Cuisine Input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Cuisine Type (Optional)
          </label>
          <input
            type="text"
            value={formData.cuisine}
            onChange={(e) => handleInputChange('cuisine', e.target.value)}
            placeholder="e.g., North Indian, Chinese, Italian"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-restaurant-primary focus:border-transparent"
          />
        </div>

        {/* Rating Slider */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Star className="w-4 h-4 inline mr-1" />
            Minimum Rating: {formData.min_rating} ⭐
          </label>
          <input
            type="range"
            min="1"
            max="5"
            step="0.5"
            value={formData.min_rating}
            onChange={(e) => handleInputChange('min_rating', parseFloat(e.target.value))}
            className="w-full"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>1 ⭐</span>
            <span>2 ⭐</span>
            <span>3 ⭐</span>
            <span>4 ⭐</span>
            <span>5 ⭐</span>
          </div>
        </div>

        {/* Additional Preferences */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Additional Preferences (Optional)
          </label>
          <textarea
            value={formData.additional_preferences}
            onChange={(e) => handleInputChange('additional_preferences', e.target.value)}
            placeholder="e.g., outdoor seating, parking, family-friendly, romantic atmosphere"
            rows={3}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-restaurant-primary focus:border-transparent"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading || !formData.location}
          className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <div className="flex items-center justify-center">
              <div className="loading-spinner mr-2"></div>
              Searching...
            </div>
          ) : (
            <div className="flex items-center justify-center">
              <Search className="w-5 h-5 mr-2" />
              Find Restaurants
              <ArrowRight className="w-5 h-5 ml-2" />
            </div>
          )}
        </button>
      </form>
    </div>
  )
}
