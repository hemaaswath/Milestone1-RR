import requests
import json

# Test data with Bellandur location
test_data = {
    "location": "Bellandur",
    "budget": "medium", 
    "cuisine": "North Indian",
    "min_rating": "4.0",
    "top_k": "5",
    "model": "llama-3.3-70b-versatile"
}

try:
    response = requests.post("http://127.0.0.1:5002/", data=test_data)
    print("Status Code:", response.status_code)
    print("Response length:", len(response.text))
    
    # Save full response to file for inspection
    with open("phase4_response.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Full response saved to phase4_response.html")
    
    # Look for any specific patterns
    if "error" in response.text.lower():
        print("Errors detected in response")
    
    if "recommendations" in response.text:
        print("Recommendations found in response")
    else:
        print("No recommendations found")
        
except Exception as e:
    print("Error:", e)
