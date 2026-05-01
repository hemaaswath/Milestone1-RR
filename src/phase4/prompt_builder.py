from __future__ import annotations

import json

from phase2.models import UserPreferences


def build_ranking_prompt(
    preferences: UserPreferences,
    shortlisted_candidates: list[dict],
    top_k: int = 5,
) -> str:
    candidate_payload = [
        {
            "restaurant_name": c.get("restaurant_name"),
            "location": c.get("location"),
            "cuisines": c.get("cuisines"),
            "cost_for_two": c.get("cost_for_two"),
            "rating": c.get("rating"),
            "relevance_score": c.get("relevance_score"),
        }
        for c in shortlisted_candidates
    ]

    return f"""
You are a restaurant recommendation ranking assistant.
Use only the shortlisted candidates provided below.
Do not invent any restaurant names or attributes.

User Preferences:
{json.dumps(preferences.to_dict(), indent=2)}

Shortlisted Candidates:
{json.dumps(candidate_payload, indent=2)}

Task:
1) Rank the best {top_k} restaurants.
2) Explain why each recommendation fits the user.
3) Base ranking on location fit, cuisine fit, rating, and cost fit.

Return strict JSON only in this format:
{{
  "recommendations": [
    {{
      "restaurant_name": "string",
      "rank": 1,
      "score": 0.0,
      "explanation": "string"
    }}
  ]
}}

Rules:
- score must be between 0 and 1.
- rank must start at 1 and be unique.
- explanation must be concise (1-2 sentences).
- restaurant_name must match one of the shortlisted candidates exactly.
""".strip()

