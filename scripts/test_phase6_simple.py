"""
Simple Phase 6 API Test

This script creates a minimal Phase 6 API to test the core functionality
without the complex integration issues.
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

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

def create_simple_phase6_app():
    """Create a simple Phase 6 API for testing."""
    
    app = Flask(__name__)
    
    # Basic CORS
    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
    
    @app.route('/')
    def index():
        return {
            "message": "Phase 6 Backend HTTP API - Simple Test",
            "version": "1.0.0",
            "phase": "6",
            "timestamp": datetime.now().isoformat()
        }
    
    @app.route('/api/v1/health')
    def health():
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "phase": "6"
        }
    
    @app.route('/api/v1/meta')
    def meta():
        return {
            "status": "success",
            "data": {
                "api_version": "1.0.0",
                "phase": "6",
                "available_locations": ["Bellandur", "Delhi", "Mumbai"],
                "available_cuisines": ["North Indian", "Chinese", "Italian"],
                "budget_options": ["low", "medium", "high"]
            }
        }
    
    @app.route('/api/v1/recommendations', methods=['POST'])
    def recommendations():
        try:
            data = request.get_json() or {}
            
            # Basic validation
            if not data.get('location'):
                return jsonify({
                    "status": "error",
                    "message": "Location is required"
                }), 400
            
            # Mock recommendation response
            return jsonify({
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "recommendations": [
                        {
                            "restaurant_name": "Test Restaurant 1",
                            "rank": 1,
                            "score": 0.95,
                            "explanation": "Great match for your preferences",
                            "location": data.get('location', 'Unknown'),
                            "cuisines": "North Indian",
                            "rating": 4.5,
                            "cost_for_two": 800
                        },
                        {
                            "restaurant_name": "Test Restaurant 2",
                            "rank": 2,
                            "score": 0.88,
                            "explanation": "Good alternative option",
                            "location": data.get('location', 'Unknown'),
                            "cuisines": "Chinese",
                            "rating": 4.2,
                            "cost_for_two": 600
                        }
                    ]
                },
                "metadata": {
                    "total_candidates": 10,
                    "filtered_candidates": 5,
                    "final_recommendations": 2
                }
            })
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Error: {str(e)}"
            }), 500
    
    return app

def main():
    """Run the simple Phase 6 API test."""
    print("🧪 Simple Phase 6 API Test")
    print("=" * 40)
    
    # Check prerequisites
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️  GROQ_API_KEY not found, but continuing with simple test")
    
    print("✅ Starting simple Phase 6 API test...")
    print("   Server: http://127.0.0.1:8000")
    print("   Press Ctrl+C to stop")
    print()
    
    app = create_simple_phase6_app()
    
    try:
        app.run(host="127.0.0.1", port=8000, debug=True)
    except KeyboardInterrupt:
        print("\n🛑 Simple API test stopped")

if __name__ == "__main__":
    main()
