from __future__ import annotations

import json

from flask import Flask, render_template_string, request

from phase2.validator import validate_preferences
from phase3.engine import load_restaurants, retrieve_top_candidates

from .llm_client import DEFAULT_GROQ_MODEL
from .service import generate_ranked_recommendations


FORM_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Phase 4 - Groq Ranking Engine</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 960px; margin: 30px auto; padding: 0 16px; }
    form { display: grid; gap: 12px; margin-top: 16px; }
    input, select, textarea { width: 100%; padding: 10px; }
    textarea { min-height: 180px; font-family: Consolas, monospace; }
    button { width: fit-content; padding: 10px 16px; cursor: pointer; }
    .error { color: #a00; margin-top: 12px; }
    .result { margin-top: 18px; background: #f6f8fa; padding: 12px; border-radius: 6px; }
    pre { white-space: pre-wrap; margin: 0; }
  </style>
</head>
<body>
  <h1>Phase 4 LLM Recommendation and Ranking (Groq)</h1>
  <p>Provide validated preferences and shortlisted candidates to generate ranked recommendations with explanations.</p>

  {% if errors %}
    <div class="error">
      <strong>Errors:</strong>
      <ul>
        {% for err in errors %}
          <li>{{ err }}</li>
        {% endfor %}
      </ul>
    </div>
  {% endif %}

  <form method="post">
    <div>
      <label for="location">Location</label>
      <input id="location" name="location" value="{{ form_data.get('location', '') }}" placeholder="e.g., Delhi">
    </div>
    <div>
      <label for="budget">Budget</label>
      <select id="budget" name="budget">
        {% for b in ['low', 'medium', 'high'] %}
          <option value="{{ b }}" {% if form_data.get('budget', 'medium') == b %}selected{% endif %}>{{ b }}</option>
        {% endfor %}
      </select>
    </div>
    <div>
      <label for="cuisine">Cuisine</label>
      <input id="cuisine" name="cuisine" value="{{ form_data.get('cuisine', '') }}" placeholder="e.g., Italian">
    </div>
    <div>
      <label for="min_rating">Minimum Rating (0 to 5)</label>
      <input id="min_rating" name="min_rating" value="{{ form_data.get('min_rating', '') }}" placeholder="e.g., 4.0">
    </div>
    <div>
      <label for="additional_preferences">Additional Preferences (comma-separated)</label>
      <input id="additional_preferences" name="additional_preferences" value="{{ form_data.get('additional_preferences', '') }}">
    </div>
    <div>
      <label for="model">Groq Model</label>
      <input id="model" name="model" value="{{ form_data.get('model', default_model) }}">
    </div>
    <div>
      <label for="top_k">Top-K recommendations</label>
      <input id="top_k" name="top_k" value="{{ form_data.get('top_k', '5') }}">
    </div>
    <div>
      <label for="candidates_json">Shortlisted candidates JSON (list of objects from Phase 3)</label>
      <textarea id="candidates_json" name="candidates_json">{{ form_data.get('candidates_json', sample_candidates_json) }}</textarea>
    </div>
    <button type="submit">Generate Ranked Recommendations</button>
  </form>

  {% if output %}
    <div class="result">
      <h3>Ranked Recommendations</h3>
      <pre>{{ output }}</pre>
    </div>
  {% endif %}
</body>
</html>
"""


SAMPLE_CANDIDATES = [
    {
        "restaurant_name": "Spice Garden",
        "location": "Delhi",
        "cuisines": "North Indian, Mughlai",
        "cost_for_two": 900,
        "rating": 4.3,
        "relevance_score": 0.91,
    },
    {
        "restaurant_name": "Pasta Hub",
        "location": "Delhi",
        "cuisines": "Italian",
        "cost_for_two": 1200,
        "rating": 4.5,
        "relevance_score": 0.88,
    },
]


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        errors: list[str] = []
        output = None
        form_data = dict(request.form) if request.method == "POST" else {
            "budget": "medium",
            "top_k": "5",
            "model": DEFAULT_GROQ_MODEL,
            "candidates_json": json.dumps(SAMPLE_CANDIDATES, indent=2),
        }

        if request.method == "POST":
            validation = validate_preferences(form_data)
            if not validation.is_valid or validation.preferences is None:
                errors.extend(validation.errors)
            else:
                try:
                    top_k = int(form_data.get("top_k", "5"))
                    if top_k <= 0:
                        errors.append("Top-K must be greater than 0.")
                except ValueError:
                    errors.append("Top-K must be a valid integer.")
                    top_k = 5

                candidates: list[dict] = []
                try:
                    # Get real candidates from Phase 3 if location is provided
                    if validation.preferences.location:
                        restaurants_df = load_restaurants("data/processed/restaurants_phase1.csv")
                        phase3_result = retrieve_top_candidates(
                            restaurants_df=restaurants_df,
                            preferences=validation.preferences,
                            top_n=10,  # Get more candidates for better ranking
                        )
                        candidates = [c.to_dict() for c in phase3_result.candidates]
                    else:
                        # Use manually entered candidates if no location
                        parsed = json.loads(form_data.get("candidates_json", "[]"))
                        if not isinstance(parsed, list):
                            errors.append("Candidates JSON must be a list.")
                        else:
                            candidates = parsed
                except json.JSONDecodeError:
                    errors.append("Candidates JSON is invalid.")
                except Exception as e:
                    errors.append(f"Error retrieving candidates: {str(e)}")

                if not errors:
                    try:
                        model = form_data.get("model", DEFAULT_GROQ_MODEL).strip() or DEFAULT_GROQ_MODEL
                        ranked = generate_ranked_recommendations(
                            preferences=validation.preferences,
                            shortlisted_candidates=candidates,
                            top_k=top_k,
                            model=model,
                        )
                        output = json.dumps({"recommendations": ranked}, indent=2)
                        
                        # Update form_data to show real candidates in the textarea
                        form_data["candidates_json"] = json.dumps(candidates, indent=2)
                    except Exception as exc:  # pragma: no cover - UI safety net
                        errors.append(str(exc))

        return render_template_string(
            FORM_TEMPLATE,
            errors=errors,
            output=output,
            form_data=form_data,
            default_model=DEFAULT_GROQ_MODEL,
            sample_candidates_json=json.dumps(SAMPLE_CANDIDATES, indent=2),
        )

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5002, debug=True)

