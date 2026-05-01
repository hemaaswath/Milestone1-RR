"""
Enhanced API Routes for Phase 6 Backend HTTP API

Implements comprehensive endpoints with Phase 6 requirements:
- Request validation and sanitization
- Structured telemetry and logging
- Rate limiting and security
- Phase 1-5 orchestration
- Stable JSON contracts
"""

import logging
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

from flask import Blueprint, request, jsonify, g
from flask_cors import cross_origin

from phase2.validator import validate_preferences
from phase2.models import UserPreferences
from phase3.engine import load_restaurants, retrieve_top_candidates
from phase4.service import generate_ranked_recommendations
from phase5.formatters import ResponseFormatter, ResponseFormat, ResponseType
from phase5.ui_components import UIComponents
from phase5.response_types import RecommendationSummary

from api.config import config
from api.enhanced_middleware import rate_limit, validate_request_size, sanitize_input, telemetry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint
enhanced_api_bp = Blueprint('enhanced_api', __name__)


def create_response(status: str, data: Any = None, message: str = None, errors: List[str] = None, 
                  metadata: Dict = None) -> Dict:
    """Create standardized API response."""
    response = {
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": getattr(g, 'request_id', None)
    }
    
    if data is not None:
        response["data"] = data
    
    if message:
        response["message"] = message
    
    if errors:
        response["errors"] = errors
    
    if metadata:
        response["metadata"] = metadata
    
    return response


@enhanced_api_bp.route('/health', methods=['GET'])
@rate_limit(max_requests=100, window_seconds=60)
def health_check():
    """Enhanced health check endpoint for Phase 6."""
    try:
        # Check critical components
        checks = {
            "api": "healthy",
            "data_source": "healthy" if config.data_path and Path(config.data_path).exists() else "unhealthy",
            "groq_api": "configured" if config.groq_api_key else "missing",
            "memory_usage": f"{int((time.process_time() / 1024) * 100)}%"
        }
        
        overall_status = "healthy" if all(status == "healthy" or status == "configured" for status in checks.values()) else "degraded"
        
        return jsonify(create_response(
            status="success",
            data={
                "status": overall_status,
                "checks": checks,
                "version": "1.0.0",
                "phase": "6",
                "uptime_seconds": time.time() - getattr(g, 'start_time', time.time())
            }
        ))
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify(create_response(
            status="error",
            message="Health check failed"
        )), 500


@enhanced_api_bp.route('/meta', methods=['GET'])
@rate_limit(max_requests=60, window_seconds=60)
def get_api_metadata():
    """Get API metadata and configuration hints for Phase 6 frontend."""
    try:
        # Load sample data to get available options
        restaurants_df = load_restaurants(config.data_path)
        
        # Extract available locations and cuisines
        locations = sorted(restaurants_df['location'].unique().tolist())[:20]  # Limit for performance
        cuisines = sorted(restaurants_df['cuisines'].str.split(', ').explode().unique().tolist())[:30]
        
        metadata = {
            "api_version": "1.0.0",
            "phase": "6",
            "supported_formats": ["json", "html", "cards", "table", "summary"],
            "default_top_k": 5,
            "max_top_k": 10,
            "available_locations": locations,
            "available_cuisines": cuisines,
            "budget_options": ["low", "medium", "high"],
            "rating_range": {"min": 1.0, "max": 5.0, "step": 0.5},
            "validation": {
                "max_text_length": 1000,
                "required_fields": ["location", "budget"],
                "optional_fields": ["cuisine", "min_rating", "additional_preferences"]
            },
            "rate_limits": {
                "requests_per_minute": config.rate_limit_per_minute,
                "max_request_size_mb": 1
            },
            "model_info": {
                "default_model": config.default_model,
                "provider": "groq"
            }
        }
        
        return jsonify(create_response(
            status="success",
            data=metadata
        ))
        
    except Exception as e:
        logger.error(f"Metadata endpoint failed: {e}")
        return jsonify(create_response(
            status="error",
            message="Failed to retrieve metadata"
        )), 500


