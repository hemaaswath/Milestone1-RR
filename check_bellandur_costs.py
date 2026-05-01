import pandas as pd

# Load dataset
df = pd.read_csv("data/processed/restaurants_phase1.csv")

# Check Bellandur restaurants
bellandur = df[df['location'].str.contains('Bellandur', case=False, na=False)]
print(f"Total Bellandur restaurants: {len(bellandur)}")

# Check cost data
print(f"Restaurants with valid cost data: {bellandur['cost_for_two'].notna().sum()}")
print(f"Restaurants with NaN cost: {bellandur['cost_for_two'].isna().sum()}")

# Show sample with cost data
print("\nSample Bellandur restaurants with cost info:")
sample = bellandur[['restaurant_name', 'location', 'cuisines', 'rating', 'cost_for_two']].head(10)
print(sample)

# Check cost distribution for all restaurants
print(f"\nOverall dataset cost info:")
print(f"Restaurants with valid cost: {df['cost_for_two'].notna().sum()}")
print(f"Restaurants with NaN cost: {df['cost_for_two'].isna().sum()}")
