"""
Results Display Component for Phase 8 Streamlit App

This component displays restaurant recommendations with beautiful UI.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

class ResultsDisplay:
    """Results display component for restaurant recommendations."""
    
    def __init__(self):
        pass
    
    def display_summary_metrics(self, recommendations_data, preferences):
        """Display summary metrics cards."""
        if not recommendations_data:
            st.error("❌ No recommendations available")
            return
        
        recommendations = recommendations_data.get("data", {}).get("recommendations", [])
        summary = recommendations_data.get("data", {}).get("summary", {})
        
        if not recommendations:
            st.info("ℹ️ No restaurants found matching your criteria. Try adjusting your preferences.")
            return
        
        # Display summary metrics
        st.header("📊 Recommendation Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{summary.get('final_recommendations', 0)}</h3>
                <p>Recommendations</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{summary.get('avg_rating', 0):.1f}</h3>
                <p>Average Rating</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{summary.get('filtered_candidates', 0)}</h3>
                <p>Candidates Found</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{preferences.get('location', 'Unknown')}</h3>
                <p>Selected Location</p>
            </div>
            """, unsafe_allow_html=True)
    
    def display_recommendations(self, recommendations_data):
        """Display individual restaurant recommendations."""
        recommendations = recommendations_data.get("data", {}).get("recommendations", [])
        
        if not recommendations:
            return
        
        st.header("🍽️ Your Restaurant Recommendations")
        
        for i, restaurant in enumerate(recommendations):
            with st.container():
                st.markdown(f"""
                <div class="restaurant-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h3>{restaurant.get('restaurant_name', 'Unknown Restaurant')}</h3>
                        <div style="display: flex; gap: 0.5rem;">
                            <span class="rank-badge">#{restaurant.get('rank', 1)}</span>
                            <span class="score-badge">{restaurant.get('score', 0) * 100:.0f}% Match</span>
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                        <div>📍 <strong>Location:</strong> {restaurant.get('location', 'Unknown')}</div>
                        <div>🍽️ <strong>Cuisine:</strong> {restaurant.get('cuisines', 'Various')}</div>
                        <div>⭐ <strong>Rating:</strong> {restaurant.get('rating', 0)}/5</div>
                        <div>💰 <strong>Cost for Two:</strong> ₹{restaurant.get('cost_for_two', 0):,}</div>
                    </div>
                    
                    <div class="explanation-box">
                        <h4>💡 Why we recommend this restaurant:</h4>
                        <p>{restaurant.get('explanation', 'Great match for your preferences')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    def display_processing_info(self, recommendations_data):
        """Display processing information and metadata."""
        metadata = recommendations_data.get("metadata", {})
        
        if not metadata:
            return
        
        st.header("📈 Processing Information")
        
        if metadata.get("source") == "demo":
            st.info("ℹ️ This is demo data. The backend API is currently unavailable.")
        else:
            pipeline_perf = metadata.get("pipeline_performance", {})
            if pipeline_perf:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Phase 3 Duration", f"{pipeline_perf.get('phase3_duration_ms', 0)}ms")
                
                with col2:
                    st.metric("Phase 4 Duration", f"{pipeline_perf.get('phase4_duration_ms', 0)}ms")
                
                with col3:
                    st.metric("Total Duration", f"{pipeline_perf.get('total_duration_ms', 0)}ms")
    
    def create_charts(self, recommendations_data):
        """Create interactive charts for recommendations."""
        recommendations = recommendations_data.get("data", {}).get("recommendations", [])
        
        if not recommendations:
            st.info("📊 No data available for charts.")
            return
        
        st.header("📊 Analytics Dashboard")
        
        # Create DataFrame for charts
        df = pd.DataFrame(recommendations)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Ratings chart
            fig_ratings = px.bar(
                df, 
                x="restaurant_name", 
                y="rating",
                title="Restaurant Ratings",
                labels={"rating": "Rating", "restaurant_name": "Restaurant"},
                color="rating",
                color_continuous_scale="Viridis"
            )
            fig_ratings.update_xaxis(tickangle=45)
            fig_ratings.update_layout(height=400)
            st.plotly_chart(fig_ratings, use_container_width=True)
        
        with col2:
            # Cost chart
            fig_cost = px.bar(
                df,
                x="restaurant_name",
                y="cost_for_two",
                title="Cost for Two (₹)",
                labels={"cost_for_two": "Cost (₹)", "restaurant_name": "Restaurant"},
                color="cost_for_two",
                color_continuous_scale="Blues"
            )
            fig_cost.update_xaxis(tickangle=45)
            fig_cost.update_layout(height=400)
            st.plotly_chart(fig_cost, use_container_width=True)
        
        # Score distribution
        st.subheader("🎯 Match Score Distribution")
        fig_scores = px.scatter(
            df,
            x="rank",
            y="score",
            size="rating",
            color="cost_for_two",
            title="Match Score vs Rank (Size = Rating)",
            labels={
                "score": "Match Score",
                "rank": "Rank",
                "rating": "Rating",
                "cost_for_two": "Cost (₹)"
            }
        )
        fig_scores.update_layout(height=500)
        st.plotly_chart(fig_scores, use_container_width=True)
        
        # Additional insights
        st.subheader("📈 Additional Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_cost = df['cost_for_two'].mean()
            st.metric("Average Cost", f"₹{avg_cost:.0f}")
        
        with col2:
            avg_rating = df['rating'].mean()
            st.metric("Average Rating", f"{avg_rating:.1f}")
        
        with col3:
            avg_score = df['score'].mean()
            st.metric("Average Match Score", f"{avg_score * 100:.1f}%")
    
    def display_empty_state(self):
        """Display empty state when no recommendations are available."""
        st.info("🔍 No recommendations yet. Please submit your preferences to get restaurant recommendations.")
    
    def display_error_state(self, error_message):
        """Display error state when something goes wrong."""
        st.error(f"❌ Error: {error_message}")
        st.info("💡 Please try again or check your preferences.")
    
    def display_loading_state(self):
        """Display loading state while processing."""
        st.info("🤖 AI is analyzing restaurants for you...")
        st.progress(0, text="Processing your preferences...")
    
    def render(self, recommendations_data, preferences, show_charts=False):
        """Render the complete results display."""
        if not recommendations_data:
            self.display_empty_state()
            return
        
        # Display summary metrics
        self.display_summary_metrics(recommendations_data, preferences)
        
        # Display individual recommendations
        self.display_recommendations(recommendations_data)
        
        # Display processing information
        self.display_processing_info(recommendations_data)
        
        # Display charts if requested
        if show_charts:
            self.create_charts(recommendations_data)
