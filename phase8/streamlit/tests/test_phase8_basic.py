"""
Basic Test Suite for Phase 8 Streamlit App

This test suite verifies the basic functionality of Phase 8 components
without requiring Streamlit to be installed.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestPhase8Basic(unittest.TestCase):
    """Basic test cases for Phase 8 components."""
    
    def test_config_import(self):
        """Test that config can be imported."""
        try:
            from config import StreamlitConfig
            self.assertIsNotNone(StreamlitConfig)
            self.assertEqual(StreamlitConfig.APP_TITLE, "Restaurant Recommendations")
            self.assertEqual(StreamlitConfig.PHASE, "8")
        except ImportError as e:
            self.fail(f"Could not import StreamlitConfig: {e}")
    
    def test_config_api_urls(self):
        """Test API URL generation."""
        try:
            from config import StreamlitConfig
            health_url = StreamlitConfig.get_api_health_url()
            recommendations_url = StreamlitConfig.get_api_recommendations_url()
            
            self.assertEqual(health_url, "http://127.0.0.1:8000/api/v1/health")
            self.assertEqual(recommendations_url, "http://127.0.0.1:8000/api/v1/recommendations")
        except ImportError as e:
            self.fail(f"Could not import StreamlitConfig: {e}")
    
    def test_default_values(self):
        """Test default configuration values."""
        try:
            from config import StreamlitConfig
            self.assertEqual(StreamlitConfig.DEFAULT_LOCATIONS, ["Bellandur", "Delhi", "Mumbai", "Bangalore", "Hyderabad"])
            self.assertEqual(StreamlitConfig.DEFAULT_CUISINES, ["North Indian", "Chinese", "Italian", "South Indian", "Continental"])
            self.assertEqual(StreamlitConfig.DEFAULT_BUDGETS, ["low", "medium", "high"])
        except ImportError as e:
            self.fail(f"Could not import StreamlitConfig: {e}")
    
    def test_file_structure(self):
        """Test that required files exist."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        required_files = [
            "app.py",
            "config.py",
            "requirements.txt",
            "README.md"
        ]
        
        for file in required_files:
            file_path = os.path.join(base_dir, file)
            self.assertTrue(os.path.exists(file_path), f"Required file {file} does not exist")
    
    def test_requirements_file(self):
        """Test that requirements.txt contains required packages."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        requirements_file = os.path.join(base_dir, "requirements.txt")
        
        with open(requirements_file, 'r') as f:
            requirements_content = f.read()
        
        required_packages = ["streamlit", "pandas", "plotly", "requests", "python-dotenv"]
        
        for package in required_packages:
            self.assertIn(package, requirements_content, f"Required package {package} not in requirements.txt")
    
    def test_readme_content(self):
        """Test that README.md contains required information."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        readme_file = os.path.join(base_dir, "README.md")
        
        with open(readme_file, 'r') as f:
            readme_content = f.read()
        
        required_sections = [
            "Phase 8: Streamlit Deployment",
            "Overview",
            "Architecture",
            "Features",
            "Exit Criteria",
            "Technology Stack"
        ]
        
        for section in required_sections:
            self.assertIn(section, readme_content, f"Required section {section} not in README.md")
    
    def test_app_file_structure(self):
        """Test that app.py has the required structure."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        app_file = os.path.join(base_dir, "app.py")
        
        with open(app_file, 'r') as f:
            app_content = f.read()
        
        required_functions = [
            "check_api_health",
            "get_recommendations",
            "display_header",
            "display_preference_form",
            "display_recommendations",
            "main"
        ]
        
        for function in required_functions:
            self.assertIn(f"def {function}", app_content, f"Required function {function} not in app.py")
    
    def test_deployment_files(self):
        """Test that deployment files exist and have correct structure."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        deployment_dir = os.path.join(base_dir, "deployment")
        
        self.assertTrue(os.path.exists(deployment_dir), "Deployment directory does not exist")
        
        deployment_files = [
            "streamlit_app.py",
            "requirements.txt"
        ]
        
        for file in deployment_files:
            file_path = os.path.join(deployment_dir, file)
            self.assertTrue(os.path.exists(file_path), f"Deployment file {file} does not exist")

def run_basic_tests():
    """Run basic tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPhase8Basic)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result

if __name__ == "__main__":
    print("🧪 Phase 8 Basic Test Suite")
    print("=" * 50)
    
    result = run_basic_tests()
    
    print("\n📊 Test Results Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.wasSuccessful():
        print("\n✅ All basic tests passed!")
        print("🎯 Phase 8 structure and configuration verified!")
    else:
        print("\n❌ Some tests failed!")
        for failure in result.failures:
            print(f"FAILURE: {failure[0]}")
            print(f"  {failure[1]}")
        
        for error in result.errors:
            print(f"ERROR: {error[0]}")
            print(f"  {error[1]}")
    
    print("\n🎯 Phase 8 Basic Test Suite Complete!")
