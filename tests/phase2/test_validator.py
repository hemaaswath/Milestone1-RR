from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from phase2.validator import validate_preferences


class TestPhase2Validator(unittest.TestCase):
    def test_valid_payload(self) -> None:
        result = validate_preferences(
            {
                "location": "Delhi",
                "budget": "medium",
                "cuisine": "italian",
                "min_rating": "4",
                "additional_preferences": "family-friendly,quick service",
            }
        )
        self.assertTrue(result.is_valid)
        self.assertIsNotNone(result.preferences)

    def test_invalid_budget(self) -> None:
        result = validate_preferences(
            {
                "location": "Delhi",
                "budget": "premium",
                "cuisine": "italian",
                "min_rating": "4",
            }
        )
        self.assertFalse(result.is_valid)
        self.assertIn("Budget must be one of: low, medium, high.", result.errors)


if __name__ == "__main__":
    unittest.main()
