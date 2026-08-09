# Energy Alpha — Power Budget Evaluator

A stateless power-budget component for compute-infrastructure scenario modeling.

> **Independent portfolio project.** This repository is not affiliated with, endorsed by, employed by, or deployed at xAI. It does not claim proprietary Colossus data, facility access, grid telemetry, or operational power authority.

## Recruiter view

The canonical public implementation is [`src/power_budget.py`](src/power_budget.py). Given caller-supplied loads, modeled capacity, and a reserve fraction, it calculates used power, reserve, remaining headroom, critical-load concentration, and a bounded scenario status.

Current verified behavior:

- sums modeled MW demand from caller-supplied loads;
- reserves a configurable fraction of modeled capacity;
- reports remaining headroom and oversubscription;
- identifies a `CRIT_HEAVY` modeled state when critical demand dominates available capacity;
- performs no grid query, telemetry read, load switch, or external action.

This is a deterministic budget evaluator, not a live grid or facility energy-management system.

## Canonical proof paths

| Path | Role |
|---|---|
| `src/power_budget.py` | stateless modeled power-budget evaluator |
| `tests/test_power_budget.py` | deterministic nominal/oversubscription checks |
| `scripts/verify_public_core.py` | receipt-producing public verifier |
| `.github/workflows/ci.yml` | exact-branch Python truth gate |

Older experimental and integration-oriented files remain preserved but are not automatically promoted by this contract.

## Alpha / Omega relationship

Energy Alpha is architecturally paired with [`xai-colossus-energy-omega`](https://github.com/GlacierEQ/xai-colossus-energy-omega). Alpha computes modeled budget evidence; Omega models a priority-aware shedding decision. No live cross-repository runtime, grid connection, or facility control plane is claimed.

## Verify

```bash
python tests/test_power_budget.py
python scripts/verify_public_core.py
```

## Machine contract

```yaml
schema: glaciereq.component-surface.v1
repository: GlacierEQ/xai-colossus-energy-alpha
canonical_branch: master
role: SPECIALIST_COMPONENT
capability: modeled_power_budget_evaluator
evidence_level: TEST
external_queries: 0
external_actions: 0
grid_telemetry: false
hardware_actuation: false
runtime_pairing_with_omega: false
company_affiliation_claim: false
```

## Nonclaims

This repository does not establish xAI affiliation, proprietary access, production deployment, live grid/facility telemetry, breaker or load-control authority, measured PUE or energy savings, validation at a specific MW/GPU/rack scale, or physical-system safety certification.
