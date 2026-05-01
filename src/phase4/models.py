from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class RankedRecommendation:
    restaurant_name: str
    rank: int
    score: float
    explanation: str

    def to_dict(self) -> dict:
        return asdict(self)

