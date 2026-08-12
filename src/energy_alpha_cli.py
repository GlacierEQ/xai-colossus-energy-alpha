"""Installed CLI for Energy Alpha's local power-budget planner."""
from __future__ import annotations

import argparse
import json

from power_budget import Load, PowerEnvelope, plan_power


def _load(value: str) -> Load:
    parts = value.split(":")
    if len(parts) not in (2, 3, 4):
        raise argparse.ArgumentTypeError("load format is name:mw[:critical|standard[:priority]]")
    name = parts[0]
    try:
        mw = float(parts[1])
        critical = len(parts) >= 3 and parts[2].lower() == "critical"
        if len(parts) >= 3 and parts[2].lower() not in {"critical", "standard"}:
            raise ValueError("bad critical flag")
        priority = int(parts[3]) if len(parts) == 4 else 100
    except ValueError as exc:
        raise argparse.ArgumentTypeError("invalid load specification") from exc
    return Load(name=name, mw=mw, critical=critical, priority=priority)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan a bounded local power budget")
    parser.add_argument("--capacity-mw", type=float, default=100.0)
    parser.add_argument("--reserve-fraction", type=float, default=0.15)
    parser.add_argument("--load", action="append", type=_load, default=None)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args(argv)
    loads = args.load or [
        Load("inference", 40.0, critical=True, priority=10),
        Load("training", 30.0, priority=20),
    ]
    result = plan_power(loads, PowerEnvelope(args.capacity_mw, args.reserve_fraction))
    print(json.dumps(result, sort_keys=True, indent=None if args.compact else 2))
    return 0 if not result["critical_deferred"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
