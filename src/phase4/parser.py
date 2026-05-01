from __future__ import annotations

import json
import re

from .models import RankedRecommendation


def _load_json_with_fallback(raw_text: str) -> dict:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        # Fallback: extract first JSON object from noisy output.
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if not match:
            raise ValueError("LLM output is not valid JSON.")
        return json.loads(match.group(0))


def parse_ranked_output(raw_text: str) -> list[RankedRecommendation]:
    payload = _load_json_with_fallback(raw_text)
    rows = payload.get("recommendations")
    if not isinstance(rows, list):
        raise ValueError("LLM output missing 'recommendations' list.")

    parsed: list[RankedRecommendation] = []
    for item in rows:
        if not isinstance(item, dict):
            continue
        parsed.append(
            RankedRecommendation(
                restaurant_name=str(item.get("restaurant_name", "")).strip(),
                rank=int(item.get("rank", 0)),
                score=float(item.get("score", 0)),
                explanation=str(item.get("explanation", "")).strip(),
            )
        )
    return parsed

