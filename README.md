# xai-colossus-energy-alpha

<!-- README-MESH:BEGIN -->
## Three-audience project map

### For recruiters and non-specialists

**What it does.** Calculates how much electrical power a compute-infrastructure scenario requires and how much reserve remains before any controller decides what to reduce.

- Turns a large infrastructure concern into an explicit, reviewable budget.
- Separates demand calculation from emergency response.
- Pairs with Energy Omega to demonstrate a complete requirements-to-control loop.

**Evidence:** [`src/power_budget.py`](src/power_budget.py) and [`tests/test_power_budget.py`](tests/test_power_budget.py).

### For senior engineers and domain experts

**Innovation and evolution.** Alpha owns stateless demand, capacity, and reserve-margin calculation. It avoids embedding load-shedding policy inside the power model, so the same evidence can support different controllers and scenario analyses. It evolved into the analytical half of the energy helix, consuming compute-placement demand from the server planner and supplying an explicit budget to Omega.

### For AI systems and toolchains

- Repository ID: `GlacierEQ/xai-colossus-energy-alpha`
- Default branch: `master`
- Protobuf package: `glaciereq.readme.v1`
- Typed role: consumes compute-demand context and provides power-budget evidence to Energy Omega.
- Canonical graph: [`manifests/readme_mesh.json`](https://github.com/GlacierEQ/job-app-helix/blob/main/manifests/readme_mesh.json)

```protobuf
repository: "GlacierEQ/xai-colossus-energy-alpha"
display_name: "Colossus Energy Alpha"
one_line_purpose: "Compute power demand, capacity, and reserve margins independently from control policy."
```

### Repository mesh

| Connected repository | Relationship | Combined value |
|---|---|---|
| [Energy Omega](https://github.com/GlacierEQ/xai-colossus-energy-omega) | consumed by | Power evidence becomes priority-aware load-shedding control. |
| [Colossus Servers](https://github.com/GlacierEQ/xai-colossus-servers) | receives capability | Compute placement supplies demand inputs for the power model. |
| [AKOS](https://github.com/GlacierEQ/AKOS) | governed by | Evidence and responsibility boundaries remain explicit. |

Real schema: [`proto/readme_mesh.proto`](https://github.com/GlacierEQ/job-app-helix/blob/main/proto/readme_mesh.proto).
<!-- README-MESH:END -->

**Alpha — what is required.** A stateless Colossus-class compute power-budget model paired with the Energy Omega control strand.

This is an independent xAI/Colossus problem-space project, not a claim of xAI employment, endorsement, proprietary data, or operational deployment.

## Fleet ops (transparent)

Integrity baselines and health sidecars, when present, are documented multi-repository operations. See [SECURITY_AND_FLEET_OPS.md](SECURITY_AND_FLEET_OPS.md).

## Helix strand

See [HELIX_STRAND.md](HELIX_STRAND.md) for the Alpha/Omega role.
