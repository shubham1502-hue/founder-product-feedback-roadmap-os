from __future__ import annotations

import pandas as pd

from founder_product_roadmap.recommendations import expected_impact
from founder_product_roadmap.utils import as_number, join_unique, lower_text, normalize_text


def _severity_count(series: pd.Series, values: set[str]) -> int:
    return int(series.apply(lambda value: lower_text(value) in values).sum())


def _suggested_resolution(group: pd.DataFrame) -> str:
    decision_counts = group["recommended_decision"].value_counts()
    top_decision = decision_counts.index[0]
    theme = normalize_text(group["feedback_theme"].iloc[0])
    if top_decision == "Build now":
        return f"Scope the highest leverage {theme} fix this cycle."
    if top_decision == "Validate with customers":
        return f"Validate {theme} with affected accounts before committing roadmap capacity."
    if top_decision.startswith("Solve with"):
        return f"Resolve {theme} through {top_decision.replace('Solve with ', '')} before adding product scope."
    if top_decision == "Reject":
        return f"Reject or archive {theme} unless strategic fit changes."
    return f"Track {theme} as a roadmap candidate and review next cycle."


def build_product_gap_summary(scored: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    grouped = scored.groupby(["feedback_theme", "product_area"], dropna=False)
    for index, ((theme, product_area), group) in enumerate(grouped, start=1):
        if len(group) < 1:
            continue
        rows.append(
            {
                "gap_id": f"GAP-{index:03d}",
                "feedback_theme": theme,
                "product_area": product_area,
                "count": int(len(group)),
                "affected_segments": join_unique(group["segment"]),
                "affected_accounts": join_unique(group["customer_name"], limit=8),
                "estimated_revenue_blocked": round(group["revenue_blocked"].sum(), 2),
                "retention_risk_count": _severity_count(group["retention_risk"], {"critical", "high", "medium"}),
                "expansion_opportunity_count": _severity_count(group["expansion_potential"], {"high", "medium"}),
                "suggested_resolution": _suggested_resolution(group),
                "owner_role": normalize_text(group["recommended_owner"].mode().iloc[0]),
            }
        )
    result = pd.DataFrame(rows)
    return result.sort_values(
        ["estimated_revenue_blocked", "retention_risk_count", "expansion_opportunity_count", "count"],
        ascending=[False, False, False, False],
    )


def repeated_themes(scored: pd.DataFrame, min_count: int = 2) -> pd.DataFrame:
    summary = build_product_gap_summary(scored)
    return summary[summary["count"] >= min_count].copy()


def revenue_blocking_gaps(scored: pd.DataFrame) -> pd.DataFrame:
    summary = build_product_gap_summary(scored)
    return summary[summary["estimated_revenue_blocked"] > 0].copy()


def retention_risk_gaps(scored: pd.DataFrame) -> pd.DataFrame:
    summary = build_product_gap_summary(scored)
    return summary[summary["retention_risk_count"] > 0].copy()


def expansion_unlocks(scored: pd.DataFrame) -> pd.DataFrame:
    summary = build_product_gap_summary(scored)
    return summary[summary["expansion_opportunity_count"] > 0].copy()


def signal_strength(group: pd.DataFrame) -> str:
    count = len(group)
    revenue = group["revenue_blocked"].sum()
    high_risk = _severity_count(group["retention_risk"], {"critical", "high"})
    expansion = _severity_count(group["expansion_potential"], {"high"})
    if count >= 4 or revenue >= 100000 or high_risk >= 2:
        return "Strong"
    if count >= 2 or revenue > 0 or expansion >= 1:
        return "Moderate"
    return "Weak"


def decision_implication(group: pd.DataFrame) -> str:
    decision = normalize_text(group["recommended_decision"].mode().iloc[0])
    theme = normalize_text(group["feedback_theme"].iloc[0])
    if decision == "Build now":
        return f"Prioritize {theme} in current roadmap cycle."
    if decision == "Validate with customers":
        return f"Validate {theme} before build decision."
    if decision.startswith("Solve with"):
        return f"Fix {theme} outside core product roadmap first."
    return f"Monitor {theme} and revisit if signal strengthens."


def build_customer_signal_matrix(scored: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for theme, group in scored.groupby("feedback_theme", dropna=False):
        rows.append(
            {
                "feedback_theme": theme,
                "source_mix": join_unique(group["source"]),
                "lifecycle_stages": join_unique(group["lifecycle_stage"]),
                "customer_segments": join_unique(group["segment"]),
                "account_value_impacted": round(group["account_value"].sum(), 2),
                "signal_strength": signal_strength(group),
                "decision_implication": decision_implication(group),
            }
        )
    result = pd.DataFrame(rows)
    strength_rank = {"Strong": 0, "Moderate": 1, "Weak": 2}
    result["_rank"] = result["signal_strength"].map(strength_rank)
    return result.sort_values(["_rank", "account_value_impacted"], ascending=[True, False]).drop(columns=["_rank"])


def build_account_feedback_view(scored: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for customer, group in scored.groupby("customer_name", dropna=False):
        top_score = as_number(group["roadmap_priority_score"].max())
        if top_score >= 80:
            account_action = "Review in roadmap decision meeting this week."
        elif group["recommended_decision"].str.startswith("Solve with").any():
            account_action = "Assign non-product owner and confirm customer expectation."
        elif top_score >= 60:
            account_action = "Validate problem with customer before roadmap commitment."
        else:
            account_action = "Monitor and revisit if signal repeats."
        rows.append(
            {
                "customer_name": customer,
                "segment": normalize_text(group["segment"].iloc[0]),
                "account_value": round(group["account_value"].max(), 2),
                "feedback_count": int(len(group)),
                "top_themes": join_unique(group.sort_values("roadmap_priority_score", ascending=False)["feedback_theme"], limit=5),
                "revenue_blocked": round(group["revenue_blocked"].sum(), 2),
                "retention_risk": join_unique(group["retention_risk"]),
                "expansion_potential": join_unique(group["expansion_potential"]),
                "recommended_account_action": account_action,
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["revenue_blocked", "account_value", "feedback_count"],
        ascending=[False, False, False],
    )


def build_non_product_candidates(scored: pd.DataFrame) -> pd.DataFrame:
    mask = scored["recommended_decision"].str.startswith("Solve with") | (scored["recommended_decision"] == "Reject")
    return scored[mask].copy()
