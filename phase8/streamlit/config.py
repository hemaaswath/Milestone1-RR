"""
Phase 8 Streamlit Configuration

Configuration settings for the Streamlit demo app.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class StreamlitConfig:
    """Configuration for Phase 8 Streamlit application."""
    
    # API Configuration
    API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api/v1")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
    
    # GROQ API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # Application Configuration
    APP_TITLE = "Restaurant Recommendations"
    APP_VERSION = "1.0.0"
    PHASE = "8"
    
    # UI Configuration
    PAGE_CONFIG = {
        "page_title": APP_TITLE,
        "page_icon": "🍽️",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }
    
    # Demo Configuration
    DEFAULT_LOCATIONS = ["Bellandur", "Delhi", "Mumbai", "Bangalore", "Hyderabad"]
    DEFAULT_CUISINES = ["North Indian", "Chinese", "Italian", "South Indian", "Continental"]
    DEFAULT_BUDGETS = ["low", "medium", "high"]
    DEFAULT_TOP_K_OPTIONS = [3, 5, 7, 10]
    
    # Chart Configuration
    CHART_THEME = "plotly_white"
    CHART_COLOR_SCALE = "viridis"
    
    # Cache Configuration
    CACHE_TTL = 300  # 5 minutes
    
    @classmethod
    def is_development(cls):
        """Check if running in development mode."""
        return os.getenv("ENVIRONMENT", "development") == "development"
    
    @classmethod
    def get_api_health_url(cls):
        """Get API health check URL."""
        return f"{cls.API_BASE_URL}/health"
    
    @classmethod
    def get_api_recommendations_url(cls):
        """Get API recommendations URL."""
        return f"{cls.API_BASE_URL}/recommendations"
    
    @classmethod
    def get_api_locations_url(cls):
        """Get API locations URL."""
        return f"{cls.API_BASE_URL}/locations"
    
    @classmethod
    def get_api_cuisines_url(cls):
        """Get API cuisines URL."""
        return f"{cls.API_BASE_URL}/cuisines"
