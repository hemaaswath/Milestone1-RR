from __future__ import annotations

import re
from typing import Iterable

import pandas as pd


TARGET_COLUMNS = {
    "restaurant_name": [
        "restaurant_name",
        "name",
        "restaurant",
        "res_name",
    ],
    "location": [
        "location",
        "city",
        "locality",
        "address",
    ],
    "cuisines": [
        "cuisines",
        "cuisine",
        "food_type",
    ],
    "cost_for_two": [
        "cost_for_two",
        "average_cost_for_two",
        "cost",
        "avg_cost",
        "price_range",
    ],
    "rating": [
        "rating",
        "aggregate_rating",
        "votes_rating",
        "user_rating",
    ],
}


def _first_existing_column(columns: Iterable[str], candidates: list[str]) -> str | None:
    available = {col.lower(): col for col in columns}
    for name in candidates:
        if name.lower() in available:
            return available[name.lower()]
    return None


def map_schema(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Map unknown dataset schema to required project fields."""
    mapped = pd.DataFrame(index=raw_df.index)
    for target, candidates in TARGET_COLUMNS.items():
        source = _first_existing_column(raw_df.columns, candidates)
        mapped[target] = raw_df[source] if source else None
    return mapped


def normalize_location(value: object) -> str | None:
    if pd.isna(value):
        return None
    text = " ".join(str(value).strip().split())
    return text.title() if text else None


def normalize_cuisines(value: object) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    if not text:
        return None
    # Normalize separators and casing while preserving multi-cuisine labels.
    text = text.replace("|", ",").replace("/", ",")
    cuisines = [segment.strip().title() for segment in text.split(",") if segment.strip()]
    return ", ".join(dict.fromkeys(cuisines)) if cuisines else None


def parse_cost(value: object) -> float | None:
    if pd.isna(value):
        return None
    text = str(value)
    # Capture numbers from values like "Rs. 300", "200-400", "₹1,200".
    numbers = re.findall(r"\d+(?:[.,]\d+)?", text.replace(",", ""))
    if not numbers:
        return None
    vals = [float(n) for n in numbers]
    return round(sum(vals) / len(vals), 2)


def parse_rating(value: object) -> float | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    if not text:
        return None
    match = re.search(r"\d+(?:\.\d+)?", text)
    if not match:
        return None
    rating = float(match.group())
    # Clamp to standard 0..5 rating scale.
    return max(0.0, min(5.0, rating))


def clean_dataframe(raw_df: pd.DataFrame) -> pd.DataFrame:
    mapped = map_schema(raw_df)
    cleaned = pd.DataFrame(
        {
            "restaurant_name": mapped["restaurant_name"].astype("string").str.strip(),
            "location": mapped["location"].map(normalize_location),
            "cuisines": mapped["cuisines"].map(normalize_cuisines),
            "cost_for_two": mapped["cost_for_two"].map(parse_cost),
            "rating": mapped["rating"].map(parse_rating),
        }
    )

    # Remove unusable records and duplicates.
    cleaned = cleaned.dropna(subset=["restaurant_name", "location"])
    cleaned = cleaned.drop_duplicates(subset=["restaurant_name", "location"], keep="first")

    cleaned["cuisine_tags"] = cleaned["cuisines"].fillna("").map(
        lambda x: [c.strip() for c in x.split(",") if c.strip()]
    )
    cleaned["quality_score"] = (
        cleaned[["cuisines", "cost_for_two", "rating"]]
        .notna()
        .sum(axis=1)
        .astype(int)
    )
    return cleaned.reset_index(drop=True)

