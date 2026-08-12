# Energy Alpha — Local Power Budget Planner

**Installable, deterministic local power-capacity, reserve, and load-admission planning for modeled compute-infrastructure scenarios.**

> **Independent portfolio project.** This repository is not affiliated with, endorsed by, employed by, or deployed at xAI. It has no grid, substation, generator, UPS, switchgear, PDU, rack-power, or facility-control authority.

Evidence state: `LOCAL_POWER_BUDGET_PLANNER_NOT_XAI_GRID_CONTROL`

## What the product does

The canonical product is `src/power_budget.py`. It turns an explicit modeled capacity, reserve policy, and requested load set into an inspectable admission plan:

- validates finite positive capacity, bounded reserve fraction, finite non-negative load demand, unique load names, and integer priority;
- protects the requested reserve before admitting modeled workload;
- orders **critical loads first**, then stable numeric priority and name;
- admits a load only when it fits inside the post-reserve loadable capacity;
- explicitly identifies deferred loads and any critical load that cannot fit;
- distinguishes `OK`, `CONSTRAINED`, and `CRITICAL_CAPACITY_DEFICIT` planner states;
- reports requested/admitted/deferred MW, reserve MW, loadable capacity, headroom, utilization, and deterministic SHA-256 receipt;
- performs zero external queries or actions and never issues a power command.

The historical `budget()` function remains as a compatibility facade. It retains `OK` / `OVERSUBSCRIBED` status while exposing the richer `planner_status` and admitted/deferred plan.

## Install and run

```bash
python -m pip install .
energy-alpha-plan
energy-alpha-plan --capacity-mw 100 --reserve-fraction 0.15 \
  --load inference:40:critical:10 \
  --load training:30:standard:20 \
  --load batch:25:standard:50
python scripts/operate.py
```

## Python API

```python
from power_budget import Load, PowerEnvelope, plan_power

plan = plan_power(
    [Load("inference", 40, critical=True, priority=10), Load("batch", 30, priority=50)],
    PowerEnvelope(capacity_mw=100, reserve_fraction=0.15),
)
print(plan["planner_status"])
print(plan["admitted_loads"])
```

## Alpha / Omega boundary

Energy Alpha answers: **which modeled loads fit while preserving an explicit power reserve?**

Energy Omega may consume a resulting budget as an architectural peer, but this repository does not claim live cross-repository execution, telemetry, dispatch, switching, or control.

## Historical material

Older root-level power, grid, emergency, predictive, orchestration, and prior promotion artifacts remain for lineage. They are not imported by the installed product and do not establish facility-scale supply, live grid state, automatic transfer, generator/UPS dispatch, GPU power capping, energy-market optimization, or hardware control.

The previous repository-known HMAC `PROMOTED` mechanism is retired. A local repository cannot independently promote itself by signing its own status with a secret committed in its own source tree.

## Verify

```bash
python -m pytest -q
python scripts/verify_public_core.py
```

CI builds and installs the wheel, executes the installed CLI and direct operator on Python 3.11 and 3.13, rejects merge-conflict markers and unsupported public claims, and enforces an empty material gap matrix.

## Evidence boundary

This repository does **not** establish:

- xAI affiliation, proprietary facility data, grid telemetry, or deployment;
- any particular MW/GW datacenter scale, utility interconnect, generation capacity, or measured energy use;
- generator, UPS, transformer, switchgear, PDU, rack, or GPU power actuation;
- automated source transfer, real-equipment load shedding, grid services, market bidding, or demand response;
- production efficiency, availability, reliability, safety, or cost savings;
- live Energy Omega, MCP, control-plane, or agent-mesh connectivity.

The complete product is a local **power-budget and load-admission planner**, not a datacenter electrical control system.
