"""
Phase 8 Streamlit Deployment App

Production-ready Streamlit app for easy deployment on Streamlit Cloud.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Restaurant Recommendations",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .restaurant-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .rank-badge {
        background: #3b82f6;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.875rem;
    }
    .score-badge {
        background: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.875rem;
    }
    .explanation-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 5px 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api/v1")

# Session state for storing recommendations
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'last_search' not in st.session_state:
    st.session_state.last_search = None

def check_api_health():
    """Check if the backend API is healthy."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_available_locations():
    """Get available locations from API."""
    try:
        response = requests.get(f"{API_BASE_URL}/locations", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("locations", [])
    except:
        return ["Bellandur", "Delhi", "Mumbai", "Bangalore", "Hyderabad"]

def get_available_cuisines():
    """Get available cuisines from API."""
    try:
        response = requests.get(f"{API_BASE_URL}/cuisines", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("cuisines", [])
    except:
        return ["North Indian", "Chinese", "Italian", "South Indian", "Continental"]

def get_recommendations(preferences):
    """Get restaurant recommendations from API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/recommendations",
            json=preferences,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def create_demo_recommendations(preferences):
    """Create demo recommendations for deployment."""
    location = preferences.get("location", "Unknown")
    budget = preferences.get("budget", "medium")
    cuisine = preferences.get("cuisine", "Various")
    top_k = preferences.get("top_k", 3)
    
    recommendations = []
    for i in range(top_k):
        recommendations.append({
            "restaurant_name": f"Demo Restaurant {i+1} - {location}",
            "rank": i + 1,
            "score": 0.95 - (i * 0.1),
            "explanation": f"This is a demo restaurant in {location} offering {cuisine} cuisine. Perfect for {budget} budget with excellent ratings and great service. Great for families and couples.",
            "location": location,
            "cuisines": cuisine,
            "rating": 4.5 - (i * 0.1),
            "cost_for_two": 800 if budget == "medium" else (500 if budget == "low" else 1200)
        })
    
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "data": {
            "recommendations": recommendations,
            "summary": {
                "total_candidates": 10,
                "filtered_candidates": 5,
                "final_recommendations": len(recommendations),
                "avg_rating": 4.2
            }
        },
        "metadata": {
            "source": "demo",
            "message": "Demo data for Streamlit Cloud deployment"
        }
    }

def display_header():
    """Display the application header."""
    st.markdown('<div class="main-header">🍽️ Restaurant Recommendations</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Phase 8: Streamlit Demo App - Fast Sharing Platform</div>', unsafe_allow_html=True)
    
    # API Status
    api_healthy = check_api_health()
    if api_healthy:
        st.success("🟢 Backend API Connected")
    else:
        st.info("ℹ️ Demo Mode - Showing sample recommendations")

def display_preference_form():
    """Display the preference input form."""
    st.header("🔍 Find Your Perfect Restaurant")
    
    # Get available options
    locations = get_available_locations()
    cuisines = get_available_cuisines()
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        location = st.selectbox(
            "📍 Select Location",
            options=locations,
            index=0,
            help="Choose your preferred location"
        )
        
        budget = st.selectbox(
            "💰 Budget Range",
            options=["low", "medium", "high"],
            index=1,
            format_func=lambda x: x.capitalize(),
            help="Select your budget preference"
        )
    
    with col2:
        cuisine = st.selectbox(
            "🍽️ Cuisine Preference",
            options=[""] + cuisines,
            index=0,
            format_func=lambda x: x if x else "Any Cuisine",
            help="Choose your preferred cuisine (optional)"
        )
        
        min_rating = st.slider(
            "⭐ Minimum Rating",
            min_value=1.0,
            max_value=5.0,
            value=3.0,
            step=0.5,
            help="Minimum restaurant rating"
        )
    
    # Number of recommendations
    top_k = st.selectbox(
        "📊 Number of Recommendations",
        options=[3, 5, 7, 10],
        index=1,
        help="How many recommendations would you like?"
    )
    
    # Additional preferences
    additional_text = st.text_area(
        "💬 Additional Preferences (Optional)",
        placeholder="e.g., family-friendly, outdoor seating, parking available, good for dates...",
        help="Add any specific requirements or preferences"
    )
    
    # Submit button
    submit_button = st.button(
        "🚀 Get Recommendations",
        type="primary",
        use_container_width=True,
        help="Click to get restaurant recommendations based on your preferences"
    )
    
    return submit_button, {
        "location": location,
        "budget": budget,
        "cuisine": cuisine,
        "minRating": min_rating,
        "top_k": top_k,
        "additionalPreferences": additional_text
    }

def display_recommendations(recommendations_data, preferences):
    """Display restaurant recommendations with beautiful UI."""
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
    
    # Display individual recommendations
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

def create_charts(recommendations_data):
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

def main():
    """Main application function."""
    # Display header
    display_header()
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        **Phase 8: Streamlit Demo App**
        
        This is a fast-sharing demo app for:
        - 🎓 Course demonstrations
        - 👥 Stakeholder previews
        - 🚀 Quick sharing
        
        **Features:**
        - ✅ Single process deployment
        - ✅ Beautiful UI with charts
        - ✅ Real-time recommendations
        - ✅ Server-side secret management
        """)
        
        st.header("🔧 System Status")
        
        api_healthy = check_api_health()
        if api_healthy:
            st.success("🟢 API Connected")
            st.caption("Backend API is healthy")
        else:
            st.info("ℹ️ Demo Mode")
            st.caption("Showing demo data")
        
        st.header("📊 Quick Stats")
        if st.session_state.recommendations:
            recs = st.session_state.recommendations.get("data", {}).get("recommendations", [])
            if recs:
                st.metric("Last Search", f"{len(recs)} results")
                st.metric("Avg Rating", f"{pd.DataFrame(recs)['rating'].mean():.1f}")
                st.metric("Avg Cost", f"₹{pd.DataFrame(recs)['cost_for_two'].mean():.0f}")
        else:
            st.metric("Searches", "0")
            st.metric("Results", "0")
            st.metric("Avg Rating", "0.0")
    
    # Main content area
    tab1, tab2 = st.tabs(["🔍 Find Restaurants", "📊 Analytics"])
    
    with tab1:
        # Preference form
        submit_button, preferences = display_preference_form()
        
        if submit_button:
            # Show loading state
            with st.spinner("🤖 AI is analyzing restaurants for you..."):
                time.sleep(1)  # Simulate processing time
                
                # Get recommendations
                recommendations_data = get_recommendations(preferences)
                
                if not recommendations_data:
                    # Use demo data for deployment
                    recommendations_data = create_demo_recommendations(preferences)
                
                # Store in session state
                st.session_state.recommendations = recommendations_data
                st.session_state.last_search = {
                    "preferences": preferences,
                    "timestamp": datetime.now().isoformat()
                }
        
        # Display recommendations
        if st.session_state.recommendations:
            display_recommendations(st.session_state.recommendations, preferences)
    
    with tab2:
        if st.session_state.recommendations:
            create_charts(st.session_state.recommendations)
        else:
            st.info("📊 No data available. Please search for restaurants first.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.875rem;">
        Phase 8 Streamlit Demo App • Restaurant Recommendation System
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
