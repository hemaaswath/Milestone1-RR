from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class CandidateRestaurant:
    restaurant_name: str
    location: str
    cuisines: str
    cost_for_two: float | None
    rating: float | None
    relevance_score: float

    def to_dict(self) -> dict:
        return asdict(self)

