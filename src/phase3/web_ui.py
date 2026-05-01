from __future__ import annotations

import json

from flask import Flask, render_template_string, request

from phase2.validator import validate_preferences

from .engine import load_restaurants, retrieve_top_candidates


FORM_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Phase 3 - Candidate Retrieval</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 860px; margin: 30px auto; padding: 0 16px; }
    form { display: grid; gap: 12px; margin-top: 16px; }
    input, select { width: 100%; padding: 10px; }
    button { width: fit-content; padding: 10px 16px; cursor: pointer; }
    .error { color: #a00; margin-top: 12px; }
    .result { margin-top: 18px; background: #f6f8fa; padding: 12px; border-radius: 6px; }
    pre { white-space: pre-wrap; margin: 0; }
  </style>
</head>
<body>
  <h1>Phase 3 Candidate Retrieval and Filtering</h1>
  <p>Filters restaurants using hard constraints, scores relevance, and returns top-N candidates.</p>

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
      <label for="csv_path">Processed CSV path</label>
      <input id="csv_path" name="csv_path" value="{{ form_data.get('csv_path', 'data/processed/restaurants_phase1.csv') }}">
    </div>
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
      <label for="top_n">Top-N candidates</label>
      <input id="top_n" name="top_n" value="{{ form_data.get('top_n', '10') }}" placeholder="10">
    </div>
    <button type="submit">Retrieve Candidates</button>
  </form>

  {% if output %}
    <div class="result">
      <h3>Retrieval Output</h3>
      <pre>{{ output }}</pre>
    </div>
  {% endif %}
</body>
</html>
"""


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        errors: list[str] = []
        output = None
        form_data = dict(request.form) if request.method == "POST" else {
            "csv_path": "data/processed/restaurants_phase1.csv",
            "budget": "medium",
            "top_n": "10",
        }

        if request.method == "POST":
            validation = validate_preferences(form_data)
            if not validation.is_valid or validation.preferences is None:
                errors.extend(validation.errors)
            else:
                try:
                    top_n = int(form_data.get("top_n", "10"))
                    if top_n <= 0:
                        errors.append("Top-N must be greater than 0.")
                except ValueError:
                    errors.append("Top-N must be a valid integer.")
                    top_n = 10

                if not errors:
                    try:
                        restaurants_df = load_restaurants(form_data["csv_path"])
                        result = retrieve_top_candidates(
                            restaurants_df=restaurants_df,
                            preferences=validation.preferences,
                            top_n=top_n,
                        )
                        output_dict = {
                            "total_records": result.total_records,
                            "filtered_records": result.filtered_records,
                            "candidates": [c.to_dict() for c in result.candidates],
                        }
                        output = json.dumps(output_dict, indent=2)
                    except Exception as exc:  # pragma: no cover - UI safety net
                        errors.append(str(exc))

        return render_template_string(
            FORM_TEMPLATE,
            errors=errors,
            output=output,
            form_data=form_data,
        )

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5001, debug=True)

