from __future__ import annotations

from pathlib import Path

from founder_product_roadmap.clustering import (
    expansion_unlocks,
    repeated_themes,
    retention_risk_gaps,
    revenue_blocking_gaps,
)
from founder_product_roadmap.config import load_company_config, load_scoring_config
from founder_product_roadmap.ingest import load_feedback_csv
from founder_product_roadmap.scoring import score_feedback


ROOT = Path(__file__).resolve().parents[1]


def _scored():
    company = load_company_config(ROOT / "config" / "company_profile.yml")
    scoring = load_scoring_config(ROOT / "config" / "scoring_rules.yml")
    return score_feedback(load_feedback_csv(ROOT / "data" / "sample_product_feedback.csv"), company, scoring)


def test_repeated_theme_aggregation() -> None:
    summary = repeated_themes(_scored())
    assert "CRM integration" in set(summary["feedback_theme"])
    assert summary["count"].max() >= 2


def test_revenue_blocking_gap_detection() -> None:
    summary = revenue_blocking_gaps(_scored())
    assert summary["estimated_revenue_blocked"].max() > 0


def test_retention_risk_gap_detection() -> None:
    summary = retention_risk_gaps(_scored())
    assert "Reporting gap" in set(summary["feedback_theme"])


def test_expansion_unlock_detection() -> None:
    summary = expansion_unlocks(_scored())
    assert summary["expansion_opportunity_count"].max() > 0
