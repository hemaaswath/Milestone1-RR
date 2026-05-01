import { ArrowRight, Sparkles } from 'lucide-react'
import Link from 'next/link'

export function CTASection() {
  return (
    <section className="hero-gradient py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="max-w-3xl mx-auto">
          <div className="inline-flex items-center px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-sm font-medium mb-8">
            <Sparkles className="w-4 h-4 mr-2" />
            Ready to discover amazing restaurants?
          </div>
          
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Find Your Perfect Dining Experience Today
          </h2>
          
          <p className="text-xl text-white/90 mb-8">
            Join thousands of users who have discovered their favorite restaurants through our AI-powered recommendations
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/search"
              className="btn-primary bg-white text-gray-900 hover:bg-gray-100"
            >
              Start Searching
              <ArrowRight className="w-5 h-5 ml-2" />
            </Link>
            
            <Link
              href="/dashboard"
              className="btn-secondary bg-transparent border-2 border-white text-white hover:bg-white hover:text-gray-900"
            >
              View Dashboard
            </Link>
          </div>
          
          <div className="mt-12 grid grid-cols-1 sm:grid-cols-3 gap-8 text-white">
            <div>
              <div className="text-3xl font-bold mb-2">12,140+</div>
              <div className="text-white/80">Restaurants</div>
            </div>
            <div>
              <div className="text-3xl font-bold mb-2">98%</div>
              <div className="text-white/80">User Satisfaction</div>
            </div>
            <div>
              <div className="text-3xl font-bold mb-2">24/7</div>
              <div className="text-white/80">AI Support</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
