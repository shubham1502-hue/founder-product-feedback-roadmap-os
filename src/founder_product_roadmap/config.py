from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


REQUIRED_COMPANY_KEYS = {
    "company_name",
    "stage",
    "business_model",
    "product_motion",
    "target_segments",
    "strategic_product_themes",
    "current_company_priorities",
    "high_value_threshold",
    "retention_risk_threshold",
    "expansion_threshold",
    "revenue_blocked_threshold",
    "roadmap_capacity_per_cycle",
    "functions_involved",
    "product_areas",
    "priority_decision_rules",
    "sensitive_data_note",
    "review_cadence",
}

REQUIRED_WEIGHT_KEYS = {
    "frequency_signal",
    "revenue_blocked",
    "retention_risk",
    "expansion_potential",
    "strategic_alignment",
    "customer_urgency",
    "account_value",
    "severity",
    "workaround_available",
    "implementation_effort",
    "confidence_level",
    "lifecycle_stage",
    "segment_fit",
    "roadmap_capacity",
}


def load_yaml(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Config file not found: {file_path}")
    with file_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Config file must contain a YAML mapping: {file_path}")
    return data


def load_company_config(path: str | Path) -> dict[str, Any]:
    config = load_yaml(path)
    missing = sorted(REQUIRED_COMPANY_KEYS.difference(config))
    if missing:
        raise ValueError(f"Company config is missing required keys: {', '.join(missing)}")
    return config


def load_scoring_config(path: str | Path) -> dict[str, Any]:
    config = load_yaml(path)
    weights = config.get("weights")
    if not isinstance(weights, dict):
        raise ValueError("Scoring config must contain a weights mapping.")
    missing = sorted(REQUIRED_WEIGHT_KEYS.difference(weights))
    if missing:
        raise ValueError(f"Scoring config is missing required weights: {', '.join(missing)}")
    return config
