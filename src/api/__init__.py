"""
Unified API Layer for Restaurant Recommendation System

This module provides a RESTful API that integrates all phases of the
restaurant recommendation system into a cohesive backend service.
"""

from .main import create_app
from .routes import api_bp
from .middleware import setup_middleware
from .config import APIConfig

__all__ = [
    "create_app",
    "api_bp", 
    "setup_middleware",
    "APIConfig",
]
