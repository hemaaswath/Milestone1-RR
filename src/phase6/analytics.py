"""
Analytics Engine for Phase 6

Provides comprehensive analytics and insights for the restaurant
recommendation system.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import pandas as pd


@dataclass
class UserBehaviorMetrics:
    """User behavior analytics."""
    user_id: Optional[str]
    session_id: str
    timestamp: str
    search_preferences: Dict
    recommendations_received: int
    click_through_rate: float
    session_duration: float
    pages_viewed: List[str]
    device_type: str
    location: Optional[str]


@dataclass
class RecommendationAnalytics:
    """Recommendation performance analytics."""
    restaurant_name: str
    times_recommended: int
    times_clicked: int
    click_through_rate: float
    avg_position: float
    user_ratings: List[float]
    avg_user_rating: float
    revenue_impact: Optional[float]


@dataclass
class BusinessInsights:
    """Business intelligence insights."""
    most_searched_locations: List[Tuple[str, int]]
    most_searched_cuisines: List[Tuple[str, int]]
    peak_usage_hours: List[Tuple[int, float]]
    user_satisfaction_trends: Dict[str, float]
    recommendation_effectiveness: float
    popular_price_ranges: Dict[str, int]


class AnalyticsEngine:
    """Advanced analytics engine for restaurant recommendations."""
    
    def __init__(self, data_file: str = "analytics_data.json"):
        self.data_file = data_file
        self.logger = logging.getLogger(__name__)
        self.user_sessions = []
        self.recommendation_events = []
        self.feedback_data = []
        
    def track_user_session(self, session_data: UserBehaviorMetrics):
        """Track user session data."""
        self.user_sessions.append(asdict(session_data))
        
        # Keep only last 10,000 sessions
        if len(self.user_sessions) > 10000:
            self.user_sessions = self.user_sessions[-10000:]
        
        self.logger.info(f"Tracked user session: {session_data.session_id}")
    
    def track_recommendation_event(self, restaurant_name: str, user_action: str, 
                               position: int = None, user_rating: float = None):
        """Track recommendation-related events."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "restaurant_name": restaurant_name,
            "action": user_action,  # recommended, clicked, rated, booked
            "position": position,
            "user_rating": user_rating
        }
        
        self.recommendation_events.append(event)
        
        # Keep only last 50,000 events
        if len(self.recommendation_events) > 50000:
            self.recommendation_events = self.recommendation_events[-50000:]
    
    def generate_user_analytics(self, days: int = 30) -> Dict:
        """Generate comprehensive user behavior analytics."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filter recent sessions
        recent_sessions = [
            session for session in self.user_sessions
            if datetime.fromisoformat(session['timestamp']) > cutoff_date
        ]
        
        if not recent_sessions:
            return {"error": "No data available for specified period"}
        
        # Calculate metrics
        total_sessions = len(recent_sessions)
        unique_users = len(set(s['user_id'] for s in recent_sessions if s['user_id']))
        avg_session_duration = sum(s['session_duration'] for s in recent_sessions) / total_sessions
        
        # Search pattern analysis
        location_counts = Counter(s['search_preferences'].get('location', '') for s in recent_sessions)
        cuisine_counts = Counter(s['search_preferences'].get('cuisine', '') for s in recent_sessions)
        budget_counts = Counter(s['search_preferences'].get('budget', '') for s in recent_sessions)
        
        # Engagement metrics
        total_recommendations = sum(s['recommendations_received'] for s in recent_sessions)
        avg_ctr = sum(s['click_through_rate'] for s in recent_sessions) / total_sessions
        
        # Device analytics
        device_stats = Counter(s['device_type'] for s in recent_sessions)
        
        return {
            "period_days": days,
            "total_sessions": total_sessions,
            "unique_users": unique_users,
            "avg_session_duration_minutes": avg_session_duration,
            "total_recommendations_generated": total_recommendations,
            "average_click_through_rate": avg_ctr,
            "top_searched_locations": location_counts.most_common(10),
            "top_searched_cuisines": cuisine_counts.most_common(10),
            "budget_preference_distribution": dict(budget_counts),
            "device_distribution": dict(device_stats),
            "peak_usage_hours": self._calculate_peak_hours(recent_sessions)
        }
    
    def generate_recommendation_analytics(self, days: int = 30) -> Dict:
        """Generate recommendation performance analytics."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filter recent events
        recent_events = [
            event for event in self.recommendation_events
            if datetime.fromisoformat(event['timestamp']) > cutoff_date
        ]
        
        if not recent_events:
            return {"error": "No recommendation data available"}
        
        # Calculate restaurant performance
        restaurant_stats = defaultdict(lambda: {
            'recommended': 0, 'clicked': 0, 'ratings': []
        })
        
        for event in recent_events:
            restaurant = event['restaurant_name']
            restaurant_stats[restaurant]['recommended'] += 1
            
            if event['action'] == 'clicked':
                restaurant_stats[restaurant]['clicked'] += 1
            
            if event['user_rating'] is not None:
                restaurant_stats[restaurant]['ratings'].append(event['user_rating'])
        
        # Generate analytics
        recommendation_analytics = []
        for restaurant, stats in restaurant_stats.items():
            ctr = (stats['clicked'] / stats['recommended']) * 100 if stats['recommended'] > 0 else 0
            avg_rating = sum(stats['ratings']) / len(stats['ratings']) if stats['ratings'] else None
            avg_position = self._calculate_avg_position(restaurant, recent_events)
            
            recommendation_analytics.append(RecommendationAnalytics(
                restaurant_name=restaurant,
                times_recommended=stats['recommended'],
                times_clicked=stats['clicked'],
                click_through_rate=ctr,
                avg_position=avg_position,
                user_ratings=stats['ratings'],
                avg_user_rating=avg_rating
            ))
        
        # Sort by click-through rate
        recommendation_analytics.sort(key=lambda x: x.click_through_rate, reverse=True)
        
        return {
            "period_days": days,
            "total_restaurants_analyzed": len(recommendation_analytics),
            "top_performing_recommendations": [asdict(r) for r in recommendation_analytics[:20]],
            "overall_ctr": sum(r.times_clicked for r in recommendation_analytics) / sum(r.times_recommended for r in recommendation_analytics) * 100,
            "avg_user_rating": sum(r.avg_user_rating for r in recommendation_analytics if r.avg_user_rating) / len([r for r in recommendation_analytics if r.avg_user_rating])
        }
    
    def generate_business_insights(self, days: int = 30) -> BusinessInsights:
        """Generate business intelligence insights."""
        user_analytics = self.generate_user_analytics(days)
        
        if 'error' in user_analytics:
            return BusinessInsights([], [], [], [], {}, 0.0, {})
        
        # Extract insights from user analytics
        most_searched_locations = user_analytics['top_searched_locations']
        most_searched_cuisines = user_analytics['top_searched_cuisines']
        peak_hours = user_analytics['peak_usage_hours']
        
        # Calculate satisfaction trends
        satisfaction_trends = self._calculate_satisfaction_trends(days)
        
        # Calculate recommendation effectiveness
        rec_analytics = self.generate_recommendation_analytics(days)
        effectiveness = rec_analytics.get('overall_ctr', 0) / 100  # Convert to decimal
        
        # Analyze price range preferences
        price_ranges = user_analytics['budget_preference_distribution']
        
        return BusinessInsights(
            most_searched_locations=most_searched_locations,
            most_searched_cuisines=most_searched_cuisines,
            peak_usage_hours=peak_hours,
            user_satisfaction_trends=satisfaction_trends,
            recommendation_effectiveness=effectiveness,
            popular_price_ranges=price_ranges
        )
    
    def _calculate_peak_hours(self, sessions: List[Dict]) -> List[Tuple[int, float]]:
        """Calculate peak usage hours."""
        hour_counts = defaultdict(int)
        
        for session in sessions:
            hour = datetime.fromisoformat(session['timestamp']).hour
            hour_counts[hour] += 1
        
        # Calculate percentage of total sessions for each hour
        total_sessions = len(sessions)
        peak_hours = [
            (hour, count / total_sessions * 100)
            for hour, count in hour_counts.items()
        ]
        
        return sorted(peak_hours, key=lambda x: x[1], reverse=True)
    
    def _calculate_avg_position(self, restaurant: str, events: List[Dict]) -> float:
        """Calculate average position of restaurant in recommendations."""
        positions = [
            event['position'] for event in events
            if event['restaurant_name'] == restaurant and event['position'] is not None
        ]
        
        return sum(positions) / len(positions) if positions else 0
    
    def _calculate_satisfaction_trends(self, days: int) -> Dict[str, float]:
        """Calculate user satisfaction trends over time."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Group ratings by day
        daily_ratings = defaultdict(list)
        
        for event in self.recommendation_events:
            if (event['user_rating'] is not None and 
                datetime.fromisoformat(event['timestamp']) > cutoff_date):
                day = datetime.fromisoformat(event['timestamp']).date().isoformat()
                daily_ratings[day].append(event['user_rating'])
        
        # Calculate daily averages
        daily_averages = {
            day: sum(ratings) / len(ratings)
            for day, ratings in daily_ratings.items()
        }
        
        return daily_averages
    
    def export_analytics_report(self, filename: str = None) -> str:
        """Export comprehensive analytics report."""
        if not filename:
            filename = f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "report_period_days": 30,
            "user_analytics": self.generate_user_analytics(),
            "recommendation_analytics": self.generate_recommendation_analytics(),
            "business_insights": asdict(self.generate_business_insights()),
            "data_summary": {
                "total_user_sessions": len(self.user_sessions),
                "total_recommendation_events": len(self.recommendation_events),
                "data_collection_start": min(s['timestamp'] for s in self.user_sessions) if self.user_sessions else None,
                "last_updated": datetime.now().isoformat()
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Analytics report exported to {filename}")
        return filename
    
    def save_data(self):
        """Persist analytics data to file."""
        data = {
            "last_updated": datetime.now().isoformat(),
            "user_sessions": self.user_sessions[-1000:],  # Save last 1000 sessions
            "recommendation_events": self.recommendation_events[-5000:],  # Save last 5000 events
            "feedback_data": self.feedback_data[-1000:]  # Save last 1000 feedback entries
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.logger.info(f"Analytics data saved to {self.data_file}")
    
    def load_data(self):
        """Load analytics data from file."""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                
            self.user_sessions = data.get('user_sessions', [])
            self.recommendation_events = data.get('recommendation_events', [])
            self.feedback_data = data.get('feedback_data', [])
            
            self.logger.info(f"Analytics data loaded from {self.data_file}")
            
        except FileNotFoundError:
            self.logger.info(f"No existing analytics data found, starting fresh")
        except Exception as e:
            self.logger.error(f"Error loading analytics data: {e}")
