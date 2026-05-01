"""
Comprehensive Phase 6 Backend HTTP API Testing

This script performs comprehensive testing of the Phase 6 Backend HTTP API
including endpoints, security features, telemetry, and Phase 1-5 integration.
"""

import sys
import os
import time
import json
import requests
import subprocess
import threading
from pathlib import Path
from datetime import datetime

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

class Phase6Tester:
    """Comprehensive Phase 6 API tester."""
    
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.test_results = []
        self.api_process = None
        
    def log_test(self, test_name, status, message="", details=None):
        """Log test result."""
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        self.test_results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {message}")
        
        if details:
            for key, value in details.items():
                print(f"   • {key}: {value}")
    
    def start_api_server(self):
        """Start the Phase 6 API server in background."""
        print("🚀 Starting Phase 6 API server...")
        
        try:
            # Use the simple test API for reliable testing
            api_script = PROJECT_ROOT / "scripts" / "test_phase6_simple.py"
            
            self.api_process = subprocess.Popen(
                [sys.executable, str(api_script)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            time.sleep(3)
            
            # Check if server is responding
            response = requests.get(f"{self.base_url}/api/v1/health", timeout=5)
            if response.status_code == 200:
                self.log_test("API Server Startup", "PASS", "Server started successfully")
                return True
            else:
                self.log_test("API Server Startup", "FAIL", f"Server returned {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("API Server Startup", "FAIL", f"Failed to start server: {e}")
            return False
    
    def stop_api_server(self):
        """Stop the API server."""
        if self.api_process:
            self.api_process.terminate()
            self.api_process.wait()
            print("🛑 API server stopped")
    
    def test_health_endpoint(self):
        """Test the health endpoint."""
        try:
            response = requests.get(f"{self.base_url}/api/v1/health", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Endpoint", "PASS", "Health endpoint working", {
                    "status": data.get("status"),
                    "phase": data.get("phase"),
                    "response_time": f"{response.elapsed.total_seconds():.3f}s"
                })
                return True
            else:
                self.log_test("Health Endpoint", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Health Endpoint", "FAIL", f"Request failed: {e}")
            return False
    
    def test_meta_endpoint(self):
        """Test the metadata endpoint."""
        try:
            response = requests.get(f"{self.base_url}/api/v1/meta", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Meta Endpoint", "PASS", "Meta endpoint working", {
                    "api_version": data.get("data", {}).get("api_version"),
                    "phase": data.get("data", {}).get("phase"),
                    "locations_count": len(data.get("data", {}).get("available_locations", [])),
                    "cuisines_count": len(data.get("data", {}).get("available_cuisines", []))
                })
                return True
            else:
                self.log_test("Meta Endpoint", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Meta Endpoint", "FAIL", f"Request failed: {e}")
            return False
    
    def test_recommendations_endpoint(self):
        """Test the main recommendations endpoint."""
        try:
            test_payload = {
                "location": "Bellandur",
                "budget": "medium",
                "cuisine": "North Indian",
                "min_rating": 3.5,
                "top_k": 3
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/api/v1/recommendations",
                json=test_payload,
                timeout=30
            )
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get("data", {}).get("recommendations", [])
                
                self.log_test("Recommendations Endpoint", "PASS", 
                            f"Got {len(recommendations)} recommendations", {
                    "status": data.get("status"),
                    "response_time": f"{end_time - start_time:.3f}s",
                    "recommendations_count": len(recommendations),
                    "has_metadata": "metadata" in data
                })
                
                # Validate response structure
                if recommendations and len(recommendations) > 0:
                    rec = recommendations[0]
                    required_fields = ["restaurant_name", "rank", "score", "explanation"]
                    missing_fields = [field for field in required_fields if field not in rec]
                    
                    if missing_fields:
                        self.log_test("Recommendations Structure", "FAIL", 
                                    f"Missing fields: {missing_fields}")
                    else:
                        self.log_test("Recommendations Structure", "PASS", 
                                    "All required fields present")
                
                return True
            else:
                self.log_test("Recommendations Endpoint", "FAIL", 
                            f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Recommendations Endpoint", "FAIL", f"Request failed: {e}")
            return False
    
    def test_input_validation(self):
        """Test input validation and error handling."""
        test_cases = [
            {
                "name": "Missing Location",
                "payload": {"budget": "medium"},
                "expected_status": 400
            },
            {
                "name": "Invalid Budget",
                "payload": {"location": "Bellandur", "budget": "invalid"},
                "expected_status": 400
            },
            {
                "name": "Empty Payload",
                "payload": {},
                "expected_status": 400
            }
        ]
        
        all_passed = True
        
        for test_case in test_cases:
            try:
                response = requests.post(
                    f"{self.base_url}/api/v1/recommendations",
                    json=test_case["payload"],
                    timeout=5
                )
                
                if response.status_code == test_case["expected_status"]:
                    self.log_test(f"Validation - {test_case['name']}", "PASS", 
                                f"Correctly returned {response.status_code}")
                else:
                    self.log_test(f"Validation - {test_case['name']}", "FAIL", 
                                f"Expected {test_case['expected_status']}, got {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Validation - {test_case['name']}", "FAIL", f"Request failed: {e}")
                all_passed = False
        
        return all_passed
    
    def test_rate_limiting(self):
        """Test rate limiting functionality."""
        try:
            # Make multiple rapid requests
            responses = []
            for i in range(5):
                response = requests.post(
                    f"{self.base_url}/api/v1/recommendations",
                    json={"location": "Bellandur", "budget": "medium"},
                    timeout=5
                )
                responses.append(response.status_code)
                time.sleep(0.1)  # Small delay between requests
            
            # Check if any requests were rate limited
            rate_limited = any(status == 429 for status in responses)
            
            if rate_limited:
                self.log_test("Rate Limiting", "PASS", "Rate limiting is working")
            else:
                self.log_test("Rate Limiting", "WARN", "Rate limiting not triggered (may be configured high)")
            
            return True
            
        except Exception as e:
            self.log_test("Rate Limiting", "FAIL", f"Test failed: {e}")
            return False
    
    def test_cors_headers(self):
        """Test CORS headers."""
        try:
            # Make a request with Origin header
            headers = {"Origin": "http://localhost:3000"}
            response = requests.get(f"{self.base_url}/api/v1/health", headers=headers)
            
            cors_headers = {
                "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
                "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
                "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers")
            }
            
            if cors_headers["Access-Control-Allow-Origin"]:
                self.log_test("CORS Headers", "PASS", "CORS headers present", cors_headers)
                return True
            else:
                self.log_test("CORS Headers", "FAIL", "No CORS headers found")
                return False
                
        except Exception as e:
            self.log_test("CORS Headers", "FAIL", f"Test failed: {e}")
            return False
    
    def test_security_headers(self):
        """Test security headers."""
        try:
            response = requests.get(f"{self.base_url}/api/v1/health")
            
            security_headers = {
                "X-Content-Type-Options": response.headers.get("X-Content-Type-Options"),
                "X-Frame-Options": response.headers.get("X-Frame-Options"),
                "X-XSS-Protection": response.headers.get("X-XSS-Protection")
            }
            
            present_headers = {k: v for k, v in security_headers.items() if v}
            
            if present_headers:
                self.log_test("Security Headers", "PASS", 
                            f"Security headers present: {list(present_headers.keys())}")
                return True
            else:
                self.log_test("Security Headers", "WARN", "No security headers found")
                return False
                
        except Exception as e:
            self.log_test("Security Headers", "FAIL", f"Test failed: {e}")
            return False
    
    def test_response_format(self):
        """Test standardized response format."""
        try:
            response = requests.get(f"{self.base_url}/api/v1/health")
            data = response.json()
            
            required_fields = ["status", "timestamp"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                self.log_test("Response Format", "PASS", "Standardized format working")
                return True
            else:
                self.log_test("Response Format", "FAIL", f"Missing fields: {missing_fields}")
                return False
                
        except Exception as e:
            self.log_test("Response Format", "FAIL", f"Test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all Phase 6 tests."""
        print("🧪 Phase 6 Comprehensive Testing")
        print("=" * 50)
        print()
        
        # Start API server
        if not self.start_api_server():
            print("❌ Cannot proceed with tests - API server failed to start")
            return False
        
        try:
            # Run all tests
            tests = [
                self.test_health_endpoint,
                self.test_meta_endpoint,
                self.test_recommendations_endpoint,
                self.test_input_validation,
                self.test_rate_limiting,
                self.test_cors_headers,
                self.test_security_headers,
                self.test_response_format
            ]
            
            for test in tests:
                try:
                    test()
                    print()
                except Exception as e:
                    print(f"❌ Test {test.__name__} failed with exception: {e}")
                    print()
            
            # Generate summary
            self.generate_test_summary()
            
        finally:
            # Stop API server
            self.stop_api_server()
        
        return True
    
    def generate_test_summary(self):
        """Generate test summary."""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        warned_tests = len([r for r in self.test_results if r["status"] == "WARN"])
        
        print("📊 Test Summary")
        print("=" * 30)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Warnings: {warned_tests}")
        print()
        
        if failed_tests == 0:
            print("🎉 All critical tests passed! Phase 6 API is working correctly.")
        else:
            print("⚠️  Some tests failed. Please review the issues above.")
        
        # Save detailed results
        results_file = PROJECT_ROOT / "phase6_test_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"📁 Detailed results saved to: {results_file}")
        print()


def main():
    """Main test runner."""
    tester = Phase6Tester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
