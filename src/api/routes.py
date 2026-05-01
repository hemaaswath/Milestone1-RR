"""
API Routes for Restaurant Recommendation System
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from phase2.validator import validate_preferences
from phase2.models import UserPreferences
from phase3.engine import load_restaurants, retrieve_top_candidates
from phase4.service import generate_ranked_recommendations
from phase5.formatters import ResponseFormatter, ResponseFormat, ResponseType
from phase5.ui_components import UIComponents
from phase5.response_types import RecommendationSummary

from .config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint
api_bp = Blueprint('api', __name__)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })


@api_bp.route('/recommendations', methods=['POST'])
@cross_origin(origins=config.allowed_origins)
def get_recommendations():
    """Main recommendation endpoint."""
    try:
        # Parse request data
        data = request.get_json() or {}
        
        # Validate preferences
        validation = validate_preferences(data)
        if not validation.is_valid or validation.preferences is None:
            return jsonify({
                "status": "error",
                "message": "Invalid preferences",
                "errors": validation.errors
            }), 400
        
        preferences = validation.preferences
        
        # Get additional parameters
        top_k = int(data.get('top_k', 5))
        response_format = data.get('format', 'json')
        include_summary = data.get('include_summary', True)
        
        logger.info(f"Processing recommendation request: {preferences.to_dict()}")
        
        # Phase 3: Retrieve candidates
        restaurants_df = load_restaurants(config.data_path)
        phase3_result = retrieve_top_candidates(
            restaurants_df=restaurants_df,
            preferences=preferences,
            top_n=min(top_k * 2, 20)  # Get more candidates for better ranking
        )
        
        candidates = [c.to_dict() for c in phase3_result.candidates]
        
        if not candidates:
            return jsonify({
                "status": "error",
                "message": "No restaurants found matching your criteria",
                "suggestions": [
                    "Try a different location",
                    "Lower your minimum rating requirement",
                    "Increase your budget range",
                    "Try a broader cuisine preference"
                ]
            }), 404
        
        # Phase 4: Generate LLM rankings
        ranked_recommendations = generate_ranked_recommendations(
            preferences=preferences,
            shortlisted_candidates=candidates,
            top_k=top_k,
            model=config.default_model
        )
        
        # Create summary
        summary = None
        if include_summary:
            summary = RecommendationSummary(
                total_candidates=phase3_result.total_records,
                filtered_candidates=phase3_result.filtered_records,
                final_recommendations=len(ranked_recommendations),
                avg_rating=sum(r.get('rating', 0) for r in ranked_recommendations if r.get('rating')) / len([r for r in ranked_recommendations if r.get('rating')]) if any(r.get('rating') for r in ranked_recommendations) else None
            )
        
        # Phase 5: Format response
        formatter = ResponseFormatter()
        
        # Determine response format
        if response_format == 'html':
            formatted_response = formatter.format_recommendations(
                ranked_recommendations, 
                ResponseFormat.HTML, 
                summary
            )
            return jsonify(formatted_response)
        elif response_format == 'cards':
            formatted_response = formatter.format_recommendations(
                ranked_recommendations, 
                ResponseFormat.CARDS, 
                summary
            )
            return jsonify(formatted_response)
        elif response_format == 'table':
            formatted_response = formatter.format_recommendations(
                ranked_recommendations, 
                ResponseFormat.TABLE, 
                summary
            )
            return jsonify(formatted_response)
        elif response_format == 'summary':
            formatted_response = formatter.format_recommendations(
                ranked_recommendations, 
                ResponseFormat.SUMMARY, 
                summary
            )
            return jsonify(formatted_response)
        else:  # Default to JSON
            formatted_response = formatter.format_recommendations(
                ranked_recommendations, 
                ResponseFormat.JSON, 
                summary
            )
            return jsonify(formatted_response)
    
    except Exception as e:
        logger.error(f"Error processing recommendation request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "details": str(e) if config.debug else "An unexpected error occurred"
        }), 500


@api_bp.route('/recommendations/web', methods=['POST'])
@cross_origin(origins=config.allowed_origins)
def get_web_recommendations():
    """Web interface for recommendations."""
    try:
        # Parse form data
        form_data = request.form.to_dict()
        
        # Convert form data to preferences
        preferences_data = {
            'location': form_data.get('location', ''),
            'budget': form_data.get('budget', 'medium'),
            'cuisine': form_data.get('cuisine', ''),
            'min_rating': float(form_data.get('min_rating', 0)),
            'additional_preferences': form_data.get('additional_preferences', '').split(',') if form_data.get('additional_preferences') else []
        }
        
        # Validate preferences
        validation = validate_preferences(preferences_data)
        if not validation.is_valid or validation.preferences is None:
            html_content = UIComponents.generate_error_html(
                f"Invalid preferences: {', '.join(validation.errors)}"
            )
            return html_content, 400
        
        preferences = validation.preferences
        top_k = int(form_data.get('top_k', 5))
        
        # Get recommendations (reuse main logic)
        restaurants_df = load_restaurants(config.data_path)
        phase3_result = retrieve_top_candidates(
            restaurants_df=restaurants_df,
            preferences=preferences,
            top_n=min(top_k * 2, 20)
        )
        
        candidates = [c.to_dict() for c in phase3_result.candidates]
        
        if not candidates:
            html_content = UIComponents.generate_error_html(
                "No restaurants found matching your criteria. Try adjusting your preferences."
            )
            return html_content, 404
        
        ranked_recommendations = generate_ranked_recommendations(
            preferences=preferences,
            shortlisted_candidates=candidates,
            top_k=top_k,
            model=config.default_model
        )
        
        summary = RecommendationSummary(
            total_candidates=phase3_result.total_records,
            filtered_candidates=phase3_result.filtered_records,
            final_recommendations=len(ranked_recommendations)
        )
        
        # Generate HTML response
        html_content = UIComponents.generate_recommendation_html(
            ranked_recommendations, 
            summary.__dict__
        )
        
        return html_content
    
    except Exception as e:
        logger.error(f"Error processing web recommendation request: {str(e)}")
        html_content = UIComponents.generate_error_html(
            "An error occurred while processing your request. Please try again."
        )
        return html_content, 500


@api_bp.route('/locations', methods=['GET'])
@cross_origin(origins=config.allowed_origins)
def get_locations():
    """Get available locations from dataset."""
    try:
        restaurants_df = load_restaurants(config.data_path)
        locations = sorted(restaurants_df['location'].dropna().unique().tolist())
        
        return jsonify({
            "status": "success",
            "data": {
                "locations": locations,
                "total_count": len(locations)
            }
        })
    
    except Exception as e:
        logger.error(f"Error fetching locations: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to fetch locations"
        }), 500


@api_bp.route('/cuisines', methods=['GET'])
@cross_origin(origins=config.allowed_origins)
def get_cuisines():
    """Get available cuisines from dataset."""
    try:
        restaurants_df = load_restaurants(config.data_path)
        # Extract and split cuisines
        all_cuisines = set()
        for cuisines in restaurants_df['cuisines'].dropna():
            all_cuisines.update([c.strip() for c in str(cuisines).split(',')])
        
        cuisine_list = sorted(list(all_cuisines))
        
        return jsonify({
            "status": "success",
            "data": {
                "cuisines": cuisine_list,
                "total_count": len(cuisine_list)
            }
        })
    
    except Exception as e:
        logger.error(f"Error fetching cuisines: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to fetch cuisines"
        }), 500


@api_bp.route('/stats', methods=['GET'])
@cross_origin(origins=config.allowed_origins))
def get_stats():
    """Get dataset statistics."""
    try:
        restaurants_df = load_restaurants(config.data_path)
        
        stats = {
            "total_restaurants": len(restaurants_df),
            "total_locations": restaurants_df['location'].nunique(),
            "avg_rating": restaurants_df['rating'].mean() if 'rating' in restaurants_df.columns else None,
            "locations": restaurants_df['location'].value_counts().head(10).to_dict(),
            "top_cuisines": {}
        }
        
        # Get top cuisines
        cuisine_counts = {}
        for cuisines in restaurants_df['cuisines'].dropna():
            for cuisine in str(cuisines).split(','):
                cuisine = cuisine.strip()
                cuisine_counts[cuisine] = cuisine_counts.get(cuisine, 0) + 1
        
        stats['top_cuisines'] = dict(sorted(cuisine_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        
        return jsonify({
            "status": "success",
            "data": stats
        })
    
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to fetch statistics"
        }), 500
