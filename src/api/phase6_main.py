"""
Phase 6: Backend HTTP API - Enhanced Implementation

This is the enhanced Phase 6 Backend HTTP API that provides a secure, scalable
HTTP service orchestrating the recommendation pipeline while keeping server-side
secrets secure and providing comprehensive telemetry.
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from flask import Flask
from flask_cors import CORS

from api.config import config
from api.enhanced_middleware import setup_enhanced_middleware, telemetry
from api.enhanced_routes import enhanced_api_bp


def create_phase6_app():
    """Create and configure Phase 6 Backend HTTP API application."""
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configure app with Phase 6 security requirements
    app.config.update({
        'SECRET_KEY': config.groq_api_key[:32],  # Use part of API key as secret
        'JSON_SORT_KEYS': False,
        'JSONIFY_PRETTYPRINT_REGULAR': True,
        'MAX_CONTENT_LENGTH': 1 * 1024 * 1024,  # 1MB max request size
    })
    
    # Setup CORS with restricted origins for Phase 6
    if config.allowed_origins == ["*"]:
        # In production, restrict to specific origins
        allowed_origins = [
            "http://localhost:3000",  # Next.js frontend
            "http://127.0.0.1:3000",
            "http://localhost:8000",  # API itself
            "http://127.0.0.1:8000"
        ]
    else:
        allowed_origins = config.allowed_origins
    
    CORS(app, origins=allowed_origins, methods=['GET', 'POST', 'OPTIONS'])
    
    # Register blueprints
    app.register_blueprint(enhanced_api_bp, url_prefix='/api/v1')
    
    # Setup enhanced Phase 6 middleware
    setup_enhanced_middleware(app)
    
    # Add Phase 6 specific endpoints
    @app.route('/')
    def index():
        """Phase 6 API root endpoint with enhanced information."""
        return {
            "message": "Phase 6 Backend HTTP API - Restaurant Recommendation System",
            "version": "1.0.0",
            "phase": "6",
            "description": "Secure HTTP service orchestrating recommendation pipeline",
            "security": {
                "secrets_management": "Server-side only (GROQ_API_KEY)",
                "cors_restricted": True,
                "rate_limiting": "Enabled",
                "input_validation": "Enabled",
                "request_size_limit": "1MB"
            },
            "endpoints": {
                "recommendations": {
                    "path": "/api/v1/recommendations",
                    "method": "POST",
                    "description": "Main recommendation endpoint",
                    "authentication": "None (Phase 6 scope)",
                    "rate_limit": f"{config.rate_limit_per_minute}/minute"
                },
                "web_interface": {
                    "path": "/api/v1/recommendations/web",
                    "method": "POST",
                    "description": "Web-based recommendation interface"
                },
                "health": {
                    "path": "/api/v1/health",
                    "method": "GET",
                    "description": "Service health check"
                },
                "meta": {
                    "path": "/api/v1/meta",
                    "method": "GET",
                    "description": "API metadata and configuration hints"
                },
                "data": {
                    "locations": "/api/v1/locations",
                    "cuisines": "/api/v1/cuisines",
                    "stats": "/api/v1/stats"
                },
                "monitoring": {
                    "system_health": "/api/v1/monitoring/health",
                    "system_metrics": "/api/v1/monitoring/metrics",
                    "performance_stats": "/api/v1/monitoring/performance",
                    "telemetry": "/api/v1/monitoring/telemetry"
                }
            },
            "documentation": "/api/v1/docs",
            "telemetry": {
                "request_logging": "Structured JSON format",
                "performance_tracking": "Enabled",
                "error_monitoring": "Enabled",
                "token_usage_tracking": "Enabled"
            }
        }
    
    # Add Phase 6 telemetry endpoint
    @app.route('/api/v1/monitoring/telemetry', methods=['GET'])
    def get_telemetry():
        """Get current telemetry metrics."""
        return {
            "status": "success",
            "data": telemetry.get_metrics()
        }
    
    return app


def run_phase6_server():
    """Run the Phase 6 Backend HTTP API server."""
    
    print("🚀 Starting Phase 6 Backend HTTP API")
    print("=" * 50)
    print(f"📍 Server: http://{config.host}:{config.port}")
    print(f"🔧 Debug Mode: {config.debug}")
    print(f"📊 Rate Limit: {config.rate_limit_per_minute}/minute")
    print(f"🔐 CORS Origins: {config.allowed_origins}")
    print(f"📝 Data Path: {config.data_path}")
    print(f"🤖 Model: {config.default_model}")
    print("=" * 50)
    
    # Validate Phase 6 requirements
    try:
        if not config.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is required for Phase 6")
        
        if not os.path.exists(config.data_path):
            raise ValueError(f"Data path does not exist: {config.data_path}")
        
        print("✅ Phase 6 configuration validated")
        
    except Exception as e:
        print(f"❌ Phase 6 configuration error: {e}")
        return
    
    # Create and run app
    app = create_phase6_app()
    
    try:
        print("🌐 Starting Phase 6 HTTP API server...")
        app.run(
            host=config.host,
            port=config.port,
            debug=config.debug,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Phase 6 server stopped by user")
    except Exception as e:
        print(f"❌ Phase 6 server error: {e}")


if __name__ == "__main__":
    run_phase6_server()
