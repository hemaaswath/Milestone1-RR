import pandas as pd

# Load the dataset
df = pd.read_csv("data/processed/restaurants_phase1.csv")

# Check Bellandur restaurants with valid ratings
bellandur = df[df['location'].str.contains('Bellandur', case=False, na=False)]
print(f"Total Bellandur restaurants: {len(bellandur)}")

# Check ratings distribution
print(f"Restaurants with valid ratings: {bellandur['rating'].notna().sum()}")
print(f"Restaurants with NaN ratings: {bellandur['rating'].isna().sum()}")

# Show restaurants with valid ratings
valid_ratings = bellandur[bellandur['rating'].notna()]
if len(valid_ratings) > 0:
    print("\nBellandur restaurants with valid ratings:")
    print(valid_ratings[['restaurant_name', 'location', 'cuisines', 'rating']].head(10))
else:
    print("\nNo Bellandur restaurants with valid ratings found!")
    
    # Check other Bangalore areas
    bangalore_areas = df[df['location'].str.contains('Bangalore|Bengaluru|Bellandur|Marathahalli|HSR|Whitefield', case=False, na=False)]
    print(f"\nTotal Bangalore area restaurants: {len(bangalore_areas)}")
    
    # Check which areas have valid ratings
    areas_with_ratings = bangalore_areas.groupby('location')['rating'].apply(lambda x: x.notna().sum()).sort_values(ascending=False)
    print("\nAreas with most valid ratings:")
    print(areas_with_ratings.head(10))
