"use client"

import { useState } from 'react'
import { Search, ArrowRight, Sparkles } from 'lucide-react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

export function HeroSection() {
  const [searchQuery, setSearchQuery] = useState('')
  const router = useRouter()

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      router.push(`/search?location=${encodeURIComponent(searchQuery.trim())}`)
    }
  }

  return (
    <section className="hero-gradient text-white py-20 lg:py-32">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* Badge */}
          <div className="inline-flex items-center px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-sm font-medium mb-8 animate-fade-in">
            <Sparkles className="w-4 h-4 mr-2" />
            Powered by Advanced AI Technology
          </div>

          {/* Main Heading */}
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 animate-slide-up">
            <span className="block">Discover Your Perfect</span>
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-yellow-200 to-pink-200">
              Dining Experience
            </span>
          </h1>

          {/* Subheading */}
          <p className="text-xl md:text-2xl text-white/90 mb-12 max-w-3xl mx-auto animate-slide-up" style={{ animationDelay: '0.1s' }}>
            Get personalized restaurant recommendations powered by AI. 
            Search by location, cuisine, budget, and preferences to find your perfect match.
          </p>

          {/* Search Form */}
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-12 animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <div className="flex flex-col sm:flex-row gap-4 bg-white/10 backdrop-blur-sm p-2 rounded-2xl">
              <div className="flex-1 relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/70" />
                <input
                  type="text"
                  placeholder="Enter location (e.g., Bellandur, Delhi)"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-4 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all duration-200"
                />
              </div>
              <button
                type="submit"
                className="px-8 py-4 bg-white text-gray-900 font-semibold rounded-xl hover:bg-gray-100 transition-all duration-200 flex items-center justify-center group"
              >
                Search Restaurants
                <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform duration-200" />
              </button>
            </div>
          </form>

          {/* Quick Links */}
          <div className="flex flex-wrap justify-center gap-6 animate-slide-up" style={{ animationDelay: '0.3s' }}>
            <Link
              href="/search"
              className="text-white/80 hover:text-white transition-colors duration-200 flex items-center"
            >
              Advanced Search
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
            <Link
              href="/dashboard"
              className="text-white/80 hover:text-white transition-colors duration-200 flex items-center"
            >
              View Dashboard
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
            <Link
              href="/monitoring"
              className="text-white/80 hover:text-white transition-colors duration-200 flex items-center"
            >
              System Status
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 mt-20 animate-fade-in" style={{ animationDelay: '0.4s' }}>
            <div className="text-center">
              <div className="text-4xl font-bold mb-2">12,140+</div>
              <div className="text-white/80">Restaurants</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold mb-2">349+</div>
              <div className="text-white/80">Locations</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold mb-2">50+</div>
              <div className="text-white/80">Cuisine Types</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
