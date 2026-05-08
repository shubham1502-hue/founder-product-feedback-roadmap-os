from __future__ import annotations

from pathlib import Path

from founder_product_roadmap.config import load_company_config, load_scoring_config
from founder_product_roadmap.ingest import load_feedback_csv
from founder_product_roadmap.reporting import build_founder_roadmap_memo, build_score_explanations
from founder_product_roadmap.scoring import score_feedback


ROOT = Path(__file__).resolve().parents[1]


def _scored():
    company = load_company_config(ROOT / "config" / "company_profile.yml")
    scoring = load_scoring_config(ROOT / "config" / "scoring_rules.yml")
    return score_feedback(load_feedback_csv(ROOT / "data" / "sample_product_feedback.csv"), company, scoring), company


def test_memo_generation() -> None:
    scored, company = _scored()
    memo = build_founder_roadmap_memo(scored, company)
    assert "## Executive summary" in memo
    assert "## Recommended next 7-day actions" in memo


def test_score_explanations_generation() -> None:
    scored, _company = _scored()
    explanations = build_score_explanations(scored)
    assert not explanations.empty
    assert "score_interpretation" in explanations.columns
