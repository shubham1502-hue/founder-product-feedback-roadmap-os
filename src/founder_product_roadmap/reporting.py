from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from founder_product_roadmap.clustering import (
    build_account_feedback_view,
    build_customer_signal_matrix,
    build_non_product_candidates,
    build_product_gap_summary,
    expansion_unlocks,
    repeated_themes,
    retention_risk_gaps,
    revenue_blocking_gaps,
)
from founder_product_roadmap.recommendations import due_timing, expected_impact
from founder_product_roadmap.scoring import build_scorecard
from founder_product_roadmap.utils import as_number, format_currency, join_unique, lower_text, normalize_text


def build_roadmap_decision_queue(scored: pd.DataFrame) -> pd.DataFrame:
    candidates = scored[scored["recommended_decision"].isin(["Build now", "Validate with customers", "Add to roadmap candidate list"])].copy()
    candidates = candidates.sort_values(["roadmap_priority_score", "revenue_blocked"], ascending=[False, False])
    rows: list[dict[str, object]] = []
    for rank, (_, row) in enumerate(candidates.iterrows(), start=1):
        rows.append(
            {
                "priority_rank": rank,
                "product_area": row["product_area"],
                "requested_feature": row["requested_feature"],
                "decision": row["recommended_decision"],
                "reason": row["decision_reason"],
                "accounts_affected": row["customer_name"],
                "revenue_blocked": row["revenue_blocked"],
                "retention_risk": row["retention_risk"],
                "expansion_potential": row["expansion_potential"],
                "implementation_effort": row["implementation_effort"],
                "next_step": row["recommended_next_action"],
                "owner": row["recommended_owner"],
                "due_timing": due_timing(row),
            }
        )
    return pd.DataFrame(rows)


def _fix_type_from_decision(decision: str, row: pd.Series) -> str:
    if decision == "Solve with onboarding":
        return "Onboarding"
    if decision == "Solve with sales narrative":
        return "Sales narrative"
    if decision == "Solve with support process":
        text = " ".join([lower_text(row.get("feedback_theme")), lower_text(row.get("requested_feature")), lower_text(row.get("notes"))])
        if "documentation" in text:
            return "Documentation"
        if "training" in text:
            return "Training"
        return "Support process"
    if decision == "Reject":
        return "Reject"
    return "Customer success playbook"


def build_non_product_fix_queue(scored: pd.DataFrame) -> pd.DataFrame:
    candidates = build_non_product_candidates(scored).sort_values(["roadmap_priority_score", "account_value"], ascending=[False, False])
    rows: list[dict[str, object]] = []
    for index, (_, row) in enumerate(candidates.iterrows(), start=1):
        decision = normalize_text(row["recommended_decision"])
        rows.append(
            {
                "item_id": f"NPF-{index:03d}",
                "feedback_theme": row["feedback_theme"],
                "issue": row["feedback_text"],
                "recommended_fix_type": _fix_type_from_decision(decision, row),
                "reason": row["decision_reason"],
                "owner": row["recommended_owner"],
                "next_step": row["recommended_next_action"],
                "expected_impact": expected_impact(row),
            }
        )
    return pd.DataFrame(rows)


def build_score_explanations(scored: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for _, row in scored.sort_values("roadmap_priority_score", ascending=False).iterrows():
        drivers = [
            f"priority {as_number(row['roadmap_priority_score']):.1f}",
            f"revenue impact {as_number(row['revenue_impact_score']):.1f}",
            f"retention impact {as_number(row['retention_impact_score']):.1f}",
            f"expansion impact {as_number(row['expansion_impact_score']):.1f}",
            f"strategic fit {as_number(row['strategic_fit_score']):.1f}",
            f"confidence {as_number(row['confidence_score']):.1f}",
        ]
        risks = [
            f"{normalize_text(row['retention_risk'])} retention risk",
            f"{normalize_text(row['severity'])} severity",
            f"{normalize_text(row['workaround_available'])} workaround available",
            f"{normalize_text(row['implementation_effort'])} implementation effort",
        ]
        rows.append(
            {
                "feedback_id": row["feedback_id"],
                "feedback_theme": row["feedback_theme"],
                "score_drivers": "; ".join(drivers),
                "risk_drivers": "; ".join(risks),
                "decision_reason": row["decision_reason"],
                "recommended_next_action": row["recommended_next_action"],
                "score_interpretation": f"{row['recommended_decision']} because this item is {row['priority_category'].lower()} with transparent weighted inputs.",
            }
        )
    return pd.DataFrame(rows)


def _markdown_table(df: pd.DataFrame, columns: list[str], limit: int = 8) -> str:
    if df.empty:
        return "No items found.\n"
    view = df[columns].head(limit).copy()
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    rows = []
    for _, row in view.iterrows():
        cells = [normalize_text(row.get(column)).replace("|", "/") for column in columns]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *rows]) + "\n"


