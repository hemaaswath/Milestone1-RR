from __future__ import annotations

from dataclasses import dataclass

from .models import UserPreferences


ALLOWED_BUDGETS = {"low", "medium", "high"}


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    preferences: UserPreferences | None
    errors: list[str]


def _normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def _parse_additional_preferences(raw: str) -> list[str]:
    if not raw.strip():
        return []
    values = [item.strip() for item in raw.split(",") if item.strip()]
    # Remove duplicates while preserving order.
    return list(dict.fromkeys(values))


def validate_preferences(payload: dict[str, str]) -> ValidationResult:
    errors: list[str] = []

    location = _normalize_text(payload.get("location", ""))
    budget = _normalize_text(payload.get("budget", "")).lower()
    cuisine = _normalize_text(payload.get("cuisine", ""))
    min_rating_raw = _normalize_text(payload.get("min_rating", ""))
    additional = _parse_additional_preferences(payload.get("additional_preferences", ""))

    if not location:
        errors.append("Location is required.")
    if not cuisine:
        errors.append("Cuisine is required.")

    if budget not in ALLOWED_BUDGETS:
        errors.append("Budget must be one of: low, medium, high.")

    min_rating = 0.0
    if not min_rating_raw:
        errors.append("Minimum rating is required.")
    else:
        try:
            min_rating = float(min_rating_raw)
            if min_rating < 0 or min_rating > 5:
                errors.append("Minimum rating must be between 0 and 5.")
        except ValueError:
            errors.append("Minimum rating must be a valid number.")

    if errors:
        return ValidationResult(is_valid=False, preferences=None, errors=errors)

    preferences = UserPreferences(
        location=location.title(),
        budget=budget,
        cuisine=cuisine.title(),
        min_rating=min_rating,
        additional_preferences=additional,
    )
    return ValidationResult(is_valid=True, preferences=preferences, errors=[])

