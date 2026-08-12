from __future__ import annotations

import json
import subprocess
import sys


def test_direct_operator_exercises_three_plan_states() -> None:
    result = subprocess.run([sys.executable, "scripts/operate.py"], check=True, capture_output=True, text=True)
    receipt = json.loads(result.stdout)
    assert receipt["result"] == "PASS"
    assert receipt["nominal"]["planner_status"] == "OK"
    assert receipt["constrained"]["planner_status"] == "CONSTRAINED"
    assert receipt["critical_deficit"]["planner_status"] == "CRITICAL_CAPACITY_DEFICIT"
