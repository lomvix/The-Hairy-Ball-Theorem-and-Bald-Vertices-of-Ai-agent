# Public methods and reproducibility notes

## Stage sequence

1. **WP1, task curation:** inspect the benchmark interface, define a task
   inventory, freeze identifiers and splits, and test the curation data model.
2. **WP2, baseline acquisition:** acquire complete runs under recorded
   conditions, distinguish attempts from valid runs, and freeze the cohort.
3. **WP3, canonical traces:** turn heterogeneous dialogue and tool events into
   typed events while retaining provenance and unknown values.
4. **WP4, semantic measurement:** measure text atoms, preserve measurement
   version and missingness, and never equate an embedding with hidden state.
5. **WP5, behavioral-state tests:** build observable features from the effective
   request; compare only pairs with auditable non-agent conditions; keep natural
   matching and deliberate history interventions as distinct estimands.
6. **WP6, branching tests:** separate agent-only next-step replay from complete
   closed-loop restoration. Report action granularity, restoration fidelity,
   independent task count, and response reuse.

## Analysis rules

- Freeze task, anchor, model, endpoint, and stopping rule before evaluating
  outcomes. Do not redraw controls in response to a result.
- Keep three counts separate: tasks/anchors, API attempts, and valid responses.
- Preserve exact request hashes and compare non-agent message sequences before
  attributing a contrast to earlier agent text.
- Report coarse action, tool name and arguments, and eventual environment
  outcome separately. An unexecuted proposed tool call is not a tool effect.
- Treat unobserved simulator or provider-side session state as an unresolved
  fidelity gap, not as evidence of independence.
- Use an explicit `UNKNOWN` value when a field cannot be established from
  archived evidence. No hidden state is inferred from semantic similarity.

## Code in this release

The accompanying `src/behavioral_state` and `src/branching` files implement
pure, offline pieces of the analysis: request-surface fingerprints, controlled
history edits, task-independent planning helpers, balanced random controls,
replay-boundary classification, capability levels, and two-restore fidelity
checks. Matching `tests` provide synthetic unit checks. They do not perform
network calls or reproduce the private benchmark data.

To run the included unit tests from the repository root after installing
`pytest`, use the test paths published alongside the modules. The stage counts
above are reported from archived research summaries, not recalculated from
public raw data; independent reproduction of those counts requires a separately
licensed and privacy-reviewed data release.
