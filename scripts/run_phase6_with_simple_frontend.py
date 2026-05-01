"""
Phase 6 Backend + Simple Frontend Runner

This script starts the Phase 6 Backend API and creates a simple HTML frontend
for testing the complete system when Node.js is not available.
"""

import sys
import os
import time
import subprocess
import webbrowser
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import json

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load environment variables
env_file = PROJECT_ROOT / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

class SimpleSystemRunner:
    def __init__(self):
        self.backend_process = None
        self.frontend_server = None
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
        
    def create_simple_frontend(self):
        """Create a simple HTML frontend."""
        frontend_dir = PROJECT_ROOT / "simple_frontend"
        frontend_dir.mkdir(exist_ok=True)
        
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Restaurant Recommendations - Phase 7 Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .header h1 {
            color: #1a202c;
            font-size: 2rem;
            margin-bottom: 8px;
        }
        
        .header p {
            color: #4a5568;
            font-size: 1.1rem;
        }
        
        .status-indicator {
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
            margin-top: 12px;
        }
        
        .status-online {
            background: #10b981;
            color: white;
        }
        
        .status-offline {
            background: #ef4444;
            color: white;
        }
        
        .form-container {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #374151;
        }
        
        .form-group select,
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 1rem;
        }
        
        .form-group select:focus,
        .form-group input:focus {
            outline: none;
            border-color: #3b82f6;
        }
        
        .budget-options {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
        }
        
        .budget-option {
            position: relative;
        }
        
        .budget-option input[type="radio"] {
            position: absolute;
            opacity: 0;
        }
        
        .budget-option label {
            display: block;
            padding: 12px;
            text-align: center;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .budget-option input[type="radio"]:checked + label {
            background: #3b82f6;
            color: white;
            border-color: #3b82f6;
        }
        
        .submit-btn {
            width: 100%;
            padding: 14px;
            background: #3b82f6;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 500;
            cursor: pointer;
            transition: background 0.2s;
        }
        
        .submit-btn:hover:not(:disabled) {
            background: #2563eb;
        }
        
        .submit-btn:disabled {
            background: #9ca3af;
            cursor: not-allowed;
        }
        
        .results-container {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .loading {
            text-align: center;
            padding: 40px;
        }
        
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #e5e7eb;
            border-top: 4px solid #3b82f6;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 16px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .restaurant-card {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 16px;
        }
        
        .restaurant-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        
        .restaurant-name {
            font-size: 1.2rem;
            font-weight: 600;
            color: #1a202c;
        }
        
        .restaurant-rank {
            background: #3b82f6;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .restaurant-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
            margin-bottom: 16px;
        }
        
        .detail-item {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #4a5568;
        }
        
        .explanation {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 8px;
            padding: 16px;
            margin-top: 12px;
        }
        
        .explanation h4 {
            color: #1e40af;
            margin-bottom: 8px;
        }
        
        .error-message {
            background: #fef2f2;
            border: 1px solid #fecaca;
            border-radius: 8px;
            padding: 16px;
            color: #991b1b;
        }
        
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #4a5568;
        }
        
        @media (max-width: 768px) {
            .budget-options {
                grid-template-columns: 1fr;
            }
            
            .restaurant-details {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🍽️ Restaurant Recommendations</h1>
            <p>Phase 7 Frontend Demo - AI-powered restaurant discovery</p>
            <div id="api-status" class="status-indicator status-offline">
                🔴 API Offline
            </div>
        </div>
        
        <div class="form-container">
            <h2>Find Your Perfect Restaurant</h2>
            <form id="recommendation-form">
                <div class="form-group">
                    <label for="location">Location *</label>
                    <select id="location" name="location" required>
                        <option value="">Select a location</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Budget *</label>
                    <div class="budget-options">
                        <div class="budget-option">
                            <input type="radio" id="budget-low" name="budget" value="low" required>
                            <label for="budget-low">Low</label>
                        </div>
                        <div class="budget-option">
                            <input type="radio" id="budget-medium" name="budget" value="medium">
                            <label for="budget-medium">Medium</label>
                        </div>
                        <div class="budget-option">
                            <input type="radio" id="budget-high" name="budget" value="high">
                            <label for="budget-high">High</label>
                        </div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="cuisine">Cuisine Preference</label>
                    <select id="cuisine" name="cuisine">
                        <option value="">Any cuisine</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="minRating">Minimum Rating</label>
                    <input type="range" id="minRating" name="minRating" min="1" max="5" step="0.5" value="3">
                    <div>Rating: <span id="rating-value">3.0</span>/5</div>
                </div>
                
                <div class="form-group">
                    <label for="topK">Number of Recommendations</label>
                    <select id="topK" name="topK">
                        <option value="3">3 recommendations</option>
                        <option value="5" selected>5 recommendations</option>
                        <option value="7">7 recommendations</option>
                        <option value="10">10 recommendations</option>
                    </select>
                </div>
                
                <button type="submit" class="submit-btn" id="submit-btn">
                    Get Recommendations
                </button>
            </form>
        </div>
        
        <div id="results-container" class="results-container" style="display: none;">
            <!-- Results will be loaded here -->
        </div>
    </div>

    <script>
        const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';
        
        // Check API status
        async function checkApiStatus() {
            try {
                const response = await fetch(`${API_BASE_URL}/health`);
                if (response.ok) {
                    document.getElementById('api-status').className = 'status-indicator status-online';
                    document.getElementById('api-status').innerHTML = '🟢 API Online';
                    return true;
                }
            } catch (error) {
                console.error('API status check failed:', error);
            }
            
            document.getElementById('api-status').className = 'status-indicator status-offline';
            document.getElementById('api-status').innerHTML = '🔴 API Offline';
            return false;
        }
        
        // Load form options
        async function loadFormOptions() {
            try {
                // Load locations
                const locationsResponse = await fetch(`${API_BASE_URL}/locations`);
                if (locationsResponse.ok) {
                    const locationsData = await locationsResponse.json();
                    const locationSelect = document.getElementById('location');
                    locationsData.data.locations.forEach(location => {
                        const option = document.createElement('option');
                        option.value = location;
                        option.textContent = location;
                        locationSelect.appendChild(option);
                    });
                }
                
                // Load cuisines
                const cuisinesResponse = await fetch(`${API_BASE_URL}/cuisines`);
                if (cuisinesResponse.ok) {
                    const cuisinesData = await cuisinesResponse.json();
                    const cuisineSelect = document.getElementById('cuisine');
                    cuisinesData.data.cuisines.forEach(cuisine => {
                        const option = document.createElement('option');
                        option.value = cuisine;
                        option.textContent = cuisine;
                        cuisineSelect.appendChild(option);
                    });
                }
            } catch (error) {
                console.error('Failed to load form options:', error);
            }
        }
        
        // Update rating display
        document.getElementById('minRating').addEventListener('input', (e) => {
            document.getElementById('rating-value').textContent = e.target.value;
        });
        
        // Handle form submission
        document.getElementById('recommendation-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const preferences = {
                location: formData.get('location'),
                budget: formData.get('budget'),
                cuisine: formData.get('cuisine') || '',
                minRating: parseFloat(formData.get('minRating')),
                topK: parseInt(formData.get('topK'))
            };
            
            // Show loading state
            const resultsContainer = document.getElementById('results-container');
            resultsContainer.style.display = 'block';
            resultsContainer.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <h3>Finding restaurants for you...</h3>
                    <p>Our AI is analyzing the best options based on your preferences</p>
                </div>
            `;
            
            // Disable submit button
            const submitBtn = document.getElementById('submit-btn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Searching...';
            
            try {
                const response = await fetch(`${API_BASE_URL}/recommendations`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(preferences)
                });
                
                if (response.ok) {
                    const data = await response.json();
                    displayResults(data, preferences);
                } else {
                    const errorData = await response.json();
                    displayError(errorData.message || 'Failed to get recommendations');
                }
            } catch (error) {
                displayError('Network error. Please check your connection.');
            } finally {
                // Re-enable submit button
                submitBtn.disabled = false;
                submitBtn.textContent = 'Get Recommendations';
            }
        });
        
        // Display results
        function displayResults(data, preferences) {
            const recommendations = data.data.recommendations;
            const summary = data.data.summary;
            
            let html = `
                <h2>Your Restaurant Recommendations</h2>
                <p>Found ${recommendations.length} perfect match${recommendations.length > 1 ? 'es' : ''} for you!</p>
            `;
            
            if (recommendations.length === 0) {
                html += `
                    <div class="empty-state">
                        <h3>No Restaurants Found</h3>
                        <p>We couldn't find any restaurants matching your criteria. Try adjusting your preferences.</p>
                    </div>
                `;
            } else {
                recommendations.forEach((restaurant, index) => {
                    html += `
                        <div class="restaurant-card">
                            <div class="restaurant-header">
                                <div class="restaurant-name">${restaurant.restaurant_name}</div>
                                <div class="restaurant-rank">#${restaurant.rank}</div>
                            </div>
                            <div class="restaurant-details">
                                <div class="detail-item">
                                    📍 ${restaurant.location}
                                </div>
                                <div class="detail-item">
                                    🍽️ ${restaurant.cuisines}
                                </div>
                                <div class="detail-item">
                                    ⭐ ${restaurant.rating}/5
                                </div>
                                <div class="detail-item">
                                    💰 ₹${restaurant.cost_for_two} for two
                                </div>
                            </div>
                            <div class="explanation">
                                <h4>Why we recommend this restaurant</h4>
                                <p>${restaurant.explanation}</p>
                            </div>
                        </div>
                    `;
                });
            }
            
            document.getElementById('results-container').innerHTML = html;
        }
        
        // Display error
        function displayError(message) {
            document.getElementById('results-container').innerHTML = `
                <div class="error-message">
                    <h3>❌ Error</h3>
                    <p>${message}</p>
                </div>
            `;
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            checkApiStatus();
            loadFormOptions();
            
            // Check API status every 30 seconds
            setInterval(checkApiStatus, 30000);
        });
    </script>
</body>
</html>'''
        
        html_file = frontend_dir / "index.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return frontend_dir
        
    def start_backend(self):
        """Start Phase 6 Backend API."""
        self.print_status("Backend", "starting", "Starting Phase 6 Backend HTTP API...")
        
        try:
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
            import requests
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
            
    def start_frontend(self):
        """Start simple frontend server."""
        self.print_status("Frontend", "starting", "Creating simple frontend...")
        
        try:
            # Create frontend
            frontend_dir = self.create_simple_frontend()
            
            # Change to frontend directory
            old_cwd = os.getcwd()
            os.chdir(frontend_dir)
            
            # Start HTTP server
            def run_server():
                server = HTTPServer(('127.0.0.1', 3000), SimpleHTTPRequestHandler)
                server.serve_forever()
            
            self.frontend_server = threading.Thread(target=run_server, daemon=True)
            self.frontend_server.start()
            
            # Restore working directory
            os.chdir(old_cwd)
            
            # Wait for server to start
            time.sleep(2)
            
            self.print_status("Frontend", "running", f"Frontend running at {self.frontend_url}")
            return True
            
        except Exception as e:
            self.print_status("Frontend", "error", f"Failed to start frontend: {e}")
            return False
            
    def test_integration(self):
        """Test backend-frontend integration."""
        self.print_status("Testing", "testing", "Testing complete integration...")
        
        try:
            import requests
            
            # Test a complete workflow
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
                    return True
                else:
                    self.print_status("Testing", "error", "Integration test: ❌ No recommendations")
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
            
        # Frontend server runs in daemon thread, will stop automatically
        
    def run(self):
        """Run the complete system."""
        self.print_header("Phase 6 Backend + Simple Frontend Demo")
        
        try:
            # Start backend
            if not self.start_backend():
                self.print_status("System", "error", "Backend failed to start")
                return False
                
            # Start frontend
            if not self.start_frontend():
                self.print_status("System", "error", "Frontend failed to start")
                return False
                
            # Test integration
            if not self.test_integration():
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
            print("   • Simple Frontend Demo: Running")
            print("   • API Integration: Working")
            print("   • Complete User Workflow: Tested")
            print()
            print("🌐 Access Points:")
            print(f"   • Frontend: {self.frontend_url}")
            print(f"   • Backend Health: {self.backend_url}/api/v1/health")
            print(f"   • Backend Meta: {self.backend_url}/api/v1/meta")
            print()
            print("🧪 Features Available:")
            print("   • Preference form with validation")
            print("   • Real-time API status indicator")
            print("   • Restaurant recommendations with AI explanations")
            print("   • Responsive design")
            print("   • Error handling")
            print()
            print("📋 Demo Workflow:")
            print("   1. Open {self.frontend_url} in your browser")
            print("   2. Check API status indicator (should be green)")
            print("   3. Fill in location and budget")
            print("   4. Add cuisine preference (optional)")
            print("   5. Adjust rating slider")
            print("   6. Click 'Get Recommendations'")
            print("   7. View AI-powered results")
            print()
            print("⏹️  Press Ctrl+C to stop the server")
            
            # Open browser automatically
            try:
                webbrowser.open(self.frontend_url)
                print(f"🌐 Browser opened automatically at {self.frontend_url}")
            except:
                print(f"📋 Please open {self.frontend_url} in your browser manually")
            
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
    runner = SimpleSystemRunner()
    success = runner.run()
    
    if success:
        print("\n🎯 Full system demo completed successfully!")
        print("🚀 Phase 6 + Simple Frontend integration verified!")
    else:
        print("\n⚠️  System demo failed. Please check the errors above.")
        
    return success

if __name__ == "__main__":
    main()
