"""
Phase 6 API Integration

Integrates monitoring, analytics, and improvement capabilities
with the main API system.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from flask import Blueprint, request, jsonify

from .monitoring import SystemMonitor, PerformanceTracker
from .analytics import AnalyticsEngine
from .feedback import FeedbackCollector, FeedbackProcessor
from .improvement import ModelOptimizer, DataRefresher

# Create Blueprint for Phase 6 endpoints
phase6_bp = Blueprint('phase6', __name__)

# Initialize components
system_monitor = SystemMonitor()
performance_tracker = PerformanceTracker()
analytics_engine = AnalyticsEngine()
feedback_collector = FeedbackCollector()
feedback_processor = FeedbackProcessor()
model_optimizer = ModelOptimizer()
data_refresher = DataRefresher()

logger = logging.getLogger(__name__)


@phase6_bp.route('/monitoring/health', methods=['GET'])
def get_system_health():
    """Get comprehensive system health status."""
    try:
        health_status = system_monitor.get_health_status()
        return jsonify({
            "status": "success",
            "data": health_status
        })
    except Exception as e:
        logger.error(f"Error getting system health: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to get system health"
        }), 500


@phase6_bp.route('/monitoring/metrics', methods=['GET'])
def get_system_metrics():
    """Get current system performance metrics."""
    try:
        metrics = system_monitor.collect_system_metrics()
        return jsonify({
            "status": "success",
            "data": metrics
        })
    except Exception as e:
        logger.error(f"Error getting system metrics: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to get system metrics"
        }), 500


@phase6_bp.route('/monitoring/performance', methods=['GET'])
def get_performance_stats():
    """Get performance statistics for endpoints."""
    try:
        endpoint = request.args.get('endpoint')
        minutes = int(request.args.get('minutes', 60))
        
        if endpoint:
            stats = system_monitor.get_endpoint_stats(endpoint, minutes)
        else:
            # Get stats for all endpoints
            stats = {
                ep: system_monitor.get_endpoint_stats(ep, minutes)
                for ep in ['/api/v1/recommendations', '/api/v1/locations', '/api/v1/cuisines']
            }
        
        return jsonify({
            "status": "success",
            "data": {
                "endpoint": endpoint,
                "time_range_minutes": minutes,
                "statistics": stats
            }
        })
    except Exception as e:
        logger.error(f"Error getting performance stats: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to get performance stats"
        }), 500


@phase6_bp.route('/analytics/user-behavior', methods=['GET'])
def get_user_analytics():
    """Get user behavior analytics."""
    try:
        days = int(request.args.get('days', 30))
        analytics = analytics_engine.generate_user_analytics(days)
        
        return jsonify({
            "status": "success",
            "data": analytics
        })
    except Exception as e:
        logger.error(f"Error getting user analytics: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to get user analytics"
        }), 500


@phase6_bp.route('/analytics/recommendations', methods=['GET'])
def get_recommendation_analytics():
    """Get recommendation performance analytics."""
    try:
        days = int(request.args.get('days', 30))
        analytics = analytics_engine.generate_recommendation_analytics(days)
        
        return jsonify({
            "status": "success",
            "data": analytics
        })
    except Exception as e:
        logger.error(f"Error getting recommendation analytics: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to get recommendation analytics"
        }), 500


@phase6_bp.route('/analytics/business-insights', methods=['GET'])
def get_business_insights():
    """Get business intelligence insights."""
    try:
        days = int(request.args.get('days', 30))
        insights = analytics_engine.generate_business_insights(days)
        
        return jsonify({
            "status": "success",
            "data": insights
        })
    except Exception as e:
        logger.error(f"Error getting business insights: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to get business insights"
        }), 500


@phase6_bp.route('/feedback/collect', methods=['POST'])
def collect_feedback():
    """Collect user feedback."""
    try:
        feedback_data = request.get_json()
        
        if not feedback_data:
            return jsonify({
                "status": "error",
                "message": "No feedback data provided"
            }), 400
        
        success = feedback_collector.collect_feedback(feedback_data)
        
        if success:
            return jsonify({
                "status": "success",
                "message": "Feedback collected successfully"
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to collect feedback"
            }), 400
            
    except Exception as e:
        logger.error(f"Error collecting feedback: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to collect feedback"
        }), 500


@phase6_bp.route('/feedback/analyze', methods=['GET'])
def analyze_feedback():
    """Analyze collected feedback."""
    try:
        days = int(request.args.get('days', 30))
        
        # Get recent feedback
        recent_feedback = feedback_collector.get_feedback_by_timeframe(days)
        
        if not recent_feedback:
            return jsonify({
                "status": "success",
                "data": {
                    "message": "No feedback data available for specified period"
                }
            })
        
        analysis = feedback_processor.analyze_feedback(recent_feedback)
        
        return jsonify({
            "status": "success",
            "data": analysis
        })
    except Exception as e:
        logger.error(f"Error analyzing feedback: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to analyze feedback"
        }), 500


@phase6_bp.route('/improvement/evaluate-model', methods=['POST'])
def evaluate_model():
    """Evaluate model performance with test cases."""
    try:
        data = request.get_json()
        
        if not data or 'model_name' not in data or 'test_cases' not in data:
            return jsonify({
                "status": "error",
                "message": "Model name and test cases required"
            }), 400
        
        model_name = data['model_name']
        test_cases = data['test_cases']
        
        performance = model_optimizer.evaluate_model_performance(model_name, test_cases)
        
        return jsonify({
            "status": "success",
            "data": performance
        })
        
    except Exception as e:
        logger.error(f"Error evaluating model: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to evaluate model"
        }), 500


@phase6_bp.route('/improvement/optimize-prompt', methods=['POST'])
def optimize_prompt():
    """Optimize prompt template for better performance."""
    try:
        data = request.get_json()
        
        if not data or 'current_prompt' not in data or 'performance_data' not in data:
            return jsonify({
                "status": "error",
                "message": "Current prompt and performance data required"
            }), 400
        
        current_prompt = data['current_prompt']
        performance_data = data['performance_data']
        
        # Convert performance data to ModelPerformance object
        from phase6.improvement import ModelPerformance
        perf = ModelPerformance(**performance_data)
        
        optimized_prompt = model_optimizer.optimize_prompt_template(current_prompt, perf)
        
        return jsonify({
            "status": "success",
            "data": {
                "original_prompt": current_prompt,
                "optimized_prompt": optimized_prompt,
                "optimizations_applied": "See optimization log"
            }
        })
        
    except Exception as e:
        logger.error(f"Error optimizing prompt: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to optimize prompt"
        }), 500


@phase6_bp.route('/improvement/run-ab-test', methods=['POST'])
def run_ab_test():
    """Run A/B test between two models."""
    try:
        data = request.get_json()
        
        if not data or 'model_a' not in data or 'model_b' not in data or 'test_cases' not in data:
            return jsonify({
                "status": "error",
                "message": "Model A, Model B, and test cases required"
            }), 400
        
        model_a = data['model_a']
        model_b = data['model_b']
        test_cases = data['test_cases']
        
        result = model_optimizer.run_a_b_test(model_a, model_b, test_cases)
        
        return jsonify({
            "status": "success",
            "data": result
        })
        
    except Exception as e:
        logger.error(f"Error running A/B test: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to run A/B test"
        }), 500


@phase6_bp.route('/improvement/check-data', methods=['GET'])
def check_data_freshness():
    """Check if data needs refresh."""
    try:
        freshness_status = data_refresher.check_data_freshness()
        
        return jsonify({
            "status": "success",
            "data": freshness_status
        })
        
    except Exception as e:
        logger.error(f"Error checking data freshness: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to check data freshness"
        }), 500


@phase6_bp.route('/improvement/refresh-data', methods=['POST'])
def refresh_data():
    """Trigger data refresh process."""
    try:
        data = request.get_json() or {}
        source_url = data.get('source_url')
        
        result = data_refresher.refresh_data(source_url)
        
        return jsonify({
            "status": "success",
            "data": result
        })
        
    except Exception as e:
        logger.error(f"Error refreshing data: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to refresh data"
        }), 500


@phase6_bp.route('/reports/export', methods=['GET'])
def export_reports():
    """Export comprehensive monitoring and analytics reports."""
    try:
        report_type = request.args.get('type', 'all')
        
        if report_type == 'all':
            # Export all reports
            metrics_file = system_monitor.export_metrics()
            analytics_file = analytics_engine.export_analytics_report()
            
            return jsonify({
                "status": "success",
                "data": {
                    "message": "Reports exported successfully",
                    "files": {
                        "system_metrics": metrics_file,
                        "analytics_report": analytics_file
                    }
                }
            })
        
        elif report_type == 'metrics':
            metrics_file = system_monitor.export_metrics()
            return jsonify({
                "status": "success",
                "data": {
                    "message": "System metrics exported",
                    "file": metrics_file
                }
            })
        
        elif report_type == 'analytics':
            analytics_file = analytics_engine.export_analytics_report()
            return jsonify({
                "status": "success",
                "data": {
                    "message": "Analytics report exported",
                    "file": analytics_file
                }
            })
        
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid report type. Use 'all', 'metrics', or 'analytics'"
            }), 400
            
    except Exception as e:
        logger.error(f"Error exporting reports: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to export reports"
        }), 500


# Middleware to integrate monitoring with main API
def setup_monitoring_middleware(app):
    """Setup monitoring middleware for main Flask app."""
    
    @app.before_request
    def track_request():
        request.start_time = datetime.now()
        
        # Record request for monitoring
        endpoint = request.endpoint or request.path
        
        # Create performance metrics object
        from phase6.monitoring import PerformanceMetrics
        metrics = PerformanceMetrics(
            endpoint=endpoint,
            response_time=0.0,  # Will be updated after request
            status_code=200,  # Will be updated after request
            user_preferences={},  # Will be populated if available
            recommendation_count=0,  # Will be populated if applicable
            llm_response_time=0.0,  # Will be populated if applicable
            database_query_time=0.0  # Will be populated if applicable
        )
        
        # Store metrics for later processing
        request.performance_metrics = metrics
    
    @app.after_request
    def log_response(response):
        if hasattr(request, 'start_time') and hasattr(request, 'performance_metrics'):
            # Update metrics with response data
            request.performance_metrics.response_time = (datetime.now() - request.start_time).total_seconds()
            request.performance_metrics.status_code = response.status_code
            
            # Record in system monitor
            system_monitor.record_request(request.performance_metrics)
        
        return response


# Utility function to integrate Phase 6 with main API
def integrate_phase6_with_main_api(app):
    """Integrate Phase 6 monitoring with main API."""
    
    # Register Phase 6 blueprint
    app.register_blueprint(phase6_bp, url_prefix='/api/v1/monitoring')
    
    # Setup monitoring middleware
    setup_monitoring_middleware(app)
    
    logger.info("Phase 6 monitoring integrated with main API")
