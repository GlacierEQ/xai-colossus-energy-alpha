from power_budget import Load, PowerEnvelope, plan_power


def test_capacity_deficit_is_plan_state_not_emergency_action() -> None:
    result = plan_power([Load("critical", 95, True)], PowerEnvelope(100, .15))
    assert result["planner_status"] == "CRITICAL_CAPACITY_DEFICIT"
    assert result["hardware_actuation"] is False
    assert result["external_actions"] == 0
