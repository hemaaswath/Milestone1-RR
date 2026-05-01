"""
Enhanced Middleware for Phase 6 Backend HTTP API

Provides rate limiting, structured telemetry, and security features
as specified in the Phase 6 Backend HTTP API requirements.
"""

import time
import logging
import json
from datetime import datetime, timedelta
from functools import wraps
from collections import defaultdict
from flask import request, jsonify, g

from .config import config

logger = logging.getLogger(__name__)

# In-memory rate limiter (for production, use Redis)
rate_limiter = defaultdict(list)


class StructuredTelemetry:
    """Structured telemetry and logging for Phase 6 API."""
    
    def __init__(self):
        self.request_counts = defaultdict(int)
        self.response_times = defaultdict(list)
        self.error_counts = defaultdict(int)
        self.token_usage = defaultdict(int)
        
    def log_request(self, method, path, user_id=None, request_id=None):
        """Log incoming request with structured data."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "request_start",
            "method": method,
            "path": path,
            "user_id": user_id,
            "request_id": request_id,
            "source_ip": getattr(request, 'remote_addr', 'unknown'),
            "user_agent": getattr(request, 'user_agent', {}).get('string', 'unknown') if hasattr(request, 'user_agent') else 'unknown'
        }
        
        logger.info(f"REQUEST_START {json.dumps(log_data)}")
        
        # Store in g for later use
        g.request_start_time = time.time()
        g.request_id = request_id
        g.log_data = log_data
        
    def log_response(self, status_code, response_size=0, token_count=0):
        """Log response completion with telemetry."""
        duration = time.time() - getattr(g, 'request_start_time', 0)
        
        log_data = getattr(g, 'log_data', {})
        log_data.update({
            "timestamp": datetime.utcnow().isoformat(),
            "event": "request_complete",
            "status_code": status_code,
            "duration_ms": int(duration * 1000),
            "response_size_bytes": response_size,
            "token_count": token_count
        })
        
        # Update metrics
        path = log_data.get('path', 'unknown')
        self.request_counts[path] += 1
        self.response_times[path].append(duration)
        self.token_usage[path] += token_count
        
        if status_code >= 400:
            self.error_counts[path] += 1
        
        logger.info(f"REQUEST_COMPLETE {json.dumps(log_data)}")
        
        # Log performance metrics
        if duration > 5.0:  # Slow requests
            logger.warning(f"SLOW_REQUEST {json.dumps(log_data)}")
    
    def get_metrics(self):
        """Get current telemetry metrics."""
        current_time = datetime.utcnow()
        metrics = {
            "timestamp": current_time.isoformat(),
            "request_counts": dict(self.request_counts),
            "error_counts": dict(self.error_counts),
            "total_requests": sum(self.request_counts.values()),
            "total_errors": sum(self.error_counts.values()),
            "avg_response_times": {},
            "token_usage": dict(self.token_usage),
            "total_tokens": sum(self.token_usage.values())
        }
        
        # Calculate average response times
        for path, times in self.response_times.items():
            if times:
                metrics["avg_response_times"][path] = sum(times) / len(times)
        
        return metrics


# Global telemetry instance
telemetry = StructuredTelemetry()


def rate_limit(max_requests=60, window_seconds=60):
    """Rate limiting decorator."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client IP
            client_ip = request.remote_addr or 'unknown'
            
            # Clean old entries
            current_time = time.time()
            cutoff_time = current_time - window_seconds
            rate_limiter[client_ip] = [
                req_time for req_time in rate_limiter[client_ip] 
                if req_time > cutoff_time
            ]
            
            # Check if rate limit exceeded
            if len(rate_limiter[client_ip]) >= max_requests:
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                return jsonify({
                    "status": "error",
                    "message": "Rate limit exceeded. Please try again later.",
                    "retry_after": window_seconds
                }), 429
            
            # Add current request
            rate_limiter[client_ip].append(current_time)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def validate_request_size(max_size_mb=1):
    """Validate request size to prevent abuse."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            content_length = request.content_length or 0
            max_size_bytes = max_size_mb * 1024 * 1024
            
            if content_length > max_size_bytes:
                logger.warning(f"Request too large: {content_length} bytes from IP: {request.remote_addr}")
                return jsonify({
                    "status": "error",
                    "message": f"Request too large. Maximum size is {max_size_mb}MB."
                }), 413
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def sanitize_input():
    """Sanitize and validate input data."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.is_json:
                data = request.get_json() or {}
                
                # Validate text field lengths
                max_text_length = 1000  # Phase 2 max length
                
                for field, value in data.items():
                    if isinstance(value, str) and len(value) > max_text_length:
                        logger.warning(f"Input too long for field {field}: {len(value)} chars")
                        return jsonify({
                            "status": "error",
                            "message": f"Field '{field}' exceeds maximum length of {max_text_length} characters."
                        }), 400
                
                # Check for potential injection patterns
                dangerous_patterns = ['<script', 'javascript:', 'eval(', 'exec(']
                for field, value in data.items():
                    if isinstance(value, str):
                        for pattern in dangerous_patterns:
                            if pattern.lower() in value.lower():
                                logger.warning(f"Potentially dangerous input detected in field {field}")
                                return jsonify({
                                    "status": "error",
                                    "message": "Invalid input detected."
                                }), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def setup_enhanced_middleware(app):
    """Setup enhanced middleware for Phase 6 compliance."""
    
    # Request ID generation
    @app.before_request
    def generate_request_id():
        g.request_id = f"req_{int(time.time() * 1000)}_{hash(str(time.time())) % 10000}"
        g.start_time = time.time()
    
    # Structured logging
    @app.before_request
    def log_request_start():
        telemetry.log_request(
            method=request.method,
            path=request.path,
            request_id=getattr(g, 'request_id', None)
        )
    
    @app.after_request
    def log_response_end(response):
        # Calculate response size
        response_size = len(response.get_data()) if hasattr(response, 'get_data') else 0
        
        # Log completion
        telemetry.log_response(
            status_code=response.status_code,
            response_size=response_size
        )
        
        # Add security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
    
    # Enhanced error handlers
    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        return jsonify({
            "status": "error",
            "message": "Rate limit exceeded",
            "retry_after": 60
        }), 429
    
    @app.errorhandler(413)
    def payload_too_large(e):
        return jsonify({
            "status": "error",
            "message": "Request payload too large"
        }), 413
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            "status": "error",
            "message": "Method not allowed",
            "allowed_methods": getattr(request, 'view_args', {}).get('methods', [])
        }), 405
    
    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"Internal server error: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "request_id": getattr(g, 'request_id', None)
        }), 500


# Export telemetry instance for monitoring endpoints
__all__ = ['telemetry', 'setup_enhanced_middleware', 'rate_limit', 'validate_request_size', 'sanitize_input']
