# Research status (WP1–WP6)

This repository studies whether a compressed observable state is sufficient to
predict an AI agent's future behavior. This page is current through 2026-11-02.
Since 2026-10-15, the work has progressed from agent-only next-step replay to
locally restored, multi-step agent–user–tool–environment experiments. These are
valuable local mechanisms, not a general sufficiency result. See the
[post-October-15 synthesis](../reports/post_2026_10_15_experiment_synthesis_2026_11_02.md)
and [deep-analysis guide](POST_2026_10_15_DEEP_ANALYSIS_GUIDE.md).
The [notable-sample addendum](../reports/post_2026_10_15_notable_sample_cases_2026_11_02.md)
documents informative positive, negative and method-limited cases side by side.

## Evidence available at the current checkpoint

| Stage | Archived evidence | Interpretation limit |
| --- | --- | --- |
| WP1 | 60 curated benchmark tasks | Selected tasks do not represent all agents or environments. |
| WP2–WP4 | 324 valid runs; 2,831 study-agent decisions; 4,114 semantic measurements and 3,640 decision-index records | Embeddings are measurements, not proof of state sufficiency. The deployed embedding model differs from the original task-book default. |
| WP5-A | 3,445 same-condition cross-run pairs; an initial geometric filter yielded 273 near-state candidates | No natural pair isolates prior agent history while keeping the full non-agent input identical. |
| WP5/R1 natural matching | 3,445 candidate cross-run pairs; zero strict Type-B-Clean tasks | The independent effect of naturally different prior histories remains unidentified. |
| WP6 restored experiments | A 10/24 audit counted 232 unique closed-loop branches across 25 tasks; later pre-registered and information-first cohorts added distinct designs | Branches, requests and repeated seeds are not independent tasks; cohorts overlap and must not be summed as a single effect sample. |
| Information-first interventions | P1: 9 tasks/108 valid one-step responses; P2: 6 tasks/72 branches; dual-domain pilot: 4 tasks/48 branches; five later single-task pilots: 60 branches | Some local tool, communication and DB-path contrasts were observed; controls, eligibility, censoring and task count limit inference. |

The latest deduplicated any-WP6-observation coverage is 55/60 frozen tasks.
This broad coverage is not 55 matched history comparisons. Local dual restore,
next-request matching and branch isolation support the application-level
closed-loop experiments; invisible provider-side state is still not proved
absent. The October 15 statement that no real closed-loop branches existed was
true then but is superseded by subsequent experiments.

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
4. A multi-step sufficiency test requires isolated restoration, a frozen state
   representation and held-out task-level prediction. Restored branch divergence
   by itself is not a sufficiency test.
5. Local address, device-setting and user-reacquisition cases show why the
   first relevant action, intervening user/tool steps and final DB state must be
   reported separately. A final-state match can hide a transient path change.

The next research step is to harmonize overlapping cohort ledgers and eligibility
rules, freeze an event-anchored endpoint, and test an expanded observable state
on tasks not used to design it. Natural-history confirmation must wait for
strict common support; controlled edits are a separate estimand.

No benchmark conversations, task payloads, raw responses, credentials, provider
configuration, or run artifacts are included in this public release.

