"""
Middleware for Restaurant Recommendation API
"""

import time
import logging
from functools import wraps
from flask import request, jsonify

from .config import config

logger = logging.getLogger(__name__)


def setup_middleware(app):
    """Setup all middleware for the Flask app."""
    
    # Request logging middleware
    @app.before_request
    def log_request():
        request.start_time = time.time()
        logger.info(f"Request: {request.method} {request.path}")
    
    @app.after_request
    def log_response(response):
        duration = time.time() - request.start_time
        logger.info(f"Response: {response.status_code} - {duration:.3f}s")
        return response
    
    # Error handling middleware
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "Endpoint not found",
            "path": request.path
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "status": "error",
            "message": "Bad request"
        }), 400


def rate_limit(max_requests_per_minute=60):
    """Simple rate limiting decorator."""
    requests = {}
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()
            
            # Clean old requests
            if client_ip in requests:
                requests[client_ip] = [t for t in requests[client_ip] if current_time - t < 60]
            else:
                requests[client_ip] = []
            
            # Check rate limit
            if len(requests[client_ip]) >= max_requests_per_minute:
                return jsonify({
                    "status": "error",
                    "message": "Rate limit exceeded"
                }), 429
            
            # Add current request
            requests[client_ip].append(current_time)
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator


def validate_json(f):
    """Validate JSON request middleware."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'PATCH'] and not request.is_json:
            return jsonify({
                "status": "error",
                "message": "Content-Type must be application/json"
            }), 400
        
        try:
            if request.data:
                request.get_json()  # Validate JSON
            return f(*args, **kwargs)
        except Exception:
            return jsonify({
                "status": "error",
                "message": "Invalid JSON format"
            }), 400
    
    return decorated_function
