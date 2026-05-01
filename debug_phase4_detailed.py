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
    
    # Save full response to file for inspection
    with open("phase4_latest_response.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    # Look for errors
    if '<div class="error">' in response.text:
        error_start = response.text.find('<div class="error">')
        error_end = response.text.find('</div>', error_start)
        error_content = response.text[error_start:error_end]
        print("ERRORS FOUND:")
        print(error_content)
    
    # Look for recommendations
    if '"recommendations":' in response.text:
        rec_start = response.text.find('"recommendations":')
        rec_end = response.text.find('}]', rec_start) + 2
        recommendations = response.text[rec_start:rec_end]
        print("\nRECOMMENDATIONS FOUND:")
        print(recommendations)
    else:
        print("\nNO RECOMMENDATIONS FOUND")
    
    # Look for candidates in textarea
    if 'candidates_json' in response.text:
        print("\nCANDIDATES TEXTAREA CONTENT:")
        # Extract textarea content
        start = response.text.find('<textarea id="candidates_json"')
        start = response.text.find('>', start) + 1
        end = response.text.find('</textarea>', start)
        textarea_content = response.text[start:end]
        print(textarea_content[:500] + "..." if len(textarea_content) > 500 else textarea_content)
        
except Exception as e:
    print("Error:", e)
