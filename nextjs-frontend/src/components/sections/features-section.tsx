import { Brain, MapPin, Clock, Shield, TrendingUp, Users } from 'lucide-react'

export function FeaturesSection() {
  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Recommendations',
      description: 'Advanced machine learning algorithms analyze your preferences to find perfect matches',
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      icon: MapPin,
      title: 'Location-Based Search',
      description: 'Find restaurants near you with accurate distance and travel time estimates',
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      icon: Clock,
      title: 'Real-Time Availability',
      description: 'Check current restaurant status, operating hours, and wait times',
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
    {
      icon: Shield,
      title: 'Verified Reviews',
      description: 'Authentic reviews and ratings from real customers to help you decide',
      color: 'text-red-600',
      bgColor: 'bg-red-100',
    },
    {
      icon: TrendingUp,
      title: 'Trending Spots',
      description: 'Discover popular restaurants and trending cuisines in your area',
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100',
    },
    {
      icon: Users,
      title: 'Personalized Experience',
      description: 'Save preferences and get better recommendations over time',
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-100',
    },
  ]

  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Why Choose FoodAI?
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Experience the future of restaurant discovery with our intelligent recommendation system
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="text-center p-8 rounded-2xl bg-gray-50 hover:bg-gray-100 transition-colors duration-200"
            >
              <div className={`w-16 h-16 ${feature.bgColor} rounded-full flex items-center justify-center mx-auto mb-6`}>
                <feature.icon className={`w-8 h-8 ${feature.color}`} />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                {feature.title}
              </h3>
              <p className="text-gray-600">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
