# WP6 static checkpoint capability audit — 2026-10-14

## Scope and outcome

WP5-A handoff validation passed and authorized **WP6 capability audit only**, not branch collection. On pinned official τ²/tau2 commit `fc0055dc4e0a316c3f83133267fbd6faaa770992`, static code audit produced `runs/wp6_capability_static_v1/capability_report.json`: `STATIC_AUDIT_COMPLETE_DYNAMIC_FIDELITY_PENDING`, with **0 API calls and 0 branch runs**. A two-restore signature comparator and Mock tests were added, but no actual benchmark decision was restored. Full closed-loop checkpoint status is **UNVERIFIED**.

The project root/workspace guard remained under `<WORKSPACE_ROOT>`. The pinned checkout `.git/HEAD` matched the expected commit. A read-only `git status` required a process-local safe-directory override because the sandbox user differs from the checkout owner; no global Git setting was changed. The checkout status showed no changes. No model/provider call, download, installation, tool mutation or environment clone was executed.

## Pinned-code findings

| Component | Static evidence | Capability conclusion |
|---|---|---|
| Runner checkpoint | `runner/checkpoint.py` `try_resume()` records completed simulations as `done_runs`; `runner/__init__.py` labels this batch-run save/resume. | **RUN/BATCH only**. It is not a decision-point snapshot. |
| Agent decision input | WP2 raw effective Agent requests are referenced for the 1,465 initially eligible current-model anchors. `LLMAgentState` holds system messages and history. | Agent-only input is present, but a repeated real provider response has **not** been tested. |
| Environment | `Environment.set_state(..., message_history, strict=True)` replays mutating tool calls against recorded responses; DB hashes are available. | Prefix replay is a plausible component of a restorer, not full state fidelity. |
| User simulator | `UserState` stores system messages and messages; `get_init_state(message_history)` reconstructs this visible runtime state. | User context reconstruction code exists; hidden/service-side state equivalence is **unverified**. |
| Orchestrator | `initialize()` reconstructs Agent/User states from history and initializes environment; live fields include turn roles, current message, step count, done/error flags and pending tool phase. | No native arbitrary-step state snapshot/restore API was found in the reviewed text-runner path; a versioned wrapper plus fidelity tests are needed. |

The static classifier therefore marks `CLOSED_LOOP_REPLAY_CANDIDATE`, **not** `CLOSED_LOOP_VALIDATED`. A DB hash match alone cannot substitute for User, pending-tool, policy, orchestrator or external session equality.

## Implemented safety contract and tests

`src/branching/capability.py` distinguishes batch resume, exact Agent request availability, replay-code candidacy and validated closed loop. `src/branching/fidelity.py` requires two distinct restore IDs and matching Agent request/history, User context/internal state, environment, tools/pending actions, policy/config, turn phase and controlled external session, plus isolated clones. Missing memory evidence is only exempt when persistent memory is explicitly declared absent. These are pure validators, not working restore adapters.

Five new fidelity tests and four capability tests reject batch-resume conflation, User mismatch despite equal environment, unknown server-side session, pending-action/clone omissions and duplicate restore IDs. Complete guarded test suite: **204 passed, 0 failed**, with three pre-existing Pydantic protected-namespace warnings.

## Next Gate and unresolved issues

Next, build an **isolated Mock/official local restorer** at a real pre-Agent decision boundary; restore twice from the same captured prefix into distinct workspace-local environments and compare the full versioned signature before generating any LLM output. If User service-side state cannot be observed/controlled, mark those anchors `AGENT_ONLY_ONLY` or `NON_REPLAYABLE`; do not relax the signature test. Only after that should a WP6 dry-run assign anchor selection probabilities, preserve ≥40% independently sampled random controls, and estimate separate Agent-only and Closed-loop paid budgets for user approval. No paid branch Pilot is authorized by this report.
