# WP4 10-attempt pilot completion — 2026-10-13

## Authorization and execution

- The user approved the remaining four requests under the original **10-attempt / 50,000 reported-input-token** boundary. The seventh total attempt (batch 5) succeeded. The eighth (batch 170) ended in a transport error without an HTTP status or usage report, so its request may or may not have reached DMX. It was counted as an API attempt, not retried, and its request evidence remained in the project workspace.
- After the user explicitly approved continuation, the eighth attempt retained `reported_input_tokens=null` and received a **separate 8,224-token budget reservation**. This is an agreed accounting allowance, **not a provider-reported measurement or proof of the actual charge**. Two more requests (batches 309 and 333) succeeded; the counter reached **10/10** and all further calls stopped.
- All project writes and process-local temp/cache locations stayed within `<WORKSPACE_ROOT>` under the workspace guard. A read-only scan of 60 pilot JSON/JSONL files found zero occurrences of the configured API key value.

## Actual results and validation

- Successful requests: **9**; transport error with unknown usage: **1**; total attempts: **10**. Successful requests produced **90/90 valid** finite, nonzero, raw float32 vectors at 2048 dimensions from returned model `qwen3.7-text-embedding`.
- Provider-reported input tokens across the nine successful requests: **16,480**. Separately reserved for the unresolved request: **8,224**. Budget-accounting total: **24,704/50,000**; actual provider total remains **unknown** because the failed request had no response.
- Pilot validation: `runs/wp4_dmx_qwen37_pilot_v1/validation_v4.json` has **zero integrity errors**, 90 unique measured keys and status `PASS_WITH_UNRESOLVED_USAGE`. The status deliberately preserves the unknown eighth-request usage.
- New immutable partial registry: `runs/wp4_partial_real_qwen37_v3/`. The previous v1/v2 partial versions were not overwritten. Manifest status is `PARTIAL_PILOT_BUDGET_PAUSED`; **90 valid / 4,024 not collected** unique embedding units, **373 valid / 8,126 unknown** atom-chunk links, and all **3,640** Agent decision evidence rows. **1,907** decisions reference at least one real vector. Unmeasured vectors remain explicit missing values, never zeros or Mock data.
- Partial-registry validation: `runs/wp4_partial_real_qwen37_v3/validation.json` is **PASS**, zero errors, including file hashes, quality/registry consistency, missing masks and unchanged causal evidence fields.
- Full local test suite: `pytest tests -q` → **168 passed**, with 3 existing Pydantic namespace warnings.

## Remaining issues and gate

- No API attempts remain under this authorization. The failed eighth request's actual token usage and billing cannot be recovered from the local response because no response arrived. The 8,224-token reservation is a conservative budget decision authorized by the user, not a measured token count.
- This remains a **partial, non-frozen WP4 measurement**. 4,024 unique inputs and the planned drift-sentinel study remain unmeasured; DMX price and serving region remain unknown. Do not treat the partial manifest as `emb_v001` or enter WP5 on it.
- Further paid collection needs a new explicit budget/run plan. Safe offline next work includes read-only retrieval APIs, resumable full-batch scheduling and final quality/sentinel design.
