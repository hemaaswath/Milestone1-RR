"""
UI components for Phase 5 presentation layer.
"""

from typing import Dict, List, Optional


class UIComponents:
    """Reusable UI components for the restaurant recommendation system."""
    
    @staticmethod
    def generate_recommendation_html(recommendations: List[Dict], summary: Optional[Dict] = None) -> str:
        """Generate complete HTML page with recommendations."""
        
        # CSS styles
        styles = """
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f8f9fa;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            .summary-card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 25px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                border-left: 4px solid #4CAF50;
            }
            .recommendations-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .recommendation-card {
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                overflow: hidden;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .recommendation-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }
            .card-header {
                background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                color: white;
                padding: 20px;
                position: relative;
            }
            .rank-badge {
                position: absolute;
                top: 15px;
                right: 15px;
                background: rgba(255,255,255,0.9);
                color: #333;
                width: 35px;
                height: 35px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 14px;
            }
            .card-body {
                padding: 20px;
            }
            .restaurant-name {
                font-size: 1.3em;
                font-weight: 600;
                margin: 0 0 10px 0;
                color: #333;
            }
            .info-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin: 15px 0;
            }
            .info-item {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .info-label {
                font-weight: 600;
                color: #666;
                font-size: 0.9em;
            }
            .explanation-box {
                background: #f8f9fa;
                border-left: 4px solid #4CAF50;
                padding: 15px;
                margin-top: 15px;
                border-radius: 0 8px 8px 0;
            }
            .score-bar {
                height: 6px;
                background: #e0e0e0;
                border-radius: 3px;
                margin: 10px 0;
                overflow: hidden;
            }
            .score-fill {
                height: 100%;
                background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
                border-radius: 3px;
                transition: width 0.5s ease;
            }
            .rating-stars {
                color: #FFD700;
                font-size: 1.1em;
            }
            .footer {
                text-align: center;
                margin-top: 40px;
                padding: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
        </style>
        """
        
        # Generate summary section
        summary_html = ""
        if summary:
            summary_html = f"""
            <div class="summary-card">
                <h2 style="margin-top: 0; color: #2c3e50;">📊 Recommendation Summary</h2>
                <p>We analyzed <strong>{summary.get('total_candidates', 0)}</strong> restaurants and found 
                   <strong>{summary.get('filtered_candidates', 0)}</strong> matching your criteria.</p>
                <p>Presenting the top <strong>{summary.get('final_recommendations', 0)}</strong> personalized recommendations.</p>
            </div>
            """
        
        # Generate recommendation cards
        cards_html = ""
        for rec in recommendations:
            score_percentage = rec.get('score', 0) * 100
            
            # Generate rating stars
            rating = rec.get('rating', 0)
            if rating and rating != "N/A":
                stars = "⭐" * min(int(rating), 5)
            else:
                stars = "No rating"
            
            cards_html += f"""
            <div class="recommendation-card">
                <div class="card-header">
                    <h3 class="restaurant-name">{rec.get('restaurant_name', 'Unknown')}</h3>
                    <div class="rank-badge">#{rec.get('rank', 1)}</div>
                </div>
                <div class="card-body">
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="info-label">📍</span>
                            <span>{rec.get('location', 'Unknown')}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">🍽️</span>
                            <span>{rec.get('cuisines', 'Various')}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">⭐</span>
                            <span class="rating-stars">{stars}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">💰</span>
                            <span>₹{rec.get('cost_for_two', 'N/A')}</span>
                        </div>
                    </div>
                    
                    <div class="score-bar">
                        <div class="score-fill" style="width: {score_percentage:.1f}%"></div>
                    </div>
                    
                    <div class="explanation-box">
                        <strong>💡 Why we recommend this:</strong><br>
                        {rec.get('explanation', 'Great match for your preferences!')}
                    </div>
                </div>
            </div>
            """
        
        # Complete HTML page
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Restaurant Recommendations - AI Powered</title>
            {styles}
        </head>
        <body>
            <div class="header">
                <h1 style="margin: 0; font-size: 2.5em;">🍽️ AI Restaurant Recommendations</h1>
                <p style="margin: 10px 0 0 0; font-size: 1.1em; opacity: 0.9;">
                    Personalized restaurant suggestions powered by advanced AI
                </p>
            </div>
            
            {summary_html}
            
            <div class="recommendations-grid">
                {cards_html}
            </div>
            
            <div class="footer">
                <p style="margin: 0; color: #666;">
                    🤖 Generated by AI Restaurant Recommendation System
                    <br>
                    <small>Recommendations updated in real-time based on your preferences</small>
                </p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    @staticmethod
    def generate_form_html() -> str:
        """Generate input form HTML."""
        return """
        <div class="input-form" style="background: white; padding: 25px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h2 style="margin-top: 0; color: #2c3e50;">🔍 Find Your Perfect Restaurant</h2>
            <form id="recommendation-form" style="display: grid; gap: 20px;">
                <div class="form-row" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">📍 Location</label>
                        <input type="text" name="location" placeholder="e.g., Bellandur, Delhi" 
                               style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px;">
                    </div>
                    <div>
                        <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">💰 Budget</label>
                        <select name="budget" style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px;">
                            <option value="low">Low (Under ₹600)</option>
                            <option value="medium" selected>Medium (₹600-1500)</option>
                            <option value="high">High (Above ₹1500)</option>
                        </select>
                    </div>
                </div>
                <div class="form-row" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">🍽️ Cuisine</label>
                        <input type="text" name="cuisine" placeholder="e.g., North Indian, Italian" 
                               style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px;">
                    </div>
                    <div>
                        <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">⭐ Minimum Rating</label>
                        <input type="number" name="min_rating" placeholder="e.g., 4.0" min="0" max="5" step="0.1"
                               style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px;">
                    </div>
                </div>
                <div>
                    <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">📝 Additional Preferences</label>
                    <input type="text" name="additional_preferences" placeholder="e.g., family-friendly, outdoor seating" 
                           style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px;">
                </div>
                <button type="submit" style="background: linear-gradient(45deg, #FF6B6B, #4ECDC4); color: white; border: none; padding: 15px 30px; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; transition: transform 0.2s ease;">
                    🚀 Get Recommendations
                </button>
            </form>
        </div>
        """
    
    @staticmethod
    def generate_error_html(error_message: str) -> str:
        """Generate error page HTML."""
        return f"""
        <div class="error-container" style="background: #ffebee; border: 2px solid #f44336; border-radius: 10px; padding: 20px; margin: 20px 0;">
            <h3 style="color: #d32f2f; margin-top: 0;">❌ Oops! Something went wrong</h3>
            <p style="color: #d32f2f; margin-bottom: 0;">{error_message}</p>
        </div>
        """
