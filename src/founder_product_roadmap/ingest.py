from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "feedback_id",
    "feedback_date",
    "source",
    "source_detail",
    "customer_name",
    "segment",
    "industry",
    "account_value",
    "lifecycle_stage",
    "feedback_type",
    "feedback_theme",
    "feedback_text",
    "product_area",
    "requested_feature",
    "severity",
    "frequency_signal",
    "revenue_blocked",
    "retention_risk",
    "expansion_potential",
    "strategic_alignment",
    "customer_urgency",
    "workaround_available",
    "implementation_effort",
    "confidence_level",
    "owner",
    "current_status",
    "next_step",
    "notes",
]

NUMERIC_COLUMNS = ["account_value", "revenue_blocked"]
DATE_COLUMNS = ["feedback_date"]


def validate_required_columns(df: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Input CSV is missing required columns: {', '.join(missing)}")


def load_feedback_csv(path: str | Path) -> pd.DataFrame:
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {csv_path}")
    df = pd.read_csv(csv_path, keep_default_na=False)
    validate_required_columns(df)
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)
    for column in DATE_COLUMNS:
        df[column] = pd.to_datetime(df[column], errors="coerce")
    return df
