from power_budget import Load, PowerEnvelope, plan_power


def test_receipt_is_local_and_machine_readable() -> None:
    result = plan_power([Load("a", 10)], PowerEnvelope(20, .1))
    assert result["planner_status"] == "OK"
    assert result["hardware_actuation"] is False
    assert result["external_queries"] == 0
    assert result["external_actions"] == 0
    assert len(result["digest"]) == 64
