# WP4 sentinel and final-repair implementation report (2026-10-13)

## Scope and authorization

The user approved a new, separate hard limit of **22 DMX requests and 100,000 accounting input tokens**: at most 10 one-shot requests to remeasure about 100 drift-sentinel texts, followed (unless drift was confirmed) by at most two attempts for each of the six missing embedding batches. This did not extend or rewrite earlier ledgers. No WP5 work was performed.

The effective root was `<WORKSPACE_ROOT>` on `D:` with 114.65 GiB free at preflight. Every writing Python command used the process-local `scripts/Initialize-WorkspaceGuard.ps1`; request/response evidence, vectors, caches, temporary files, tests and reports stayed inside the project root. No package installation or global environment mutation occurred. A read-only scan of 57 new-run JSON/JSONL files found zero occurrences of the local API key value; the key was never printed or copied into this report.

## Frozen plan and implementation

- Configuration: `configs/wp4/embedding_dmx_qwen37_sentinel_repair_v1.yaml`; model remains the previously approved DMX proxy `qwen3.7-text-embedding`, 2048D, `dmx_qwen37_epoch_001`. This is still a documented deviation from the WP4 task-book `text-embedding-v4` default; proxy region remains undisclosed.
- Input plan: `runs/wp4_plan_qwen37_sentinel_repair_v1/wp4_input_plan.json`, the same 4,114 unique text units and 8,499 atom-chunk links as earlier WP4 plans. The new causal evidence plan under `runs/wp4_evidence_plan_qwen37_sentinel_repair_v1/` reports zero future events, zero private/oracle atoms and zero unmapped context messages.
- The immutable `runs/wp4_sentinel_repair_plan_v1.json` selected 100 already measured texts deterministically: 32 USER, 32 AGENT, 10 error-like TOOL_RESULT, 24 other TOOL_RESULT and 2 POLICY units. It pinned original vector hashes, text hashes, thresholds, the six repair batch indexes, and all budgets before API calls. Sentinel input was 19,567 UTF-8 bytes; an all-requests-fail reservation check was 75,241 tokens, below the approved 100,000 cap. Dry-run made zero API calls.
- New code: `scripts/wp4_plan_sentinel_repair.py`, `scripts/wp4_collect_sentinel.py`, `scripts/wp4_analyze_sentinel.py`, `scripts/wp4_collect_final_repair.py`, `scripts/wp4_validate_final_repair.py`, `scripts/wp4_assemble_final_repair.py`; updated the paid-scope allowlist and partial-registry validator, with drift-threshold unit tests.

## Actual measurements

| Phase | Attempts | Successful batches | Provider-reported input tokens | Unknown usage reserved | Accounting total |
|---|---:|---:|---:|---:|---:|
| Sentinel | 10 / 10 | 7 / 10 (70 valid text pairs) | 4,469 | 9,215 | 13,684 |
| Six-batch repair | 8 / 12 | 4 / 6 (40 valid new vectors) | 4,110 | 14,644 | 18,754 |
| **New authorization total** | **18 / 22** | — | **8,579** | **23,859** | **32,438 / 100,000** |

All seven no-response attempts in this authorization were `SSLError` (three sentinel and four repair). Their true provider usage and monetary charges are **unknown**; the `input_utf8_bytes + 1024` per-attempt reservation is accounting, not provider-reported usage. DMX price remains unknown.

Sentinel comparison: `runs/wp4_sentinel_repair_v1/sentinel_analysis/sentinel_drift_report.json`, validation `PASS`, **drift status `INCONCLUSIVE`** because only 70 of the prespecified minimum 80 pairs returned. Among those 70, median cosine distance was about 1.03×10⁻⁶ and maximum 1.76×10⁻⁶; median relative norm change was about 1.91×10⁻⁸ and maximum 9.28×10⁻⁸. These small observed differences do not establish absence of drift for the unobserved texts. Drift was not confirmed, so the six-batch repair proceeded with explicit provisional status.

Repair validation: `runs/wp4_sentinel_repair_v1/repair/validation_after_008.json`, `PASS_WITH_UNRESOLVED_USAGE`, zero integrity errors. Batches 88, 112, 393 and 395 succeeded; batches **380 and 394** failed twice each and were not attempted a third time. Four request slots and 67,562 accounting tokens remain numerically, but the sentinel 10-request limit and per-batch two-attempt limit are exhausted for their respective tasks.

The new non-frozen registry is `runs/wp4_partial_real_qwen37_final_repair_v1/embedding_manifest.json`, with validation `runs/wp4_partial_real_qwen37_final_repair_v1/validation_report.json` reporting `PASS`, zero errors. It contains **4,094 VALID and 20 UNKNOWN** of 4,114 unique embedding units; 8,374 valid and 125 missing of 8,499 atom-chunk links; all 3,640 decision rows, 3,237 without a missing embedding reference. Original vector files were not overwritten or synthesized. The complete local test suite passed: **177 passed**, with three existing Pydantic protected-namespace warnings.

## Gate and unresolved issues

**WP4 Gate: PARTIAL; `frozen_wp4_gate=false`.** Twenty vectors still lack a valid measurement, and the drift sentinel is `INCONCLUSIVE`, not a clean stability clearance. The proxy region is undisclosed and the approved model substitutes for the task-book default. The current registry must not be published as frozen `emb_v001`, treated as proof of a stable embedding epoch, or used to start WP5.

Any additional sentinel retries or third attempt on batches 380/394 requires a new explicit scope and hard budget. Before paying for more attempts, investigating the recurring DMX SSL transport failure would improve the likelihood of obtaining the missing measurements.