@enhanced_api_bp.route('/recommendations', methods=['POST'])
@rate_limit(max_requests=config.rate_limit_per_minute, window_seconds=60)
@validate_request_size(max_size_mb=1)
@sanitize_input()
def get_recommendations():
    """Enhanced main recommendation endpoint for Phase 6."""
    request_start_time = time.time()
    
    try:
        # Parse and validate request data
        data = request.get_json() or {}
        
        # Validate preferences using Phase 2
        validation = validate_preferences(data)
        if not validation.is_valid or validation.preferences is None:
            return jsonify(create_response(
                status="error",
                message="Invalid preferences",
                errors=validation.errors
            )), 400
        
        preferences = validation.preferences
        
        # Get additional parameters with defaults
        top_k = min(int(data.get('top_k', 5)), 10)  # Cap at 10 for performance
        response_format = data.get('format', 'json')
        include_summary = data.get('include_summary', True)
        include_metadata = data.get('include_metadata', True)
        
        logger.info(f"Processing recommendation request: {preferences.to_dict()}")
        
        # Phase 3: Retrieve candidates with performance tracking
        phase3_start = time.time()
        restaurants_df = load_restaurants(config.data_path)
        phase3_result = retrieve_top_candidates(
            restaurants_df=restaurants_df,
            preferences=preferences,
            top_n=min(top_k * 2, 20)  # Get more candidates for better ranking
        )
        phase3_duration = time.time() - phase3_start
        
        candidates = [c.to_dict() for c in phase3_result.candidates]
        
        if not candidates:
            return jsonify(create_response(
                status="error",
                message="No restaurants found matching your criteria",
                data={
                    "suggestions": [
                        "Try a different location",
                        "Lower your minimum rating requirement", 
                        "Increase your budget range",
                        "Try a broader cuisine preference"
                    ],
                    "total_candidates": 0,
                    "filtered_candidates": 0
                }
            )), 404
        
        # Phase 4: Generate LLM rankings with performance tracking
        phase4_start = time.time()
        ranked_recommendations = generate_ranked_recommendations(
            preferences=preferences,
            shortlisted_candidates=candidates,
            top_k=top_k,
            model=config.default_model
        )
        phase4_duration = time.time() - phase4_start
        
        # Phase 5: Format response with performance tracking
        phase5_start = time.time()
        formatter = ResponseFormatter()
        
        # Determine response format
        format_mapping = {
            'json': ResponseFormat.JSON,
            'html': ResponseFormat.HTML,
            'cards': ResponseFormat.CARDS,
            'table': ResponseFormat.TABLE,
            'summary': ResponseFormat.SUMMARY
        }
        
        format_enum = format_mapping.get(response_format, ResponseFormat.JSON)
        formatted_response = formatter.format_recommendations(
            ranked_recommendations, 
            format_enum
        )
        phase5_duration = time.time() - phase5_start
        
        # Create summary if requested
        summary = None
        if include_summary:
            summary = RecommendationSummary(
                total_candidates=phase3_result.total_records,
                filtered_candidates=phase3_result.filtered_records,
                final_recommendations=len(ranked_recommendations),
                avg_rating=sum(r.get('rating', 0) for r in ranked_recommendations if r.get('rating')) / len([r for r in ranked_recommendations if r.get('rating')]) if any(r.get('rating') for r in ranked_recommendations) else None
            )
        
        # Create metadata for Phase 6 telemetry
        metadata = None
        if include_metadata:
            total_duration = time.time() - request_start_time
            metadata = {
                "pipeline_performance": {
                    "phase3_duration_ms": int(phase3_duration * 1000),
                    "phase4_duration_ms": int(phase4_duration * 1000),
                    "phase5_duration_ms": int(phase5_duration * 1000),
                    "total_duration_ms": int(total_duration * 1000)
                },
                "data_stats": {
                    "total_candidates": phase3_result.total_records,
                    "filtered_candidates": phase3_result.filtered_records,
                    "final_recommendations": len(ranked_recommendations),
                    "candidates_used_for_llm": len(candidates)
                },
                "model_info": {
                    "model": config.default_model,
                    "provider": "groq"
                },
                "request_info": {
                    "top_k_requested": top_k,
                    "response_format": response_format,
                    "preferences": preferences.to_dict()
                }
            }
        
        # Log successful completion
        logger.info(f"Recommendation completed: {len(ranked_recommendations)} results in {total_duration:.2f}s")
        
        return jsonify(create_response(
            status="success",
            data=formatted_response,
            metadata={
                "summary": summary.to_dict() if summary else None,
                "telemetry": metadata
            }
        ))
        
    except Exception as e:
        logger.error(f"Recommendation endpoint failed: {e}", exc_info=True)
        return jsonify(create_response(
            status="error",
            message="Failed to generate recommendations",
            errors=[str(e)]
        )), 500


