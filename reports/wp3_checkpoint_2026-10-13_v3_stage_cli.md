# WP3 checkpoint v3 — staged CLI closure

Date: 2026-10-13. Status: **PASS for the stage-CLI follow-up**. The frozen 324-run WP3 dataset and WP2 sampling state were not modified. No LLM or Embedding call was made; WP4 was not started.

## Implementation

Added `scripts/wp3_stages.py` with all task-book commands: `compatibility-audit`, `build-events`, `build-decisions`, `build-transitions`, `validate`, and `finalize`. The per-run build stages recompute from the pinned raw WP2 run and verify the preceding stage before writing a new, non-overwriting output directory. Stage context records source-run manifest and producer-code hashes. Stage manifests record exact table sets, counts, file sizes, and SHA-256 hashes; `validate` compares their JSONL content to a fresh canonical reconstruction and checks Parquet row counts. `finalize` verifies every staged JSONL/Parquet file against the resulting canonical run bundle.

The CLI is intentionally per-run. The existing `scripts/wp3_build_full.py` remains the bounded-memory frozen-corpus builder, and `scripts/wp3_validate_dataset.py` remains the merged-dataset validator. This avoids rebuilding the 324-run archive solely to add a command facade.

## Actual tests

- Six CLI commands: PASS. Compatibility audit regenerated the exact prior SHA-256 `d6792c054dc133d93b442960bedc75171d95df1c3a6f0e0bbaee0c7a6d3fcaac`.
- One archived run completed all five build/validation/finalization steps. Output: 177 events, 59 native links, 36 decision frames, 30 actions, 38 transitions, and 1 private TASK atom plus 1 private Oracle label. Final run-manifest SHA-256: `c188248b441e6e5efe876e8696d4abeb0e150de86f94d2a9624b9393dac26625`.
- Negative tests confirm rejection when a stage omits a required table file or a staged file changes after manifest creation.
- Whole-project regression: **150 passed**, 3 pre-existing Pydantic protected-namespace warnings.
- Workspace guard: PASS for offline local work; all process-local temp/cache paths stayed under `<WORKSPACE_ROOT>`.

## Remaining boundary

This closes the CLI gap listed in checkpoint v2, not the scientific limits: 35 `calculate` effects remain UNKNOWN; context truncation and hidden external state do not justify full Markov-state recovery; no Level-3/WP6 closed-loop checkpoint validation has occurred. Oracle tables remain directory-separated but are not protected by operating-system access-control rules in this local workspace.

Evidence: `runs/wp3_stage_cli_smoke_v2/stage_validation.json`, `runs/wp3_stage_cli_smoke_v2/stage_finalize.json`, and `runs/wp3_stage_cli_compatibility_audit_v2.json`.
