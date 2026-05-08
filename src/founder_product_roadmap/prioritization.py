from __future__ import annotations

from typing import Any

import pandas as pd

from founder_product_roadmap.utils import as_number, clamp, lower_text, weighted_average


SEVERITY_SCORES = {
    "critical": 100,
    "high": 80,
    "medium": 50,
    "low": 20,
}

FREQUENCY_SCORES = {
    "widespread": 100,
    "repeated": 80,
    "some": 55,
    "single": 25,
}

RISK_SCORES = {
    "critical": 100,
    "high": 85,
    "medium": 55,
    "low": 25,
    "none": 0,
}

EXPANSION_SCORES = {
    "high": 90,
    "medium": 60,
    "low": 25,
    "none": 0,
}

ALIGNMENT_SCORES = {
    "high": 100,
    "medium": 65,
    "low": 25,
    "outside": 0,
}

URGENCY_SCORES = {
    "high": 90,
    "medium": 55,
    "low": 20,
}

WORKAROUND_SCORES = {
    "no": 100,
    "partial": 55,
    "yes": 10,
}

EFFORT_SCORES = {
    "low": 20,
    "medium": 50,
    "high": 80,
    "very high": 100,
}

CONFIDENCE_SCORES = {
    "high": 90,
    "medium": 60,
    "low": 30,
}

LIFECYCLE_SCORES = {
    "sales": 75,
    "demo": 65,
    "onboarding": 80,
    "activation": 90,
    "support": 65,
    "retention": 95,
    "renewal": 100,
    "expansion": 90,
}


def map_score(value: object, mapping: dict[str, float], default: float = 0.0) -> float:
    return float(mapping.get(lower_text(value), default))


def account_value_score(account_value: object, high_value_threshold: float) -> float:
    threshold = max(as_number(high_value_threshold), 1.0)
    return clamp(as_number(account_value) / threshold * 100)


def revenue_blocked_score(revenue_blocked: object, revenue_blocked_threshold: float) -> float:
    threshold = max(as_number(revenue_blocked_threshold), 1.0)
    return clamp(as_number(revenue_blocked) / threshold * 100)


def roadmap_capacity_score(priority_score: float, capacity: int, rank: int | None = None) -> float:
    if rank is None or capacity <= 0:
        return 60
    if rank <= capacity:
        return 100
    if rank <= capacity * 2:
        return 60
    return 25 if priority_score >= 40 else 10


def segment_fit_score(segment: object, target_segments: list[str]) -> float:
    segment_text = lower_text(segment)
    targets = {lower_text(target) for target in target_segments}
    return 100 if segment_text in targets else 35


def calculate_component_scores(row: pd.Series, company_config: dict[str, Any]) -> dict[str, float]:
    return {
        "frequency_signal": map_score(row.get("frequency_signal"), FREQUENCY_SCORES, 25),
        "revenue_blocked": revenue_blocked_score(
            row.get("revenue_blocked"),
            company_config.get("revenue_blocked_threshold", 50000),
        ),
        "retention_risk": map_score(row.get("retention_risk"), RISK_SCORES, 0),
        "expansion_potential": map_score(row.get("expansion_potential"), EXPANSION_SCORES, 0),
        "strategic_alignment": map_score(row.get("strategic_alignment"), ALIGNMENT_SCORES, 25),
        "customer_urgency": map_score(row.get("customer_urgency"), URGENCY_SCORES, 20),
        "account_value": account_value_score(
            row.get("account_value"),
            company_config.get("high_value_threshold", 50000),
        ),
        "severity": map_score(row.get("severity"), SEVERITY_SCORES, 20),
        "workaround_available": map_score(row.get("workaround_available"), WORKAROUND_SCORES, 10),
        "implementation_effort": 100 - map_score(row.get("implementation_effort"), EFFORT_SCORES, 50),
        "confidence_level": map_score(row.get("confidence_level"), CONFIDENCE_SCORES, 30),
        "lifecycle_stage": map_score(row.get("lifecycle_stage"), LIFECYCLE_SCORES, 50),
        "segment_fit": segment_fit_score(row.get("segment"), company_config.get("target_segments", [])),
        "roadmap_capacity": 60,
    }


def calculate_roadmap_priority_score(
    row: pd.Series,
    company_config: dict[str, Any],
    scoring_config: dict[str, Any],
) -> float:
    scores = calculate_component_scores(row, company_config)
    weights = scoring_config.get("weights", {})
    return round(weighted_average(scores, weights), 1)


def priority_category(score: float) -> str:
    if score >= 80:
        return "Build now"
    if score >= 60:
        return "Validate next"
    if score >= 40:
        return "Watch"
    if score >= 20:
        return "Defer"
    return "Reject or solve elsewhere"
