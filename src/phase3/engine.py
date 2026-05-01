from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from phase2.models import UserPreferences

from .models import CandidateRestaurant


BUDGET_TO_MAX_COST = {
    "low": 600.0,
    "medium": 1500.0,
    "high": float("inf"),
}


@dataclass(frozen=True)
class RetrievalResult:
    candidates: list[CandidateRestaurant]
    total_records: int
    filtered_records: int


def load_restaurants(csv_path: str) -> pd.DataFrame:
    required_cols = ["restaurant_name", "location", "cuisines", "cost_for_two", "rating"]
    df = pd.read_csv(csv_path)
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(
            f"Processed dataset missing required columns: {', '.join(missing)}"
        )
    return df


def _normalize_text(value: str) -> str:
    return " ".join(value.strip().lower().split())


def _score_row(row: pd.Series, preferences: UserPreferences) -> float:
    score = 0.0

    row_location = _normalize_text(str(row["location"]))
    pref_location = _normalize_text(preferences.location)
    if row_location == pref_location:
        score += 0.35

    row_cuisines = _normalize_text(str(row.get("cuisines", "")))
    pref_cuisine = _normalize_text(preferences.cuisine)
    if pref_cuisine and pref_cuisine in row_cuisines:
        score += 0.35

    rating = row.get("rating")
    if pd.notna(rating):
        score += min(float(rating), 5.0) / 5.0 * 0.2

    cost = row.get("cost_for_two")
    max_cost = BUDGET_TO_MAX_COST.get(preferences.budget, float("inf"))
    if pd.notna(cost) and float(cost) <= max_cost:
        score += 0.1

    return round(score, 4)


def _apply_hard_filters(df: pd.DataFrame, preferences: UserPreferences) -> pd.DataFrame:
    out = df.copy()

    out = out[
        out["location"]
        .astype("string")
        .str.lower()
        .str.strip()
        .eq(preferences.location.lower().strip())
    ]

    # Filter by rating: include restaurants with valid ratings >= min_rating, OR those with missing ratings
    valid_rating_filter = out["rating"].notna() & (out["rating"] >= preferences.min_rating)
    missing_rating_filter = out["rating"].isna()
    out = out[valid_rating_filter | missing_rating_filter]

    max_cost = BUDGET_TO_MAX_COST.get(preferences.budget, float("inf"))
    if max_cost != float("inf"):
        # Include restaurants with valid cost <= max_cost OR those with missing cost data
        valid_cost_filter = out["cost_for_two"].notna() & (out["cost_for_two"] <= max_cost)
        missing_cost_filter = out["cost_for_two"].isna()
        out = out[valid_cost_filter | missing_cost_filter]

    return out


def retrieve_top_candidates(
    restaurants_df: pd.DataFrame,
    preferences: UserPreferences,
    top_n: int = 10,
) -> RetrievalResult:
    filtered = _apply_hard_filters(restaurants_df, preferences)
    if filtered.empty:
        return RetrievalResult(candidates=[], total_records=len(restaurants_df), filtered_records=0)

    scored = filtered.copy()
    scored["relevance_score"] = scored.apply(
        lambda row: _score_row(row, preferences),
        axis=1,
    )
    scored = scored.sort_values(
        by=["relevance_score", "rating", "restaurant_name"],
        ascending=[False, False, True],
    )

    top_rows = scored.head(max(top_n, 1))
    candidates = [
        CandidateRestaurant(
            restaurant_name=str(row["restaurant_name"]),
            location=str(row["location"]),
            cuisines=str(row.get("cuisines", "")),
            cost_for_two=float(row["cost_for_two"]) if pd.notna(row["cost_for_two"]) else None,
            rating=float(row["rating"]) if pd.notna(row["rating"]) else None,
            relevance_score=float(row["relevance_score"]),
        )
        for _, row in top_rows.iterrows()
    ]

    return RetrievalResult(
        candidates=candidates,
        total_records=len(restaurants_df),
        filtered_records=len(filtered),
    )

