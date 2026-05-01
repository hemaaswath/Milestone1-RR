"""
Phase 6: Backend HTTP API Runner

This script runs the Phase 6 Backend HTTP API service that provides
a secure, scalable HTTP service orchestrating the recommendation pipeline.
"""

import sys
import os
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Load environment variables from .env file
env_file = PROJECT_ROOT / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

def check_phase6_prerequisites():
    """Check Phase 6 prerequisites."""
    print("🔍 Checking Phase 6 prerequisites...")
    
    # Check environment variables
    required_env_vars = ['GROQ_API_KEY']
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("   Please set these in your .env file or environment")
        return False
    
    # Check data files
    data_path = os.getenv("DATA_PATH", "data/processed/restaurants_phase1.csv")
    if not os.path.exists(data_path):
        print(f"❌ Data file not found: {data_path}")
        print("   Please run Phase 1 to generate the processed data")
        return False
    
    print("✅ Phase 6 prerequisites met")
    return True


def run_phase6_api():
    """Run the Phase 6 Backend HTTP API."""
    try:
        from api.phase6_main import run_phase6_server
        run_phase6_server()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Please ensure all dependencies are installed:")
        print("   pip install flask flask-cors")
        return False
    except Exception as e:
        print(f"❌ Error running Phase 6 API: {e}")
        return False


def test_phase6_endpoints():
    """Test Phase 6 API endpoints."""
    import requests
    import json
    
    base_url = "http://127.0.0.1:8000"
    
    print("\n🧪 Testing Phase 6 API endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"⚠️  Health endpoint returned: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Health endpoint test failed: {e}")
        return False
    
    # Test meta endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/meta", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Meta endpoint working")
            print(f"   API Version: {data.get('data', {}).get('api_version', 'unknown')}")
            print(f"   Available locations: {len(data.get('data', {}).get('available_locations', []))}")
        else:
            print(f"⚠️  Meta endpoint returned: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Meta endpoint test failed: {e}")
    
    # Test recommendations endpoint
    try:
        test_payload = {
            "location": "Bellandur",
            "budget": "medium",
            "cuisine": "North Indian",
            "min_rating": 3.5,
            "top_k": 3
        }
        
        response = requests.post(
            f"{base_url}/api/v1/recommendations",
            json=test_payload,
            timeout=30  # Longer timeout for LLM processing
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Recommendations endpoint working")
            print(f"   Status: {data.get('status', 'unknown')}")
            if data.get('data') and data['data'].get('recommendations'):
                print(f"   Recommendations returned: {len(data['data']['recommendations'])}")
        else:
            print(f"⚠️  Recommendations endpoint returned: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Recommendations endpoint test failed: {e}")
    
    return True


def show_phase6_info():
    """Show Phase 6 API information."""
    print("\n📚 Phase 6 Backend HTTP API Information")
    print("=" * 60)
    print()
    print("🎯 Phase 6 Goal:")
    print("   Provide a secure, scalable HTTP service that orchestrates")
    print("   the recommendation pipeline while keeping server-side secrets secure.")
    print()
    print("🔐 Security Features:")
    print("   • Server-side secret management (GROQ_API_KEY)")
    print("   • CORS configuration")
    print("   • Rate limiting (60 requests/minute)")
    print("   • Input validation and sanitization")
    print("   • Request size limits (1MB max)")
    print()
    print("📊 Telemetry Features:")
    print("   • Structured JSON logging")
    print("   • Performance tracking (Phase 1-5 timing)")
    print("   • Error monitoring")
    print("   • Token usage tracking")
    print()
    print("🔗 Main Endpoints:")
    print("   • POST /api/v1/recommendations - Main recommendation endpoint")
    print("   • GET  /api/v1/health - Service health check")
    print("   • GET  /api/v1/meta - API metadata and hints")
    print("   • POST /api/v1/recommendations/web - Web interface")
    print("   • GET  /api/v1/locations - Available locations")
    print("   • GET  /api/v1/cuisines - Available cuisines")
    print("   • GET  /api/v1/stats - Dataset statistics")
    print()
    print("🚀 Usage:")
    print("   1. Start the API server")
    print("   2. Frontend calls POST /api/v1/recommendations")
    print("   3. API orchestrates Phase 1-5 pipeline")
    print("   4. Returns structured JSON response")
    print()
    print("📋 Contract:")
    print("   • Input: User preferences (location, budget, cuisine, rating, etc.)")
    print("   • Output: Ranked recommendations with explanations and metadata")
    print("   • Format: Stable JSON with status, data, and telemetry fields")
    print()


def main():
    """Main Phase 6 runner."""
    print("🚀 Phase 6: Backend HTTP API")
    print("=" * 60)
    
    # Show Phase 6 information
    show_phase6_info()
    
    # Check prerequisites
    if not check_phase6_prerequisites():
        print("\n❌ Phase 6 prerequisites not met. Please fix the issues above.")
        return
    
    print("\n✅ Starting Phase 6 Backend HTTP API...")
    print("   Press Ctrl+C to stop the server")
    print()
    
    # Run the API server
    run_phase6_api()


if __name__ == "__main__":
    main()
