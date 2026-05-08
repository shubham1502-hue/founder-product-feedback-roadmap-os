from __future__ import annotations

from pathlib import Path

from founder_product_roadmap.config import load_company_config, load_scoring_config
from founder_product_roadmap.ingest import load_feedback_csv
from founder_product_roadmap.recommendations import detect_non_product_fix_type
from founder_product_roadmap.reporting import build_non_product_fix_queue, build_roadmap_decision_queue
from founder_product_roadmap.scoring import score_feedback


ROOT = Path(__file__).resolve().parents[1]


def _scored():
    company = load_company_config(ROOT / "config" / "company_profile.yml")
    scoring = load_scoring_config(ROOT / "config" / "scoring_rules.yml")
    return score_feedback(load_feedback_csv(ROOT / "data" / "sample_product_feedback.csv"), company, scoring)


def test_non_product_fix_detection() -> None:
    scored = _scored()
    row = scored.loc[scored["feedback_id"] == "FB-022"].iloc[0]
    assert detect_non_product_fix_type(row) == "Sales narrative"


def test_roadmap_decision_queue_generation() -> None:
    queue = build_roadmap_decision_queue(_scored())
    assert not queue.empty
    assert "priority_rank" in queue.columns


def test_non_product_fix_queue_generation() -> None:
    queue = build_non_product_fix_queue(_scored())
    assert not queue.empty
    assert {"Onboarding", "Sales narrative", "Support process", "Documentation", "Reject"}.intersection(
        set(queue["recommended_fix_type"])
    )
