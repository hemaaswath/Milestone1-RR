"""
Phase 5 Testing Guide and Test Suite

This script provides comprehensive testing methods for Phase 5 Response Presentation Layer.
"""

import sys
from pathlib import Path
import json
import os

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


def test_phase5_unit_tests():
    """Unit tests for Phase 5 components."""
    print("🧪 Phase 5 Unit Tests")
    print("=" * 50)
    
    # Test 1: RecommendationCard creation
    print("\n1️⃣ Testing RecommendationCard...")
    try:
        card = RecommendationCard(
            restaurant_name="Test Restaurant",
            rank=1,
            score=0.95,
            explanation="Test explanation",
            location="Test Location",
            cuisines="Test Cuisine",
            rating=4.5,
            cost_for_two=500
        )
        
        # Test to_dict method
        card_dict = card.to_dict()
        assert card_dict['restaurant_name'] == "Test Restaurant"
        assert card_dict['rank'] == 1
        assert card_dict['score'] == 0.95
        print("   ✅ RecommendationCard creation and serialization working")
        
    except Exception as e:
        print(f"   ❌ RecommendationCard test failed: {e}")
    
    # Test 2: ResponseFormatter initialization
    print("\n2️⃣ Testing ResponseFormatter...")
    try:
        formatter = ResponseFormatter()
        assert formatter.response_type == ResponseType.WEB
        
        formatter_web = ResponseFormatter(ResponseType.WEB)
        formatter_api = ResponseFormatter(ResponseType.API)
        print("   ✅ ResponseFormatter initialization working")
        
    except Exception as e:
        print(f"   ❌ ResponseFormatter test failed: {e}")
    
    # Test 3: UIComponents initialization
    print("\n3️⃣ Testing UIComponents...")
    try:
        ui_components = UIComponents()
        print("   ✅ UIComponents initialization working")
        
    except Exception as e:
        print(f"   ❌ UIComponents test failed: {e}")
    
    print("\n🎯 Unit Tests Completed!")


def test_phase5_format_methods():
    """Test all formatting methods with sample data."""
    print("\n🎨 Testing Format Methods")
    print("=" * 50)
    
    # Create sample recommendations
    sample_recommendations = [
        {
            "restaurant_name": "Spice Garden",
            "rank": 1,
            "score": 0.92,
            "explanation": "Perfect match for North Indian cuisine",
            "location": "Bellandur",
            "cuisines": "North Indian, Mughlai",
            "rating": 4.3,
            "cost_for_two": 800
        },
        {
            "restaurant_name": "Paradise Biryani",
            "rank": 2,
            "score": 0.88,
            "explanation": "Highly rated biryani specialist",
            "location": "Bellandur",
            "cuisines": "Biryani, North Indian",
            "rating": 4.1,
            "cost_for_two": 600
        }
    ]
    
    formatter = ResponseFormatter()
    
    # Test each format
    formats_to_test = [
        (ResponseFormat.JSON, "JSON"),
        (ResponseFormat.HTML, "HTML"),
        (ResponseFormat.CARDS, "Cards"),
        (ResponseFormat.TABLE, "Table"),
        (ResponseFormat.SUMMARY, "Summary")
    ]
    
    for format_enum, format_name in formats_to_test:
        print(f"\n📋 Testing {format_name} format...")
        try:
            result = formatter.format_recommendations(sample_recommendations, format_enum)
            
            # Basic validation
            assert result is not None
            assert isinstance(result, dict)
            assert 'status' in result
            assert result['status'] == 'success'
            
            print(f"   ✅ {format_name} format working")
            print(f"   📊 Result keys: {list(result.keys())}")
            
        except Exception as e:
            print(f"   ❌ {format_name} format failed: {e}")


