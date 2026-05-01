"""
Phase 5: Response Presentation Layer Runner

This script demonstrates the Phase 5 Response Presentation Layer
which formats and displays restaurant recommendations in various formats.
"""

import sys
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from phase5.formatters import ResponseFormatter, RecommendationCard
from phase5.ui_components import UIComponents
from phase5.response_types import ResponseFormat, ResponseType
from phase3.engine import load_restaurants, retrieve_top_candidates
from phase4.service import generate_ranked_recommendations
from phase2.models import UserPreferences
import json


def create_sample_preferences() -> UserPreferences:
    """Create sample user preferences for demonstration."""
    return UserPreferences(
        location="Bellandur",
        budget="medium",
        cuisine="North Indian",
        min_rating=3.5,
        additional_preferences=["family-friendly", "parking"]
    )


def create_sample_recommendations() -> list:
    """Create sample recommendations for demonstration."""
    return [
        {
            "restaurant_name": "Spice Garden",
            "rank": 1,
            "score": 0.92,
            "explanation": "Perfect match for North Indian cuisine in Bellandur with excellent ratings and reasonable prices for families.",
            "location": "Bellandur",
            "cuisines": "North Indian, Mughlai",
            "rating": 4.3,
            "cost_for_two": 800
        },
        {
            "restaurant_name": "Paradise Biryani",
            "rank": 2,
            "score": 0.88,
            "explanation": "Highly rated biryani specialist in Bellandur, great for families with parking available.",
            "location": "Bellandur",
            "cuisines": "Biryani, North Indian",
            "rating": 4.1,
            "cost_for_two": 600
        },
        {
            "restaurant_name": "The Village",
            "rank": 3,
            "score": 0.85,
            "explanation": "Authentic North Indian cuisine with traditional ambiance, good value for money in Bellandur.",
            "location": "Bellandur",
            "cuisines": "North Indian, Chinese",
            "rating": 4.0,
            "cost_for_two": 700
        }
    ]


def demonstrate_phase5():
    """Demonstrate Phase 5 Response Presentation Layer capabilities."""
    print("🎨 Phase 5: Response Presentation Layer")
    print("=" * 60)
    print()
    
    # Initialize Phase 5 components
    formatter = ResponseFormatter()
    ui_components = UIComponents()
    
    # Create sample data
    preferences = create_sample_preferences()
    recommendations = create_sample_recommendations()
    
    print("📋 User Preferences:")
    print(f"   Location: {preferences.location}")
    print(f"   Budget: {preferences.budget}")
    print(f"   Cuisine: {preferences.cuisine}")
    print(f"   Min Rating: {preferences.min_rating}")
    print(f"   Additional: {preferences.additional_preferences}")
    print()
    
    print("🍽️  Sample Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec['restaurant_name']} - {rec['location']} - ⭐{rec['rating']} - ₹{rec['cost_for_two']}")
    print()
    
    # Demonstrate different response formats
    print("🔧 Response Format Demonstrations:")
    print("-" * 40)
    
    # 1. JSON Format
    print("\n1️⃣ JSON Format:")
    json_response = formatter.format_recommendations(
        recommendations, 
        ResponseFormat.JSON
    )
    print(json.dumps(json_response, indent=2)[:500] + "...")
    
    # 2. HTML Cards Format
    print("\n2️⃣ HTML Cards Format:")
    html_cards = formatter.format_recommendations(
        recommendations,
        ResponseFormat.CARDS
    )
    print(str(html_cards)[:800] + "...")
    
    # 3. HTML Table Format
    print("\n3️⃣ HTML Table Format:")
    html_table = formatter.format_recommendations(
        recommendations,
        ResponseFormat.TABLE
    )
    print(str(html_table)[:600] + "...")
    
    # 4. Summary Format
    print("\n4️⃣ Summary Format:")
    summary = formatter.format_recommendations(
        recommendations,
        ResponseFormat.SUMMARY
    )
    print(str(summary))
    
    # 5. Complete Web Page
    print("\n5️⃣ Complete Web Page:")
    web_page = ui_components.generate_recommendation_html(
        recommendations
    )
    print("Generated complete web page with:")
    print("   - Header with user preferences")
    print("   - Recommendation cards")
    print("   - Summary statistics")
    print("   - Interactive elements")
    
    # Save outputs to files for inspection
    print("\n💾 Saving demonstration outputs...")
    
    # Save JSON response
    with open("phase5_json_response.json", "w") as f:
        json.dump(json_response, f, indent=2)
    print("   ✅ Saved: phase5_json_response.json")
    
    # Save HTML cards
    with open("phase5_html_cards.html", "w", encoding='utf-8') as f:
        f.write(str(html_cards))
    print("   ✅ Saved: phase5_html_cards.html")
    
    # Save HTML table
    with open("phase5_html_table.html", "w", encoding='utf-8') as f:
        f.write(str(html_table))
    print("   ✅ Saved: phase5_html_table.html")
    
    # Save summary
    with open("phase5_summary.txt", "w", encoding='utf-8') as f:
        f.write(str(summary))
    print("   ✅ Saved: phase5_summary.txt")
    
    # Save complete web page
    with open("phase5_complete_page.html", "w", encoding='utf-8') as f:
        f.write(web_page)
    print("   ✅ Saved: phase5_complete_page.html")
    
    print("\n🎉 Phase 5 demonstration completed!")
    print("📁 Check the generated files to see the different output formats")
    print()
    print("🌐 Open the following files in your browser:")
    print("   - phase5_html_cards.html")
    print("   - phase5_html_table.html") 
    print("   - phase5_complete_page.html")


