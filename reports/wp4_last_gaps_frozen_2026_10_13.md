# WP4 last-gap retry and frozen release (2026-10-13)

## Authorization and preflight

The user confirmed a new, separate hard ceiling of **10 DMX API attempts and 40,000 accounting input tokens**. Scope was only three previously failed sentinel batches (0, 1, 9) and two missing embedding batches (380, 394), each with at most two attempts. The offline plan `runs/wp4_last_gaps_plan_v1.json` fixed request payload hashes before any call. Dry-run made zero calls; the all-10-fail conservative reservation was 33,074 tokens. No earlier budget or raw artifact was modified.

Effective project root: `<WORKSPACE_ROOT>` on D:, with 123,061,886,976 free bytes at preflight. The project root itself was not a reparse point. There is no Git repository at this root, so no project commit can be reported. Every writing Python command ran with `scripts/Initialize-WorkspaceGuard.ps1`, which redirected temp, cache and bytecode paths into the project. All research artifacts for this round are inside the project root. No installation or persistent environment change occurred.

## Paid execution and accounting

Live evidence and the append-preserving ledger are in `runs/wp4_last_gaps_v1/`.

| Batch | Attempts | Outcome |
|---|---:|---|
| Sentinel 0, 1, 9 | 1 each | 30 valid new comparison pairs |
| Embedding 380 | 1 | 10 valid vectors |
| Embedding 394 | 2 | First attempt: SSL transport error with unknown usage; second: 10 valid vectors |

Total: **6 / 10 attempts**. Provider-reported input: **3,600 tokens**. Conservative reserve for the one SSL no-response attempt: **2,764 tokens**. Accounting total: **6,364 / 40,000 tokens**. The reserve is not a provider usage statement or a price estimate; actual monetary cost and the failed request's usage remain unknown. No additional paid calls were made for validation or release.

## Sentinel and release Gate

Combined with the prior seven successful sentinel batches, all **100/100** prespecified text pairs were measured, covering USER, AGENT, TOOL_RESULT error/other and POLICY. The predeclared drift classifier returned **`NO_DRIFT_DETECTED`**. Median cosine distance was 1.027932712e-6; maximum was 1.764521625e-6. Median relative norm change was 2.020993967e-8; maximum was 9.281601126e-8. This is evidence for the selected sentinel set, not a guarantee of perpetual provider stability.

The immutable release is `data/embeddings/emb_v001/`. Validation `PASS`, `frozen_wp4_gate=true`: **4,114/4,114 VALID** 2048-dimensional float32 vectors, **8,499/8,499 VALID** atom-chunk links and **3,640/3,640** decision rows without missing embedding refs. Finalization verified live retry payloads, responses, vectors, usage ledger, source table hashes and all stored vector dimensions/finite values. It reused the earlier validated causal evidence plan with zero future events, zero private/oracle atoms and zero unmapped context messages. No vector was synthesized or overwritten. A read-only `FrozenEmbeddingStore` now exposes atom, quality, decision, effective-context and visible-history access while preserving the context/history distinction.

Full local test suite after the release: **178 passed**, with three existing Pydantic protected-namespace warnings. A read-only scan of 58 new run/release files found **zero API-key occurrences**.

## Deviations and remaining limitations

The user-approved measurement model is DMX-proxied `qwen3.7-text-embedding`, not the task-book default Alibaba direct `text-embedding-v4`. DMX's region remains undisclosed. All vectors are pinned to `dmx_qwen37_epoch_001`; any future confirmed drift requires a new epoch rather than silent reuse. This round had one SSL transport failure, and its true usage is unknown. DMX pricing was not available locally, so no monetary estimate is asserted. No WP5 experiment was started.
