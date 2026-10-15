# WP3 v3 backfill and WP4 offline remapping — 2026-10-13

## Scope and boundary

- User-approved WP3 versioned backfill to repair two source-confirmed gaps: the first assistant greeting in each native transcript and nonempty assistant text attached to tool-call responses. No WP2 resampling or new benchmark API calls.
- Existing WP3 v2 dataset remains unchanged; its manifest SHA-256 is `b13fcfe7b6ae19046ece6fffec4b411f0ad3d86784bfa6af176fcc2dbb26ff4d`.
- The process-local workspace guard was applied to all potentially writing Python commands. Project outputs and temporary/cache paths remain under this project root on `D:`. No research-file write to `C:` was requested.

## WP3 v3 implementation and actual validation

- New immutable output: `runs/wp3_full_frozen_v3/`; dataset manifest SHA-256 `045ded6317ad294831100fc21543002bcb85877bad31c9d5b78ee8b4ea85aefb`.
- Bootstrap text uses an exact transcript JSON pointer (`#/messages/0/content`), with a validated assistant role; its SourceLink resolves to the original transcript file. Assistant responses with both text and tool calls now yield an AGENT_MESSAGE plus tool events. The native-message map permits both links for the same native turn.
- 324/324 completed valid runs built and validated. Public semantic atoms: 7,770 (v2: 7,275), an increase of 495 distinct atom occurrences. Native links: 9,881; unmapped reasons: none. Private TASK atoms: 324, stored separately.
- Dataset validation: PASS with zero errors, including parent order, source references, native mapping, No-Future and No-Oracle. Builder/validator LLM or embedding calls: 0.

## WP4 offline plan and evidence remapping

- User-approved substitute remains DMX proxy `qwen3.7-text-embedding` at 2048 dimensions; provider region is `PROXY_UNDISCLOSED`, not falsely attributed to direct Alibaba Model Studio. The prior fixed-text capability probe passed, but benchmark atom collection remains disabled.
- New pinned config: `configs/wp4/embedding_dmx_qwen37_v2.yaml`, pointing only to WP3 v3. Offline input plan: `runs/wp4_plan_qwen37_v2/`.
- 7,770/7,770 public atoms have verified normalized text and chunk status `VALID_INPUT`; 324 private TASK atoms excluded. Deterministic chunk plan: 8,499 atom-chunk links, 4,114 unique embedding inputs, 412 maximum-ten-input batches, 1,267,212 unique UTF-8 bytes. Exact provider tokens and monetary cost remain unknown; no benchmark embedding request was sent.
- New evidence index plan: `runs/wp4_evidence_plan_qwen37_v2/`. All 3,640 Agent decisions indexed. Actual API-context text has **zero unmapped messages**; audit found 15,230 assistant, 3,640 system, 14,319 tool and 14,263 user text-message occurrences with available public atoms. No private atom or future event was loaded.
- Visibility quality: 3,438 `EXACT_CONTEXT_MATCH`, 202 `PARTIAL_MAPPING`; the latter arise from 321 duplicate-text candidate matches. The index preserves these ambiguities rather than claiming unique provenance. Embedding references are absent by design until real collection.
- Tests: `pytest tests -q` → **157 passed, 3 existing Pydantic namespace warnings**. Focused canonical/semantic tests → **18 passed**.

## Remaining work / gate

1. Resolve the 202 duplicate-text provenance ambiguities if exact per-occurrence attribution is needed; they do not represent missing text or private/future leakage.
2. Real benchmark embedding calls require the pending explicit pilot budget decision. The offline plan is not an embedding registry, vector corpus, sentinel run, or frozen WP4 gate.
3. DMX proxy price, exact tokenizer accounting, actual region, batch behavior on benchmark-sized inputs, and drift stability remain unknown. Do not enter WP5 on this report.
