from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from founder_product_roadmap.config import load_company_config, load_scoring_config
from founder_product_roadmap.ingest import REQUIRED_COLUMNS, load_feedback_csv, validate_required_columns


ROOT = Path(__file__).resolve().parents[1]


def test_csv_ingestion_loads_sample_data() -> None:
    df = load_feedback_csv(ROOT / "data" / "sample_product_feedback.csv")
    assert len(df) >= 35
    assert set(REQUIRED_COLUMNS).issubset(df.columns)
    assert pd.api.types.is_numeric_dtype(df["account_value"])


def test_required_column_validation_fails_when_missing_column() -> None:
    df = pd.DataFrame({"feedback_id": ["FB-001"]})
    with pytest.raises(ValueError, match="missing required columns"):
        validate_required_columns(df)


def test_config_loading() -> None:
    company = load_company_config(ROOT / "config" / "company_profile.yml")
    scoring = load_scoring_config(ROOT / "config" / "scoring_rules.yml")
    assert company["company_name"] == "Synthetic B2B SaaS Co"
    assert "revenue_blocked" in scoring["weights"]
