from power_budget import Load, PowerEnvelope, plan_power


def test_plan_is_deterministic() -> None:
    loads = [Load("critical", 40, True, 10), Load("batch", 30, False, 50)]
    first = plan_power(loads, PowerEnvelope(100, .15))
    second = plan_power(loads, PowerEnvelope(100, .15))
    assert first == second
    assert first["digest"] == second["digest"]
