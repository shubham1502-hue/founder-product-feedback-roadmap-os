from __future__ import annotations

from pathlib import Path

from founder_product_roadmap.config import load_company_config, load_scoring_config
from founder_product_roadmap.ingest import load_feedback_csv
from founder_product_roadmap.scoring import score_feedback


ROOT = Path(__file__).resolve().parents[1]


def _scored():
    company = load_company_config(ROOT / "config" / "company_profile.yml")
    scoring = load_scoring_config(ROOT / "config" / "scoring_rules.yml")
    df = load_feedback_csv(ROOT / "data" / "sample_product_feedback.csv")
    return score_feedback(df, company, scoring)


def test_roadmap_priority_scoring_boundaries() -> None:
    scored = _scored()
    assert scored["roadmap_priority_score"].between(0, 100).all()
    assert scored["priority_category"].notna().all()


def test_high_revenue_feedback_scores_above_low_fit_customization() -> None:
    scored = _scored()
    enterprise = scored.loc[scored["feedback_id"] == "FB-012", "roadmap_priority_score"].iloc[0]
    niche = scored.loc[scored["feedback_id"] == "FB-016", "roadmap_priority_score"].iloc[0]
    assert enterprise > niche
