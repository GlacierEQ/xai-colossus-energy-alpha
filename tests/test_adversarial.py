from __future__ import annotations

import pytest

from power_budget import Load, PowerEnvelope, plan_power


def test_duplicate_names_refuse() -> None:
    with pytest.raises(ValueError, match="duplicate_load_name"):
        plan_power([Load("a", 1), Load("a", 2)], PowerEnvelope(10))


def test_negative_load_refuses() -> None:
    with pytest.raises(ValueError, match="load_mw_must_be_non_negative"):
        plan_power([Load("a", -1)], PowerEnvelope(10))


def test_bad_reserve_refuses() -> None:
    with pytest.raises(ValueError, match="reserve_fraction_must_be_between_zero_and_one"):
        plan_power([], PowerEnvelope(10, 1.0))


def test_non_integer_priority_refuses() -> None:
    with pytest.raises(ValueError, match="priority_must_be_integer"):
        plan_power([Load("a", 1, priority=1.5)], PowerEnvelope(10))
