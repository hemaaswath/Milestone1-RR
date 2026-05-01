"use client"

import { useState } from 'react'
import { SearchForm } from '@/components/search/search-form'
import { TrendingUp, MapPin, Clock, Star } from 'lucide-react'

export function SearchSection() {
  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Find Your Perfect Restaurant
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Use our AI-powered search to discover restaurants that match your exact preferences
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12 items-start">
          {/* Search Form */}
          <div>
            <SearchForm />
          </div>

          {/* Features */}
          <div className="space-y-8">
            <h3 className="text-2xl font-semibold text-gray-900 mb-6">
              Why Choose Our AI Recommendations?
            </h3>
            
            <div className="space-y-6">
              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0 w-12 h-12 bg-restaurant-primary/10 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-restaurant-primary" />
                </div>
                <div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">
                    Smart Matching Algorithm
                  </h4>
                  <p className="text-gray-600">
                    Our AI analyzes thousands of data points to find restaurants that perfectly match your preferences
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0 w-12 h-12 bg-restaurant-secondary/10 rounded-lg flex items-center justify-center">
                  <MapPin className="w-6 h-6 text-restaurant-secondary" />
                </div>
                <div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">
                    Location-Based Results
                  </h4>
                  <p className="text-gray-600">
                    Get recommendations from your preferred area with accurate distance and travel time estimates
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0 w-12 h-12 bg-restaurant-accent/10 rounded-lg flex items-center justify-center">
                  <Clock className="w-6 h-6 text-restaurant-accent" />
                </div>
                <div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">
                    Real-Time Availability
                  </h4>
                  <p className="text-gray-600">
                    Check current restaurant status and operating hours before you visit
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0 w-12 h-12 bg-yellow-500/10 rounded-lg flex items-center justify-center">
                  <Star className="w-6 h-6 text-yellow-500" />
                </div>
                <div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">
                    Quality Insights
                  </h4>
                  <p className="text-gray-600">
                    Get detailed explanations for why each restaurant is recommended for you
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Popular Searches */}
        <div className="mt-20">
          <h3 className="text-2xl font-semibold text-gray-900 text-center mb-8">
            Popular Searches
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              'Bellandur Restaurants',
              'Best North Indian Food',
              'Budget-Friendly Options',
              'Fine Dining Experience',
              'Quick Bites & Cafes',
              'Family-Friendly Places',
              'Romantic Dinner Spots',
              'Weekend Brunch',
            ].map((search) => (
              <button
                key={search}
                className="px-4 py-3 bg-white border border-gray-200 rounded-lg text-gray-700 hover:border-restaurant-primary hover:text-restaurant-primary transition-colors duration-200"
              >
                {search}
              </button>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
