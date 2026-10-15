# WP3 checkpoint v2 — frozen-corpus canonical trace gate

Date: 2026-10-13. Status: **WP3 gate PASS for observable evidence**, with the recovery limits below. WP2 sampling remained stopped; this work made zero LLM or Embedding calls and did not enter WP4.

## Implementation

- Rebuilt the frozen, compatibility-audited 324 valid WP2 runs (251 Study, 73 Sentinel; 222 epoch 1, 102 epoch 2) from pinned local sources. The full builder rejects a changed run-manifest inventory.
- Canonicalized ordered native events, actual decision input frames, Agent actions, user-side tools, durable environment deltas, agent-only and closed-loop transitions, history anchors, source links, visibility-scoped semantic atoms, and isolated Oracle labels/TASK atoms.
- Reconciled the frozen telecom user-tool ontology and corrected observed effects: a requested WRITE with no durable state change is now NONE, not READ. Native bootstrap greetings are explicitly unmapped rather than silently dropped.
- Added a post-hoc-only future-window helper for horizons 1/2/4/8, preserving natural terminal versus censoring without synthetic absorbing transitions. This helper is not exposed through the current-state package API.
- Added per-run gate records for downstream use. Public observed-history data is eligible for visibility-filtered semantic measurement and partial-state learning; full Markov recovery and closed-loop checkpoint validity are **not** claimed.

## Actual validation

- Full build: 324/324 per-run validations PASS. Merged dataset: 10/10 checks PASS, 0 errors, 0 model calls. Dataset manifest SHA-256: `b13fcfe7b6ae19046ece6fffec4b411f0ad3d86784bfa6af176fcc2dbb26ff4d`.
- Rows: 31,132 events; 4,801 actions; 6,625 decision frames and history anchors; 7,280 transitions (3,640 Agent-decision and 3,640 closed-loop); 2,975 environment deltas; 7,275 public semantic atoms; 324 private TASK atoms and 324 Oracle labels; 9,881 native event links; 119,431 source links; 6,703 quality flags.
- Native mapping: 9,557 mapped; 324 initial bootstrap messages explicitly marked `BOOTSTRAP_MESSAGE`. All 846 user-origin tool calls are `USER_VISIBLE`.
- Effect audit: 665 confirmed writes; 24 intended writes without durable change; 2,126 read/read; 63 read/none; 62 handoffs; 35 generic `calculate` calls remain UNKNOWN. The validator rejects WRITE/READ contradictions.
- Independent second full build: 7,788 matching JSONL/Parquet content files, 0 hash mismatches and 0 missing files. Output-path-dependent manifests are intentionally excluded from this content comparison.
- Whole-project test suite: **148 passed, 3 existing Pydantic namespace warnings**. The default pytest configuration now uses importlib mode to avoid same-basename collection conflicts.

## Per-run downstream boundary

- 324/324: `ELIGIBLE_VISIBILITY_FILTERED` for semantic measurement, using each atom's visibility and event availability.
- 324/324: `ELIGIBLE_PARTIAL_STATE` for learning from decision-time observed history and actual API inputs, **not** full hidden state. All 3,640 Agent frames have context and tool references; all 6,625 frame truncation statuses remain UNKNOWN, and 43 post-hoc evaluator frames have PARTIAL memory observability.
- 324/324: `NOT_ESTABLISHED` for full Markov-state recovery; 324/324: `NOT_VALIDATED` for closed-loop forks. History anchors carry at most Level-1 Agent-only checkpoint metadata. WP6 must validate higher recovery levels before fork claims.

## Unresolved issues and scope limits

1. The 35 `calculate` actions retain UNKNOWN intended/observed effect because the pinned generic tool definition does not establish a stronger effect. No effect is inferred from name alone.
2. Oracle labels and TASK atoms are physically separated into `dataset/oracle/`, but this local build does **not** establish operating-system access-control isolation. Downstream readers must use visibility-aware APIs and must not import Oracle data into current-state features.
3. Context truncation is not independently observable for these captured runs. External/hidden state and post-hoc evaluator internals do not support a strict full-state recovery assertion.
4. The WP3 task book lists separate `build-events`, `build-decisions`, `build-transitions`, and `finalize` CLI verbs. The implemented full builder executes these stages together; the outputs and validator exist, but separate subcommand wrappers were not added.

Evidence: `runs/wp3_full_frozen_v2/wp3_full_build_report.json`, `runs/wp3_full_frozen_v2_validation/report.json`, `runs/wp3_full_frozen_v2_determinism/report.json`, and `runs/wp3_full_frozen_v2_gate/wp3_gate_summary.json`. The older v1 corpus remains untouched for audit comparison.
