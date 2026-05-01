import requests
import json

# Test data for Phase 4
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
            "location": "Bellandur", 
            "cuisines": "North Indian, Mughlai",
            "cost_for_two": 900,
            "rating": 4.3,
            "relevance_score": 0.91,
        },
        {
            "restaurant_name": "Pasta Hub",
            "location": "Bellandur",
            "cuisines": "Italian", 
            "cost_for_two": 1200,
            "rating": 4.5,
            "relevance_score": 0.88,
        },
        {
            "restaurant_name": "Chinese Wok",
            "location": "Bellandur",
            "cuisines": "Chinese",
            "cost_for_two": 800,
            "rating": 4.2,
            "relevance_score": 0.85,
        },
        {
            "restaurant_name": "Biryani House",
            "location": "Bellandur", 
            "cuisines": "Mughlai, Biryani",
            "cost_for_two": 1000,
            "rating": 4.4,
            "relevance_score": 0.89,
        },
        {
            "restaurant_name": "Cafe Coffee Day",
            "location": "Bellandur",
            "cuisines": "Cafe, Continental",
            "cost_for_two": 600,
            "rating": 4.1,
            "relevance_score": 0.82,
        }
    ], indent=2)
}

try:
    response = requests.post("http://127.0.0.1:5002/", data=test_data)
    print("Status Code:", response.status_code)
    print("Response:")
    print(response.text)
except Exception as e:
    print("Error:", e)