@enhanced_api_bp.route('/recommendations/web', methods=['POST'])
@rate_limit(max_requests=config.rate_limit_per_minute, window_seconds=60)
@validate_request_size(max_size_mb=1)
@sanitize_input()
def get_web_recommendations():
    """Web-based recommendation endpoint for Phase 6."""
    try:
        # Parse and validate request data
        data = request.get_json() or {}
        
        # Validate preferences
        validation = validate_preferences(data)
        if not validation.is_valid or validation.preferences is None:
            return jsonify(create_response(
                status="error",
                message="Invalid preferences",
                errors=validation.errors
            )), 400
        
        preferences = validation.preferences
        top_k = min(int(data.get('top_k', 5)), 10)
        
        # Phase 3: Retrieve candidates
        restaurants_df = load_restaurants(config.data_path)
        phase3_result = retrieve_top_candidates(
            restaurants_df=restaurants_df,
            preferences=preferences,
            top_n=min(top_k * 2, 20)
        )
        
        candidates = [c.to_dict() for c in phase3_result.candidates]
        
        if not candidates:
            return create_response(
                status="error",
                message="No restaurants found matching your criteria"
            ), 404
        
        # Phase 4: Generate LLM rankings
        ranked_recommendations = generate_ranked_recommendations(
            preferences=preferences,
            shortlisted_candidates=candidates,
            top_k=top_k,
            model=config.default_model
        )
        
        # Phase 5: Generate HTML response
        ui_components = UIComponents()
        html_response = ui_components.generate_recommendation_html(ranked_recommendations)
        
        logger.info(f"Web recommendations generated: {len(ranked_recommendations)} results")
        
        return html_response, 200, {'Content-Type': 'text/html; charset=utf-8'}
        
    except Exception as e:
        logger.error(f"Web recommendations failed: {e}", exc_info=True)
        return jsonify(create_response(
            status="error",
            message="Failed to generate web recommendations"
        )), 500


@enhanced_api_bp.route('/locations', methods=['GET'])
@rate_limit(max_requests=60, window_seconds=60)
def get_locations():
    """Get available locations from dataset."""
    try:
        restaurants_df = load_restaurants(config.data_path)
        locations = sorted(restaurants_df['location'].unique().tolist())
        
        return jsonify(create_response(
            status="success",
            data={
                "locations": locations,
                "total_count": len(locations)
            }
        ))
        
    except Exception as e:
        logger.error(f"Locations endpoint failed: {e}")
        return jsonify(create_response(
            status="error",
            message="Failed to retrieve locations"
        )), 500


@enhanced_api_bp.route('/cuisines', methods=['GET'])
@rate_limit(max_requests=60, window_seconds=60)
def get_cuisines():
    """Get available cuisines from dataset."""
    try:
        restaurants_df = load_restaurants(config.data_path)
        # Split cuisines and get unique values
        all_cuisines = []
        for cuisines_str in restaurants_df['cuisines'].dropna():
            all_cuisines.extend([c.strip() for c in cuisines_str.split(',')])
        
        unique_cuisines = sorted(list(set(all_cuisines)))
        
        return jsonify(create_response(
            status="success",
            data={
                "cuisines": unique_cuisines,
                "total_count": len(unique_cuisines)
            }
        ))
        
    except Exception as e:
        logger.error(f"Cuisines endpoint failed: {e}")
        return jsonify(create_response(
            status="error",
            message="Failed to retrieve cuisines"
        )), 500


@enhanced_api_bp.route('/stats', methods=['GET'])
@rate_limit(max_requests=30, window_seconds=60)
def get_stats():
    """Get dataset statistics."""
    try:
        restaurants_df = load_restaurants(config.data_path)
        
        stats = {
            "total_restaurants": len(restaurants_df),
            "unique_locations": restaurants_df['location'].nunique(),
            "unique_cuisines": len(set([c.strip() for cuisines in restaurants_df['cuisines'].dropna() for c in cuisines.split(',')])),
            "avg_rating": restaurants_df['rating'].mean(),
            "price_ranges": {
                "low": len(restaurants_df[restaurants_df['cost_for_two'] <= 600]),
                "medium": len(restaurants_df[(restaurants_df['cost_for_two'] > 600) & (restaurants_df['cost_for_two'] <= 1500)]),
                "high": len(restaurants_df[restaurants_df['cost_for_two'] > 1500])
            },
            "top_locations": restaurants_df['location'].value_counts().head(10).to_dict(),
            "data_updated": datetime.fromtimestamp(Path(config.data_path).stat().st_mtime).isoformat()
        }
        
        return jsonify(create_response(
            status="success",
            data=stats
        ))
        
    except Exception as e:
        logger.error(f"Stats endpoint failed: {e}")
        return jsonify(create_response(
            status="error",
            message="Failed to retrieve statistics"
        )), 500


# Export the enhanced blueprint
__all__ = ['enhanced_api_bp']
