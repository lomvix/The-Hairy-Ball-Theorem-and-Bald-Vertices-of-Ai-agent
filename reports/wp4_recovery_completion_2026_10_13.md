# WP4 recovery implementation report — retry limit reached (2026-10-13)

## Scope and controls

The user approved a separate recovery cap of **130 API attempts and 250,000 accounting input tokens**, limited to at most two attempts per batch and retrying only no-response transport failures. This cap did not extend or rewrite the previous pilot/campaign ledgers. No WP5 work was performed.

The effective project root was `<WORKSPACE_ROOT>` on `D:` (114.77 GiB available at preflight, NTFS, no project-root Git worktree). Every potentially writing Python command invoked the process-local `scripts/Initialize-WorkspaceGuard.ps1`. Temp/cache files, plans, request and response evidence, vectors, tests and reports remained inside the project root. No package installation or global environment mutation occurred. Runtime: Python 3.12.4, requests 2.32.3, NumPy 1.26.4, PyArrow 14.0.2, pytest 9.0.3. The benchmark and WP3 source remained the previously frozen WP3 v3 dataset; no benchmark source was changed.

## Implementation and provenance

- New approved configuration: `configs/wp4/embedding_dmx_qwen37_recovery_v1.yaml`. Model/epoch remain DMX proxy `qwen3.7-text-embedding`, 2048D, `dmx_qwen37_epoch_001`; this remains the user-approved deviation from the WP4 task-book default `text-embedding-v4`.
- New input plan: `runs/wp4_plan_qwen37_recovery_v1/wp4_input_plan.json`. The 4,114 embedding units have the same content and cache keys as the previous campaign. The recovery inventory `runs/wp4_recovery_inventory_v1.json` pinned exactly 99 still-unmeasured batches / 984 inputs / 293,745 UTF-8 bytes. Estimated provider-reported input usage if all succeeded was 101,707 tokens, not a guaranteed upper bound. DMX monetary price remains unknown.
- New independent request/response/vector evidence and budget ledger: `runs/wp4_dmx_qwen37_recovery_v1/`. Attempt-specific paths preserve both failed and successful attempts without overwriting prior data.
- Code: added `scripts/wp4_recovery_inventory.py`, `scripts/wp4_collect_recovery.py`, `scripts/wp4_validate_recovery.py`, `scripts/wp4_assemble_recovery.py`, and retry-scheduler tests; updated the paid-scope allowlist in `src/semantic_measurement/planning.py` and the partial-registry validator.
- Rebuilt the causal index plan under `runs/wp4_evidence_plan_qwen37_recovery_v1/`; its report found zero future events, zero private/oracle atoms and zero unmapped context messages.

## Actual results and tests

| Recovery measure | Result |
|---|---:|
| API attempts | 120 / 130 |
| Successful batches | 93 / 99 |
| Valid new vectors | 924 |
| No-response transport attempts | 27, all `SSLError` |
| Provider-reported input tokens | 96,206 |
| Unknown usage accounting reservation | 103,855 |
| Reported plus reserved accounting total | 200,061 / 250,000 |
| Batches with two failed attempts | 6 |

The six unresolved batch indexes are **88, 112, 380, 393, 394 and 395**. All had `SSLError` on both attempts. Actual provider usage and monetary charges for the 27 failed attempts are unknown; `input_utf8_bytes + 1024` per attempt is the user-approved conservative reservation, not provider-reported usage. Ten attempt slots and 49,939 accounting tokens remain, but the separate two-attempts-per-batch restriction prevents another attempt on these six batches in this authorization.

A read-only scan checked 589 recovery JSON/JSONL evidence files against the project-local API key value and found zero occurrences; the key value was not printed or copied into the report.

Final recovery validation: `runs/wp4_dmx_qwen37_recovery_v1/validation_after_120.json`, **PASS_WITH_UNRESOLVED_USAGE**, zero integrity errors. Full test suite: **172 passed**, 3 existing Pydantic protected-namespace warnings.

The new immutable, non-frozen combined registry is `runs/wp4_partial_real_qwen37_recovery_v1/embedding_manifest.json`; its validation report is `runs/wp4_partial_real_qwen37_recovery_v1/validation_report.json`, **PASS**, zero errors. Across pilot, first campaign and recovery it records 4,054 `VALID` and 60 explicitly missing of 4,114 unique units; 8,284 valid and 215 missing of 8,499 atom-chunk links; all 3,640 decision rows are present, with 2,842 having no missing embedding reference. All raw vector files retain their original source paths and are not overwritten or synthesized.

## Gate and unresolved issues

**WP4 Gate: PARTIAL; `frozen_wp4_gate=false`.** The 60 vectors from six double-failed batches remain missing. The required drift sentinel has not been run, DMX proxy region is undisclosed, and this uses the explicitly approved substitute model rather than the task-book default. Do not publish frozen `emb_v001` or advance to WP5 on this basis.

Any third attempt on those six batches, any larger retry budget, or drift-sentinel paid calls require a new explicit authorization and a new versioned run plan. The remaining numerical budget in this recovery cannot override the approved per-batch retry limit.
