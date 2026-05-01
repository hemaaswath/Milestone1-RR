"""
Test Suite for Phase 8 Streamlit App

This test suite verifies the functionality of the Streamlit demo app.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import StreamlitConfig
from components.preference_form import PreferenceForm
from components.results_display import ResultsDisplay

class TestStreamlitConfig(unittest.TestCase):
    """Test cases for StreamlitConfig class."""
    
    def test_api_urls(self):
        """Test API URL generation."""
        health_url = StreamlitConfig.get_api_health_url()
        recommendations_url = StreamlitConfig.get_api_recommendations_url()
        
        self.assertEqual(health_url, "http://127.0.0.1:8000/api/v1/health")
        self.assertEqual(recommendations_url, "http://127.0.0.1:8000/api/v1/recommendations")
    
    def test_default_values(self):
        """Test default configuration values."""
        self.assertEqual(StreamlitConfig.APP_TITLE, "Restaurant Recommendations")
        self.assertEqual(StreamlitConfig.PHASE, "8")
        self.assertEqual(StreamlitConfig.API_TIMEOUT, 30)
    
    def test_development_mode(self):
        """Test development mode detection."""
        # Test with default environment
        self.assertTrue(StreamlitConfig.is_development())

class TestPreferenceForm(unittest.TestCase):
    """Test cases for PreferenceForm component."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.form = PreferenceForm()
    
    def test_init(self):
        """Test PreferenceForm initialization."""
        self.assertIsInstance(self.form, PreferenceForm)
        self.assertIsInstance(self.form.locations, list)
        self.assertIsInstance(self.form.cuisines, list)
    
    def test_get_form_data(self):
        """Test getting form data."""
        data = self.form.get_form_data()
        self.assertIsInstance(data, dict)
        self.assertIn('locations', data)
        self.assertIn('cuisines', data)
    
    @patch('components.preference_form.requests.get')
    def test_load_available_options_success(self, mock_get):
        """Test successful loading of available options."""
        # Mock API response for locations
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "locations": ["Test Location 1", "Test Location 2"]
            }
        }
        mock_get.return_value = mock_response
        
        # Reload options
        self.form.load_available_options()
        
        # Verify locations were loaded
        self.assertEqual(self.form.locations, ["Test Location 1", "Test Location 2"])
    
    @patch('components.preference_form.requests.get')
    def test_load_available_options_failure(self, mock_get):
        """Test failure handling when loading options."""
        # Mock API failure
        mock_get.side_effect = Exception("API Error")
        
        # Reload options
        self.form.load_available_options()
        
        # Verify default options are used
        self.assertEqual(self.form.locations, StreamlitConfig.DEFAULT_LOCATIONS)
        self.assertEqual(self.form.cuisines, StreamlitConfig.DEFAULT_CUISINES)

class TestResultsDisplay(unittest.TestCase):
    """Test cases for ResultsDisplay component."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.display = ResultsDisplay()
        self.sample_recommendations = {
            "status": "success",
            "data": {
                "recommendations": [
                    {
                        "restaurant_name": "Test Restaurant 1",
                        "rank": 1,
                        "score": 0.95,
                        "explanation": "Great test restaurant",
                        "location": "Test Location",
                        "cuisines": "Test Cuisine",
                        "rating": 4.5,
                        "cost_for_two": 800
                    },
                    {
                        "restaurant_name": "Test Restaurant 2",
                        "rank": 2,
                        "score": 0.85,
                        "explanation": "Another great test restaurant",
                        "location": "Test Location",
                        "cuisines": "Test Cuisine",
                        "rating": 4.0,
                        "cost_for_two": 600
                    }
                ],
                "summary": {
                    "total_candidates": 10,
                    "filtered_candidates": 5,
                    "final_recommendations": 2,
                    "avg_rating": 4.25
                }
            },
            "metadata": {
                "pipeline_performance": {
                    "phase3_duration_ms": 150,
                    "phase4_duration_ms": 2500,
                    "total_duration_ms": 2650
                }
            }
        }
    
    def test_init(self):
        """Test ResultsDisplay initialization."""
        self.assertIsInstance(self.display, ResultsDisplay)
    
    def test_create_charts_data(self):
        """Test chart creation with sample data."""
        recommendations = self.sample_recommendations.get("data", {}).get("recommendations", [])
        df = pd.DataFrame(recommendations)
        
        # Verify DataFrame creation
        self.assertEqual(len(df), 2)
        self.assertIn('restaurant_name', df.columns)
        self.assertIn('rating', df.columns)
        self.assertIn('cost_for_two', df.columns)
        self.assertIn('score', df.columns)
    
    def test_empty_recommendations(self):
        """Test handling of empty recommendations."""
        empty_data = {"data": {"recommendations": []}}
        
        # Should not raise an error
        self.display.create_charts(empty_data)
    
    def test_no_recommendations(self):
        """Test handling of no recommendations data."""
        no_data = None
        
        # Should not raise an error
        self.display.create_charts(no_data)

class TestIntegration(unittest.TestCase):
    """Integration tests for the Streamlit app components."""
    
    def test_config_and_form_integration(self):
        """Test integration between config and preference form."""
        config = StreamlitConfig()
        form = PreferenceForm()
        
        # Verify form can access config defaults
        self.assertEqual(len(form.locations), len(config.DEFAULT_LOCATIONS))
        self.assertEqual(len(form.cuisines), len(config.DEFAULT_CUISINES))
    
    def test_results_with_sample_data(self):
        """Test results display with sample data."""
        display = ResultsDisplay()
        sample_data = {
            "status": "success",
            "data": {
                "recommendations": [
                    {
                        "restaurant_name": "Integration Test Restaurant",
                        "rank": 1,
                        "score": 0.95,
                        "explanation": "Perfect for integration testing",
                        "location": "Test City",
                        "cuisines": "Test Cuisine",
                        "rating": 4.8,
                        "cost_for_two": 1000
                    }
                ],
                "summary": {
                    "total_candidates": 5,
                    "filtered_candidates": 3,
                    "final_recommendations": 1,
                    "avg_rating": 4.8
                }
            }
        }
        preferences = {
            "location": "Test City",
            "budget": "medium",
            "cuisine": "Test Cuisine"
        }
        
        # Should not raise an error
        display.render(sample_data, preferences, show_charts=False)

def run_tests():
    """Run all tests and return results."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestStreamlitConfig))
    test_suite.addTest(unittest.makeSuite(TestPreferenceForm))
    test_suite.addTest(unittest.makeSuite(TestResultsDisplay))
    test_suite.addTest(unittest.makeSuite(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result

if __name__ == "__main__":
    print("🧪 Phase 8 Streamlit App Test Suite")
    print("=" * 50)
    
    result = run_tests()
    
    print("\n📊 Test Results Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        for failure in result.failures:
            print(f"FAILURE: {failure[0]}")
            print(f"  {failure[1]}")
        
        for error in result.errors:
            print(f"ERROR: {error[0]}")
            print(f"  {error[1]}")
    
    print("\n🎯 Phase 8 Test Suite Complete!")
