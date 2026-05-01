from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class UserPreferences:
    location: str
    budget: str
    cuisine: str
    min_rating: float
    additional_preferences: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

