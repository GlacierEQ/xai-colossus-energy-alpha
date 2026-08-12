#!/usr/bin/env python3
"""Deterministic local power-budget and load-admission planning.

The module models capacity only. It performs no telemetry query, dispatch,
switching, or hardware actuation.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Iterable, Any

EVIDENCE_STATE = "LOCAL_POWER_BUDGET_PLANNER_NOT_XAI_GRID_CONTROL"


def _finite(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}_must_be_number")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name}_must_be_finite")
    return value


def _digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Load:
    name: str
    mw: float
    critical: bool = False
    priority: int = 100

    def validated(self) -> "Load":
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("load_name_required")
        demand = _finite("load_mw", self.mw)
        if demand < 0:
            raise ValueError("load_mw_must_be_non_negative")
        if not isinstance(self.critical, bool):
            raise ValueError("critical_must_be_boolean")
        if isinstance(self.priority, bool) or not isinstance(self.priority, int):
            raise ValueError("priority_must_be_integer")
        return self


@dataclass(frozen=True)
class PowerEnvelope:
    capacity_mw: float
    reserve_fraction: float = 0.15

    def validated(self) -> "PowerEnvelope":
        capacity = _finite("capacity_mw", self.capacity_mw)
        reserve = _finite("reserve_fraction", self.reserve_fraction)
        if capacity <= 0:
            raise ValueError("capacity_mw_must_be_positive")
        if not 0.0 <= reserve < 1.0:
            raise ValueError("reserve_fraction_must_be_between_zero_and_one")
        return self


def plan_power(loads: Iterable[Load], envelope: PowerEnvelope) -> dict[str, Any]:
    envelope.validated()
    rows = [load.validated() for load in loads]
    names = [row.name for row in rows]
    if len(names) != len(set(names)):
        raise ValueError("duplicate_load_name")

    capacity = float(envelope.capacity_mw)
    reserve_fraction = float(envelope.reserve_fraction)
    reserve_mw = capacity * reserve_fraction
    loadable_mw = capacity - reserve_mw

    ordered = sorted(rows, key=lambda row: (not row.critical, row.priority, row.name))
    admitted: list[Load] = []
    deferred: list[Load] = []
    used = 0.0
    for row in ordered:
        if used + float(row.mw) <= loadable_mw + 1e-12:
            admitted.append(row)
            used += float(row.mw)
        else:
            deferred.append(row)

    critical_deferred = [row for row in deferred if row.critical]
    if critical_deferred:
        planner_status = "CRITICAL_CAPACITY_DEFICIT"
    elif deferred:
        planner_status = "CONSTRAINED"
    else:
        planner_status = "OK"

    requested = sum(float(row.mw) for row in rows)
    deferred_mw = sum(float(row.mw) for row in deferred)
    result: dict[str, Any] = {
        "schema": "glaciereq.energy-alpha.power-plan.v1",
        "evidence_state": EVIDENCE_STATE,
        "strand": "alpha",
        "planner_status": planner_status,
        "capacity_mw": round(capacity, 9),
        "reserve_fraction": round(reserve_fraction, 9),
        "reserve_mw": round(reserve_mw, 9),
        "loadable_capacity_mw": round(loadable_mw, 9),
        "requested_mw": round(requested, 9),
        "admitted_mw": round(used, 9),
        "deferred_mw": round(deferred_mw, 9),
        "headroom_mw": round(loadable_mw - used, 9),
        "physical_headroom_mw": round(capacity - used, 9),
        "loadable_utilization_fraction": round(0.0 if loadable_mw == 0 else used / loadable_mw, 9),
        "reserve_protected": True,
        "admitted_loads": [
            {"name": row.name, "mw": float(row.mw), "critical": row.critical, "priority": row.priority}
            for row in admitted
        ],
        "deferred_loads": [
            {"name": row.name, "mw": float(row.mw), "critical": row.critical, "priority": row.priority}
            for row in deferred
        ],
        "critical_deferred": [row.name for row in critical_deferred],
        "hardware_actuation": False,
        "runtime_pairing_with_omega": False,
        "external_queries": 0,
        "external_actions": 0,
    }
    result["digest"] = _digest(result)
    return result


def budget(loads: list[Load], capacity_mw: float, reserve_frac: float = 0.15) -> dict[str, Any]:
    """Compatibility facade preserving historical OK/OVERSUBSCRIBED status."""
    plan = plan_power(loads, PowerEnvelope(capacity_mw=capacity_mw, reserve_fraction=reserve_frac))
    return {
        **plan,
        "status": "OK" if plan["planner_status"] == "OK" else "OVERSUBSCRIBED",
        "used_mw": plan["requested_mw"],
    }


if __name__ == "__main__":
    print(json.dumps(plan_power([Load("inference", 40, True, 10), Load("batch", 30, False, 50)], PowerEnvelope(100)), indent=2, sort_keys=True))
