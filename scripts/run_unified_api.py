"""
Unified API Server for Restaurant Recommendation System

This script runs the complete backend API that integrates all phases
into a cohesive RESTful service with modern frontend.
"""

import sys
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from api.main import create_app
from api.config import config


def main():
    """Run the unified API server."""
    print("🚀 Starting Restaurant Recommendation API")
    print(f"📍 Server: http://{config.host}:{config.port}")
    print(f"🔧 Debug Mode: {config.debug}")
    print(f"📊 Data Source: {config.data_path}")
    print(f"🤖 LLM Model: {config.default_model}")
    print()
    print("Available Endpoints:")
    print("  GET  /api/v1/health              - Health check")
    print("  POST /api/v1/recommendations      - Get recommendations (JSON)")
    print("  POST /api/v1/recommendations/web   - Get recommendations (Web UI)")
    print("  GET  /api/v1/locations           - List available locations")
    print("  GET  /api/v1/cuisines            - List available cuisines")
    print("  GET  /api/v1/stats                - Dataset statistics")
    print()
    print("Frontend: http://127.0.0.1:5500/frontend/")
    print("API Docs: http://127.0.0.1:8000/")
    print()
    print("Press CTRL+C to stop the server")

    app = create_app()
    app.run(
        host=config.host,
        port=config.port,
        debug=config.debug
    )


if __name__ == "__main__":
    main()
