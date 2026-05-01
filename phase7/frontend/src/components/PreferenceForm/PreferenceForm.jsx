import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { MapPin, DollarSign, Utensils, Star, Plus, Loader2 } from 'lucide-react'
import { useApiMeta, useLocations, useCuisines } from '../../hooks/useRecommendations'

const PreferenceForm = ({ onSubmit, isLoading, apiDisabled }) => {
  const [additionalPreferences, setAdditionalPreferences] = useState('')
  
  // React Hook Form
  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
    watch,
    setValue,
    trigger,
  } = useForm({
    mode: 'onChange',
    defaultValues: {
      location: '',
      budget: '',
      cuisine: '',
      minRating: 3.0,
      topK: 5,
      additionalPreferences: '',
    },
  })

  // API Data
  const { data: meta, isLoading: metaLoading } = useApiMeta()
  const { data: locations, isLoading: locationsLoading } = useLocations()
  const { data: cuisines, isLoading: cuisinesLoading } = useCuisines()

  const selectedLocation = watch('location')
  const selectedBudget = watch('budget')
  const selectedCuisine = watch('cuisine')

  // Form submission handler
  const onFormSubmit = (data) => {
    const formData = {
      ...data,
      additionalPreferences: additionalPreferences.trim(),
    }
    onSubmit(formData)
  }

  // Add additional preference
  const handleAddPreference = () => {
    if (additionalPreferences.trim()) {
      const currentAdditional = watch('additionalPreferences') || ''
      const newAdditional = currentAdditional 
        ? `${currentAdditional}, ${additionalPreferences.trim()}`
        : additionalPreferences.trim()
      
      setValue('additionalPreferences', newAdditional)
      setAdditionalPreferences('')
      trigger('additionalPreferences')
    }
  }

  // Get budget options from API or fallback
  const budgetOptions = meta?.data?.budget_options || ['low', 'medium', 'high']
  
  // Get rating range from API or fallback
  const ratingRange = meta?.data?.rating_range || { min: 1.0, max: 5.0, step: 0.5 }

  if (apiDisabled) {
    return (
      <div className="card">
        <div className="card-body">
          <div className="text-center py-12">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mb-4">
              <MapPin className="w-8 h-8 text-red-600" />
            </div>
            <h3 className="text-lg font-semibold text-slate-900 mb-2">
              API Unavailable
            </h3>
            <p className="text-slate-600 mb-4">
              Please start the Phase 6 Backend API to use this application.
            </p>
            <div className="bg-slate-50 rounded-lg p-4 text-left">
              <p className="text-sm font-medium text-slate-900 mb-2">
                To start the API:
              </p>
              <code className="block text-xs bg-slate-800 text-slate-100 p-2 rounded">
                cd "c:/Users/Family/Documents/Milestone1-Build Hours"<br/>
                python scripts/test_phase6_direct.py
              </code>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="text-xl font-semibold text-slate-900">
          Find Your Perfect Restaurant
        </h2>
        <p className="text-slate-600 mt-1">
          Tell us your preferences and we'll find the best restaurants for you.
        </p>
      </div>

      <form onSubmit={handleSubmit(onFormSubmit)} className="card-body space-y-6">
        {/* Location */}
        <div className="form-group">
          <label htmlFor="location" className="form-label">
            <MapPin className="w-4 h-4 inline mr-2" />
            Location *
          </label>
          {locationsLoading ? (
            <div className="skeleton-text h-10 w-full"></div>
          ) : (
            <select
              id="location"
              className="form-input"
              {...register('location', { required: 'Location is required' })}
              disabled={isLoading}
            >
              <option value="">Select a location</option>
              {locations?.map((location) => (
                <option key={location} value={location}>
                  {location}
                </option>
              ))}
            </select>
          )}
          {errors.location && (
            <p className="form-error">{errors.location.message}</p>
          )}
        </div>

        {/* Budget */}
        <div className="form-group">
          <label htmlFor="budget" className="form-label">
            <DollarSign className="w-4 h-4 inline mr-2" />
            Budget *
          </label>
          <div className="grid grid-cols-3 gap-3">
            {budgetOptions.map((budget) => (
              <label
                key={budget}
                className={`
                  relative flex items-center justify-center px-4 py-3 border rounded-lg cursor-pointer transition-colors
                  ${selectedBudget === budget
                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                    : 'border-slate-300 bg-white text-slate-700 hover:bg-slate-50'
                  }
                  ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}
                `}
              >
                <input
                  type="radio"
                  value={budget}
                  className="sr-only"
                  {...register('budget', { required: 'Budget is required' })}
                  disabled={isLoading}
                />
                <span className="capitalize font-medium">{budget}</span>
              </label>
            ))}
          </div>
          {errors.budget && (
            <p className="form-error">{errors.budget.message}</p>
          )}
        </div>

        {/* Cuisine */}
        <div className="form-group">
          <label htmlFor="cuisine" className="form-label">
            <Utensils className="w-4 h-4 inline mr-2" />
            Cuisine Preference
          </label>
          {cuisinesLoading ? (
            <div className="skeleton-text h-10 w-full"></div>
          ) : (
            <select
              id="cuisine"
              className="form-input"
              {...register('cuisine')}
              disabled={isLoading}
            >
              <option value="">Any cuisine</option>
              {cuisines?.map((cuisine) => (
                <option key={cuisine} value={cuisine}>
                  {cuisine}
                </option>
              ))}
            </select>
          )}
          <p className="form-help">Optional - Leave empty for any cuisine</p>
        </div>

        {/* Minimum Rating */}
        <div className="form-group">
          <label htmlFor="minRating" className="form-label">
            <Star className="w-4 h-4 inline mr-2" />
            Minimum Rating
          </label>
          <div className="flex items-center space-x-4">
            <input
              type="range"
              id="minRating"
              min={ratingRange.min}
              max={ratingRange.max}
              step={ratingRange.step}
              className="flex-1"
              {...register('minRating')}
              disabled={isLoading}
            />
            <span className="text-sm font-medium text-slate-700 w-12 text-right">
              {watch('minRating')?.toFixed(1)}
            </span>
          </div>
          <p className="form-help">
            Only show restaurants with rating {watch('minRating')?.toFixed(1)} or higher
          </p>
        </div>

        {/* Number of Recommendations */}
        <div className="form-group">
          <label htmlFor="topK" className="form-label">
            Number of Recommendations
          </label>
          <select
            id="topK"
            className="form-input"
            {...register('topK')}
            disabled={isLoading}
          >
            <option value={3}>3 recommendations</option>
            <option value={5}>5 recommendations</option>
            <option value={7}>7 recommendations</option>
            <option value={10}>10 recommendations</option>
          </select>
        </div>

        {/* Additional Preferences */}
        <div className="form-group">
          <label htmlFor="additionalPreferences" className="form-label">
            <Plus className="w-4 h-4 inline mr-2" />
            Additional Preferences
          </label>
          <div className="space-y-3">
            <div className="flex space-x-2">
              <input
                type="text"
                value={additionalPreferences}
                onChange={(e) => setAdditionalPreferences(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddPreference())}
                placeholder="e.g., family-friendly, outdoor seating, parking"
                className="form-input flex-1"
                disabled={isLoading}
              />
              <button
                type="button"
                onClick={handleAddPreference}
                disabled={!additionalPreferences.trim() || isLoading}
                className="btn btn-outline"
              >
                Add
              </button>
            </div>
            
            {/* Display added preferences */}
            {watch('additionalPreferences') && (
              <div className="flex flex-wrap gap-2">
                {watch('additionalPreferences').split(',').map((pref, index) => (
                  <span
                    key={index}
                    className="badge badge-primary"
                  >
                    {pref.trim()}
                  </span>
                ))}
              </div>
            )}
          </div>
          <p className="form-help">
            Add specific requirements like "family-friendly" or "parking available"
          </p>
        </div>

        {/* Submit Button */}
        <div className="pt-4">
          <button
            type="submit"
            disabled={!isValid || isLoading || !selectedLocation || !selectedBudget}
            className="btn btn-primary w-full text-lg py-3"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 loading-spinner" />
                Finding Restaurants...
              </>
            ) : (
              'Get Recommendations'
            )}
          </button>
          
          {!isValid && (selectedLocation || selectedBudget) && (
            <p className="text-sm text-slate-500 mt-2 text-center">
              Please fix any errors above to continue
            </p>
          )}
        </div>
      </form>
    </div>
  )
}

export default PreferenceForm
