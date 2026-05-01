from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from phase4.guardrails import apply_guardrails
from phase4.models import RankedRecommendation


class TestPhase4Guardrails(unittest.TestCase):
    def test_guardrails_filters_invalid_and_reindexes(self) -> None:
        recs = [
            RankedRecommendation("A", 2, 1.2, "Good match."),
            RankedRecommendation("Unknown", 1, 0.9, "Should be removed."),
            RankedRecommendation("A", 3, 0.4, "Duplicate should be removed."),
            RankedRecommendation("B", 4, -1.0, "Also good."),
        ]
        candidates = [{"restaurant_name": "A"}, {"restaurant_name": "B"}]

        final = apply_guardrails(recs, candidates, top_k=5)
        self.assertEqual(len(final), 2)
        self.assertEqual(final[0].restaurant_name, "A")
        self.assertEqual(final[0].rank, 1)
        self.assertEqual(final[0].score, 1.0)
        self.assertEqual(final[1].restaurant_name, "B")
        self.assertEqual(final[1].score, 0.0)


if __name__ == "__main__":
    unittest.main()
