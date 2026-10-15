# WP2 Sampling Freeze and WP3 Kickoff Report

Date: 2026-10-12

## Outcome

WP2 sampling was stopped at the user's requested provisional sample size. No
collector or Python worker remains active. Three runs that were in flight were
preserved and terminalized as `INTERRUPTED` with `run_valid=false`; no partial
run is eligible for WP3.

The frozen WP3 compatibility audit passes with no critical blocker. WP3 has
started with an offline deterministic canonicalization prototype over one real
completed epoch-2 run.

## Frozen input inventory

- Valid completed runs: 324
- Study runs: 251
- Sentinel runs: 73
- Epoch 1 valid runs: 222
- Epoch 2 valid runs: 102
- Excluded terminal states: 45 `PROVIDER_FAILED`, 11 `INFRA_FAILED`, 3
  `INTERRUPTED`
- Valid runs by domain: airline 112, retail 115, telecom 97
- Valid runs by model: `gpt-6.1-sol-cdx` 110,
  `claude-sonnet-5-5-cc` 32, `gemini-3.8-flash` 34, legacy epoch-1 Claude 73,
  legacy epoch-1 Gemini 75
- Recorded raw volume across both collection roots, including failed and
  interrupted evidence: 7,437 API attempts and 39,356,166 tokens
- Sampling processes after shutdown: 0

Compatibility audit:
`runs/wp3_preflight/compatibility_audit_v3.json`

Audit SHA-256:
`d6792c054dc133d93b442960bedc75171d95df1c3a6f0e0bbaee0c7a6d3fcaac`

## WP3 implementation completed in this stage

- Added canonical run builder for events, actions, decision state frames,
  two-level transitions, and history anchors.
- Causal order is based on recorded trajectory-prefix source order and explicit
  decision/tool linkage; timestamps are retained as evidence but are not the
  sole ordering mechanism.
- API retries remain attached to one logical decision.
- Parallel tool calls have distinct call/result/mutation nodes with a shared
  source decision.
- Evaluation is represented only as `POSTHOC_ONLY`.
- Added `get_causal_observations(decision_id)`, which returns only
  `AGENT_VISIBLE` events whose sequence precedes the decision anchor.
- Added graph/reference, No-Future, and No-Oracle validation.
- Added a no-network terminalizer for stopped WP2 runs.

## Real prototype result

Source run:
`run_006e7d986c0ae0b5bbf3b1632a5cb4df11b5851e05cf40f2d09289f83371b65d`

Output:
`runs/wp3_prototype/run_006e7d986c0ae0b5bbf3b1632a5cb4df11b5851e05cf40f2d09289f83371b65d_v2`

- Canonical events: 133
- Actions: 17
- Decision state frames: 24
- Behavioral transitions: 34
- History anchors: 24
- LLM or embedding calls: 0
- Validation: PASS for event/parent order, reference integrity, No-Future, and
  No-Oracle

Two independent builds produced identical hashes for all six output/validation
files. The canonical event-stream SHA-256 was
`e68189fc58b2f255903ba866f0a78cc561d50369437ba0e9a0271c12ff5888f0`.

## Tests

Command scope: canonical-trace tests plus affected acquisition lifecycle,
parallel collector, and workspace-storage tests.

Result: 17 passed, 0 failed. Three existing Pydantic protected-namespace
warnings remain and do not affect the result.

## Open work before WP3 finalization

- Promote prototype JSONL outputs to the contracted Parquet dataset layout.
- Implement semantic atoms, explicit environment-delta records, source links,
  quality flags, and physically separate oracle labels.
- Run cross-domain/cross-model canonicalization before applying it to all 324
  valid runs.
- Keep 43 runs with partial memory observability physically labelled UNKNOWN;
  do not claim complete Markov-state recovery.
- Replace currently conservative `intended_effect=UNKNOWN` tool annotations
  only where a deterministic, versioned tool ontology supports the mapping.
