# WP4 campaign implementation report — budget stop (2026-10-13)

## Scope and authorization

- Current work package: WP4 Semantic Measurement Foundation. No WP5 work was started.
- The user approved DMX proxy `qwen3.7-text-embedding` (2048 dimensions) as a documented deviation from the WP4 `text-embedding-v4` default, and separately approved a new remaining-work campaign capped at 403 API attempts and 600,000 input tokens. The earlier pilot had its own 10-attempt/50,000-token budget.
- For requests with no HTTP response, the user approved a conservative accounting reservation of `input_utf8_bytes + 1024` tokens, with actual provider usage kept unknown and no automatic retry.

## Implementation and evidence

- Campaign plan: `runs/wp4_plan_qwen37_campaign_v1/wp4_input_plan.json`; 4,114 unique embedding units, 412 planned batches, 8,499 atom-chunk links. The prior pilot successfully measured 90 units before this campaign.
- Campaign request/response evidence, vectors and ledger: `runs/wp4_dmx_qwen37_campaign_v1/`. Final ledger status is `PAUSED_BUDGET`, reason `TOKEN_CAP_PRECALL`. No request was launched after the pre-call budget check failed.
- Campaign validation: `runs/wp4_dmx_qwen37_campaign_v1/validation_after_371.json`, status `PASS_WITH_UNRESOLVED_USAGE`, zero integrity errors, 304 successful batches and 3,040 valid vectors.
- New offline combined registry: `runs/wp4_partial_real_qwen37_campaign_v1/embedding_manifest.json`; combines 90 pilot and 3,040 campaign vectors without rewriting their original raw vector files. Validation: `runs/wp4_partial_real_qwen37_campaign_v1/validation_report_v2.json`, status `PASS`, zero errors.
- Code changed: `scripts/wp4_assemble_campaign.py` (new); `scripts/wp4_validate_partial.py` (supports and checks the campaign's explicit missing reasons and exact decision-to-vector mapping). All Python commands used the process-local `Initialize-WorkspaceGuard.ps1`; caches, temp files, evidence, outputs and test artifacts stayed inside the project root on `D:`. No package installation was performed.

## Actual usage and results

| Boundary | Attempts | Successful batches / vectors | Provider-reported input tokens | Unknown usage reserved | Accounting total |
|---|---:|---:|---:|---:|---:|
| Earlier pilot (separate authorization) | 10 / 10 | 9 / 90 | 16,480 | 8,224 | 24,704 |
| New campaign | 371 / 403 | 304 / 3,040 | 320,420 | 271,161 | 591,581 / 600,000 |

The campaign's 67 unresolved no-response attempts comprise 64 `SSLError`, 1 `ReadTimeout`, and 2 earlier generic transport errors. Their actual DMX token usage and monetary charges are **unknown**; the reservation is an accounting bound, not provider-reported usage. DMX proxy price was not available, so monetary cost is unknown. The remaining 32 campaign batches were not attempted. The separate pilot and campaign accounting totals must not be compared to the 600,000-token campaign cap as one combined budget.

The combined non-frozen registry has a status for all 4,114 planned units: 3,130 `VALID`, 670 missing due to unresolved provider transport, and 314 missing due to the token-budget stop. It contains 8,499 atom-chunk links (6,596 with vectors) and all 3,640 causal decision-index rows; all 3,640 have at least one real vector, but only 466 have no missing embedding reference. The input plan excludes 324 private/oracle atoms. `frozen_wp4_gate=false` is explicit.

The full local test suite passed: **169 passed**, 3 pre-existing Pydantic protected-namespace warnings. The campaign and combined-registry validators both passed with zero integrity errors.

## Gate and unresolved issues

**WP4 Gate: PARTIAL, not frozen.** Missing vectors and unresolved provider usage prevent publication of `emb_v001`. The drift sentinel required by WP4 has not been run. The approved proxy does not disclose a fixed region, and is a model substitution from the original task book. No state-fusion, topology or WP5 claims are made.

To complete the remaining measurements, a new explicit budget/attempt authorization would be needed for 67 failed batches plus 32 unattempted batches (up to 99 batches, subject to any deduplication and a new plan). Before any further paid call, preserve the current immutable artifacts, verify DMX transport stability, prepare a new run plan and clarify how unknown historical charges should be accounted for. Do not silently retry within the exhausted campaign.
