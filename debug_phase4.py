import sys
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).resolve().parents[0]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from phase2.models import UserPreferences
from phase4.prompt_builder import build_ranking_prompt
from phase4.llm_client import run_groq_inference

# Create test preferences
preferences = UserPreferences(
    location="Bellandur",
    budget="medium", 
    cuisine="North Indian",
    min_rating=4.0,
    additional_preferences=[]
)

# Test with Delhi candidates
delhi_candidates = [
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
]

print("=== DEBUG: Phase 4 LLM Output ===")
print("User Preferences:", preferences.to_dict())
print("Candidates:", delhi_candidates)
print()

# Build the prompt
prompt = build_ranking_prompt(
    preferences=preferences,
    shortlisted_candidates=delhi_candidates,
    top_k=5,
)

print("=== PROMPT SENT TO LLM ===")
print(prompt)
print("\n" + "="*50 + "\n")

# Get LLM response
try:
    llm_response = run_groq_inference(prompt=prompt)
    print("=== LLM RAW RESPONSE ===")
    print(llm_response)
    print("\n" + "="*50 + "\n")
    
    # Try to parse it
    import json
    try:
        parsed = json.loads(llm_response)
        print("=== PARSED JSON ===")
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError as e:
        print("JSON PARSE ERROR:", e)
        
except Exception as e:
    print("LLM ERROR:", e)
