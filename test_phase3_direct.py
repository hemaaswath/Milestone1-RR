import sys
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).resolve().parents[0]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from phase2.models import UserPreferences
from phase3.engine import load_restaurants, retrieve_top_candidates

# Test Phase 3 directly with Bellandur
preferences = UserPreferences(
    location="Bellandur",
    budget="medium", 
    cuisine="North Indian",
    min_rating=4.0,
    additional_preferences=[]
)

print("=== TESTING PHASE 3 DIRECTLY ===")
print("Preferences:", preferences.to_dict())

try:
    restaurants_df = load_restaurants("data/processed/restaurants_phase1.csv")
    print(f"Total restaurants in dataset: {len(restaurants_df)}")
    
    # Check if Bellandur exists in dataset
    bellandur_restaurants = restaurants_df[restaurants_df['location'].str.contains('Bellandur', case=False, na=False)]
    print(f"Restaurants with 'Bellandur' in location: {len(bellandur_restaurants)}")
    
    if len(bellandur_restaurants) > 0:
        print("\nSample Bellandur restaurants:")
        print(bellandur_restaurants[['restaurant_name', 'location', 'cuisines', 'rating']].head())
    
    # Test Phase 3 retrieval
    result = retrieve_top_candidates(
        restaurants_df=restaurants_df,
        preferences=preferences,
        top_n=10,
    )
    
    print(f"\nPhase 3 Results:")
    print(f"Total records: {result.total_records}")
    print(f"Filtered records: {result.filtered_records}")
    print(f"Candidates returned: {len(result.candidates)}")
    
    if result.candidates:
        print("\nCandidates:")
        for i, candidate in enumerate(result.candidates[:5], 1):
            print(f"{i}. {candidate.restaurant_name} ({candidate.location}) - Rating: {candidate.rating}, Score: {candidate.relevance_score}")
    else:
        print("No candidates returned!")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
