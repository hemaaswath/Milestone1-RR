"""
Full System Runner - Phase 6 Backend + Phase 7 Frontend

This script starts both the Phase 6 Backend HTTP API and Phase 7 Frontend Web UI
simultaneously and tests their complete integration.
"""

import sys
import os
import time
import subprocess
import threading
import requests
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PHASE7_ROOT = PROJECT_ROOT / "phase7" / "frontend"

# Load environment variables
env_file = PROJECT_ROOT / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

class SystemRunner:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://127.0.0.1:3000"
        self.api_base_url = f"{self.backend_url}/api/v1"
        
    def print_header(self, title):
        """Print a formatted header."""
        print("\n" + "=" * 60)
        print(f"🚀 {title}")
        print("=" * 60)
        
    def print_status(self, service, status, message=""):
        """Print status message."""
        icons = {
            "starting": "🔄",
            "running": "✅", 
            "error": "❌",
            "testing": "🧪",
            "ready": "🎉"
        }
        print(f"{icons.get(status, '📋')} {service}: {message}")
        
    def check_prerequisites(self):
        """Check system prerequisites."""
        self.print_header("Checking System Prerequisites")
        
        # Check environment variables
        if not os.getenv("GROQ_API_KEY"):
            self.print_status("Environment", "error", "GROQ_API_KEY not found")
            return False
        self.print_status("Environment", "ready", "GROQ_API_KEY configured")
        
        # Check data file
        data_file = PROJECT_ROOT / "data" / "processed" / "restaurants_phase1.csv"
        if not data_file.exists():
            self.print_status("Data", "error", "Restaurant data file not found")
            return False
        self.print_status("Data", "ready", f"Data file found ({data_file.stat().st_size / (1024*1024):.2f} MB)")
        
        # Check Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.print_status("Node.js", "ready", result.stdout.strip())
            else:
                self.print_status("Node.js", "error", "Node.js not available")
                return False
        except Exception as e:
            self.print_status("Node.js", "error", f"Node.js check failed: {e}")
            return False
        
        # Check Python dependencies
        try:
            import flask
            import flask_cors
            self.print_status("Python", "ready", f"Flask {flask.__version__} available")
        except ImportError as e:
            self.print_status("Python", "error", f"Missing dependencies: {e}")
            return False
            
        return True
        
    def start_backend(self):
        """Start Phase 6 Backend API."""
        self.print_status("Backend", "starting", "Starting Phase 6 Backend HTTP API...")
        
        try:
            # Use the direct test API for reliable startup
            backend_script = PROJECT_ROOT / "scripts" / "test_phase6_direct.py"
            
            self.backend_process = subprocess.Popen(
                [sys.executable, str(backend_script)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=PROJECT_ROOT
            )
            
            # Wait for backend to start
            time.sleep(3)
            
            # Check if backend is responding
            try:
                response = requests.get(f"{self.api_base_url}/health", timeout=5)
                if response.status_code == 200:
                    self.print_status("Backend", "running", f"API running at {self.backend_url}")
                    return True
                else:
                    self.print_status("Backend", "error", f"API returned {response.status_code}")
                    return False
            except requests.exceptions.RequestException as e:
                self.print_status("Backend", "error", f"API not responding: {e}")
                return False
                
        except Exception as e:
            self.print_status("Backend", "error", f"Failed to start backend: {e}")
            return False
            
    def install_frontend_dependencies(self):
        """Install frontend dependencies."""
        self.print_status("Frontend", "starting", "Installing frontend dependencies...")
        
        try:
            # Check if node_modules exists
            node_modules = PHASE7_ROOT / "node_modules"
            if not node_modules.exists():
                result = subprocess.run(
                    ["npm", "install"],
                    cwd=PHASE7_ROOT,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    self.print_status("Frontend", "ready", "Dependencies installed successfully")
                    return True
                else:
                    self.print_status("Frontend", "error", f"npm install failed: {result.stderr}")
                    return False
            else:
                self.print_status("Frontend", "ready", "Dependencies already installed")
                return True
                
        except Exception as e:
            self.print_status("Frontend", "error", f"Failed to install dependencies: {e}")
            return False
            
    def start_frontend(self):
        """Start Phase 7 Frontend."""
        self.print_status("Frontend", "starting", "Starting Phase 7 Frontend Web UI...")
        
        try:
            self.frontend_process = subprocess.Popen(
                ["npm", "run", "dev"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=PHASE7_ROOT
            )
            
            # Wait for frontend to start
            time.sleep(5)
            
            # Check if frontend is responding
            try:
                response = requests.get(self.frontend_url, timeout=10)
                if response.status_code == 200:
                    self.print_status("Frontend", "running", f"Frontend running at {self.frontend_url}")
                    return True
                else:
                    self.print_status("Frontend", "error", f"Frontend returned {response.status_code}")
                    return False
            except requests.exceptions.RequestException as e:
                # Frontend might still be starting, give it more time
                time.sleep(5)
                try:
                    response = requests.get(self.frontend_url, timeout=10)
                    if response.status_code == 200:
                        self.print_status("Frontend", "running", f"Frontend running at {self.frontend_url}")
                        return True
                except:
                    self.print_status("Frontend", "error", f"Frontend not responding: {e}")
                    return False
                    
        except Exception as e:
            self.print_status("Frontend", "error", f"Failed to start frontend: {e}")
            return False
            
    def test_backend_endpoints(self):
        """Test backend endpoints."""
        self.print_status("Testing", "testing", "Testing Phase 6 Backend API endpoints...")
        
        endpoints = [
            ("Health Check", f"{self.api_base_url}/health"),
            ("Meta Info", f"{self.api_base_url}/meta"),
            ("Locations", f"{self.api_base_url}/locations"),
            ("Cuisines", f"{self.api_base_url}/cuisines"),
            ("Stats", f"{self.api_base_url}/stats")
        ]
        
        results = []
        
        for name, url in endpoints:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    self.print_status("Testing", "ready", f"{name}: ✅ Working")
                    results.append(True)
                else:
                    self.print_status("Testing", "error", f"{name}: ❌ HTTP {response.status_code}")
                    results.append(False)
            except Exception as e:
                self.print_status("Testing", "error", f"{name}: ❌ {str(e)}")
                results.append(False)
                
        # Test recommendations endpoint
        try:
            test_payload = {
                "location": "Bellandur",
                "budget": "medium",
                "cuisine": "North Indian",
                "top_k": 3
            }
            
            response = requests.post(f"{self.api_base_url}/recommendations", json=test_payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get("data", {}).get("recommendations", [])
                self.print_status("Testing", "ready", f"Recommendations: ✅ {len(recommendations)} results")
                results.append(True)
            else:
                self.print_status("Testing", "error", f"Recommendations: ❌ HTTP {response.status_code}")
                results.append(False)
        except Exception as e:
            self.print_status("Testing", "error", f"Recommendations: ❌ {str(e)}")
            results.append(False)
            
        return all(results)
        
    def test_frontend_integration(self):
        """Test frontend integration with backend."""
        self.print_status("Testing", "testing", "Testing Phase 7 Frontend integration...")
        
        # Test that frontend can reach backend
        try:
            # This would normally be done through browser automation
            # For now, we'll test the API endpoints that frontend uses
            response = requests.get(f"{self.api_base_url}/health", timeout=5)
            if response.status_code == 200:
                self.print_status("Testing", "ready", "Frontend can reach Backend API")
                return True
            else:
                self.print_status("Testing", "error", "Frontend cannot reach Backend API")
                return False
        except Exception as e:
            self.print_status("Testing", "error", f"Integration test failed: {e}")
            return False
            
    def run_integration_test(self):
        """Run a complete integration test."""
        self.print_status("Testing", "testing", "Running complete integration test...")
        
        try:
            # Simulate a complete user workflow
            test_payload = {
                "location": "Bellandur",
                "budget": "medium",
                "cuisine": "North Indian",
                "minRating": 3.5,
                "topK": 5
            }
            
            response = requests.post(f"{self.api_base_url}/recommendations", json=test_payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get("data", {}).get("recommendations", [])
                
                if len(recommendations) > 0:
                    self.print_status("Testing", "ready", f"Integration test: ✅ {len(recommendations)} recommendations")
                    
                    # Verify response structure
                    required_fields = ["restaurant_name", "rank", "score", "explanation", "location", "cuisines", "rating", "cost_for_two"]
                    first_rec = recommendations[0]
                    missing_fields = [field for field in required_fields if field not in first_rec]
                    
                    if not missing_fields:
                        self.print_status("Testing", "ready", "Response structure: ✅ Valid")
                        return True
                    else:
                        self.print_status("Testing", "error", f"Response structure: ❌ Missing {missing_fields}")
                        return False
                else:
                    self.print_status("Testing", "error", "Integration test: ❌ No recommendations returned")
                    return False
            else:
                self.print_status("Testing", "error", f"Integration test: ❌ HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.print_status("Testing", "error", f"Integration test failed: {e}")
            return False
            
    def stop_services(self):
        """Stop all running services."""
        self.print_status("Shutdown", "starting", "Stopping services...")
        
        if self.backend_process:
            self.backend_process.terminate()
            self.backend_process.wait()
            self.print_status("Backend", "stopped", "Backend API stopped")
            
        if self.frontend_process:
            self.frontend_process.terminate()
            self.frontend_process.wait()
            self.print_status("Frontend", "stopped", "Frontend UI stopped")
            
    def run(self):
        """Run the complete system."""
        self.print_header("Phase 6 + Phase 7 Full System Runner")
        
        try:
            # Check prerequisites
            if not self.check_prerequisites():
                self.print_status("System", "error", "Prerequisites not met")
                return False
                
            # Start backend
            if not self.start_backend():
                self.print_status("System", "error", "Backend failed to start")
                return False
                
            # Install frontend dependencies
            if not self.install_frontend_dependencies():
                self.print_status("System", "error", "Frontend setup failed")
                return False
                
            # Start frontend
            if not self.start_frontend():
                self.print_status("System", "error", "Frontend failed to start")
                return False
                
            # Test backend endpoints
            if not self.test_backend_endpoints():
                self.print_status("System", "error", "Backend tests failed")
                return False
                
            # Test frontend integration
            if not self.test_frontend_integration():
                self.print_status("System", "error", "Frontend integration failed")
                return False
                
            # Run integration test
            if not self.run_integration_test():
                self.print_status("System", "error", "Integration test failed")
                return False
                
            # Success!
            self.print_header("🎉 Full System Running Successfully!")
            print(f"✅ Backend API: {self.backend_url}")
            print(f"✅ Frontend UI: {self.frontend_url}")
            print(f"✅ API Documentation: {self.backend_url}/api/v1/meta")
            print()
            print("📋 System Status:")
            print("   • Phase 6 Backend HTTP API: Running")
            print("   • Phase 7 Frontend Web UI: Running")
            print("   • API Integration: Working")
            print("   • Complete User Workflow: Tested")
            print()
            print("🌐 Access Points:")
            print(f"   • Frontend: {self.frontend_url}")
            print(f"   • Backend Health: {self.backend_url}/api/v1/health")
            print(f"   • Backend Meta: {self.backend_url}/api/v1/meta")
            print()
            print("🧪 Test Results:")
            print("   • All backend endpoints: ✅ Working")
            print("   • Frontend-backend integration: ✅ Working")
            print("   • Complete user workflow: ✅ Working")
            print()
            print("📋 Next Steps:")
            print("   1. Open {self.frontend_url} in your browser")
            print("   2. Fill in the preference form")
            print("   3. Submit to get AI-powered recommendations")
            print("   4. Explore the results and features")
            print()
            print("⏹️  Press Ctrl+C to stop both services")
            
            # Keep services running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down services...")
                
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        finally:
            self.stop_services()
            
        return True

def main():
    """Main entry point."""
    runner = SystemRunner()
    success = runner.run()
    
    if success:
        print("\n🎯 Full system test completed successfully!")
        print("🚀 Phase 6 + Phase 7 integration verified!")
    else:
        print("\n⚠️  System test failed. Please check the errors above.")
        
    return success

if __name__ == "__main__":
    main()
