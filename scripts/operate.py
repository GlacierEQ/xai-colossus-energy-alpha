#!/usr/bin/env python3
"""Execute Energy Alpha's actual local power planner directly."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from power_budget import EVIDENCE_STATE, Load, PowerEnvelope, plan_power  # noqa: E402


def main() -> int:
    nominal = plan_power(
        [Load("inference", 40, True, 10), Load("training", 30, False, 20)],
        PowerEnvelope(100, 0.15),
    )
    constrained = plan_power(
        [Load("inference", 40, True, 10), Load("training", 50, False, 20)],
        PowerEnvelope(100, 0.15),
    )
    critical_deficit = plan_power(
        [Load("critical-a", 90, True, 10), Load("batch", 5, False, 20)],
        PowerEnvelope(100, 0.15),
    )
    receipt = {
        "schema": "glaciereq.energy-alpha.operability.v1",
        "evidence_state": EVIDENCE_STATE,
        "nominal": nominal,
        "constrained": constrained,
        "critical_deficit": critical_deficit,
        "result": "PASS" if (
            nominal["planner_status"] == "OK"
            and constrained["planner_status"] == "CONSTRAINED"
            and critical_deficit["planner_status"] == "CRITICAL_CAPACITY_DEFICIT"
        ) else "FAIL",
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["result"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