def build_founder_roadmap_memo(scored: pd.DataFrame, company_config: dict[str, Any]) -> str:
    scorecard = build_scorecard(scored)
    gaps = build_product_gap_summary(scored)
    revenue_gaps = revenue_blocking_gaps(scored)
    retention_gaps = retention_risk_gaps(scored)
    expansion = expansion_unlocks(scored)
    non_product = build_non_product_fix_queue(scored)
    repeated = repeated_themes(scored)
    decision_queue = build_roadmap_decision_queue(scored)
    build_now_count = int((scored["recommended_decision"] == "Build now").sum())
    validate_count = int((scored["recommended_decision"] == "Validate with customers").sum())
    non_product_count = int(len(non_product))
    revenue_blocked = scored["revenue_blocked"].sum()
    high_retention = int(scored["retention_risk"].apply(lambda value: lower_text(value) in {"critical", "high"}).sum())
    lines = [
        "# Founder Roadmap Memo",
        "",
        "## Executive summary",
        f"- Synthetic demo dataset analyzed for {company_config.get('company_name')}.",
        f"- {build_now_count} items are recommended to build now, {validate_count} need validation, and {non_product_count} should be solved outside product or rejected.",
        f"- Estimated revenue blocked across feedback items is {format_currency(revenue_blocked)}.",
        f"- {high_retention} feedback items carry high or critical retention risk.",
        "",
        "## Roadmap priorities this cycle",
        _markdown_table(decision_queue, ["priority_rank", "product_area", "requested_feature", "decision", "owner", "due_timing"], 8),
        "## Feedback themes that repeated",
        _markdown_table(repeated, ["gap_id", "feedback_theme", "count", "affected_accounts", "suggested_resolution"], 8),
        "## Revenue-blocking product gaps",
        _markdown_table(revenue_gaps, ["gap_id", "feedback_theme", "estimated_revenue_blocked", "affected_accounts", "suggested_resolution"], 8),
        "## Retention-risk product gaps",
        _markdown_table(retention_gaps, ["gap_id", "feedback_theme", "retention_risk_count", "affected_accounts", "suggested_resolution"], 8),
        "## Expansion unlocks",
        _markdown_table(expansion, ["gap_id", "feedback_theme", "expansion_opportunity_count", "affected_accounts", "suggested_resolution"], 8),
        "## Noisy asks to avoid",
    ]
    noisy = scored[
        (scored["recommended_decision"].isin(["Reject", "Defer"]))
        | (scored["strategic_alignment"].apply(lower_text) == "outside")
    ].sort_values("roadmap_priority_score")
    lines.append(_markdown_table(noisy, ["feedback_id", "customer_name", "requested_feature", "recommended_decision", "recommended_next_action"], 8))
    lines.extend(
        [
            "## Issues to solve outside product",
            _markdown_table(non_product, ["item_id", "feedback_theme", "recommended_fix_type", "owner", "next_step"], 8),
            "## Discovery questions for next week",
            "- Which top-ranked asks show repeated pain across multiple target segments?",
            "- Which revenue-blocking gaps can be solved with a narrow workflow instead of a broad platform build?",
            "- Which retention risks need a customer call before product scope is approved?",
            "- Which non-product fixes should be tested before roadmap capacity is used?",
            "",
            "## Recommended next 7-day actions",
            "- Review the roadmap decision queue with product, founder, CS, and GTM owners.",
            "- Approve or reject the top build-now items based on current roadmap capacity.",
            "- Schedule customer validation calls for validate-next items.",
            "- Assign non-product fixes to onboarding, sales, support, documentation, or CS owners.",
            "- Update the product tracker, CRM, CS tracker, or weekly review with owners and due dates.",
            "",
        ]
    )
    return "\n".join(lines)


