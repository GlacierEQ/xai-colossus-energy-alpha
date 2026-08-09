#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from power_budget import Load, budget  # noqa: E402


def sha256_json(payload: object) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def main() -> None:
    test = subprocess.run(
        [sys.executable, "tests/test_power_budget.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if test.returncode != 0:
        raise SystemExit(test.stderr or test.stdout or "power-budget test failed")

    scenario = budget(
        [Load("critical-compute", 10.0, True), Load("support", 2.0, False)],
        20.0,
        reserve_frac=0.10,
    )
    if scenario["used_mw"] != 12.0 or scenario["reserve_mw"] != 2.0:
        raise SystemExit("modeled budget calculation drifted from the bounded scenario")

    receipt = {
        "schema": "glaciereq.energy-alpha.public-proof.v1",
        "capability": "modeled_power_budget_evaluator",
        "evidence_level": "TEST",
        "scenario": scenario,
        "external_queries": 0,
        "external_actions": 0,
        "grid_telemetry": False,
        "hardware_actuation": False,
        "runtime_pairing_with_omega": False,
        "test_returncode": test.returncode,
    }
    receipt["receipt_sha256"] = sha256_json(receipt)
    out = ROOT / "artifacts" / "public-core"
    out.mkdir(parents=True, exist_ok=True)
    (out / "verification.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
