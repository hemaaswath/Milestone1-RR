from __future__ import annotations

import json

from flask import Flask, render_template_string, request

from .service import create_user_profile
from .validator import validate_preferences


FORM_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Phase 2 - Preference Capture</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 760px; margin: 30px auto; padding: 0 16px; }
    h1 { margin-bottom: 8px; }
    p { color: #333; }
    form { display: grid; gap: 12px; margin-top: 20px; }
    label { font-weight: 600; }
    input, select { width: 100%; padding: 10px; }
    button { width: fit-content; padding: 10px 18px; cursor: pointer; }
    .error { color: #a00; margin: 8px 0; }
    .result { margin-top: 22px; background: #f6f8fa; padding: 12px; border-radius: 6px; }
    pre { white-space: pre-wrap; margin: 0; }
  </style>
</head>
<body>
  <h1>Restaurant Preference Capture (Phase 2)</h1>
  <p>Enter user preferences from the basic web UI to create a validated preference profile.</p>

  {% if errors %}
    <div class="error">
      <strong>Validation errors:</strong>
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
          <option value="{{ b }}" {% if form_data.get('budget') == b %}selected{% endif %}>{{ b }}</option>
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
      <input id="additional_preferences" name="additional_preferences" value="{{ form_data.get('additional_preferences', '') }}" placeholder="family-friendly, quick service">
    </div>

    <button type="submit">Create Profile</button>
  </form>

  {% if profile %}
    <div class="result">
      <h3>Validated User Profile</h3>
      <pre>{{ profile }}</pre>
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
        profile = None
        form_data = dict(request.form) if request.method == "POST" else {"budget": "medium"}

        if request.method == "POST":
            result = validate_preferences(form_data)
            if result.is_valid and result.preferences:
                profile_dict = create_user_profile(result.preferences)
                profile = json.dumps(profile_dict, indent=2)
            else:
                errors = result.errors

        return render_template_string(
            FORM_TEMPLATE,
            errors=errors,
            profile=profile,
            form_data=form_data,
        )

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=True)