def build_product_operating_review(scored: pd.DataFrame) -> str:
    decision_queue = build_roadmap_decision_queue(scored)
    non_product = build_non_product_fix_queue(scored)
    signal_matrix = build_customer_signal_matrix(scored)
    lines = [
        "# Product Operating Review",
        "",
        "## Weekly product feedback review agenda",
        "- Review top roadmap decisions.",
        "- Review repeated themes and customer signal strength.",
        "- Separate product work from onboarding, sales, support, documentation, CS, or pricing fixes.",
        "- Confirm owners and due dates.",
        "",
        "## Metrics to inspect",
        "- Count of build-now items.",
        "- Count of validate-next items.",
        "- Revenue blocked by product gap.",
        "- Retention-risk feedback count.",
        "- Expansion-unlock feedback count.",
        "- Non-product fix count.",
        "",
        "## Themes to discuss",
        _markdown_table(signal_matrix, ["feedback_theme", "signal_strength", "account_value_impacted", "decision_implication"], 8),
        "## Roadmap decisions needed",
        _markdown_table(decision_queue, ["priority_rank", "requested_feature", "decision", "owner", "due_timing"], 10),
        "## Discovery needed",
        "- Validate any high-scoring item with low confidence before build commitment.",
        "- Confirm whether enterprise-specific asks generalize to target segments.",
        "- Ask customers what current workaround costs them in time, revenue, or risk.",
        "",
        "## Owners and due dates",
        _markdown_table(decision_queue, ["priority_rank", "requested_feature", "owner", "due_timing", "next_step"], 10),
        "## What to update in product tracker, CRM, CS tracker, or weekly review",
        "- Product tracker: decision, owner, stage, and validation requirement.",
        "- CRM: revenue-blocking product gaps and deal impact.",
        "- CS tracker: retention-risk product gaps and customer expectation.",
        "- Weekly review: founder decisions, blocked owners, and next-week commitments.",
        "",
    ]
    if not non_product.empty:
        lines.extend(
            [
                "## Non-product fixes to assign",
                _markdown_table(non_product, ["item_id", "recommended_fix_type", "owner", "next_step"], 10),
            ]
        )
    return "\n".join(lines)


def write_outputs(scored: pd.DataFrame, company_config: dict[str, Any], output_dir: str | Path) -> dict[str, Path]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    outputs = {
        "roadmap_priority_scorecard": output_path / "roadmap_priority_scorecard.csv",
        "product_gap_summary": output_path / "product_gap_summary.csv",
        "roadmap_decision_queue": output_path / "roadmap_decision_queue.csv",
        "non_product_fix_queue": output_path / "non_product_fix_queue.csv",
        "customer_signal_matrix": output_path / "customer_signal_matrix.csv",
        "account_feedback_view": output_path / "account_feedback_view.csv",
        "founder_roadmap_memo": output_path / "founder_roadmap_memo.md",
        "product_operating_review": output_path / "product_operating_review.md",
        "score_explanations": output_path / "score_explanations.csv",
    }
    build_scorecard(scored).to_csv(outputs["roadmap_priority_scorecard"], index=False)
    build_product_gap_summary(scored).to_csv(outputs["product_gap_summary"], index=False)
    build_roadmap_decision_queue(scored).to_csv(outputs["roadmap_decision_queue"], index=False)
    build_non_product_fix_queue(scored).to_csv(outputs["non_product_fix_queue"], index=False)
    build_customer_signal_matrix(scored).to_csv(outputs["customer_signal_matrix"], index=False)
    build_account_feedback_view(scored).to_csv(outputs["account_feedback_view"], index=False)
    build_score_explanations(scored).to_csv(outputs["score_explanations"], index=False)
    outputs["founder_roadmap_memo"].write_text(build_founder_roadmap_memo(scored, company_config), encoding="utf-8")
    outputs["product_operating_review"].write_text(build_product_operating_review(scored), encoding="utf-8")
    return outputs
