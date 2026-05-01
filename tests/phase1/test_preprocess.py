from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from phase1.preprocess import clean_dataframe, parse_cost, parse_rating


class TestPhase1Preprocess(unittest.TestCase):
    def test_parse_cost_range(self) -> None:
        self.assertEqual(parse_cost("Rs. 200-400"), 300.0)

    def test_parse_rating_clamp(self) -> None:
        self.assertEqual(parse_rating("6.4"), 5.0)

    def test_clean_dataframe_deduplicates(self) -> None:
        raw = pd.DataFrame(
            [
                {
                    "restaurant_name": "A",
                    "location": "Delhi",
                    "cuisines": "Italian",
                    "cost_for_two": "500",
                    "rating": "4.2",
                },
                {
                    "restaurant_name": "A",
                    "location": "Delhi",
                    "cuisines": "Italian",
                    "cost_for_two": "500",
                    "rating": "4.2",
                },
            ]
        )
        cleaned = clean_dataframe(raw)
        self.assertEqual(len(cleaned), 1)


if __name__ == "__main__":
    unittest.main()
