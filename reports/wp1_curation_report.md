# WP1 Curation Implementation Report

## Current outcome

- Work package: WP1 Task Curation & Audit
- Effective project root: `<WORKSPACE_ROOT>`
- Gate: `WP1_COMPLETE`
- WP2: not started
- Real Agent API calls: 0
- Embedding API calls: 0

WP1 now has four deliberately separated evidence layers:

1. Contract-only Mock flow: validates schemas, audit semantics, deterministic stratification, shortfall reporting, storage, and CLI boundaries.
2. Pinned Hugging Face mirror: provides a reproducible 278-task candidate-source inventory, but does not claim official commit equivalence.
3. Pinned official checkout: provides the authoritative 278-task `base` inventory, tool/evaluator architecture audit, static effect profile, and deterministic 60-task candidate selection.
4. Official executable smoke: runs 3 seeded real tasks per domain through reference action replay, official component evaluators, five resets, deterministic prefixes, and negative controls.

`CuratedTaskRegistry-v1` and `pilot_selection_v1` are frozen. All 60 selected tasks were audited locally; gating NL/communication evidence gaps remain explicit `CONDITIONAL` statuses rather than fabricated judgments.

## Implemented architecture

- Strict Pydantic identity, provenance, task-profile, audit, eligibility, and selection models.
- Canonical task UID/content hashing and full-commit validation.
- Workspace-contained atomic JSON/JSONL/Parquet writers with SHA256 manifests.
- Deterministic domain x horizon x mutation selection with inclusion probabilities, weights, unique selection, and explicit deficits.
- Mock, Hugging Face static, and official static adapters that do not overclaim unavailable execution capabilities.
- Process-local workspace guard for temp, cache, configuration, runtime, Hugging Face, Python bytecode, and test paths.
- Reusable output validation and regression tests.

## Stage results

| Stage | Inventory | Selection | Tests | Status |
|---|---:|---:|---:|---|
| Mock | 27 | 27 of requested 60; honest shortfall 33 | included in suite | Mock only |
| HF pinned mirror | 278 | not run; mutation semantics unavailable | 14 passed at stage | Candidate source only |
| Official `v1.0.1` static | 278 | 60 unique, 20/domain | 17 passed final | Candidate, not frozen |
| Official executable smoke | 9 (3/domain) | Seeded audit sample | 29 passed final | Minimum smoke passed |
| Official executable pilot | 60 (20/domain) | Frozen selection, no outcome replacement | 30 passed final | WP1 complete |

Official source: `sierra-research/tau2-bench` tag `v1.0.1`, commit `fc0055dc4e0a316c3f83133267fbd6faaa770992`. The checkout is clean, detached, MIT-licensed, and stored entirely inside `third_party/`.

Official static eligibility remains 0 eligible, 278 conditional, and 0 quarantined because that immutable artifact records the earlier static-only evidence layer. Dependencies were subsequently installed in an isolated workspace environment and the separate executable sample below adds runtime evidence without silently rewriting the static audit.

The separate executable sample produced 5 eligible, 4 conditional, and 0 quarantined tasks. All 9 reset checks were stable; 8/9 reference trajectories and prefix suites executed without tool errors. Retail task `4` consistently references a missing product. Two telecom DB mismatches are non-gating diagnostics: their declared environment assertions pass and official reward remains 1.0.

The full selected pilot produced 38 eligible, 22 conditional, and 0 quarantined tasks. All 60 reset checks were stable and all 60 complete reference trajectories executed without tool errors. All 57 applicable prefix suites were stable; 3 zero-action tasks were correctly marked not applicable. The selected UID set exactly matched the static candidate selection, so no result-driven task replacement occurred.

## Reproducibility and outputs

- Mock outputs: `runs/wp1_mock_v001/`; four static data hashes matched the repeat run.
- HF outputs: `runs/wp1_hf_candidate_ec3f3dbee04ce793378e0eb48b6dc258b01fdc69/`; four static data hashes matched the repeat run.
- Official outputs: `runs/wp1_official_static_fc0055dc4e0a316c3f83133267fbd6faaa770992/`; five core output hashes matched the repeat run.
- Executable smoke: `runs/wp1_executable_smoke_fc0055dc4e0a316c3f83133267fbd6faaa770992/executable_audit.json`; 49 reference actions across 9 real tasks.
- Executable pilot: `runs/wp1_executable_pilot_fc0055dc4e0a316c3f83133267fbd6faaa770992/executable_audit.json`; 228 reference actions across all 60 selected tasks.
- Final registry: `runs/wp1_final_v1_fc0055dc4e0a316c3f83133267fbd6faaa770992/`; registry, executable audit, and selection are published as JSONL/Parquet/JSON with a final manifest.
- Official independent validation confirmed 278 inventory rows, 278 audit rows, identical unique UID sets, valid manifest hashes, and a balanced 60-task candidate selection.

Detailed evidence:

- `reports/workspace_guard_report.md`
- `reports/hf_dataset_acquisition_report.md`
- `reports/wp1_hf_candidate_inventory_report.md`
- `reports/wp1_official_static_inventory_report.md`
- `reports/wp1_executable_audit_report.md`

## Workspace boundary

All project-related downloads, Git checkout data, caches, temp files, bytecode, test artifacts, outputs, and reports are beneath the effective project root. Guarded write variables point to `.workspace_*` or `runs/`; no reparse points were found. No global package installation, permanent environment mutation, credential read, or C-drive research write was performed.

## Remaining issues

1. The pip-resolved local official environment is recorded but is not an exact `uv.lock` recreation because `uv` is unavailable.
2. Gating NL assertions remain untested by design; communication requirements without gold assistant utterances remain conditional.
3. Create/delete/irreversible effect labels are not derivable from ToolType alone and remain explicitly unknown.
4. Producer code provenance is `UNVERSIONED_WORKSPACE` because this implementation root has no Git repository.

## Frozen handoff hashes

- Registry JSONL: `968e2742ebae4ea74044276203b5388f98dbe0d4dcaa4246c14df2a6e680f73b`
- Selection: `4d9a0cdba356bd8b130f1b0f7de8555619e495c496ccf43e0d94c66888902b4d`
- Final manifest: `f7d75b6f4580d51af99c7734259c14ad4aeb6d1817272da667194aa6ba27621f`
- Independent validation: PASS

No large-scale API sampling is authorized or performed. WP2 must not start until WP1 passes its gate and the user explicitly confirms progression.
