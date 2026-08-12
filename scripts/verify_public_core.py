#!/usr/bin/env python3
"""Fail-closed public/product truth verification for Energy Alpha."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from power_budget import EVIDENCE_STATE, Load, PowerEnvelope, plan_power  # noqa: E402

FORBIDDEN_README = (
    "<<<<<<<", "=======", ">>>>>>>", "1.5 GW", "100,000+", "99.999%",
    "automatic failover", "emergency power", "grid control", "energy_status",
    "Mastermind", "APEX",
)


def main() -> int:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for token in FORBIDDEN_README:
        if token.lower() in readme.lower():
            raise SystemExit(f"forbidden_public_claim:{token}")
    capabilities = json.loads((ROOT / "machine" / "capabilities.json").read_text())
    target = json.loads((ROOT / "machine" / "target-contract.json").read_text())
    excellence = json.loads((ROOT / "machine" / "excellence-state.json").read_text())
    promotion = json.loads((ROOT / "machine" / "promotion_authority.json").read_text())
    gaps = json.loads((ROOT / "machine" / "crystallization" / "gap-matrix.json").read_text())
    if capabilities["evidence_state"] != EVIDENCE_STATE or target["evidence_state"] != EVIDENCE_STATE:
        raise SystemExit("evidence_state_mismatch")
    if excellence["state"] != "FUNCTIONAL_CRYSTALLIZATION_CANDIDATE":
        raise SystemExit("false_terminal_state")
    if promotion["status"] != "RETIRED":
        raise SystemExit("legacy_local_promotion_not_retired")
    if gaps["gaps"] != []:
        raise SystemExit("material_gaps_remain")
    nominal = plan_power([Load("critical", 40, True, 10), Load("batch", 30, False, 50)], PowerEnvelope(100, .15))
    constrained = plan_power([Load("critical", 40, True, 10), Load("batch", 50, False, 50)], PowerEnvelope(100, .15))
    if nominal["planner_status"] != "OK" or constrained["planner_status"] != "CONSTRAINED":
        raise SystemExit("planner_contract_failed")
    source_sha = hashlib.sha256((ROOT / "src" / "power_budget.py").read_bytes()).hexdigest()
    receipt = {
        "schema": "glaciereq.energy-alpha.public-proof.v2",
        "evidence_state": EVIDENCE_STATE,
        "source_sha256": source_sha,
        "nominal_digest": nominal["digest"],
        "constrained_digest": constrained["digest"],
        "external_queries": 0,
        "external_actions": 0,
        "hardware_actuation": False,
        "runtime_pairing_with_omega": False,
        "legacy_promotion_authority": "RETIRED",
        "result": "PASS",
    }
    out = ROOT / "artifacts" / "public-core" / "verification.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
