# WP5-A additional continuation report — 2026-10-14

## Gate and workspace

WP5-A remains **PARTIAL / NOT READY FOR WP6**. This stage extended E2 event-head coverage and ran a bounded E3 fixed-encoder artifact audit. It did not freeze a candidate encoder or enter WP6/WP5-B. The true root is `<WORKSPACE_ROOT>`, with 121,302,216,704 available D: bytes at preflight, no root `.git`, and no reparse point. Process-local temp/cache/bytecode paths were verified inside that root before writing. No external research file, installation, download, API call or sampling run was made.

Effective immutable artifacts are `runs/wp5_offline_v1/horizon_screen_v4/`, `representation_audit_v2/`, `validity_v3/`, and `continuation_validation_v3.json`. Intermediate `horizon_screen_v3/` incorrectly applied the future-action survival mask to event heads and is **superseded**; its metrics must not be used. Intermediate `representation_audit_v1/` used a common history-slot coordinate permutation, which is geometrically invariant and is also **superseded**. Both were retained rather than overwritten.

## E2 five-head offline screening

Pinned WP3 `environment_deltas` now distinguish `changed=true` exact state changes from mere delta-record presence. The horizon target builder stores future labels separately from state features and validates every transition's delta ID. The five binary heads are natural terminal within the next L closed-loop transitions, the L-th next Agent action (ACT versus COMMUNICATE, masked after terminal), any observed user event, any tool execution, and any exact environment change in the observed up-to-L window. The latter three are *event-occurrence proxies*: they do not amount to user intent, tool success, or a full environment-delta category model. L={1,2,4,8}; all event/terminal heads include all 443 TEST decisions and 401 VALIDATION decisions. Only future-action is survival-masked. Source actions, environment changes and future events remain target-only and are never placed into encoder inputs.

Across seven fixed representations, four horizons and five heads, the v4 output has 11,324 Study target rows, 280 metric rows and 110,488 held-out prediction rows. TEST examples (nine Task UID clusters; Δ is task-balanced B1-history-2 minus B0, with 95% 1,000-resample task-bootstrap interval):

| Head | L | B0 NLL | B1-history-2 NLL | Δ NLL [CI] |
|---|---:|---:|---:|---:|
| Any user event | 1 | 0.688 | 0.675 | −0.029 [−0.166, +0.104] |
| Any tool execution | 1 | 0.571 | 0.566 | −0.015 [−0.150, +0.107] |
| Exact environment change | 1 | 0.411 | 0.464 | +0.044 [−0.028, +0.109] |
| Any user event | 4 | 0.314 | 0.355 | +0.045 [−0.048, +0.199] |
| Any tool execution | 4 | 0.313 | 0.364 | +0.053 [−0.016, +0.150] |
| Exact environment change | 4 | 0.760 | 0.925 | +0.189 [+0.021, +0.369] |

The pooled NLL and task-balanced Δ use different weighting, so they need not have the same sign. This is a predictive proxy comparison, not a causal ablation or sufficiency proof. Tool *execution outcome* and full environment delta category remain unmodeled because the public WP3 table exposes transition tool IDs and coarse action effects, not a validated outcome label per execution. E2 residual-history analysis remains limited to nested B0/B1 held-out loss comparisons; no separate conditional residual learner was trained.

## E3 projection/geometry controls and State Validity Map

Two new target-free feature builds repeated the same 2,831 Study decisions with random-projection seeds 503102/503103, alongside the original 503101. The audit also truncates 32 projected coordinates to 16/8 as a fixed-dimensional control and uses a deterministic **per-state** two-slot history-order perturbation for B1-history-2. For each of 443 TEST query decisions, its 10 nearest TRAIN candidates are restricted to the same Agent model and domain. This avoids same-task train/test leakage but does **not** establish task/policy-equivalent state pairs. Nine-test-task bootstrap intervals are reported in the audit table.

Task-balanced top-10 overlap with the base projection:

| Representation | Seed 503102 | Seed 503103 | 16D truncation | 8D truncation | Per-state history-order perturbation |
|---|---:|---:|---:|---:|---:|
| B0 current | 0.543 | 0.567 | 0.695 | 0.546 | — |
| B1 history-2 | 0.637 | 0.652 | 0.738 | 0.608 | 0.684 |

The B0 seed-503102 overlap interval is [0.483, 0.598]; B0 seed-503103 is [0.524, 0.615]. Neighborhoods are therefore materially representation-dependent. These are **fixed random-projection** controls, not learned-encoder seed/dimension audits or branch-support estimates. The 8/16D controls zero coordinates from the same 32D projection; they are not independently trained embeddings. No raw kNN graph is treated as a smooth manifold or a repair trajectory.

The updated 2,831-row State Validity Map carries the mean two-seed B0 top-10 overlap for the 443 TEST decisions only; it retains `data_density=null`, `branch_status=PENDING_WP6`, and `candidate_representation_id=null` in the alignment contract. The 2,655 `PENDING_BRANCH_CONFIRMATION` / 176 `WEAKLY_SUPPORTED` labels remain WP4 visibility-quality annotations, **not** evidence of conditional state equivalence. No anchor priority or aliasing pair is frozen: same Agent/domain is insufficient to guarantee comparable task/policy/tool conditions.

## Verification and next work

`continuation_validation_v3.json`: **PASS, 0 errors**. It verifies immutable hashes/sizes and lineage for the horizon, audit and validity outputs; target/feature Study alignment; natural-terminal masks; exact-change versus delta presence; complete event-head TEST/VALIDATION coverage; prediction loss; E3/validity row coverage and no unsupported branch claim. Full guarded local suite: **191 passed, 0 failed**, with three pre-existing Pydantic namespace warnings. No Sentinel entered features or fitting/evaluation; no oracle table was loaded; API calls: **0**.

Still required for WP5-A Gate: a justified and frozen candidate encoder (B5 or stronger controls), learned-encoder seed/dimension/task-bootstrap stability, more defensible task/policy/tool-conditioned local support and aliasing candidates, a stronger residual-history test, validated tool-outcome/environment-category targets where observable, and an Anchor Priority design that includes independent random controls. The unknown Agent-context truncation status for every decision and prior Scout task-selection bias remain. WP5-B strict/approximate distributional sufficiency remains `UNIDENTIFIED` until WP6 branch data exist.
