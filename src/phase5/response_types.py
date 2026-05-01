"""
Response type definitions for Phase 5 presentation layer.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Any


class ResponseType(Enum):
    """Types of response formats supported."""
    WEB = "web"
    API = "api"
    MOBILE = "mobile"
    CLI = "cli"


class ResponseFormat(Enum):
    """Output formats for recommendations."""
    JSON = "json"
    HTML = "html"
    CARDS = "cards"
    TABLE = "table"
    SUMMARY = "summary"


@dataclass
class RecommendationSummary:
    """Summary statistics for recommendations."""
    total_candidates: int
    filtered_candidates: int
    final_recommendations: int
    avg_rating: Optional[float] = None
    price_range: Optional[str] = None
    cuisine_variety: Optional[List[str]] = None


@dataclass
class RecommendationMetadata:
    """Metadata for each recommendation."""
    confidence_score: float
    match_reasons: List[str]
    additional_info: Dict[str, Any]
    timestamp: str
