from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    dataset_id: str = "ManikaSaini/zomato-restaurant-recommendation"
    output_dir: Path = Path("data/processed")
    csv_file: str = "restaurants_phase1.csv"
    sqlite_file: str = "restaurants_phase1.db"
    sqlite_table: str = "restaurants"
    metadata_file: str = "phase1_summary.txt"

