# WP1 Official Executable Audit Report

## Outcome

- Benchmark: `sierra-research/tau2-bench`
- Tag / commit: `v1.0.1` / `fc0055dc4e0a316c3f83133267fbd6faaa770992`
- Runtime: `envs/tau2-v1.0.1/`, Python 3.12.4
- Scope: 9 real `base` tasks, 3 per domain, selected only by seed `20261008`, domain, and task ID
- Agent API calls: 0
- Embedding API calls: 0
- LLM judge calls: 0
- WP2: not started

The executable smoke gate passed at the minimum required real-task coverage. The same adapter was then run across all 60 preselected pilot tasks and used to freeze the final registry.

## Runtime architecture check

The official source was imported from the pinned checkout rather than the installed package copy. The `base` task counts are:

| Domain | Tasks | Assistant tools | User tools | Tool types |
|---|---:|---:|---:|---|
| airline | 50 | 14 | 0 | 6 read, 6 write, 2 generic |
| retail | 114 | 16 | 0 | 7 read, 7 write, 2 generic |
| telecom | 114 | 13 | 30 | assistant: 6 read, 6 write, 1 generic; user: 15 read, 15 write |

Evidence: `runs/wp1_runtime_setup/runtime_probe.json`. The official checkout remained clean after installation and execution.

The initial probe found and fixed three portability/interface assumptions without changing upstream source:

1. LiteLLM attempted to fetch its remote model-cost map during import. The workspace guard now sets `LITELLM_LOCAL_MODEL_COST_MAP=True`.
2. Airline and retail legitimately expose no `user_tools`; the probe now records zero tools and a null user DB hash.
3. The official telecom loader inherits the Windows locale when opening policy text. The guard now sets `PYTHONUTF8=1` before interpreter startup.

## Real-task audit results

| Check | Result |
|---|---:|
| Tasks audited | 9 |
| Reference actions replayed | 49 |
| Five-reset stability | 9/9 |
| 25/50/75% prefix stability | 8/9 |
| Reference trajectories without tool error | 8/9 |
| DB component | 7 pass, 2 non-gating diagnostic mismatches |
| Environment assertions | 3 pass, 6 not applicable |
| Omit-write negative control | 7 correctly rejected, 2 not applicable |
| No-op diagnostic with matching DB | 2/9 |
| Initial eligibility | 5 eligible, 4 conditional, 0 quarantined |

The two telecom DB mismatches are explicitly `INCONCLUSIVE`, not failures: their official `reward_basis` contains only `ENV_ASSERTION`; all declared assertions pass and the official environment reward is 1.0. This distinction corrected an initially over-strict adapter classification.

The stable real issue is retail task `4`. Its second reference action calls `get_product_details(product_id="6086499569")` and consistently returns `Product not found`. The official evaluator logs the same warning. The task remains `CONDITIONAL`; its DB component still matches, but reference tool execution and every tested prefix containing that action fail the executability check.

Three retail tasks have gating `NL_ASSERTION` components that WP1 deliberately did not run. Airline task `18` has non-empty communication requirements that cannot be established from a tool-only reference replay. These are recorded as conditional evidence gaps, not fabricated failures.

Wrong-entity mutation controls are `NOT_APPLICABLE`: no domain-generic mutation was synthesized without task-specific safety proof.

## Tests and artifacts

- Executable audit: `runs/wp1_executable_smoke_fc0055dc4e0a316c3f83133267fbd6faaa770992/executable_audit.json`
- Smoke audit SHA256: `ef7a0fb6be6317c5cf5e1178df354c4cff3493f1d4b8e155f5d98bd5155fad9f`
- Runtime probe: `runs/wp1_runtime_setup/runtime_probe.json`
- Dependency installation record: `runs/wp1_runtime_setup/pip_install_report.json`
- Project suite after finalization/storage tests: `30 passed in 1.62s`
- Workspace boundary / reparse-point check: PASS
- Official checkout status: clean

A first unscoped `pytest` invocation collected optional tests inside `third_party/` and stopped with 7 collection errors for uninstalled voice/agentify dependencies. No project test failed. `pytest.ini` now confines project discovery to `tests/`; the final default invocation passed all 30 tests.

## Full 60-task pilot audit and freeze

The frozen candidate selection was audited without resampling or using outcomes to replace tasks:

| Check | Result |
|---|---:|
| Selected UID set vs executable UID set | exact match, 60/60 |
| Domain balance | 20 airline / 20 retail / 20 telecom |
| Reference actions executed | 228 |
| Five-reset stability | 60/60 |
| Complete reference trajectories without tool errors | 60/60 |
| Applicable 25/50/75% prefixes | 57/57 stable |
| Zero-action prefix cases | 3 not applicable |
| Eligibility | 38 eligible / 22 conditional / 0 quarantined |
| Component failures | 0 |
| Non-gating/incomplete diagnostics | 11 inconclusive |

The 22 conditional tasks are the disjoint union of 20 tasks with gating NL assertions and 2 tasks whose gating communication requirement cannot be established from tool-only gold replay. Six additional `communicate_info` fields are non-gating diagnostics and do not affect eligibility. No task was dropped or replaced based on these results. Ten telecom DB mismatches are non-gating because their official reward basis is environment assertions; one omitted-write control was inconclusive. Forty-one omit-write controls were correctly rejected and 18 were not applicable.

Final artifacts are under `runs/wp1_final_v1_fc0055dc4e0a316c3f83133267fbd6faaa770992/`:

- Registry JSONL SHA256: `968e2742ebae4ea74044276203b5388f98dbe0d4dcaa4246c14df2a6e680f73b`
- Frozen selection SHA256: `4d9a0cdba356bd8b130f1b0f7de8555619e495c496ccf43e0d94c66888902b4d`
- Final manifest SHA256: `f7d75b6f4580d51af99c7734259c14ad4aeb6d1817272da667194aa6ba27621f`
- Independent JSONL/Parquet/hash/UID validation: PASS

## Unresolved issues

1. The local environment was resolved by pip from the pinned checkout's declared constraints because `uv` is unavailable. It is recorded, but it is not an exact recreation of the upstream `uv.lock`.
2. Gating NL assertions remain unaudited by design because WP1 prohibits LLM judge calls; affected tasks are explicitly conditional.
3. Communication requirements cannot be validated from a tool-only gold replay when no gold assistant utterance exists; affected tasks are explicitly conditional.
4. The non-gating telecom DB mismatch warrants source-level investigation before treating DB hashes as a cross-domain universal criterion.
