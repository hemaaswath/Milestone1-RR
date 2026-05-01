"""
System Monitoring for Phase 6

Provides real-time monitoring, performance tracking, and health checks
for the restaurant recommendation system.
"""

import time
import psutil
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import json


@dataclass
class SystemMetrics:
    """System performance metrics."""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_used_gb: float
    disk_usage_percent: float
    active_connections: int
    response_time_avg: float
    error_rate: float
    requests_per_minute: float


@dataclass
class PerformanceMetrics:
    """Application performance metrics."""
    endpoint: str
    response_time: float
    status_code: int
    user_preferences: Dict
    recommendation_count: int
    llm_response_time: float
    database_query_time: float


class SystemMonitor:
    """Real-time system monitoring."""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics_history = deque(maxlen=max_history)
        self.request_times = deque(maxlen=100)
        self.error_count = 0
        self.total_requests = 0
        self.endpoint_stats = defaultdict(list)
        self.logger = logging.getLogger(__name__)
        
    def collect_system_metrics(self) -> SystemMetrics:
        """Collect current system performance metrics."""
        return SystemMetrics(
            timestamp=datetime.now().isoformat(),
            cpu_percent=psutil.cpu_percent(interval=1),
            memory_percent=psutil.virtual_memory().percent,
            memory_used_gb=psutil.virtual_memory().used / (1024**3),
            disk_usage_percent=psutil.disk_usage('/').percent,
            active_connections=len(psutil.net_connections()),
            response_time_avg=sum(self.request_times) / len(self.request_times) if self.request_times else 0,
            error_rate=(self.error_count / self.total_requests * 100) if self.total_requests > 0 else 0,
            requests_per_minute=self._calculate_rpm()
        )
    
    def _calculate_rpm(self) -> float:
        """Calculate requests per minute."""
        if not self.request_times:
            return 0
        
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        recent_requests = [t for t in self.request_times if t > one_minute_ago.timestamp()]
        return len(recent_requests)
    
    def record_request(self, metrics: PerformanceMetrics):
        """Record performance metrics for a request."""
        self.total_requests += 1
        self.request_times.append(datetime.now())
        
        if metrics.status_code >= 400:
            self.error_count += 1
        
        self.endpoint_stats[metrics.endpoint].append(metrics)
        
        # Keep only recent metrics (last 100 per endpoint)
        if len(self.endpoint_stats[metrics.endpoint]) > 100:
            self.endpoint_stats[metrics.endpoint] = self.endpoint_stats[metrics.endpoint][-100:]
    
    def get_health_status(self) -> Dict:
        """Get overall system health status."""
        current_metrics = self.collect_system_metrics()
        
        # Determine health status
        status = "healthy"
        issues = []
        
        if current_metrics.cpu_percent > 80:
            status = "degraded"
            issues.append("High CPU usage")
        
        if current_metrics.memory_percent > 85:
            status = "degraded"
            issues.append("High memory usage")
        
        if current_metrics.error_rate > 5:
            status = "unhealthy"
            issues.append("High error rate")
        
        if current_metrics.response_time_avg > 2.0:
            status = "degraded"
            issues.append("Slow response times")
        
        return {
            "status": status,
            "timestamp": current_metrics.timestamp,
            "issues": issues,
            "metrics": asdict(current_metrics)
        }
    
    def get_endpoint_stats(self, endpoint: str, minutes: int = 60) -> Dict:
        """Get performance statistics for specific endpoint."""
        if endpoint not in self.endpoint_stats:
            return {}
        
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_metrics = [
            m for m in self.endpoint_stats[endpoint]
            if datetime.fromisoformat(m.timestamp) > cutoff_time
        ]
        
        if not recent_metrics:
            return {}
        
        response_times = [m.response_time for m in recent_metrics]
        llm_times = [m.llm_response_time for m in recent_metrics if m.llm_response_time]
        db_times = [m.database_query_time for m in recent_metrics if m.database_query_time]
        
        return {
            "endpoint": endpoint,
            "time_range_minutes": minutes,
            "total_requests": len(recent_metrics),
            "avg_response_time": sum(response_times) / len(response_times),
            "min_response_time": min(response_times),
            "max_response_time": max(response_times),
            "error_count": sum(1 for m in recent_metrics if m.status_code >= 400),
            "avg_llm_time": sum(llm_times) / len(llm_times) if llm_times else None,
            "avg_db_time": sum(db_times) / len(db_times) if db_times else None,
            "most_common_preferences": self._get_common_preferences(recent_metrics)
        }
    
    def _get_common_preferences(self, metrics: List[PerformanceMetrics]) -> Dict:
        """Analyze most common user preferences."""
        if not metrics:
            return {}
        
        locations = defaultdict(int)
        cuisines = defaultdict(int)
        budgets = defaultdict(int)
        
        for m in metrics:
            prefs = m.user_preferences
            if prefs.get('location'):
                locations[prefs['location']] += 1
            if prefs.get('cuisine'):
                cuisines[prefs['cuisine']] += 1
            if prefs.get('budget'):
                budgets[prefs['budget']] += 1
        
        return {
            "top_locations": dict(sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5]),
            "top_cuisines": dict(sorted(cuisines.items(), key=lambda x: x[1], reverse=True)[:5]),
            "budget_distribution": dict(budgets)
        }
    
    def export_metrics(self, filename: str = None) -> str:
        """Export metrics history to JSON."""
        if not filename:
            filename = f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "system_metrics": [asdict(self.collect_system_metrics())],
            "endpoint_stats": {
                endpoint: self.get_endpoint_stats(endpoint) 
                for endpoint in self.endpoint_stats.keys()
            },
            "history_size": len(self.metrics_history)
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.logger.info(f"Metrics exported to {filename}")
        return filename


