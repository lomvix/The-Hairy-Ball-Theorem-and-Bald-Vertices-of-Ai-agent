# Research status (WP1–WP6)

This repository studies whether a compressed observable state is sufficient to
predict an AI agent's future behavior. The current evidence is narrower than that
claim: it supports analysis of next-step agent responses under archived effective
requests, but not a general result about complete agent–user–tool–environment
trajectories.

## Evidence available at the current checkpoint

| Stage | Archived evidence | Interpretation limit |
| --- | --- | --- |
| WP1 | 60 curated benchmark tasks | Selected tasks do not represent all agents or environments. |
| WP2–WP4 | 324 valid runs; 2,831 study-agent decisions; 4,114 semantic measurements and 3,640 decision-index records | Embeddings are measurements, not proof of state sufficiency. The deployed embedding model differs from the original task-book default. |
| WP5-A | 3,445 same-condition cross-run pairs; an initial geometric filter yielded 273 near-state candidates | No natural pair isolates prior agent history while keeping the full non-agent input identical. |
| WP5-B | 12 tasks, 216 intervention attempts, 10 successful responses, and 7 complete three-arm sets | Small independent-task support and incomplete arms prevent a confirmatory history-effect estimate. |
| WP6 | 24 first-round anchors with 8 attempts each; 21 anchors had unchanged coarse next actions and 3 showed a divergence | Repeated next-step responses are not independent tasks and are not closed-loop outcomes. |

Additional temporal blocks and local restore probes were conducted. Their timing,
response reuse, and incomplete restoration prevent a causal conclusion about
time drift or multi-step branching. The number of validated closed-loop branch
divergences remains **zero**.

## Main research conclusions

1. A near neighbor in the current representation can conceal differences in
   recent user messages, tool results, goals, identity cues, or confirmations.
   Those variables must be audited before a difference is attributed to agent
   history.
2. Repeated calls at one anchor estimate within-anchor variability; they do
   not increase the number of independent tasks. Uncertainty should be reported
   at the task/anchor level and by the chosen action granularity.
3. A tool name, its normalized arguments, the meaning of a communication, and
   an actual environment transition are different endpoints. Agreement at a
   coarse endpoint does not establish agreement at a finer one.
4. A valid multi-step sufficiency test requires two isolated restorations of
   the full causal checkpoint, including the user simulator, tool/environment
   state, pending actions, and any external session state. Agent-request replay
   alone does not meet that requirement.

The next research step is to strengthen the observable-state definition and
task-level support, while separately validating complete checkpoint restoration.
If full restoration is unavailable, the claim must remain explicitly limited
to agent-only next-step behavior.

No benchmark conversations, task payloads, raw responses, credentials, provider
configuration, or run artifacts are included in this public release.