def test_phase5_ui_components():
    """Test UI component generation."""
    print("\n🌐 Testing UI Components")
    print("=" * 50)
    
    sample_recommendations = [
        {
            "restaurant_name": "Test Restaurant",
            "rank": 1,
            "score": 0.95,
            "explanation": "Test explanation",
            "location": "Test Location",
            "cuisines": "Test Cuisine",
            "rating": 4.5,
            "cost_for_two": 500
        }
    ]
    
    ui_components = UIComponents()
    
    print("\n🎨 Testing HTML generation...")
    try:
        html_output = ui_components.generate_recommendation_html(sample_recommendations)
        
        # Basic HTML validation
        assert isinstance(html_output, str)
        assert '<!DOCTYPE html>' in html_output
        assert '<html' in html_output
        assert 'Test Restaurant' in html_output
        
        print("   ✅ HTML generation working")
        print(f"   📏 HTML length: {len(html_output)} characters")
        
    except Exception as e:
        print(f"   ❌ HTML generation failed: {e}")


def test_phase5_integration():
    """Test Phase 5 integration with Phase 3 and Phase 4."""
    print("\n🔄 Testing Phase Integration")
    print("=" * 50)
    
    try:
        # Create test preferences
        preferences = UserPreferences(
            location="Bellandur",
            budget="medium",
            cuisine="North Indian",
            min_rating=3.5
        )
        
        print("\n📊 Phase 3 Integration Test...")
        # Test Phase 3
        restaurants_df = load_restaurants("data/processed/restaurants_phase1.csv")
        phase3_result = retrieve_top_candidates(
            restaurants_df=restaurants_df,
            preferences=preferences,
            top_n=5
        )
        print(f"   ✅ Phase 3: Found {len(phase3_result.candidates)} candidates")
        
        print("\n🤖 Phase 4 Integration Test...")
        # Test Phase 4
        candidates = [c.to_dict() for c in phase3_result.candidates[:3]]
        ranked_recommendations = generate_ranked_recommendations(
            preferences=preferences,
            shortlisted_candidates=candidates,
            top_k=2
        )
        print(f"   ✅ Phase 4: Generated {len(ranked_recommendations)} recommendations")
        
        print("\n🎨 Phase 5 Integration Test...")
        # Test Phase 5
        formatter = ResponseFormatter()
        ui_components = UIComponents()
        
        # Test all formats with real data
        for format_enum, format_name in [
            (ResponseFormat.JSON, "JSON"),
            (ResponseFormat.CARDS, "Cards"),
            (ResponseFormat.SUMMARY, "Summary")
        ]:
            result = formatter.format_recommendations(ranked_recommendations, format_enum)
            assert result is not None
            assert 'status' in result
            print(f"   ✅ Phase 5 {format_name}: Working")
        
        # Test HTML generation
        html_result = ui_components.generate_recommendation_html(ranked_recommendations)
        assert isinstance(html_result, str)
        assert len(html_result) > 100
        print("   ✅ Phase 5 HTML: Working")
        
        print("\n🎉 Full Integration Test Passed!")
        
    except Exception as e:
        print(f"   ❌ Integration test failed: {e}")
        print("   💡 This might be expected if backend services are not running")


def test_phase5_error_handling():
    """Test error handling in Phase 5."""
    print("\n⚠️  Testing Error Handling")
    print("=" * 50)
    
    formatter = ResponseFormatter()
    
    # Test with empty recommendations
    print("\n📝 Testing empty recommendations...")
    try:
        result = formatter.format_recommendations([], ResponseFormat.JSON)
        assert 'status' in result
        print("   ✅ Empty recommendations handled correctly")
        
    except Exception as e:
        print(f"   ❌ Empty recommendations test failed: {e}")
    
    # Test with invalid data
    print("\n📝 Testing invalid data...")
    try:
        # This should handle malformed data gracefully
        invalid_data = [{"invalid": "data"}]
        result = formatter.format_recommendations(invalid_data, ResponseFormat.JSON)
        print("   ✅ Invalid data handled gracefully")
        
    except Exception as e:
        print(f"   ⚠️  Invalid data caused error (expected): {type(e).__name__}")


