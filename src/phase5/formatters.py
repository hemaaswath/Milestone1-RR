"""
Response formatters for Phase 5 presentation layer.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

from .response_types import (
    RecommendationSummary,
    RecommendationMetadata,
    ResponseFormat,
    ResponseType
)


class RecommendationCard:
    """Individual recommendation card with rich formatting."""
    
    def __init__(
        self,
        restaurant_name: str,
        rank: int,
        score: float,
        explanation: str,
        location: str,
        cuisines: str,
        rating: Optional[float] = None,
        cost_for_two: Optional[float] = None,
        metadata: Optional[RecommendationMetadata] = None
    ):
        self.restaurant_name = restaurant_name
        self.rank = rank
        self.score = score
        self.explanation = explanation
        self.location = location
        self.cuisines = cuisines
        self.rating = rating
        self.cost_for_two = cost_for_two
        self.metadata = metadata or RecommendationMetadata(
            confidence_score=score,
            match_reasons=[],
            additional_info={},
            timestamp=datetime.now().isoformat()
        )
    
    def to_dict(self) -> Dict:
        """Convert card to dictionary."""
        return {
            "restaurant_name": self.restaurant_name,
            "rank": self.rank,
            "score": self.score,
            "explanation": self.explanation,
            "location": self.location,
            "cuisines": self.cuisines,
            "rating": self.rating,
            "cost_for_two": self.cost_for_two,
            "metadata": {
                "confidence_score": self.metadata.confidence_score,
                "match_reasons": self.metadata.match_reasons,
                "additional_info": self.metadata.additional_info,
                "timestamp": self.metadata.timestamp
            }
        }


class ResponseFormatter:
    """Formats recommendations for different output types."""
    
    def __init__(self, response_type: ResponseType = ResponseType.WEB):
        self.response_type = response_type
    
    def format_recommendations(
        self,
        recommendations: List[Dict],
        format_type: ResponseFormat = ResponseFormat.JSON,
        summary: Optional[RecommendationSummary] = None
    ) -> Dict:
        """Format recommendations based on specified format."""
        
        cards = [RecommendationCard(**rec) for rec in recommendations]
        
        if format_type == ResponseFormat.JSON:
            return self._format_json(cards, summary)
        elif format_type == ResponseFormat.HTML:
            return self._format_html(cards, summary)
        elif format_type == ResponseFormat.CARDS:
            return self._format_cards(cards, summary)
        elif format_type == ResponseFormat.TABLE:
            return self._format_table(cards, summary)
        elif format_type == ResponseFormat.SUMMARY:
            return self._format_summary(cards, summary)
        else:
            return self._format_json(cards, summary)
    
    def _format_json(self, cards: List[RecommendationCard], summary: Optional[RecommendationSummary]) -> Dict:
        """Format as JSON response."""
        return {
            "status": "success",
            "data": {
                "recommendations": [card.to_dict() for card in cards],
                "summary": summary.__dict__ if summary else None,
                "generated_at": datetime.now().isoformat()
            }
        }
    
    def _format_html(self, cards: List[RecommendationCard], summary: Optional[RecommendationSummary]) -> Dict:
        """Format as HTML response."""
        html_cards = []
        for card in cards:
            html_card = f"""
            <div class="recommendation-card" style="border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 8px;">
                <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0; color: #333;">#{card.rank} {card.restaurant_name}</h3>
                    <span class="score" style="background: #4CAF50; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px;">
                        Score: {card.score:.2f}
                    </span>
                </div>
                <div class="card-body" style="margin-top: 10px;">
                    <p><strong>Location:</strong> {card.location}</p>
                    <p><strong>Cuisine:</strong> {card.cuisines}</p>
                    {f'<p><strong>Rating:</strong> {"⭐" * int(card.rating or 0)} {card.rating}</p>' if card.rating else ''}
                    {f'<p><strong>Cost for Two:</strong> ₹{card.cost_for_two}</p>' if card.cost_for_two else ''}
                    <div class="explanation" style="background: #f8f9fa; padding: 10px; border-radius: 4px; margin-top: 10px;">
                        <strong>Why we recommend this:</strong> {card.explanation}
                    </div>
                </div>
            </div>
            """
            html_cards.append(html_card)
        
        html_summary = ""
        if summary:
            html_summary = f"""
            <div class="summary" style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="margin-top: 0;">Summary</h3>
                <p>We analyzed <strong>{summary.total_candidates}</strong> restaurants and found <strong>{summary.filtered_candidates}</strong> matching your criteria.</p>
                <p>Presenting the top <strong>{summary.final_recommendations}</strong> recommendations.</p>
            </div>
            """
        
        return {
            "status": "success",
            "data": {
                "html": html_summary + "".join(html_cards),
                "generated_at": datetime.now().isoformat()
            }
        }
    
    def _format_cards(self, cards: List[RecommendationCard], summary: Optional[RecommendationSummary]) -> Dict:
        """Format as card components for frontend."""
        return {
            "status": "success",
            "data": {
                "cards": [card.to_dict() for card in cards],
                "summary": summary.__dict__ if summary else None,
                "generated_at": datetime.now().isoformat()
            }
        }
    
    def _format_table(self, cards: List[RecommendationCard], summary: Optional[RecommendationSummary]) -> Dict:
        """Format as table data."""
        table_data = []
        for card in cards:
            table_data.append({
                "rank": card.rank,
                "restaurant": card.restaurant_name,
                "location": card.location,
                "cuisine": card.cuisines,
                "rating": card.rating or "N/A",
                "cost": f"₹{card.cost_for_two}" if card.cost_for_two else "N/A",
                "score": f"{card.score:.2f}",
                "explanation": card.explanation
            })
        
        return {
            "status": "success",
            "data": {
                "table": table_data,
                "summary": summary.__dict__ if summary else None,
                "generated_at": datetime.now().isoformat()
            }
        }
    
    def _format_summary(self, cards: List[RecommendationCard], summary: Optional[RecommendationSummary]) -> Dict:
        """Format as concise summary."""
        top_recommendations = []
        for card in cards[:3]:  # Top 3 for summary
            top_recommendations.append(f"{card.rank}. {card.restaurant_name} ({card.location}) - {card.explanation}")
        
        return {
            "status": "success",
            "data": {
                "summary_text": f"Based on your preferences, here are our top recommendations:\n\n" + "\n".join(top_recommendations),
                "detailed_summary": summary.__dict__ if summary else None,
                "generated_at": datetime.now().isoformat()
            }
        }
