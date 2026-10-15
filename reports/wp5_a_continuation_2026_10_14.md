# WP5-A continuation report — 2026-10-14

## Stage and boundary

WP5 remains **PARTIAL**, and the WP6 Gate is **not passed**. This continuation adds a causal multi-horizon target table, two offline prediction heads, a conservative State Validity Map, and a repair-alignment precondition contract. It does not freeze a behavioral encoder, estimate strict lumpability, or begin WP6. All work used the frozen local WP1–WP4 inputs; **0 API calls**, downloads, installations, or new sampling runs. The D: workspace guard passed and every Python writer initialized it in its own process. Effective artifacts are `runs/wp5_offline_v1/horizon_screen_v2/` and `runs/wp5_offline_v1/validity_v2/`; exploratory `horizon_screen_v1` and `validity_v1` are retained but superseded. No research output was directed outside the project root.

## E2 horizon construction and measured coverage

The source is pinned WP3 `CLOSED_LOOP` transitions. Within each run, Agent frames are sorted by event sequence and each transition pointer is checked against the next Agent decision or the natural `user_stop` terminal. An incomplete/censored, duplicate, or broken chain fails rather than receiving a fabricated label. The future targets are physically separate from WP5 state features. The terminal target means a natural stop within the next `L` closed-loop transitions **including the current transition**; the future-action target is the **L-th next Agent decision** and is masked if termination comes first. Thus the two heads have different observation sets; they are not a joint future-distribution model.

The 2,831 Study decisions yield 11,324 rows at L={1,2,4,8}. Future-action observed counts are 2,580/2,329/1,828/936; natural-terminal-within-horizon counts are 251/502/1,003/1,895. The validation/test predictions comprise 39,592 rows and 112 metric rows for seven fixed representations, four horizons, two heads and two held-out splits. Model/domain are conditioned; task UID groups stay disjoint. Train-only standardization and fixed C=1 logistic heads were used. Test comparisons use 1,000 resamples of nine Task UID clusters, not decision-wise bootstrap. `user_event`, tool-execution and environment-delta *presence* are recorded as target-only descriptive fields, but are **not yet predictive heads**. Delta presence is not the same as environment change.

Illustrative test results (443 decisions for terminal, fewer uncensored future-action decisions):

| Head / horizon | B0 NLL | B1-history-2 NLL | Task-balanced Δ(B1−B0), 95% task-bootstrap interval | Eligible future-action decisions |
|---|---:|---:|---:|---:|
| terminal L=1 | 0.284 | 0.291 | −0.006 [−0.071, +0.065] | — |
| future action L=1 | 0.718 | 0.764 | +0.050 [+0.009, +0.085] | 404 |
| terminal L=4 | 0.668 | 0.822 | +0.129 [+0.012, +0.262] | — |
| future action L=4 | 0.669 | 0.709 | +0.001 [−0.089, +0.087] | 287 |
| future action L=8 | 0.720 | 1.060 | +0.311 [+0.204, +0.426] | 163 |

Negative Δ means lower B1 task-balanced loss. Note that the pooled NLL and task-balanced Δ weight tasks differently and can have different signs. These fixed-feature proxies show **no stable multi-horizon history benefit** and some worse long-horizon predictions. This does not establish that history is behaviorally unnecessary: representation capacity, truncation unknown, task selection, survival conditioning, nine held-out tasks and small L=8 coverage limit the inference. No E2 residual-history test with a separately fit nuisance representation was completed; the nested B0/B1 held-out loss comparison is only an initial residual-information proxy.

## E4 and validity map

The 2,831-row `state_validity_map.parquet` links each Study decision to a B0 reference vector and history anchor. It records 2,655 `PENDING_BRANCH_CONFIRMATION` and 176 `WEAKLY_SUPPORTED` states based on WP4 visibility matching; these labels are **not** branch support estimates. Held-out B0 L=4 terminal predictive entropy exists for 844 validation/test decisions; training and diagnostic decisions explicitly lack held-out uncertainty. `data_density` is null and `local_stability=NOT_AUDITED` everywhere, because E3 has not run. Context completeness remains `UNKNOWN`, and persistent Agent memory is `NOT_ESTABLISHED`. The E4 JSON specifies matching embedding epoch/schema/normalization/encoder/dimension and policy/anchor pairing fields; no repair pair or common-support conclusion exists, and `candidate_representation_id=null` / `encoder_frozen=false`.

## Verification, limitations and next Gate work

The independent continuation validator returned `PASS`, zero errors: 11,324 target rows, 112 metric rows, 39,592 prediction rows, and 2,831 validity rows; all manifest hashes/sizes and relevant masks were checked. The full local suite returned **188 passed, 0 failed**, with three previously observed Pydantic namespace warnings. Four new unit tests exercise natural terminal, action masking, censoring and broken-chain rejection. No Sentinel entered feature fitting, evaluation, or the validity map; no oracle/future column was added to state features.

Before WP5-A Gate can pass, add the taskbook's tool-outcome, real environment-change, user-interaction and applicable termination heads with missingness masks; a stronger residual-history analysis; E3 seed/dimension/neighborhood and task-bootstrap artifact controls; meaningful local density/aliasing priority; and then freeze a justified candidate encoder. B4 memory and B5 learned state remain unresolved. Every Agent context truncation status is still `UNKNOWN`. WP5-B's distributional/strict sufficiency claims require WP6 branch data and remain `UNIDENTIFIED`, not zero.
