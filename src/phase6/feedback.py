"""
Feedback Collection and Processing for Phase 6

Handles user feedback collection, analysis, and integration
with the continuous improvement pipeline.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import re


@dataclass
class UserFeedback:
    """User feedback data structure."""
    session_id: str
    restaurant_name: str
    recommendation_position: int
    user_rating: Optional[float]
    clicked: bool
    explanation_helpful: Optional[bool]
    relevance_score: Optional[float]  # 1-5 scale
    comments: Optional[str]
    timestamp: str
    user_id: Optional[str] = None


@dataclass
class FeedbackAnalysis:
    """Analysis results from feedback processing."""
    overall_satisfaction: float
    common_issues: List[str]
    improvement_suggestions: List[str]
    rating_distribution: Dict[str, int]
    feedback_volume_trends: Dict[str, int]


class FeedbackCollector:
    """Collects and manages user feedback."""
    
    def __init__(self, storage_file: str = "user_feedback.json"):
        self.storage_file = storage_file
        self.logger = logging.getLogger(__name__)
        self.feedback_data = []
        self.load_feedback_data()
    
    def load_feedback_data(self):
        """Load existing feedback data."""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                self.feedback_data = data.get('feedback', [])
            self.logger.info(f"Loaded {len(self.feedback_data)} feedback entries")
        except FileNotFoundError:
            self.logger.info("No existing feedback data found, starting fresh")
        except Exception as e:
            self.logger.error(f"Error loading feedback data: {e}")
    
    def collect_feedback(self, feedback_data: Dict) -> bool:
        """Collect new user feedback."""
        try:
            # Validate required fields
            required_fields = ['session_id', 'restaurant_name', 'recommendation_position']
            for field in required_fields:
                if field not in feedback_data:
                    self.logger.error(f"Missing required field: {field}")
                    return False
            
            # Validate data types
            if not isinstance(feedback_data.get('recommendation_position'), int):
                feedback_data['recommendation_position'] = int(feedback_data['recommendation_position'])
            
            if 'user_rating' in feedback_data and feedback_data['user_rating'] is not None:
                try:
                    feedback_data['user_rating'] = float(feedback_data['user_rating'])
                    if not (1 <= feedback_data['user_rating'] <= 5):
                        raise ValueError("Rating must be between 1 and 5")
                except (ValueError, TypeError):
                    self.logger.error("Invalid user rating format")
                    return False
            
            # Create feedback object
            feedback = UserFeedback(
                session_id=feedback_data['session_id'],
                restaurant_name=feedback_data['restaurant_name'],
                recommendation_position=feedback_data['recommendation_position'],
                user_rating=feedback_data.get('user_rating'),
                clicked=feedback_data.get('clicked', False),
                explanation_helpful=feedback_data.get('explanation_helpful'),
                relevance_score=feedback_data.get('relevance_score'),
                comments=feedback_data.get('comments', ''),
                timestamp=datetime.now().isoformat(),
                user_id=feedback_data.get('user_id')
            )
            
            # Store feedback
            self.feedback_data.append(asdict(feedback))
            
            # Keep only last 10,000 entries
            if len(self.feedback_data) > 10000:
                self.feedback_data = self.feedback_data[-10000:]
            
            self.save_feedback_data()
            self.logger.info(f"Collected feedback for {feedback.restaurant_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error collecting feedback: {e}")
            return False
    
    def collect_batch_feedback(self, feedback_list: List[Dict]) -> Dict[str, bool]:
        """Collect multiple feedback entries."""
        results = {}
        
        for i, feedback_data in enumerate(feedback_list):
            session_id = feedback_data.get('session_id', f'batch_{i}')
            results[session_id] = self.collect_feedback(feedback_data)
        
        return results
    
    def get_feedback_by_restaurant(self, restaurant_name: str, days: int = 30) -> List[UserFeedback]:
        """Get all feedback for a specific restaurant."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        feedback_for_restaurant = [
            UserFeedback(**fb) for fb in self.feedback_data
            if (fb['restaurant_name'] == restaurant_name and 
                datetime.fromisoformat(fb['timestamp']) > cutoff_date)
        ]
        
        return feedback_for_restaurant
    
    def get_feedback_by_timeframe(self, days: int = 7) -> List[UserFeedback]:
        """Get feedback within specified timeframe."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_feedback = [
            UserFeedback(**fb) for fb in self.feedback_data
            if datetime.fromisoformat(fb['timestamp']) > cutoff_date
        ]
        
        return recent_feedback
    
    def save_feedback_data(self):
        """Persist feedback data to file."""
        try:
            data = {
                'last_updated': datetime.now().isoformat(),
                'total_entries': len(self.feedback_data),
                'feedback': self.feedback_data
            }
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving feedback data: {e}")


class FeedbackProcessor:
    """Processes and analyzes user feedback."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_feedback(self, feedback_list: List[UserFeedback]) -> FeedbackAnalysis:
        """Analyze feedback data and generate insights."""
        if not feedback_list:
            return FeedbackAnalysis(0.0, [], [], {}, {})
        
        # Calculate overall satisfaction
        ratings = [fb.user_rating for fb in feedback_list if fb.user_rating is not None]
        overall_satisfaction = sum(ratings) / len(ratings) if ratings else 0.0
        
        # Analyze common issues from comments
        comments = [fb.comments for fb in feedback_list if fb.comments and fb.comments.strip()]
        common_issues = self._extract_common_issues(comments)
        
        # Generate improvement suggestions
        improvement_suggestions = self._generate_improvement_suggestions(feedback_list)
        
        # Analyze rating distribution
        rating_distribution = self._calculate_rating_distribution(ratings)
        
        # Analyze feedback volume trends
        feedback_volume_trends = self._calculate_feedback_trends(feedback_list)
        
        return FeedbackAnalysis(
            overall_satisfaction=overall_satisfaction,
            common_issues=common_issues,
            improvement_suggestions=improvement_suggestions,
            rating_distribution=rating_distribution,
            feedback_volume_trends=feedback_volume_trends
        )
    
    def _extract_common_issues(self, comments: List[str]) -> List[str]:
        """Extract common issues from user comments."""
        if not comments:
            return []
        
        # Common issue keywords
        issue_keywords = {
            'expensive': ['expensive', 'costly', 'price', 'overpriced'],
            'location': ['far', 'location', 'distance', 'area'],
            'service': ['service', 'staff', 'waiter', 'slow'],
            'food_quality': ['food', 'taste', 'quality', 'portion'],
            'ambience': ['ambience', 'atmosphere', 'clean', 'noisy']
        }
        
        issue_counts = defaultdict(int)
        
        for comment in comments:
            comment_lower = comment.lower()
            for issue, keywords in issue_keywords.items():
                if any(keyword in comment_lower for keyword in keywords):
                    issue_counts[issue] += 1
        
        # Return top issues
        common_issues = [
            f"{issue.replace('_', ' ').title()}: {count} mentions"
            for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
        
        return common_issues
    
    def _generate_improvement_suggestions(self, feedback_list: List[UserFeedback]) -> List[str]:
        """Generate actionable improvement suggestions."""
        suggestions = []
        
        # Calculate metrics
        avg_rating = sum(fb.user_rating for fb in feedback_list if fb.user_rating) / len([fb for fb in feedback_list if fb.user_rating])
        ctr = sum(fb.clicked for fb in feedback_list) / len(feedback_list) * 100
        explanation_helpfulness = sum(fb.explanation_helpful for fb in feedback_list if fb.explanation_helpful is not None) / len([fb for fb in feedback_list if fb.explanation_helpful is not None]) * 100
        
        # Generate suggestions based on metrics
        if avg_rating < 3.5:
            suggestions.append("Improve restaurant quality scoring algorithm")
        
        if ctr < 20:
            suggestions.append("Enhance recommendation relevance and positioning")
        
        if explanation_helpfulness < 60:
            suggestions.append("Improve AI explanation quality and clarity")
        
        # Check for position bias
        positions = [fb.recommendation_position for fb in feedback_list]
        if positions:
            avg_position = sum(positions) / len(positions)
            if avg_position > 3:
                suggestions.append("Optimize ranking algorithm to surface better matches earlier")
        
        # Check for restaurant diversity
        restaurants = set(fb.restaurant_name for fb in feedback_list)
        if len(restaurants) < len(feedback_list) * 0.3:  # Less than 30% diversity
            suggestions.append("Increase restaurant diversity in recommendations")
        
        return suggestions
    
    def _calculate_rating_distribution(self, ratings: List[float]) -> Dict[str, int]:
        """Calculate distribution of user ratings."""
        if not ratings:
            return {}
        
        distribution = defaultdict(int)
        for rating in ratings:
            if rating >= 4.5:
                distribution['5 stars'] += 1
            elif rating >= 3.5:
                distribution['4 stars'] += 1
            elif rating >= 2.5:
                distribution['3 stars'] += 1
            elif rating >= 1.5:
                distribution['2 stars'] += 1
            else:
                distribution['1 star'] += 1
        
        return dict(distribution)
    
    def _calculate_feedback_trends(self, feedback_list: List[UserFeedback]) -> Dict[str, int]:
        """Calculate feedback volume trends over time."""
        if not feedback_list:
            return {}
        
        # Group feedback by day
        daily_counts = defaultdict(int)
        
        for fb in feedback_list:
            day = datetime.fromisoformat(fb['timestamp']).date().isoformat()
            daily_counts[day] += 1
        
        # Get last 7 days
        recent_days = sorted(daily_counts.keys())[-7:]
        
        return {day: daily_counts[day] for day in recent_days}
    
    def generate_feedback_report(self, feedback_list: List[UserFeedback], 
                             filename: str = None) -> str:
        """Generate comprehensive feedback analysis report."""
        if not filename:
            filename = f"feedback_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        analysis = self.analyze_feedback(feedback_list)
        
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "analysis_period_days": 30,
            "total_feedback_entries": len(feedback_list),
            "analysis": asdict(analysis),
            "detailed_feedback": [asdict(fb) for fb in feedback_list[:100]]  # Last 100 entries
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Feedback analysis report saved to {filename}")
        return filename
