"""
Streamlit App - Simplified Version for Cloud Deployment
This version is optimized for Streamlit Cloud deployment with minimal dependencies.
"""

import streamlit as st
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
        margin-bottom: 1rem;
    }
    .status-indicator {
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        font-weight: bold;
    }
    .status-connected {
        background-color: #10b981;
        color: white;
    }
    .status-demo {
        background-color: #f59e0b;
        color: white;
    }
    .restaurant-card {
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f9fafb;
    }
    .metric-card {
        background-color: #f3f4f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        border: 1px solid #d1d5db;
    }
</style>
""", unsafe_allow_html=True)

def get_api_status():
    """Check if the backend API is available."""
    try:
        api_base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api/v1")
        response = requests.get(f"{api_base_url}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_demo_recommendations():
    """Get demo recommendations when API is not available."""
    return {
        "status": "success",
        "data": {
            "recommendations": [
                {
                    "rank": 1,
                    "restaurant_name": "Test Restaurant 1 - Bellandur",
                    "score": 0.95,
                    "rating": 4.5,
                    "cost_for_two": 800,
                    "location": "Bellandur",
                    "cuisines": "North Indian, Chinese",
                    "explanation": "Great option in Bellandur with excellent ratings and reasonable prices for medium budget."
                },
                {
                    "rank": 2,
                    "restaurant_name": "Test Restaurant 2 - Bellandur",
                    "score": 0.88,
                    "rating": 4.2,
                    "cost_for_two": 600,
                    "location": "Bellandur",
                    "cuisines": "South Indian",
                    "explanation": "Good South Indian cuisine with affordable prices and decent ratings."
                },
                {
                    "rank": 3,
                    "restaurant_name": "Test Restaurant 3 - Bellandur",
                    "score": 0.82,
                    "rating": 4.0,
                    "cost_for_two": 900,
                    "location": "Bellandur",
                    "cuisines "Continental, Italian",
                    "explanation": "Continental and Italian cuisine with good ratings, slightly higher cost."
                }
            ],
            "summary": {
                "final_recommendations": 3,
                "avg_rating": 4.23,
                "filtered_candidates": 3
            }
        },
        "metadata": {
            "source": "demo",
            "timestamp": datetime.now().isoformat()
        }
    }

def get_recommendations_from_api(preferences):
    """Get recommendations from the backend API."""
    try:
        api_base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api/v1")
        response = requests.post(
            f"{api_base_url}/recommendations",
            json=preferences,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def display_header():
    """Display the application header."""
    st.markdown('<h1 class="main-header">🍽️ Restaurant Recommendation System</h1>', unsafe_allow_html=True)
    
    # API Status
    if get_api_status():
        st.markdown('<div class="status-indicator status-connected">🟢 Backend API Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-indicator status-demo">ℹ️ Demo Mode - Showing sample recommendations</div>', unsafe_allow_html=True)

def get_user_preferences():
    """Get user preferences from the form."""
    st.header("🎯 Your Preferences")
    
    # Sample data for demo
    locations = ["Bellandur", "HSR Layout", "Koramangala", "Indiranagar", "Marathahalli"]
    cuisines = ["North Indian", "South Indian", "Chinese", "Continental", "Italian", "Thai", "Mexican"]
    
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
    if st.button("🚀 Get Recommendations", type="primary"):
        preferences = {
            "location": location,
            "budget": budget,
            "cuisine": cuisine if cuisine else None,
            "min_rating": min_rating,
            "top_k": top_k,
            "additional_preferences": additional_text
        }
        return preferences
    
    return None

def display_recommendations(recommendations_data, preferences):
    """Display restaurant recommendations."""
    if not recommendations_data:
        st.error("No recommendations available")
        return
    
    recommendations = recommendations_data.get("data", {}).get("recommendations", [])
    summary = recommendations_data.get("data", {}).get("summary", {})
    metadata = recommendations_data.get("metadata", {})
    
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
            # Restaurant header with badges
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"🍽️ {restaurant.get('restaurant_name', 'Unknown Restaurant')}")
            with col2:
                st.markdown(f"""
                <div style="display: flex; gap: 0.5rem; justify-content: flex-end; margin-top: 1rem;">
                    <span style="background: #3b82f6; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-weight: bold; font-size: 0.875rem;">#{restaurant.get('rank', 1)}</span>
                    <span style="background: #10b981; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-weight: bold; font-size: 0.875rem;">{restaurant.get('score', 0) * 100:.0f}% Match</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Restaurant details
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"📍 **Location:** {restaurant.get('location', 'Unknown')}")
                st.write(f"🍽️ **Cuisine:** {restaurant.get('cuisines', 'Various')}")
            with col2:
                st.write(f"⭐ **Rating:** {restaurant.get('rating', 0)}/5")
                st.write(f"💰 **Cost for Two:** ₹{restaurant.get('cost_for_two', 0):,}")
            
            # Explanation
            with st.expander("💡 Why we recommend this restaurant", expanded=True):
                st.write(restaurant.get('explanation', 'Great match for your preferences'))
            
            st.divider()
    
    # Display metadata if available
    if metadata:
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

def main():
    """Main application function."""
    # Display header
    display_header()
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        **Restaurant Recommendation System**
        
        This is a demo app for:
        - 🎓 Course demonstrations
        - 👥 Stakeholder previews
        - 🚀 Quick sharing
        
        **Features:**
        - ✅ Single process deployment
        - ✅ Beautiful UI with cards
        - ✅ Demo mode when API offline
        - ✅ Mobile responsive design
        """)
        
        st.header("📊 Status")
        if get_api_status():
            st.success("🟢 API Connected")
        else:
            st.warning("ℹ️ Demo Mode")
    
    # Get user preferences
    preferences = get_user_preferences()
    
    if preferences:
        # Show loading spinner
        with st.spinner("🤖 Finding the perfect restaurants for you..."):
            time.sleep(1)  # Simulate processing
            
            # Try to get recommendations from API, fallback to demo
            if get_api_status():
                recommendations = get_recommendations_from_api(preferences)
                if recommendations:
                    display_recommendations(recommendations, preferences)
                else:
                    st.warning("API request failed, showing demo data")
                    demo_recommendations = get_demo_recommendations()
                    display_recommendations(demo_recommendations, preferences)
            else:
                # Show demo recommendations
                demo_recommendations = get_demo_recommendations()
                display_recommendations(demo_recommendations, preferences)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6b7280; margin-top: 2rem;'>
        <p>🍽️ Restaurant Recommendation System | Phase 8 Demo</p>
        <p>Built with Streamlit | Deployed on Cloud</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
