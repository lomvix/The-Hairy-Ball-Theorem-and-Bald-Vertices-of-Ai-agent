# WP3 Checkpoint v1 — Cross-Model/Domain Parquet Pilot

Date: 2026-10-12

## Outcome

WP3 progressed from a single-run JSONL prototype to a merged Parquet pilot
covering all nine epoch-2 model/domain cells. Sampling remained stopped and no
LLM or embedding call was made.

Pilot dimensions:

- Models: `gpt-6.1-sol-cdx`, `claude-sonnet-5-5-cc`, `gemini-3.8-flash`
- Domains: airline, retail, telecom
- Runs: 9 Study runs, one deterministic selection per model/domain cell
- Both successful and unsuccessful trajectories are represented
- Per-run validation: 9/9 PASS
- Merged dataset validation: PASS, zero errors

## Contracted dataset layout

Public Parquet tables:

- `events.parquet`
- `actions.parquet`
- `decision_frames.parquet`
- `transitions.parquet`
- `environment_deltas.parquet`
- `semantic_atoms.parquet`
- `history_anchors.parquet`
- `source_links.parquet`
- `quality_flags.parquet`

Oracle labels are not present in the public table directory. They are stored
under the separate `dataset/oracle/oracle_labels.parquet` path. Public source
links contain no `ORACLE_LABEL` links.

The physical Parquet encoding represents the logical
`source_manifest_hashes: dict[str, str]` as a sorted list of key/value pairs so
that different run-manifest paths cannot create incompatible Arrow struct
schemas during aggregation.

## Pilot inventory

- Events: 696
- Actions: 98
- Decision state frames: 136
- Agent-decision transitions: 82
- Closed-loop transitions: 82
- Environment delta records: 63
- Semantic atoms: 151
- History anchors: 136
- Source links: 2,593
- Quality flags: 200
- Oracle labels: 9

Semantic atoms:

- Agent text: 35
- User text: 44
- Tool-result text: 63
- Policy text: 9

Environment/action classification:

- Exact durable-state changes / observed WRITE: 9
- No durable-state change / observed READ: 54
- Communicative NONE effects: 35

## Correctness issue found and fixed

The first pilot draft compared complete environment snapshot files. Read-only
tools appeared changed because `snapshot_timing` changes from `before` to
`after`, so every tool was incorrectly classified as WRITE.

The corrected implementation computes a durable environment fingerprint from
the recorded `agent_db_hash` and `user_db_hash`, excluding capture metadata.
It emits `ENVIRONMENT_MUTATION` only when this durable state changes and keeps
an explicit `NO_CHANGE` delta record for read operations. A regression test now
protects this distinction.

## Validation evidence

All checks passed:

- Manifest hashes and row counts
- Causal parent order and contiguous per-run event sequence
- Decision-frame anchor integrity
- No-Future boundary
- No-Oracle boundary and physical Oracle separation
- Source-reference existence
- Environment-delta semantics
- Quality-flag integrity

Two independent builds compared 199 non-manifest output files with zero hash
mismatches.

Relevant hashes:

- Pilot manifest:
  `2455210f9ed2cb2c60504b8f104073ecf6561a47348cc32fe08de2ec97b0fbae`
- Dataset manifest:
  `a979b1ce647fc82122b260b24afc895e7c4615fa6afff8c4f698dabc30fc2c92`
- Validation report:
  `c593d070735db5e5a65eaae014cba3d5bbb7207fb0573ca6db61e92d95b2df5d`

Regression scope: 18 passed, 0 failed. Three pre-existing Pydantic namespace
warnings remain.

## Remaining WP3 work

- Add deterministic TASK atoms from the WP1 task-content source; they must
  retain their actual visibility rather than being assumed Agent-visible.
- Replace `intended_effect=UNKNOWN` only where a frozen tool ontology provides
  an explicit mapping. All 63 unknown intended effects currently carry a
  quality flag.
- Define structural environment-diff payloads beyond durable before/after
  fingerprints, without treating execution metadata as state.
- Add explicit recovery-reason records for native events that cannot be mapped.
- Expand the validated build from the 9-run pilot to the frozen 324 valid runs
  only after the above schema decisions are stable.
