# WP1 Official Static Inventory Report

## Status

- Stage: official-source architecture audit and static Task Inventory
- Benchmark: `sierra-research/tau2-bench`
- Tag: `v1.0.1`
- Commit: `fc0055dc4e0a316c3f83133267fbd6faaa770992`
- Task split: `base`
- Gate: `PARTIAL`
- WP2: not started

This stage establishes a source-pinned official inventory and a reproducible candidate selection. It does not publish `CuratedTaskRegistry-v1`: official evaluator execution, environment reset, and deterministic action-prefix replay have not yet been run.

## Source and architecture findings

- The official checkout is a clean detached checkout of `v1.0.1` at the full commit above. The repository license is MIT; `LICENSE` SHA256 is `e67c5aa0074dfcaefd3c3a1aedb94cb539234aecd15d5a972574e3200e6252fe`.
- Checkout evidence is recorded in `third_party/manifests/tau2-bench-v1.0.1.json`; its SHA256 is `5ec0a7784b3f2156b0e92941126514f23e830b082b6c1bedf37c829f57987180`.
- Official tasks are loaded from `data/tau2/domains/<domain>/tasks.json` and filtered through the declared `base` IDs in `split_tasks.json`.
- Tool effects are read without importing the benchmark: `tools.py` and `user_tools.py` are parsed with Python AST for `@is_tool(ToolType.READ|WRITE|GENERIC)`.
- The official evaluator distinguishes DB/environment assertions, reference actions, communicated information, and natural-language assertions. Reference actions are treated as grading evidence, not as a unique valid trajectory.
- The official project declares Python `>=3.12,<3.14` and a uv-based environment. Those dependencies were not installed or executed in this stage.

## Hugging Face comparison

The pinned Hugging Face source remains useful acquisition evidence, but it is not used as proof of official-commit identity:

- Airline and retail have the same base task IDs but different `tasks.json` content hashes.
- The Hugging Face telecom `tasks.json` has 114 tasks, while official `tasks.json` has 2,285; the 114 IDs are the official `base` split.
- The Hugging Face `telecom/tasks_full.json` matches the official full telecom task file by content hash.

Therefore the official checkout is the authoritative source for this stage, and the HF records retain their separate `CANDIDATE_SOURCE_ONLY` provenance.

## Implementation

- `src/curation/official_adapter.py`: exact-commit verification, split filtering, canonical task bytes, evaluator-component discovery, AST tool-type extraction, and explicit refusal to claim reset/replay execution.
- `src/curation/official_static.py`: identity/profile/audit generation, within-domain horizon tertiles, ToolType-based read/write mutation bins, deterministic candidate selection, JSONL/Parquet output, and content manifest.
- `src/curation/cli.py`: `official-static-inventory` dry-run and execution path.
- `configs/curation/tau3_wp1.official_v1_0_1.yaml`: pinned source, base split, seed, and 20-per-domain target.
- `scripts/validate_official_static_output.py`: independent row-count, UID, domain balance, eligibility, hash, and repeatability checks.
- `tests/curation/test_official_static_adapter.py`: split filtering, missing-ID rejection, tool parsing, and static-adapter execution refusal.

## Actual results

| Metric | Result |
|---|---:|
| Inventory rows | 278 |
| Audit rows | 278 |
| Airline / retail / telecom | 50 / 114 / 114 |
| `ELIGIBLE` | 0 |
| `CONDITIONAL` | 278 |
| `QUARANTINED` | 0 |
| Candidate selection | 60 unique |
| Selected per domain | 20 / 20 / 20 |
| Real Agent API calls | 0 |
| Embedding API calls | 0 |

Observed evaluation-component presence is: actions 269, communicate-info 42, environment assertions 114, natural-language assertions 90, and reward basis 278.

Reference action ToolTypes were fully mapped: 448 `READ`, 721 `WRITE`, and 39 `GENERIC`; unmapped action names: 0. Mutation bins use only `WRITE` counts. Create, delete, and irreversible action counts remain null with explicit uncertainty reasons because ToolType does not encode those distinctions.

Horizon tertile thresholds based on reference-action counts are airline `[1, 3]`, retail `[3, 6]`, and telecom `[3, 6]`.

## Tests and reproducibility

1. Final guarded WP1 unit suite: `17 passed in 0.45s`.
2. CLI dry-run: passed and reported 0 real/Embedding API calls.
3. Official static inventory execution: passed.
4. Independent validation: 278 JSONL and 278 Parquet rows in each inventory/audit pair; unique/equal UID sets; manifest hashes valid; selection has 60 unique tasks and 20 per domain.
5. Independent repeat run: all five core output hashes were identical.
6. Final boundary check: all guarded write variables resolved beneath the project root, no reparse points were found, official HEAD matched the pinned commit, tag was `v1.0.1`, and checkout status was clean.

Two environment/diagnostic command failures were retained in the run history: an initial pytest command omitted the process-local execution-policy bypass/PYTHONPATH setup, and one nested PowerShell boundary-print command expanded variables too early. Neither reached research execution or modified the generated outputs; corrected guarded commands passed.

## Outputs and hashes

Output directory: `runs/wp1_official_static_fc0055dc4e0a316c3f83133267fbd6faaa770992/`

| File | SHA256 |
|---|---|
| `task_inventory.official_static.jsonl` | `9107bd6727f9c5f34652a364ca1a56cc9634d319c6043848a8ff01d4c1da8e2a` |
| `task_inventory.official_static.parquet` | `cfae1efbe781148148b8c210388bb4a0df0a465748d5442aa10c27441d6143af` |
| `task_audit.official_static.jsonl` | `900a3c9e17480213885b05d94e9f21e15676b69c88b84fe70049e7cbaf40b732` |
| `task_audit.official_static.parquet` | `6c339c466fc14be3a46c1246ce81d80364543161dabc3c3bc2279d7bdf5b81a3` |
| `pilot_selection.candidate.json` | `4d9a0cdba356bd8b130f1b0f7de8555619e495c496ccf43e0d94c66888902b4d` |
| `dataset_manifest.official_static.json` | `3368d9d6efca9455bb9d491c206f49a4f60cdbdc1ef861a4ff33eb5a94c7f463` |

The config SHA256 is `1306725321b320966bbba5d1fa275744edfa701ae47d4e29523f2ab0000decaf`. The byte-identical repeat is in `runs/wp1_official_static_fc0055dc4e0a316c3f83133267fbd6faaa770992_repeat/`.

## Unresolved issues and next WP1 gate

1. Install the official benchmark dependencies only into a workspace-local environment after an explicit dependency/write-path review.
2. Execute the minimum per-domain real smoke, official grader-component tests, five-reset semantic-state checks, and deterministic action-prefix replay at 25%, 50%, and 75%.
3. Classify failures into eligible, conditional, or quarantine with evidence; do not infer reset reliability from static source inspection.
4. Refine create/delete/irreversible effects from verified tool semantics rather than action-name heuristics.
5. Freeze registry and selection hashes only after the executable audit passes. The current 60-task file is `CANDIDATE_NOT_FROZEN`.
6. The implementation workspace itself has no Git repository, so producer code provenance remains `UNVERSIONED_WORKSPACE`.

WP1 remains `PARTIAL`. Do not enter WP2 without a frozen registry and explicit user confirmation.
