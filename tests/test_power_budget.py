from __future__ import annotations

import pytest

from power_budget import Load, PowerEnvelope, budget, plan_power


def test_nominal_plan_protects_reserve_and_admits_all() -> None:
    result = plan_power([Load("critical", 40, True, 10), Load("batch", 30, False, 50)], PowerEnvelope(100, .15))
    assert result["planner_status"] == "OK"
    assert result["reserve_mw"] == 15.0
    assert result["admitted_mw"] == 70.0
    assert result["headroom_mw"] == 15.0
    assert result["reserve_protected"] is True


def test_noncritical_load_is_deferred_when_reserve_would_be_consumed() -> None:
    result = plan_power([Load("critical", 40, True, 10), Load("batch", 50, False, 50)], PowerEnvelope(100, .15))
    assert result["planner_status"] == "CONSTRAINED"
    assert [row["name"] for row in result["admitted_loads"]] == ["critical"]
    assert [row["name"] for row in result["deferred_loads"]] == ["batch"]


def test_critical_deficit_is_explicit() -> None:
    result = plan_power([Load("critical", 90, True, 10)], PowerEnvelope(100, .15))
    assert result["planner_status"] == "CRITICAL_CAPACITY_DEFICIT"
    assert result["critical_deferred"] == ["critical"]


def test_priority_is_stable_after_criticality() -> None:
    result = plan_power([
        Load("late", 30, False, 50),
        Load("early", 30, False, 10),
        Load("critical", 40, True, 99),
    ], PowerEnvelope(100, .15))
    assert [row["name"] for row in result["admitted_loads"]] == ["critical", "early"]
    assert [row["name"] for row in result["deferred_loads"]] == ["late"]


def test_compatibility_budget_preserves_old_status() -> None:
    assert budget([Load("a", 10)], 20)["status"] == "OK"
    assert budget([Load("a", 30)], 20)["status"] == "OVERSUBSCRIBED"


@pytest.mark.parametrize("capacity", [0.0, -1.0, float("nan"), float("inf")])
def test_bad_capacity_refuses(capacity: float) -> None:
    with pytest.raises(ValueError):
        plan_power([], PowerEnvelope(capacity))
