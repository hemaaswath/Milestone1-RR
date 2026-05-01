"""
API Configuration for Restaurant Recommendation System
"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class APIConfig:
    """Configuration settings for the API."""
    
    # Server settings
    host: str = os.getenv("API_HOST", "127.0.0.1")
    port: int = int(os.getenv("API_PORT", "8000"))
    debug: bool = os.getenv("API_DEBUG", "false").lower() == "true"
    
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///restaurants.db")
    
    # LLM settings
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    default_model: str = os.getenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")
    
    # Data paths
    data_path: str = os.getenv("DATA_PATH", "data/processed/restaurants_phase1.csv")
    
    # CORS settings
    allowed_origins: list = field(default_factory=lambda: os.getenv("ALLOWED_ORIGINS", "*").split(","))
    
    # Rate limiting
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # Cache settings
    cache_ttl: int = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        if not self.data_path or not os.path.exists(self.data_path):
            raise ValueError(f"Data path does not exist: {self.data_path}")


# Global configuration instance
config = APIConfig()
