from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from phase2.models import UserPreferences
from phase3.engine import retrieve_top_candidates


class TestPhase3Engine(unittest.TestCase):
    def test_retrieve_top_candidates_filters_and_scores(self) -> None:
        df = pd.DataFrame(
            [
                {
                    "restaurant_name": "Alpha",
                    "location": "Delhi",
                    "cuisines": "Italian",
                    "cost_for_two": 900,
                    "rating": 4.5,
                },
                {
                    "restaurant_name": "Beta",
                    "location": "Delhi",
                    "cuisines": "Chinese",
                    "cost_for_two": 400,
                    "rating": 4.8,
                },
                {
                    "restaurant_name": "Gamma",
                    "location": "Bangalore",
                    "cuisines": "Italian",
                    "cost_for_two": 700,
                    "rating": 4.6,
                },
            ]
        )
        prefs = UserPreferences(
            location="Delhi",
            budget="medium",
            cuisine="Italian",
            min_rating=4.0,
            additional_preferences=[],
        )
        result = retrieve_top_candidates(df, prefs, top_n=2)
        self.assertEqual(result.filtered_records, 2)
        self.assertEqual(len(result.candidates), 2)
        self.assertEqual(result.candidates[0].restaurant_name, "Alpha")


if __name__ == "__main__":
    unittest.main()
