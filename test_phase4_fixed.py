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
    
    # Extract the recommendations from the HTML response
    if '"recommendations":' in response.text:
        start = response.text.find('"recommendations":')
        end = response.text.find('}]', start) + 2
        recommendations_json = response.text[start:end]
        print("Recommendations found:")
        print(recommendations_json)
    else:
        print("No recommendations found in response")
        print("Checking for errors in response...")
        if '<div class="error">' in response.text:
            error_start = response.text.find('<div class="error">')
            error_end = response.text.find('</div>', error_start)
            error_content = response.text[error_start:error_end]
            print("Errors found:", error_content)
        
except Exception as e:
    print("Error:", e)