class PerformanceTracker:
    """Track application performance over time."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.performance_log = []
        
    def track_recommendation_quality(self, user_feedback: Dict):
        """Track recommendation quality based on user feedback."""
        quality_score = self._calculate_quality_score(user_feedback)
        
        performance_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "recommendation_quality",
            "score": quality_score,
            "feedback": user_feedback
        }
        
        self.performance_log.append(performance_entry)
        self.logger.info(f"Recommendation quality score: {quality_score}")
        
        return quality_score
    
    def _calculate_quality_score(self, feedback: Dict) -> float:
        """Calculate quality score from user feedback."""
        score = 0.0
        
        # Click-through rate (40% weight)
        if feedback.get('clicked_restaurant'):
            score += 0.4
        
        # Rating satisfaction (30% weight)
        if feedback.get('user_rating'):
            user_rating = feedback['user_rating']
            score += (user_rating / 5.0) * 0.3
        
        # Relevance feedback (20% weight)
        if feedback.get('relevance_score'):
            score += feedback['relevance_score'] * 0.2
        
        # Explanation helpfulness (10% weight)
        if feedback.get('explanation_helpful'):
            score += 0.1
        
        return min(score, 1.0)
    
    def get_performance_trends(self, days: int = 7) -> Dict:
        """Analyze performance trends over time."""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_entries = [
            entry for entry in self.performance_log
            if datetime.fromisoformat(entry['timestamp']) > cutoff_date
        ]
        
        if not recent_entries:
            return {}
        
        quality_scores = [
            entry['score'] for entry in recent_entries
            if entry['type'] == 'recommendation_quality'
        ]
        
        return {
            "period_days": days,
            "total_entries": len(recent_entries),
            "avg_quality_score": sum(quality_scores) / len(quality_scores) if quality_scores else 0,
            "quality_trend": self._calculate_trend(quality_scores),
            "improvement_areas": self._identify_improvement_areas(recent_entries)
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from values."""
        if len(values) < 2:
            return "insufficient_data"
        
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg + 0.05:
            return "improving"
        elif second_avg < first_avg - 0.05:
            return "declining"
        else:
            return "stable"
    
    def _identify_improvement_areas(self, entries: List[Dict]) -> List[str]:
        """Identify areas needing improvement."""
        issues = []
        
        quality_entries = [
            entry for entry in entries
            if entry['type'] == 'recommendation_quality'
        ]
        
        if quality_entries:
            avg_score = sum(entry['score'] for entry in quality_entries) / len(quality_entries)
            
            if avg_score < 0.7:
                issues.append("Overall recommendation quality")
            
            # Check specific feedback patterns
            low_explanation_scores = [
                entry for entry in quality_entries
                if entry['feedback'].get('explanation_helpful') is False
            ]
            
            if len(low_explanation_scores) > len(quality_entries) * 0.3:
                issues.append("AI explanation quality")
        
        return issues
