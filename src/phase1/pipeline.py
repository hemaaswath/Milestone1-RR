from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
from datasets import load_dataset

from .config import PipelineConfig
from .preprocess import clean_dataframe


def _select_primary_split(dataset_dict) -> str:
    for preferred in ("train", "validation", "test"):
        if preferred in dataset_dict:
            return preferred
    return list(dataset_dict.keys())[0]


def load_raw_dataset(dataset_id: str) -> pd.DataFrame:
    dataset = load_dataset(dataset_id)
    split = _select_primary_split(dataset)
    return dataset[split].to_pandas()


def save_csv(df: pd.DataFrame, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    export_df = df.copy()
    export_df["cuisine_tags"] = export_df["cuisine_tags"].map(
        lambda tags: ",".join(tags) if isinstance(tags, list) else ""
    )
    export_df.to_csv(output_file, index=False)


def save_sqlite(df: pd.DataFrame, db_file: Path, table_name: str) -> None:
    db_file.parent.mkdir(parents=True, exist_ok=True)
    export_df = df.copy()
    export_df["cuisine_tags"] = export_df["cuisine_tags"].map(
        lambda tags: ",".join(tags) if isinstance(tags, list) else ""
    )
    with sqlite3.connect(db_file) as conn:
        export_df.to_sql(table_name, conn, if_exists="replace", index=False)


def write_summary(raw_df: pd.DataFrame, clean_df: pd.DataFrame, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    summary = [
        "Phase 1 Data Foundation Summary",
        f"Raw records: {len(raw_df)}",
        f"Clean records: {len(clean_df)}",
        f"Duplicate/invalid removed: {len(raw_df) - len(clean_df)}",
        f"Unique locations: {clean_df['location'].nunique()}",
        f"Unique restaurants: {clean_df['restaurant_name'].nunique()}",
        f"Average rating: {round(clean_df['rating'].dropna().mean(), 2) if clean_df['rating'].notna().any() else 'N/A'}",
        f"Average cost_for_two: {round(clean_df['cost_for_two'].dropna().mean(), 2) if clean_df['cost_for_two'].notna().any() else 'N/A'}",
    ]
    output_file.write_text("\n".join(summary), encoding="utf-8")


def run_pipeline(config: PipelineConfig) -> dict[str, str]:
    raw_df = load_raw_dataset(config.dataset_id)
    clean_df = clean_dataframe(raw_df)

    csv_path = config.output_dir / config.csv_file
    db_path = config.output_dir / config.sqlite_file
    summary_path = config.output_dir / config.metadata_file

    save_csv(clean_df, csv_path)
    save_sqlite(clean_df, db_path, config.sqlite_table)
    write_summary(raw_df, clean_df, summary_path)

    return {
        "csv_path": str(csv_path),
        "sqlite_path": str(db_path),
        "summary_path": str(summary_path),
        "raw_records": str(len(raw_df)),
        "clean_records": str(len(clean_df)),
    }