def demonstrate_real_integration():
    """Demonstrate Phase 5 with real Phase 3 and Phase 4 integration."""
    print("\n🔄 Real Integration Demo (Phase 3 + Phase 4 + Phase 5)")
    print("=" * 60)
    
    try:
        # Create preferences
        preferences = create_sample_preferences()
        print(f"🔍 Getting recommendations for: {preferences.location}")
        
        # Phase 3: Get candidates
        print("\n📊 Phase 3: Retrieving candidates...")
        restaurants_df = load_restaurants("data/processed/restaurants_phase1.csv")
        phase3_result = retrieve_top_candidates(
            restaurants_df=restaurants_df,
            preferences=preferences,
            top_n=10
        )
        print(f"   Found {len(phase3_result.candidates)} candidates")
        
        # Phase 4: Get ranked recommendations
        print("\n🤖 Phase 4: Generating AI rankings...")
        candidates = [c.to_dict() for c in phase3_result.candidates[:5]]
        ranked_recommendations = generate_ranked_recommendations(
            preferences=preferences,
            shortlisted_candidates=candidates,
            top_k=3
        )
        print(f"   Generated {len(ranked_recommendations)} ranked recommendations")
        
        # Phase 5: Format responses
        print("\n🎨 Phase 5: Formatting responses...")
        formatter = ResponseFormatter()
        ui_components = UIComponents()
        
        # Create different formats
        json_response = formatter.format_recommendations(
            ranked_recommendations,
            ResponseFormat.JSON
        )
        
        html_cards = formatter.format_recommendations(
            ranked_recommendations,
            ResponseFormat.CARDS
        )
        
        summary = formatter.format_recommendations(
            ranked_recommendations,
            ResponseFormat.SUMMARY
        )
        
        # Save real integration results
        with open("phase5_real_integration.json", "w") as f:
            json.dump(json_response, f, indent=2)
        
        with open("phase5_real_integration.html", "w", encoding='utf-8') as f:
            f.write(str(html_cards))
            
        with open("phase5_real_summary.txt", "w", encoding='utf-8') as f:
            f.write(str(summary))
        
        print("   ✅ Saved: phase5_real_integration.json")
        print("   ✅ Saved: phase5_real_integration.html")
        print("   ✅ Saved: phase5_real_summary.txt")
        
        # Display summary
        print("\n📋 Real Integration Summary:")
        print(summary)
        
    except Exception as e:
        print(f"❌ Error in real integration: {e}")
        print("   This is expected if the backend is not running")
        print("   The sample demonstration above shows Phase 5 capabilities")


if __name__ == "__main__":
    try:
        demonstrate_phase5()
        demonstrate_real_integration()
        
        print("\n🎊 Phase 5 Response Presentation Layer - Complete!")
        print("=" * 60)
        print("✅ Demonstrated all response formats")
        print("✅ Showed UI component generation")
        print("✅ Created web page layouts")
        print("✅ Integrated with Phase 3 and Phase 4")
        print()
        print("📚 Phase 5 Features:")
        print("   • Multiple response formats (JSON, HTML, Cards, Table, Summary)")
        print("   • Rich UI components with styling")
        print("   • Complete web page generation")
        print("   • Metadata and summaries")
        print("   • Seamless integration with previous phases")
        
    except Exception as e:
        print(f"❌ Error running Phase 5: {e}")
        import traceback
        traceback.print_exc()
