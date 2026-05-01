from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from .models import UserPreferences


def create_user_profile(preferences: UserPreferences) -> dict:
    return {
        "profile_id": str(uuid4()),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "preferences": preferences.to_dict(),
        "summary": (
            f"{preferences.location} | {preferences.budget} budget | "
            f"{preferences.cuisine} | min rating {preferences.min_rating}"
        ),
    }

