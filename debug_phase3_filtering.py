import sys
from pathlib import Path
import pandas as pd

# Add src to path
PROJECT_ROOT = Path(__file__).resolve().parents[0]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from phase2.models import UserPreferences

# Test the filtering step by step
preferences = UserPreferences(
    location="Bellandur",
    budget="medium", 
    cuisine="North Indian",
    min_rating=4.0,
    additional_preferences=[]
)

print("=== DEBUGGING PHASE 3 FILTERING ===")
print("Preferences:", preferences.to_dict())

# Load data
df = pd.read_csv("data/processed/restaurants_phase1.csv")
print(f"Total restaurants: {len(df)}")

# Step 1: Location filter
out = df.copy()
location_filter = (
    out["location"]
    .astype("string")
    .str.lower()
    .str.strip()
    .eq(preferences.location.lower().strip())
)
out = out[location_filter]
print(f"After location filter: {len(out)}")

# Step 2: Rating filter (current logic)
valid_rating_filter = out["rating"].notna() & (out["rating"] >= preferences.min_rating)
missing_rating_filter = out["rating"].isna()
rating_filter = valid_rating_filter | missing_rating_filter

print(f"Valid rating filter count: {valid_rating_filter.sum()}")
print(f"Missing rating filter count: {missing_rating_filter.sum()}")
print(f"Combined rating filter count: {rating_filter.sum()}")

out = out[rating_filter]
print(f"After rating filter: {len(out)}")

# Step 3: Cost filter
BUDGET_TO_MAX_COST = {
    "low": 600.0,
    "medium": 1500.0,
    "high": float("inf"),
}
max_cost = BUDGET_TO_MAX_COST.get(preferences.budget, float("inf"))
if max_cost != float("inf"):
    cost_filter = out["cost_for_two"].fillna(float("inf")) <= max_cost
    print(f"Cost filter count: {cost_filter.sum()}")
    out = out[cost_filter]

print(f"After cost filter: {len(out)}")

if len(out) > 0:
    print("\nSample filtered restaurants:")
    print(out[['restaurant_name', 'location', 'cuisines', 'rating', 'cost_for_two']].head())
else:
    print("\nNo restaurants passed all filters!")
