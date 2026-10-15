# WP5-A initial offline screening report (2026-10-13)

## Scope and boundary

User instruction: enter WP5. This stage implements a frozen-input inventory, Task UID group split, seven deterministic E1 feature controls and a held-out **one-step action-function prediction proxy**. It does **not** implement E2 multi-step sufficiency, E3 representation stability, E4 repair alignment, WP5-B branch confirmation or WP6 sampling. Current WP5-A Gate is **PARTIAL**; no encoder or Anchor Priority was frozen for WP6.

Effective project root `<WORKSPACE_ROOT>` on D: passed process-local workspace guard. Preflight free space was 123,054,616,576 bytes; root is not a reparse point and has no `.git` directory. `TEMP/TMP/TMPDIR`, pip/uv/HF/PyTorch/Jupyter/Matplotlib/Numba/bytecode/joblib caches were redirected inside the project by `scripts/Initialize-WorkspaceGuard.ps1` before writing Python commands. No installation, download, external database, model API or other paid call occurred. Runtime: Python 3.12.4, NumPy 1.26.4, PyArrow 14.0.2, scikit-learn 1.4.2. Benchmark commit remains `fc0055dc4e0a316c3f83133267fbd6faaa770992`.

## Input audit and split

The pinned config is `configs/wp5/offline_v1.yaml`. Effective immutable artifacts are:

- `runs/wp5_offline_v1/plan_v3/input_plan.json` (SHA-256 `d4d3cc44cb373339c9ccc5f641f98348e5a51d34c71a34746d35171eff1def02`);
- `runs/wp5_offline_v1/features_v2/feature_manifest.json` (SHA-256 `9f72fe47078ae3ce3fcfd51a66e6378952a9f5995c9d356e351f9893de05766f`);
- `runs/wp5_offline_v1/action_proxy_v1/evaluation_manifest.json` (SHA-256 `20ea013a6639fd2a97069910b6821987f7954041ef194fa48ac7d9b0f2155076`);
- `runs/wp5_offline_v1/action_proxy_validation_v2.json` (validation `PASS`, zero errors).

Upstream: frozen WP1 60-task registry, WP3 324-run public dataset, WP4 `emb_v001` with 4,114 valid 2048D measurements and 3,640 Agent decision indexes. The 324 runs resolve as **251 STUDY** and **73 SENTINEL**, including one valid replacement linked to its planned Study run. Sentinel contributed **809 Agent decisions**, excluded from the 2,831 Study feature rows and all model fitting/evaluation. No oracle table was opened; actions were read only into a separate target table after splitting. A causal feature check rejected any post-cutoff or private atom.

Per-domain deterministic Task UID grouping assigned **30 TRAIN / 9 VALIDATION / 9 TEST / 12 CURATION_DIAGNOSTIC** tasks. Study decisions: 1,461 / 401 / 443 / 526 respectively. The 12 diagnostic tasks are **not independent confirmation**: all 60 tasks were previously part of the WP2 Scout pool. Task IDs and run IDs are grouping/provenance fields, never model input.

## E1 pilot implementation and actual result

`src/behavioral_state/` and `scripts/wp5_*.py` added task/run provenance, deterministic causal feature extraction, held-out action proxy training and an independent integrity audit. All seven representations use the same 646-dimensional fixed layout, deterministic 32D projection of frozen WP4 vectors, the same binary `ACT` versus `COMMUNICATE` logistic head, the same train-only scaler and model/domain conditions. B0 uses latest available user/tool/policy measurements and the actual tool-name set; B1 adds the last 1/2/4/8 prior Agent utterances from the effective context; B2 uses role-wise EWMA of the actual effective context; B3 uses role-wise EWMA of harness-visible history. Long-text chunk aggregation is only a length-weighted **feature heuristic**, not a claim that the aggregate equals the original text's embedding. Encoder input includes present, truncation-unknown and source-quality masks. It excludes reward, gold, future events, target labels and pure identity UIDs.

Fixed-hyperparameter evaluation used 30 training tasks; validation and test tasks were never in fitting. Test results on 443 decisions from nine tasks:

| Representation | Test NLL | Task-balanced ΔNLL vs B0 | 95% task-bootstrap interval |
|---|---:|---:|---|
| B0 current | 0.6883 | 0 | [0, 0] |
| B1 history 1 | 0.7026 | +0.0002 | [-0.1197, +0.1236] |
| B1 history 2 | 0.6750 | -0.0285 | [-0.1554, +0.1081] |
| B1 history 4 | 0.6858 | -0.0486 | [-0.1889, +0.0822] |
| B1 history 8 | 0.8308 | +0.0682 | [-0.1318, +0.2916] |
| B2 effective | 1.0043 | +0.4279 | [+0.0164, +0.9022] |
| B3 observer | 0.7548 | +0.1110 | [-0.0565, +0.3266] |

The B1 history gains are uncertain: their task-cluster intervals cross zero. B2's poor result is a property of this fixed projection/EWMA/classifier pilot, **not** evidence that actual Agent context is harmful or that a representation is behaviorally sufficient. The nine-task test set and incomplete scout sample limit generalization. Task-cluster bootstrap used 2,000 resamples. The proxy produced 5,908 validation/test decision-prediction rows and 14 metric rows. No branch distance or strict `ε_L` was estimated.

## Tests and unresolved issues

Commands (all under the process-local guard): `scripts/wp5_plan_offline.py`, `scripts/wp5_build_features.py`, `scripts/wp5_evaluate_action_proxy.py`, `scripts/wp5_validate_action_proxy.py`, and `python -m pytest -q tests`. Validation returned `PASS`; full suite **184 passed, 0 failed**, with three pre-existing Pydantic protected-namespace warnings. Earlier `plan`, `plan_v2` and `features_v1` exploratory versions were retained, not overwritten; the manifest hashes above identify the effective versions.

Every Agent decision has `context_truncation_status=UNKNOWN` (3,640/3,640); this remains explicit and is not treated as `NOT_TRUNCATED`. Of WP4 Agent evidence rows, 202 are `PARTIAL_MAPPING`. A standalone persistent Agent memory mechanism is not established; B4 memory-aware effects are `NOT_TESTABLE` in this pilot. E2 multi-horizon action/tool/environment/user/terminal heads, residual-history tests, E3 seed/dimension/neighborhood stability, E4 repair-compatible alignment contract and a calibrated State Validity Map remain. These are required before freezing a candidate encoder and passing the WP5-A Gate to WP6. No WP6 work was started.
