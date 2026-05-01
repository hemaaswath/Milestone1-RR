from __future__ import annotations

from .models import RankedRecommendation


def apply_guardrails(
    recommendations: list[RankedRecommendation],
    shortlisted_candidates: list[dict],
    top_k: int,
) -> list[RankedRecommendation]:
    valid_names = {
        str(row.get("restaurant_name", "")).strip() for row in shortlisted_candidates
    }
    cleaned: list[RankedRecommendation] = []
    seen: set[str] = set()

    for rec in recommendations:
        if not rec.restaurant_name or rec.restaurant_name not in valid_names:
            continue
        if rec.restaurant_name in seen:
            continue
        if not rec.explanation:
            continue

        score = min(max(rec.score, 0.0), 1.0)
        cleaned.append(
            RankedRecommendation(
                restaurant_name=rec.restaurant_name,
                rank=rec.rank,
                score=round(score, 4),
                explanation=rec.explanation,
            )
        )
        seen.add(rec.restaurant_name)
        if len(cleaned) >= top_k:
            break

    # Enforce stable sequential ranking in final output.
    return [
        RankedRecommendation(
            restaurant_name=item.restaurant_name,
            rank=i + 1,
            score=item.score,
            explanation=item.explanation,
        )
        for i, item in enumerate(cleaned)
    ]

