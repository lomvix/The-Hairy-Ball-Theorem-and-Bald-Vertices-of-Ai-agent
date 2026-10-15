# WP1 Hugging Face Candidate Inventory Report

## Status

- Stage: WP1 static Inventory from a pinned Hugging Face mirror
- Source: `HuggingFaceH4/tau2-bench-data`
- Source revision: `ec3f3dbee04ce793378e0eb48b6dc258b01fdc69`
- Output schema: `wp1.hf_candidate.v1`
- Gate: `PARTIAL`
- WP2: not started

This stage creates a source-scoped candidate inventory. It does not claim equivalence to an official Sierra benchmark commit and does not publish `CuratedTaskRegistry-v1`.

## Implemented changes

- Added `HuggingFaceStaticDatasetAdapter`, which validates local HF revision metadata, unique nonblank task IDs, containment, and per-task canonical content.
- Added `CandidateInventoryRecord` with explicit `HF_MIRROR`, source repo/revision, `official_benchmark_commit=null`, and `CANDIDATE_SOURCE_ONLY` status.
- Added deterministic reference-action horizon profiling and domain-specific tertile bins.
- Added component-presence extraction from actual `evaluation_criteria` objects.
- Added atomic Parquet output alongside canonical JSONL.
- Added `hf-candidate-inventory` CLI and pinned config.
- Added three adapter tests for normal inventory, revision mismatch rejection, and refusal to claim reset/prefix replay.

## Data results

| Domain | Candidate tasks | Horizon tertile thresholds |
|---|---:|---|
| airline | 50 | `[1, 3]` reference actions |
| retail | 114 | `[3, 6]` reference actions |
| telecom | 114 | `[3, 6]` reference actions |
| Total | 278 | — |

Evaluation component presence across tasks:

- `actions`: 269
- `communicate_info`: 44
- `nl_assertions`: 58
- `env_assertions`: 114
- `reward_basis`: 114

All 278 task IDs and generated task UIDs are unique. Inventory and audit UID sets are identical.

Eligibility results:

- `ELIGIBLE`: 0
- `CONDITIONAL`: 278
- `QUARANTINED`: 0

Every record remains conditional because upstream commit equivalence, official grader execution, environment reset, and prefix replay are not available from the static mirror.

## Scientific boundary decisions

- `reference_action_count` is recorded because it is directly present in the task file.
- `horizon_bin` is a deterministic within-domain reference-action-count tertile proxy.
- `mutation_bin`, read/write/create/delete counts, and irreversibility remain null with explicit uncertainty reasons.
- Action names were not used to guess tool effects.
- Gold/reference actions are not treated as the unique successful route.
- No selection was run because WP1's horizon × mutation design cannot be satisfied without verified tool semantics.

## Commands and validation

1. Full WP1 unit suite after adapter implementation: `14 passed in 0.50s`.
2. Candidate CLI dry-run: passed; reported 0 Agent and 0 Embedding API calls.
3. Candidate Inventory execution: passed; produced 278 inventory and 278 audit rows.
4. Parquet validation: 278 unique inventory UIDs, 278 unique audit UIDs, equal UID sets, all official commits null, all mutation bins null.
5. Independent repeat execution: all four static output hashes matched.

Two exploratory shell formatting commands failed while printing validation summaries (tuple-key JSON serialization and quoting). They did not alter outputs; the corrected read-only validation command passed.

## Outputs and hashes

Output directory: `runs/wp1_hf_candidate_ec3f3dbee04ce793378e0eb48b6dc258b01fdc69/`

| File | SHA256 |
|---|---|
| `task_inventory.hf_candidate.jsonl` | `944613bd644a4f8f3ae9ff2d9bf72189cd82f842640a824478cd12d48cefa7d2` |
| `task_inventory.hf_candidate.parquet` | `7a88b68c13e10368004bca07a28f57f55de6be2f5e6ed892a0cd9143b004d611` |
| `task_audit.hf_candidate.jsonl` | `8442309e211e5e4c32cdc73c0a02231c6c7e16ed42fc9235ebfaac61249d7a37` |
| `task_audit.hf_candidate.parquet` | `6ebd47b778cd7d58e2267e689bc468bdfe3087f77e4982cc55ec6c139ccf7321` |
| `dataset_manifest.hf_candidate.json` | `1df9bfab97405a9cad8e1666d014c6080e509ba29df9140972093f79727d02c4` |

Independent repeat directory: `runs/wp1_hf_candidate_ec3f3dbee04ce793378e0eb48b6dc258b01fdc69_repeat/`.

Config SHA256: `a71d04968bd69d55e535f83f513f8b9d91d6d36cdf8f9852517b68e959c849d3`.

## API and workspace accounting

- Agent API calls: 0
- Embedding API calls: 0
- LLM Judge calls: 0
- Additional downloads in this stage: 0
- Cost: 0
- All generated files, PyArrow temporary files, caches, logs, and repeat artifacts stayed within the workspace guard paths.

## Remaining WP1 blockers

1. Exact official `sierra-research/tau2-bench` full commit corresponding to this data is unknown.
2. Official tool schemas and tool implementations are absent.
3. Official grader/evaluator execution is unavailable.
4. Reset reliability and deterministic prefix replay cannot be tested.
5. Mutation strata and the final 60-task Pilot selection cannot be frozen.
6. The project still lacks a Git commit for producer-code provenance.

WP1 remains `PARTIAL`; do not enter WP2.

