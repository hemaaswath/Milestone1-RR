import requests
import json

# Test data with Delhi candidates (user's actual scenario)
test_data = {
    "location": "Bellandur",
    "budget": "medium", 
    "cuisine": "North Indian",
    "min_rating": "4.0",
    "top_k": "5",
    "model": "llama-3.3-70b-versatile",
    "candidates_json": json.dumps([
        {
            "restaurant_name": "Spice Garden",
            "location": "Delhi", 
            "cuisines": "North Indian, Mughlai",
            "cost_for_two": 900,
            "rating": 4.3,
            "relevance_score": 0.91,
        },
        {
            "restaurant_name": "Pasta Hub",
            "location": "Delhi",
            "cuisines": "Italian", 
            "cost_for_two": 1200,
            "rating": 4.5,
            "relevance_score": 0.88,
        }
    ], indent=2)
}

try:
    response = requests.post("http://127.0.0.1:5002/", data=test_data)
    print("Status Code:", response.status_code)
    
    # Extract the recommendations from the HTML response
    if '"recommendations":' in response.text:
        start = response.text.find('"recommendations":')
        end = response.text.find('}', start) + 1
        recommendations_json = response.text[start:end]
        print("Recommendations found:")
        print(recommendations_json)
    else:
        print("No recommendations found in response")
        print("Full response length:", len(response.text))
        
except Exception as e:
    print("Error:", e)
