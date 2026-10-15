# WP4 collection foundation — 2026-10-13

## Implementation

- Added strict batch reconstruction against the pinned WP3 v3 / WP4 v2 manifest and each source text hash. The request payload keeps the original atom text without role prefixes or learned transformations.
- Added response validation using provider `data[*].index`, exact requested/returned model agreement, dimensions, finite float32 conversion and nonzero-vector quality. Shuffled response array order is accepted only when indexes map correctly; duplicate, missing or out-of-range indexes are rejected.
- Added immutable per-batch artifact writer for request/response evidence, quality JSONL, registry Parquet and raw float32 `.npy` files. Its manifest includes workspace-local file hashes and an explicit execution mode; Mock artifacts are never publishable as real measurements.
- Added a one-attempt DMX transport adapter with no retry, redacted error categories, exact response-schema validation and credential-free timing/request-ID evidence. It has been exercised only with an injected fake transport; no benchmark request was made.
- Added `scripts/wp4_mock_batch.py`, an offline end-to-end smoke CLI. It never reads credentials or sends an API request.

## Actual tests

- `pytest tests/semantic_measurement -q`: 16 passed.
- `pytest tests -q`: 167 passed, 3 existing Pydantic protected-namespace warnings.
- Offline smoke over real frozen plan batch 0: 10/10 mock vectors persisted, 0 API attempts, `publishable_as_real_measurement=false`; output `runs/wp4_mock_batch_qwen37_v2_001/`.
- Process-local workspace guard was applied for every potentially writing Python command; all generated research artifacts and Python temporary/cache files remained scoped to this project root.

## Open items

- Mock vectors are not semantic measurements and do not satisfy the WP4 embedding gate.
- Live DMX collection, real request-error evidence, resumable batch scheduler, atom-to-vector merged registry, drift sentinel and read-only retrieval API remain to be implemented or validated.
- The previously requested real pilot budget has not been confirmed in this stage. No benchmark text was sent to DMX.
