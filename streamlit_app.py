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

def get_demo_recommendations(location="Bellandur"):
    """Get demo recommendations when API is not available."""
    
    # Demo data for different locations
    demo_data = {
        "Bellandur": [
            {
                "rank": 1,
                "restaurant_name": "Paradise Biryani - Bellandur",
                "score": 0.95,
                "rating": 4.5,
                "cost_for_two": 800,
                "location": "Bellandur",
                "cuisines": "North Indian, Chinese",
                "explanation": "Great option in Bellandur with excellent ratings and reasonable prices for medium budget."
            },
            {
                "rank": 2,
                "restaurant_name": "Karnataka Food Corner - Bellandur",
                "score": 0.88,
                "rating": 4.2,
                "cost_for_two": 600,
                "location": "Bellandur",
                "cuisines": "South Indian",
                "explanation": "Good South Indian cuisine with affordable prices and decent ratings."
            },
            {
                "rank": 3,
                "restaurant_name": "The Italian Kitchen - Bellandur",
                "score": 0.82,
                "rating": 4.0,
                "cost_for_two": 900,
                "location": "Bellandur",
                "cuisines": "Continental, Italian",
                "explanation": "Continental and Italian cuisine with good ratings, slightly higher cost."
            }
        ],
        "Indiranagar": [
            {
                "rank": 1,
                "restaurant_name": "Toit - Indiranagar",
                "score": 0.96,
                "rating": 4.6,
                "cost_for_two": 1200,
                "location": "Indiranagar",
                "cuisines": "Brewery, Continental",
                "explanation": "Popular brewery with excellent ambiance and great food in Indiranagar."
            },
            {
                "rank": 2,
                "restaurant_name": "Chai Point - Indiranagar",
                "score": 0.89,
                "rating": 4.3,
                "cost_for_two": 400,
                "location": "Indiranagar",
                "cuisines": "Cafe, Indian",
                "explanation": "Cozy cafe perfect for quick meals and meetings in Indiranagar."
            },
            {
                "rank": 3,
                "restaurant_name": "Fenny's Kitchen - Indiranagar",
                "score": 0.84,
                "rating": 4.1,
                "cost_for_two": 800,
                "location": "Indiranagar",
                "cuisines": "Goan, Seafood",
                "explanation": "Authentic Goan cuisine with fresh seafood options in Indiranagar."
            }
        ],
        "HSR Layout": [
            {
                "rank": 1,
                "restaurant_name": "Brahmin's Coffee Bar - HSR Layout",
                "score": 0.94,
                "rating": 4.4,
                "cost_for_two": 300,
                "location": "HSR Layout",
                "cuisines": "South Indian, Breakfast",
                "explanation": "Traditional South Indian breakfast spot famous for filter coffee in HSR Layout."
            },
            {
                "rank": 2,
                "restaurant_name": "Wang's Kitchen - HSR Layout",
                "score": 0.87,
                "rating": 4.2,
                "cost_for_two": 700,
                "location": "HSR Layout",
                "cuisines": "Chinese, Thai",
                "explanation": "Authentic Asian cuisine with great variety in HSR Layout."
            },
            {
                "rank": 3,
                "restaurant_name": "Fresh Menu - HSR Layout",
                "score": 0.81,
                "rating": 4.0,
                "cost_for_two": 500,
                "location": "HSR Layout",
                "cuisines": "Healthy, Salad",
                "explanation": "Healthy meal options with fresh ingredients in HSR Layout."
            }
        ],
        "Koramangala": [
            {
                "rank": 1,
                "restaurant_name": "Olive Bar & Kitchen - Koramangala",
                "score": 0.97,
                "rating": 4.7,
                "cost_for_two": 1500,
                "location": "Koramangala",
                "cuisines": "Mediterranean, European",
                "explanation": "Upscale dining experience with Mediterranean cuisine in Koramangala."
            },
            {
                "rank": 2,
                "restaurant_name": "Cafe Coffee Day - Koramangala",
                "score": 0.85,
                "rating": 4.0,
                "cost_for_two": 400,
                "location": "Koramangala",
                "cuisines": "Cafe, Beverages",
                "explanation": "Popular coffee chain perfect for casual meetings in Koramangala."
            },
            {
                "rank": 3,
                "restaurant_name": "Truffles - Koramangala",
                "score": 0.83,
                "rating": 3.9,
                "cost_for_two": 600,
                "location": "Koramangala",
                "cuisines": "Continental, Fast Food",
                "explanation": "Fusion cuisine with quick service in Koramangala."
            }
        ],
        "Marathahalli": [
            {
                "rank": 1,
                "restaurant_name": "Meghana Foods - Marathahalli",
                "score": 0.93,
                "rating": 4.3,
                "cost_for_two": 600,
                "location": "Marathahalli",
                "cuisines": "Andhra, Biryani",
                "explanation": "Spicy Andhra cuisine famous for biryani in Marathahalli."
            },
            {
                "rank": 2,
                "restaurant_name": "Absolute Barbecues - Marathahalli",
                "score": 0.86,
                "rating": 4.1,
                "cost_for_two": 1000,
                "location": "Marathahalli",
                "cuisines": "Barbecue, Grill",
                "explanation": "Live barbecue experience with great ambiance in Marathahalli."
            },
            {
                "rank": 3,
                "restaurant_name": "Pizza Hut - Marathahalli",
                "score": 0.80,
                "rating": 3.8,
                "cost_for_two": 500,
                "location": "Marathahalli",
                "cuisines": "Pizza, Italian",
                "explanation": "Popular pizza chain with quick delivery in Marathahalli."
            }
        ]
    }
    
    # Get recommendations for the selected location, fallback to Bellandur
    recommendations = demo_data.get(location, demo_data["Bellandur"])
    
    # Calculate summary
    avg_rating = sum(r["rating"] for r in recommendations) / len(recommendations)
    
    return {
        "status": "success",
        "data": {
            "recommendations": recommendations,
            "summary": {
                "final_recommendations": len(recommendations),
                "avg_rating": round(avg_rating, 2),
                "filtered_candidates": len(recommendations)
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
                    demo_recommendations = get_demo_recommendations(preferences.get("location", "Bellandur"))
                    display_recommendations(demo_recommendations, preferences)
            else:
                # Show demo recommendations
                demo_recommendations = get_demo_recommendations(preferences.get("location", "Bellandur"))
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