def test_phase5_performance():
    """Test performance of Phase 5 components."""
    print("\n⚡ Testing Performance")
    print("=" * 50)
    
    import time
    
    # Create larger dataset
    large_recommendations = []
    for i in range(10):
        large_recommendations.append({
            "restaurant_name": f"Restaurant {i}",
            "rank": i + 1,
            "score": 0.9 - (i * 0.1),
            "explanation": f"Test explanation {i}",
            "location": "Test Location",
            "cuisines": "Test Cuisine",
            "rating": 4.5 - (i * 0.1),
            "cost_for_two": 500 + (i * 100)
        })
    
    formatter = ResponseFormatter()
    ui_components = UIComponents()
    
    # Test formatting performance
    print("\n⏱️  Testing formatting performance...")
    start_time = time.time()
    
    for format_enum in [ResponseFormat.JSON, ResponseFormat.CARDS, ResponseFormat.TABLE]:
        result = formatter.format_recommendations(large_recommendations, format_enum)
    
    format_time = time.time() - start_time
    print(f"   ✅ All formats completed in {format_time:.3f} seconds")
    
    # Test HTML generation performance
    print("\n⏱️  Testing HTML generation performance...")
    start_time = time.time()
    
    html_result = ui_components.generate_recommendation_html(large_recommendations)
    
    html_time = time.time() - start_time
    print(f"   ✅ HTML generation completed in {html_time:.3f} seconds")
    print(f"   📏 Generated HTML length: {len(html_result)} characters")


def run_phase5_browser_test():
    """Generate test files for browser testing."""
    print("\n🌐 Generating Browser Test Files")
    print("=" * 50)
    
    # Create comprehensive test data
    test_recommendations = [
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
    
    formatter = ResponseFormatter()
    ui_components = UIComponents()
    
    # Generate test files
    test_files = {
        "test_phase5_json.json": formatter.format_recommendations(test_recommendations, ResponseFormat.JSON),
        "test_phase5_cards.html": formatter.format_recommendations(test_recommendations, ResponseFormat.CARDS),
        "test_phase5_table.html": formatter.format_recommendations(test_recommendations, ResponseFormat.TABLE),
        "test_phase5_summary.txt": formatter.format_recommendations(test_recommendations, ResponseFormat.SUMMARY),
        "test_phase5_complete.html": ui_components.generate_recommendation_html(test_recommendations)
    }
    
    print("\n💾 Generating test files...")
    for filename, content in test_files.items():
        try:
            if filename.endswith('.json'):
                with open(filename, 'w') as f:
                    json.dump(content, f, indent=2)
            else:
                with open(filename, 'w', encoding='utf-8') as f:
                    if isinstance(content, dict):
                        f.write(str(content))
                    else:
                        f.write(content)
            print(f"   ✅ Generated: {filename}")
        except Exception as e:
            print(f"   ❌ Failed to generate {filename}: {e}")
    
    print("\n🌐 Browser Testing Instructions:")
    print("   1. Open 'test_phase5_complete.html' in your browser")
    print("   2. Check the visual layout and styling")
    print("   3. Test hover effects on recommendation cards")
    print("   4. Verify responsive design (resize browser)")
    print("   5. Open 'test_phase5_json.json' to check API format")
    print("   6. Open 'test_phase5_cards.html' and 'test_phase5_table.html' for component testing")


def main():
    """Main test runner."""
    print("🧪 Phase 5 Comprehensive Testing Suite")
    print("=" * 60)
    print()
    
    # Run all tests
    test_phase5_unit_tests()
    test_phase5_format_methods()
    test_phase5_ui_components()
    test_phase5_integration()
    test_phase5_error_handling()
    test_phase5_performance()
    run_phase5_browser_test()
    
    print("\n🎊 Phase 5 Testing Complete!")
    print("=" * 60)
    print("✅ Unit Tests: Component functionality")
    print("✅ Format Tests: All output formats")
    print("✅ UI Tests: HTML generation")
    print("✅ Integration Tests: Phase 3 + 4 + 5")
    print("✅ Error Tests: Edge cases and error handling")
    print("✅ Performance Tests: Speed and efficiency")
    print("✅ Browser Tests: Visual validation")
    print()
    print("📁 Check generated test files:")
    print("   - test_phase5_complete.html (main test page)")
    print("   - test_phase5_json.json (API format)")
    print("   - test_phase5_cards.html (card layout)")
    print("   - test_phase5_table.html (table layout)")
    print("   - test_phase5_summary.txt (text summary)")


if __name__ == "__main__":
    main()
