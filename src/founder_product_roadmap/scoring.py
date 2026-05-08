from __future__ import annotations

from typing import Any

import pandas as pd

from founder_product_roadmap.prioritization import (
    calculate_component_scores,
    calculate_roadmap_priority_score,
    priority_category,
)
from founder_product_roadmap.recommendations import (
    decision_reason,
    recommended_decision,
    recommended_next_action,
    recommended_owner,
)


def score_feedback(
    df: pd.DataFrame,
    company_config: dict[str, Any],
    scoring_config: dict[str, Any],
) -> pd.DataFrame:
    scored = df.copy()
    component_rows: list[dict[str, float]] = []
    priority_scores: list[float] = []
    for _, row in scored.iterrows():
        components = calculate_component_scores(row, company_config)
        component_rows.append(components)
        priority_scores.append(calculate_roadmap_priority_score(row, company_config, scoring_config))

    components_df = pd.DataFrame(component_rows)
    scored["revenue_impact_score"] = components_df["revenue_blocked"].round(1)
    scored["retention_impact_score"] = components_df["retention_risk"].round(1)
    scored["expansion_impact_score"] = components_df["expansion_potential"].round(1)
    scored["strategic_fit_score"] = components_df["strategic_alignment"].round(1)
    scored["urgency_score"] = components_df["customer_urgency"].round(1)
    scored["effort_score"] = components_df["implementation_effort"].round(1)
    scored["confidence_score"] = components_df["confidence_level"].round(1)
    scored["roadmap_priority_score"] = priority_scores
    scored["priority_category"] = scored["roadmap_priority_score"].apply(priority_category)
    scored["recommended_decision"] = scored.apply(recommended_decision, axis=1)
    scored["recommended_owner"] = scored.apply(lambda row: recommended_owner(row, company_config), axis=1)
    scored["recommended_next_action"] = scored.apply(recommended_next_action, axis=1)
    scored["decision_reason"] = scored.apply(decision_reason, axis=1)
    return scored


def build_scorecard(scored: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "feedback_id",
        "feedback_theme",
        "product_area",
        "requested_feature",
        "customer_name",
        "segment",
        "lifecycle_stage",
        "roadmap_priority_score",
        "priority_category",
        "recommended_decision",
        "recommended_owner",
        "recommended_next_action",
    ]
    sorted_scored = scored.sort_values(
        ["roadmap_priority_score", "revenue_blocked"],
        ascending=[False, False],
    )
    return sorted_scored[columns]
