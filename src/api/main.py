"""
Main Flask Application for Restaurant Recommendation API
"""

from flask import Flask
from flask_cors import CORS

from .config import config
from .routes import api_bp
from .middleware import setup_middleware
from phase6.api_integration import integrate_phase6_with_main_api


def create_app():
    """Create and configure Flask application."""
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configure app
    app.config.update({
        'SECRET_KEY': config.groq_api_key[:32],  # Use part of API key as secret
        'JSON_SORT_KEYS': False,
        'JSONIFY_PRETTYPRINT_REGULAR': True,
    })
    
    # Setup CORS
    CORS(app, origins=config.allowed_origins)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Setup middleware
    setup_middleware(app)
    
    # Integrate Phase 6 monitoring
    integrate_phase6_with_main_api(app)
    
    # Add root endpoint
    @app.route('/')
    def index():
        return {
            "message": "Restaurant Recommendation API",
            "version": "1.0.0",
            "endpoints": {
                "recommendations": "/api/v1/recommendations",
                "web_interface": "/api/v1/recommendations/web",
                "locations": "/api/v1/locations",
                "cuisines": "/api/v1/cuisines",
                "stats": "/api/v1/stats",
                "health": "/api/v1/health",
                "monitoring": {
                    "system_health": "/api/v1/monitoring/health",
                    "system_metrics": "/api/v1/monitoring/metrics",
                    "performance_stats": "/api/v1/monitoring/performance",
                    "user_analytics": "/api/v1/analytics/user-behavior",
                    "recommendation_analytics": "/api/v1/analytics/recommendations",
                    "business_insights": "/api/v1/analytics/business-insights"
                },
                "feedback": {
                    "collect": "/api/v1/feedback/collect",
                    "analyze": "/api/v1/feedback/analyze"
                },
                "improvement": {
                    "evaluate_model": "/api/v1/improvement/evaluate-model",
                    "optimize_prompt": "/api/v1/improvement/optimize-prompt",
                    "run_ab_test": "/api/v1/improvement/run-ab-test",
                    "check_data": "/api/v1/improvement/check-data",
                    "refresh_data": "/api/v1/improvement/refresh-data"
                },
                "reports": "/api/v1/reports/export"
            },
            "documentation": "/api/v1/docs"
        }
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=config.host,
        port=config.port,
        debug=config.debug
    )
