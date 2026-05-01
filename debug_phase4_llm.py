import sys
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).resolve().parents[0]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from phase2.models import UserPreferences
from phase3.engine import load_restaurants, retrieve_top_candidates
from phase4.service import generate_ranked_recommendations

# Test the full Phase 4 pipeline
preferences = UserPreferences(
    location="Bellandur",
    budget="medium", 
    cuisine="North Indian",
    min_rating=4.0,
    additional_preferences=[]
)

print("=== TESTING FULL PHASE 4 PIPELINE ===")
print("Preferences:", preferences.to_dict())

try:
    # Get candidates from Phase 3
    restaurants_df = load_restaurants("data/processed/restaurants_phase1.csv")
    phase3_result = retrieve_top_candidates(
        restaurants_df=restaurants_df,
        preferences=preferences,
        top_n=10,
    )
    candidates = [c.to_dict() for c in phase3_result.candidates]
    
    print(f"\nPhase 3 returned {len(candidates)} candidates:")
    for i, candidate in enumerate(candidates[:3], 1):
        print(f"{i}. {candidate['restaurant_name']} ({candidate['location']}) - Score: {candidate['relevance_score']}")
    
    # Test Phase 4 LLM ranking
    print(f"\nTesting Phase 4 LLM ranking...")
    ranked = generate_ranked_recommendations(
        preferences=preferences,
        shortlisted_candidates=candidates,
        top_k=5,
        model="llama-3.3-70b-versatile",
    )
    
    print(f"Phase 4 returned {len(ranked)} ranked recommendations:")
    for i, rec in enumerate(ranked, 1):
        print(f"{i}. {rec['restaurant_name']} - Rank: {rec['rank']}, Score: {rec['score']}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
