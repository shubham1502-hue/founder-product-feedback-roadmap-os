from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Iterable

import pandas as pd


DEFAULT_ANALYSIS_DATE = date(2026, 5, 8)


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return max(lower, min(upper, float(value)))


def as_number(value: object, default: float = 0.0) -> float:
    if value is None or pd.isna(value):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def normalize_text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def lower_text(value: object) -> str:
    return normalize_text(value).lower()


def parse_date(value: object, default: date | None = None) -> date:
    if default is None:
        default = DEFAULT_ANALYSIS_DATE
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return default
    return parsed.date()


def days_between(start: object, end: object | None = None) -> int:
    end_date = parse_date(end, DEFAULT_ANALYSIS_DATE) if end is not None else DEFAULT_ANALYSIS_DATE
    start_date = parse_date(start, end_date)
    return (end_date - start_date).days


def join_unique(values: Iterable[object], limit: int = 6) -> str:
    seen: list[str] = []
    for value in values:
        text = normalize_text(value)
        if text and text not in seen:
            seen.append(text)
    if len(seen) > limit:
        return "; ".join(seen[:limit]) + f"; and {len(seen) - limit} more"
    return "; ".join(seen)


def format_currency(value: object) -> str:
    amount = as_number(value)
    return f"${amount:,.0f}"


def weighted_average(scores: dict[str, float], weights: dict[str, float]) -> float:
    total_weight = 0.0
    total_score = 0.0
    for key, score in scores.items():
        weight = as_number(weights.get(key), 0.0)
        total_weight += weight
        total_score += clamp(score) * weight
    if total_weight <= 0:
        return 0.0
    return clamp(total_score / total_weight)
