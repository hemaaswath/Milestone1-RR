from __future__ import annotations

from phase2.models import UserPreferences

from .guardrails import apply_guardrails
from .llm_client import DEFAULT_GROQ_MODEL, run_groq_inference
from .parser import parse_ranked_output
from .prompt_builder import build_ranking_prompt


def generate_ranked_recommendations(
    preferences: UserPreferences,
    shortlisted_candidates: list[dict],
    top_k: int = 5,
    model: str = DEFAULT_GROQ_MODEL,
) -> list[dict]:
    if not shortlisted_candidates:
        return []

    prompt = build_ranking_prompt(
        preferences=preferences,
        shortlisted_candidates=shortlisted_candidates,
        top_k=top_k,
    )
    llm_raw = run_groq_inference(prompt=prompt, model=model)
    parsed = parse_ranked_output(llm_raw)
    final_recommendations = apply_guardrails(
        recommendations=parsed,
        shortlisted_candidates=shortlisted_candidates,
        top_k=top_k,
    )
    return [rec.to_dict() for rec in final_recommendations]

