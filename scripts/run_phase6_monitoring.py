"""
Phase 6 Monitoring and Continuous Improvement Runner

This script runs the complete restaurant recommendation system
with Phase 6 monitoring, analytics, and improvement capabilities.
"""

import sys
import time
import threading
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from api.main import create_app
from api.config import config
from phase6.monitoring import SystemMonitor
from phase6.analytics import AnalyticsEngine
from phase6.feedback import FeedbackCollector
from phase6.improvement import ModelOptimizer, DataRefresher


def main():
    """Run the complete system with Phase 6 monitoring."""
    print("🚀 Starting Restaurant Recommendation System with Phase 6 Monitoring")
    print(f"📍 API Server: http://{config.host}:{config.port}")
    print(f"🔧 Debug Mode: {config.debug}")
    print(f"📊 Data Source: {config.data_path}")
    print(f"🤖 LLM Model: {config.default_model}")
    print()
    print("📈 Phase 6 Features Enabled:")
    print("  ✅ Real-time System Monitoring")
    print("  ✅ User Behavior Analytics") 
    print("  ✅ Feedback Collection & Analysis")
    print("  ✅ Model Performance Optimization")
    print("  ✅ Data Freshness Monitoring")
    print("  ✅ Continuous Improvement Pipeline")
    print()
    print("🔗 Available Endpoints:")
    print("  API Endpoints:")
    print("    GET  /api/v1/health              - Health check")
    print("    POST /api/v1/recommendations      - Get recommendations (JSON)")
    print("    POST /api/v1/recommendations/web   - Get recommendations (Web UI)")
    print("    GET  /api/v1/locations           - List available locations")
    print("    GET  /api/v1/cuisines            - List available cuisines")
    print("    GET  /api/v1/stats                - Dataset statistics")
    print()
    print("  Monitoring Endpoints:")
    print("    GET  /api/v1/monitoring/health      - System health status")
    print("    GET  /api/v1/monitoring/metrics     - System performance metrics")
    print("    GET  /api/v1/monitoring/performance - Endpoint performance stats")
    print("    GET  /api/v1/analytics/user-behavior - User behavior analytics")
    print("    GET  /api/v1/analytics/recommendations - Recommendation analytics")
    print("    GET  /api/v1/analytics/business-insights - Business intelligence")
    print("    POST /api/v1/feedback/collect     - Collect user feedback")
    print("    GET  /api/v1/feedback/analyze       - Analyze feedback")
    print("    POST /api/v1/improvement/evaluate-model - Evaluate model performance")
    print("    POST /api/v1/improvement/optimize-prompt - Optimize prompts")
    print("    POST /api/v1/improvement/run-ab-test - Run A/B tests")
    print("    GET  /api/v1/improvement/check-data   - Check data freshness")
    print("    POST /api/v1/improvement/refresh-data - Refresh data")
    print("    GET  /api/v1/reports/export          - Export monitoring reports")
    print()
    print("🌐 Frontend: http://127.0.0.1:5500/frontend/")
    print("📊 Monitoring Dashboard: http://127.0.0.1:8000/api/v1/monitoring/health")
    print("📈 Analytics Dashboard: http://127.0.0.1:8000/api/v1/analytics/user-behavior")
    print()
    print("Press CTRL+C to stop the server")
    
    # Initialize Phase 6 components
    system_monitor = SystemMonitor()
    analytics_engine = AnalyticsEngine()
    feedback_collector = FeedbackCollector()
    model_optimizer = ModelOptimizer()
    data_refresher = DataRefresher()
    
    # Start background monitoring tasks
    def start_monitoring_tasks():
        """Start background monitoring and improvement tasks."""
        print("🔄 Starting background monitoring tasks...")
        
        while True:
            try:
                # Collect system metrics
                metrics = system_monitor.collect_system_metrics()
                
                # Check if system needs attention
                if metrics.cpu_percent > 80 or metrics.memory_percent > 85:
                    print(f"⚠️  System Alert: High CPU ({metrics.cpu_percent:.1f}%) or Memory ({metrics.memory_percent:.1f}%)")
                
                # Check error rate
                if metrics.error_rate > 5:
                    print(f"🚨  Error Rate Alert: {metrics.error_rate:.1f}% error rate")
                
                # Save metrics periodically
                system_monitor.export_metrics()
                
                # Check data freshness every hour
                freshness_status = data_refresher.check_data_freshness()
                if freshness_status.get('needs_refresh'):
                    print("📊 Data refresh recommended")
                
                time.sleep(60)  # Check every minute
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping monitoring tasks...")
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(60)  # Continue monitoring even if error occurs
    
    # Create and configure app
    app = create_app()
    
    # Start monitoring in background thread
    monitoring_thread = threading.Thread(target=start_monitoring_tasks, daemon=True)
    monitoring_thread.start()
    
    try:
        # Run the main Flask app
        app.run(
            host=config.host,
            port=config.port,
            debug=config.debug,
            use_reloader=False  # Important when running background threads
        )
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Restaurant Recommendation System...")
    finally:
        print("✅ System stopped gracefully")


if __name__ == "__main__":
    main()
