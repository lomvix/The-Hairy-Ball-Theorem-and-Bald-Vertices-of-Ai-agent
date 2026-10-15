# WP4 full-remaining campaign: first pause — 2026-10-13

## Authorization and input plan

- User approved a new campaign capped at **403 API attempts** and **600,000 provider-reported input tokens** for the remaining 4,024 unique embedding inputs. This budget is separate from the exhausted ten-attempt pilot.
- Immutable inventory: `runs/wp4_campaign_inventory_v1.json`. It contains 403 remaining batches and 1,219,166 UTF-8 input bytes. The nine successful pilot batches imply an extrapolation of about 418,180 input tokens for the remainder; this is not an upper bound. DMX monetary price remains unknown.
- New paid configuration and plan: `configs/wp4/embedding_dmx_qwen37_campaign_v1.yaml` and `runs/wp4_plan_qwen37_campaign_v1/`. The embedding-unit and batch-plan hashes match the prior pilot; only scheduler/budget metadata changed. The plan excludes the 324 private TASK atoms.

## Actual calls and pause

- Campaign ledger: `runs/wp4_dmx_qwen37_campaign_v1/budget_ledger.json`. The first four requests at concurrency 4 all succeeded and passed offline vector/file/usage validation (`validation_after_004.json`).
- The next invocation reserved seven additional attempts. Five returned valid embeddings; batches **10** and **13** ended in transport errors with no HTTP status or usage. Both count toward the 403 attempt cap and were not retried. Other in-flight requests finished, then the scheduler stopped creating work.
- Current new-campaign totals: **11/403 attempts**, **9 successful batches / 90 valid 2048D float32 vectors**, **7,989 provider-reported input tokens for successes**, **two requests with unknown usage**, **392 never-attempted batches**. The failed request input sizes were 3,735 and 3,779 UTF-8 bytes.
- `runs/wp4_dmx_qwen37_campaign_v1/validation_after_011.json`: **PASS_WITH_UNRESOLVED_USAGE**, zero integrity errors. A read-only scan of 59 campaign JSON/JSONL evidence files found zero occurrences of the configured API key value.
- The full local suite passed: `pytest tests -q` → **169 passed**, with 3 existing Pydantic namespace warnings.

## Decision pending and next safe step

- The scheduler intentionally blocks new requests while token usage is unknown. The user has been asked whether the campaign may reserve each future no-response transport failure as `input_utf8_bytes + 1,024` tokens, keep actual reported usage null, avoid retries, and continue within the 403-attempt/600,000-token cap. The two existing errors would require reservations of **4,759** and **4,803** tokens respectively, 9,562 total.
- Until that policy is confirmed, no further paid request will be made. If approved, resume at lower concurrency to reduce pressure on the transport, without claiming the earlier errors were caused by concurrency. If declined, keep the campaign paused and report the unknown billing boundary.
- WP4 remains incomplete and unfrozen; do not enter WP5.
