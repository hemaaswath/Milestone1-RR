"""
Preference Form Component for Phase 8 Streamlit App

This component provides the preference input form with Streamlit widgets.
"""

import streamlit as st
import requests
from datetime import datetime
from config import StreamlitConfig

class PreferenceForm:
    """Preference form component for restaurant recommendations."""
    
    def __init__(self):
        self.locations = []
        self.cuisines = []
        self.load_available_options()
    
    def load_available_options(self):
        """Load available locations and cuisines from API."""
        try:
            # Get locations
            response = requests.get(
                StreamlitConfig.get_api_locations_url(), 
                timeout=StreamlitConfig.API_TIMEOUT
            )
            if response.status_code == 200:
                data = response.json()
                self.locations = data.get("data", {}).get("locations", [])
            else:
                self.locations = StreamlitConfig.DEFAULT_LOCATIONS
        except:
            self.locations = StreamlitConfig.DEFAULT_LOCATIONS
        
        try:
            # Get cuisines
            response = requests.get(
                StreamlitConfig.get_api_cuisines_url(), 
                timeout=StreamlitConfig.API_TIMEOUT
            )
            if response.status_code == 200:
                data = response.json()
                self.cuisines = data.get("data", {}).get("cuisines", [])
            else:
                self.cuisines = StreamlitConfig.DEFAULT_CUISINES
        except:
            self.cuisines = StreamlitConfig.DEFAULT_CUISINES
    
    def render(self):
        """Render the preference form."""
        st.header("🔍 Find Your Perfect Restaurant")
        
        # Create columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            location = st.selectbox(
                "📍 Select Location",
                options=self.locations,
                index=0,
                help="Choose your preferred location"
            )
            
            budget = st.selectbox(
                "💰 Budget Range",
                options=StreamlitConfig.DEFAULT_BUDGETS,
                index=1,
                format_func=lambda x: x.capitalize(),
                help="Select your budget preference"
            )
        
        with col2:
            cuisine = st.selectbox(
                "🍽️ Cuisine Preference",
                options=[""] + self.cuisines,
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
            options=StreamlitConfig.DEFAULT_TOP_K_OPTIONS,
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
    
    def get_form_data(self):
        """Get current form data."""
        return {
            "locations": self.locations,
            "cuisines": self.cuisines
        }
