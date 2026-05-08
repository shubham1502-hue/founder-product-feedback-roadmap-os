from __future__ import annotations

from typing import Any

import pandas as pd

from founder_product_roadmap.prioritization import priority_category
from founder_product_roadmap.utils import as_number, lower_text, normalize_text


NON_PRODUCT_RULES = [
    ("sales narrative", "Solve with sales narrative", "Sales narrative"),
    ("positioning", "Solve with sales narrative", "Sales narrative"),
    ("onboarding", "Solve with onboarding", "Onboarding"),
    ("setup", "Solve with onboarding", "Onboarding"),
    ("training", "Solve with onboarding", "Training"),
    ("documentation", "Solve with support process", "Documentation"),
    ("support process", "Solve with support process", "Support process"),
    ("support triage", "Solve with support process", "Support process"),
    ("success playbook", "Add to roadmap candidate list", "Customer success playbook"),
    ("pricing", "Defer", "Pricing or packaging"),
    ("packaging", "Defer", "Pricing or packaging"),
]


def detect_non_product_fix_type(row: pd.Series) -> str:
    combined = " ".join(
        [
            lower_text(row.get("feedback_theme")),
            lower_text(row.get("feedback_text")),
            lower_text(row.get("requested_feature")),
            lower_text(row.get("notes")),
        ]
    )
    if lower_text(row.get("strategic_alignment")) == "outside":
        return "Reject"
    for keyword, _decision, fix_type in NON_PRODUCT_RULES:
        if keyword in combined:
            return fix_type
    return ""


def recommended_decision(row: pd.Series) -> str:
    fix_type = detect_non_product_fix_type(row)
    score = as_number(row.get("roadmap_priority_score"))
    confidence = lower_text(row.get("confidence_level"))
    implementation = lower_text(row.get("implementation_effort"))
    strategic_alignment = lower_text(row.get("strategic_alignment"))
    if fix_type == "Reject":
        return "Reject"
    if fix_type == "Onboarding":
        return "Solve with onboarding"
    if fix_type in {"Support process", "Documentation", "Training"}:
        return "Solve with support process"
    if fix_type == "Sales narrative":
        return "Solve with sales narrative"
    if strategic_alignment == "outside":
        return "Reject"
    if score >= 80 and implementation != "very high" and confidence != "low":
        return "Build now"
    if score >= 60:
        return "Validate with customers"
    if score >= 40:
        return "Add to roadmap candidate list"
    if score >= 20:
        return "Defer"
    return "Reject"


def recommended_owner(row: pd.Series, company_config: dict[str, Any]) -> str:
    decision = normalize_text(row.get("recommended_decision"))
    owner = normalize_text(row.get("owner"))
    if decision == "Build now":
        return "Product"
    if decision == "Validate with customers":
        return "Founder or Product"
    if decision == "Solve with onboarding":
        return "Customer Success"
    if decision == "Solve with sales narrative":
        return "Sales or Founder"
    if decision == "Solve with support process":
        return "Support or Customer Success"
    if decision == "Reject":
        return "Founder"
    return owner or "Product"


def recommended_next_action(row: pd.Series) -> str:
    decision = normalize_text(row.get("recommended_decision"))
    theme = normalize_text(row.get("feedback_theme"))
    feature = normalize_text(row.get("requested_feature"))
    if decision == "Build now":
        return f"Scope {feature} for this roadmap cycle and assign product owner."
    if decision == "Validate with customers":
        return f"Run discovery with 3 to 5 accounts on {theme} before committing build capacity."
    if decision == "Add to roadmap candidate list":
        return f"Keep {feature} in candidate list and review if signal repeats next cycle."
    if decision == "Solve with onboarding":
        return f"Update onboarding flow or checklist for {theme} before adding product scope."
    if decision == "Solve with sales narrative":
        return f"Rewrite sales narrative and proof for {theme}; monitor if objection persists."
    if decision == "Solve with support process":
        return f"Add support, docs, or CS playbook fix for {theme}; track ticket reduction."
    if decision == "Defer":
        return f"Defer {feature} until revenue, retention, or frequency signal increases."
    return f"Reject or archive {feature} because fit or leverage is too low."


def decision_reason(row: pd.Series) -> str:
    category = priority_category(as_number(row.get("roadmap_priority_score")))
    decision = normalize_text(row.get("recommended_decision"))
    parts = [
        f"{category} priority",
        f"{normalize_text(row.get('frequency_signal'))} frequency",
        f"{normalize_text(row.get('retention_risk'))} retention risk",
        f"{normalize_text(row.get('expansion_potential'))} expansion potential",
        f"{normalize_text(row.get('implementation_effort'))} effort",
    ]
    if as_number(row.get("revenue_blocked")) > 0:
        parts.append(f"${as_number(row.get('revenue_blocked')):,.0f} revenue blocked")
    parts.append(f"decision: {decision}")
    return "; ".join(parts)


def due_timing(row: pd.Series) -> str:
    decision = normalize_text(row.get("recommended_decision"))
    score = as_number(row.get("roadmap_priority_score"))
    if decision == "Build now" or score >= 80:
        return "This week"
    if decision == "Validate with customers" or score >= 60:
        return "Next 14 days"
    if decision.startswith("Solve with"):
        return "This week"
    return "Next roadmap review"


def expected_impact(row: pd.Series) -> str:
    if as_number(row.get("revenue_blocked")) > 0:
        return "Unblock revenue or reduce deal friction"
    if lower_text(row.get("retention_risk")) in {"critical", "high"}:
        return "Protect retention risk"
    if lower_text(row.get("expansion_potential")) in {"high", "medium"}:
        return "Create expansion leverage"
    return "Improve operating clarity"
