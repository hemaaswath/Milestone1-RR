from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from phase1.config import PipelineConfig  # noqa: E402
from phase1.pipeline import run_pipeline  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Phase 1 data foundation and preprocessing pipeline."
    )
    parser.add_argument(
        "--dataset-id",
        default="ManikaSaini/zomato-restaurant-recommendation",
        help="Hugging Face dataset ID",
    )
    parser.add_argument(
        "--output-dir",
        default="data/processed",
        help="Output directory for CSV, SQLite DB, and summary",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = PipelineConfig(
        dataset_id=args.dataset_id,
        output_dir=Path(args.output_dir),
    )
    result = run_pipeline(config)

    print("Phase 1 pipeline completed successfully.")
    print(f"Raw records: {result['raw_records']}")
    print(f"Clean records: {result['clean_records']}")
    print(f"CSV: {result['csv_path']}")
    print(f"SQLite DB: {result['sqlite_path']}")
    print(f"Summary: {result['summary_path']}")


if __name__ == "__main__":
    main()
