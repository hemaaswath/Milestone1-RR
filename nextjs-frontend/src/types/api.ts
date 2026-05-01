export interface SearchPreferences {
  location: string
  budget: 'low' | 'medium' | 'high'
  cuisine?: string
  min_rating?: number
  additional_preferences?: string[]
}

export interface Restaurant {
  restaurant_name: string
  location: string
  cuisines: string
  cost_for_two?: number | null
  rating?: number | null
  relevance_score?: number
}

export interface Recommendation {
  restaurant_name: string
  rank: number
  score: number
  explanation: string
  location: string
  cuisines: string
  rating?: number | null
  cost_for_two?: number | null
  metadata?: {
    confidence_score: number
    match_reasons: string[]
    additional_info: Record<string, any>
    timestamp: string
  }
}

export interface RecommendationResponse {
  status: 'success' | 'error'
  data?: {
    recommendations: Recommendation[]
    summary?: RecommendationSummary
    generated_at: string
  }
  message?: string
  errors?: string[]
}

export interface RecommendationSummary {
  total_candidates: number
  filtered_candidates: number
  final_recommendations: number
  avg_rating?: number
  price_range?: string
  cuisine_variety?: string[]
}

export interface ApiResponse<T = any> {
  status: 'success' | 'error'
  data?: T
  message?: string
  errors?: string[]
}

export interface Location {
  name: string
  count: number
}

export interface Cuisine {
  name: string
  count: number
}

export interface SystemHealth {
  status: 'healthy' | 'degraded' | 'unhealthy'
  timestamp: string
  issues: string[]
  metrics: SystemMetrics
}

export interface SystemMetrics {
  timestamp: string
  cpu_percent: number
  memory_percent: number
  memory_used_gb: number
  disk_usage_percent: number
  active_connections: number
  response_time_avg: number
  error_rate: number
  requests_per_minute: number
}

export interface UserAnalytics {
  period_days: number
  total_sessions: number
  unique_users: number
  avg_session_duration_minutes: number
  total_recommendations_generated: number
  average_click_through_rate: number
  top_searched_locations: [string, number][]
  top_searched_cuisines: [string, number][]
  budget_preference_distribution: Record<string, number>
  device_distribution: Record<string, number>
  peak_usage_hours: [number, number][]
}

export interface FeedbackData {
  session_id: string
  restaurant_name: string
  recommendation_position: number
  user_rating?: number
  clicked: boolean
  explanation_helpful?: boolean
  relevance_score?: number
  comments?: string
  timestamp: string
  user_id?: string
}

export interface FeedbackAnalysis {
  overall_satisfaction: number
  common_issues: string[]
  improvement_suggestions: string[]
  rating_distribution: Record<string, number>
  feedback_volume_trends: Record<string, number>
}
