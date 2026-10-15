# WP4 bounded DMX real pilot — 2026-10-13

## Authorization and boundary

- User approved at most **10 DMX embedding API attempts** and **50,000 provider-reported input tokens** for this real WP4 pilot. The configured model is the explicitly approved substitute `qwen3.7-text-embedding` through the DMX proxy, requested at 2048 dimensions. The proxy's actual serving region remains `PROXY_UNDISCLOSED`; these are not Alibaba-direct measurements.
- All requests used public WP3 v3 semantic atoms from the pinned plan; 324 private TASK atoms were excluded. Full WP2 benchmark requests, hidden simulator scenarios, grader labels and secrets were not sent as embedding inputs. The API key was read from project-local `<LOCAL_SECRET_FILE>` and did not enter request/response artifacts or printed output.
- Before each potentially writing Python command, the process-local workspace guard redirected temporary/cache paths under `<WORKSPACE_ROOT>`. Requests, responses, vectors, ledgers, validation and reports were written only inside this project root.
- Real batch execution is single-attempt, sequential and non-retrying. The budget ledger reserves an attempt before each network call. Unknown reported usage blocks further calls.

## Implementation and actual measurement

- Pinned real-pilot configuration: `configs/wp4/embedding_dmx_qwen37_pilot_v1.yaml`; plan: `runs/wp4_plan_qwen37_pilot_v1/`. The plan verifies **7,770/7,770** public atoms, 8,499 atom-chunk links and 4,114 unique embedding inputs. Exact provider token totals and price for the uncollected full plan remain unknown.
- Real request archive and budget ledger: `runs/wp4_dmx_qwen37_pilot_v1/`. Batch indexes **0, 1, 2, 4, 85, 377** were chosen to cover ordinary Agent/User text, POLICY, TOOL_RESULT and longer chunks. All six requests returned exact requested model, complete index mapping, and **60/60 finite nonzero 2048D float32 vectors**.
- Actual budget use: **6/10 API attempts**, **10,143/50,000 provider-reported input tokens**. No retry or additional attempt was made. Four approved attempts remain unused; collection was stopped voluntarily after the capability and artifact checks succeeded.
- `runs/wp4_dmx_qwen37_pilot_v1/validation_v2.json`: **PASS**, zero errors; verified pinned request content, batch and file hashes, registry keys, exact stored vector values/dtype/dimensions, response usage against ledger, and unique embedding keys.
- A read-only scan of all 39 pilot JSON/JSONL evidence files found **zero occurrences of the configured API key value**; no credential value was printed.
- Partial registry: `runs/wp4_partial_real_qwen37_v1/`, manifest status **`PARTIAL_PILOT_NOT_FROZEN`**. It contains 60 valid unique embedding units and 4,054 explicitly `UNKNOWN/NOT_COLLECTED_IN_BUDGETED_PILOT` units. The 60 measured units cover 311 of 8,499 atom-chunk links through exact text-hash reuse; no missing unit was filled with a zero or mock vector.
- Decision evidence has 3,640 Agent rows; 1,830 have at least one real embedding reference, with all other needed keys left in the missing list. Existing text-source ambiguity remains: 202 decisions have duplicate-text `PARTIAL_MAPPING`, although actual context text has zero unmapped messages. No private atom or future event was intentionally loaded.
- `runs/wp4_partial_real_qwen37_v1/validation.json`: **PASS**, zero errors; verified 4,114 unit status rows, 8,499 links, 3,640 decision rows, file hashes, quality/registry consistency, missing masks and unchanged causal evidence fields.
- `pytest tests -q`: **168 passed**, 3 pre-existing Pydantic namespace warnings.

## Unresolved / gate

- This is a real but **partial** measurement, not frozen `emb_v001`, not a completed drift sentinel and not the WP4 acceptance gate. Do not enter WP5 on these artifacts.
- The remaining 4,054 unique inputs would require more than the current 10-attempt pilot cap to collect; any larger paid campaign needs a separately visible run plan and budget approval. DMX pricing, actual serving region and longer-term drift remain unknown.
- Before a full WP4 freeze, implement resumable multi-batch scheduling, versioned sentinel repeats, read-only retrieval APIs, full coverage and final quality checks; resolve or retain explicit duplicate-text provenance ambiguity without overclaiming exact attribution.
