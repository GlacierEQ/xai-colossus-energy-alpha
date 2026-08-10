<<<<<<< HEAD
# Energy Alpha — Power Budget Evaluator
=======
# xAI Colossus Energy Alpha — Primary Power Distribution & Management ⚡

> **Primary power distribution unit management for 150MW+ GPU datacenter with demand-response optimization.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue)]()
[![Domain](https://img.shields.io/badge/Domain-Power%20Systems-yellow)]()
>>>>>>> 621977d (docs(readme): upgrade to 3-section recruiter/engineer/mesh structure & update SHA-256 baseline)

A stateless power-budget component for compute-infrastructure scenario modeling.

<<<<<<< HEAD
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
=======
## 🎯 For Recruiters & Hiring Managers

This is the **primary power distribution controller** — managing electrical distribution from grid connection through switchgear to individual GPU rack PDUs. It demonstrates:

- **Load balancing** across multiple utility feeds with automatic transfer switching
- **Demand-response integration** with grid operator signals for peak shaving
- **Power quality monitoring** with harmonic analysis and voltage regulation
- **UPS coordination** managing battery backup state-of-charge and transfer timing

**Why this matters**: Power systems engineering at datacenter scale requires the same **electrical engineering, control theory, and reliability design** used in grid management, industrial power, and renewable energy integration.

---

## 🔬 For Engineers & Technical Reviewers

### Core Components

| Component | Language | Purpose |
|---|---|---|
| `src/energy_alpha.py` | Python | Power distribution, load balancing, UPS coordination |
| `tests/` | Python | Power failure cascade simulation |

---

## 🤖 ML/AI & Programmatic Mesh Integration

- **MCP Tool**: `power_status()` — power distribution state queryable by energy optimization agents
- **Mastermind Sidecar**: Publishes power alerts to APEX Highway mesh
- **AI Extension**: Load forecasting model for proactive demand-response participation

```python
power = await mcp_client.call_tool("colossus-energy-alpha", "distribution_status")
```

---

## ⚡ Quick Start

```bash
python3 src/energy_alpha.py
python3 tests/test_energy_alpha.py
```
>>>>>>> 621977d (docs(readme): upgrade to 3-section recruiter/engineer/mesh structure & update SHA-256 baseline)
