from __future__ import annotations

from founder_product_roadmap.prioritization import priority_category


def test_priority_category_boundaries() -> None:
    assert priority_category(95) == "Build now"
    assert priority_category(70) == "Validate next"
    assert priority_category(50) == "Watch"
    assert priority_category(30) == "Defer"
    assert priority_category(10) == "Reject or solve elsewhere"
