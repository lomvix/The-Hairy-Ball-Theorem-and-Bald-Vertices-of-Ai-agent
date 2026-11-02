# WP7 数据资产盘点 v1（2026-11-02）

本轮仅离线读取 WP1–WP6 归档，未修改旧数据。统一键：`task_uid → run_uid/trajectory_uid → decision_id → checkpoint_id → branch_uid → transition_id`。后两层不是每条决策均存在；一个 API attempt 或 response 不自动构成新决策、分支或独立 Task。

| 层 | 冻结来源/口径 | 实际数量 | 可用边界 |
|---|---|---:|---|
| WP1 | `runs/wp1_final_v1_fc0055dc4e0a316c3f83133267fbd6faaa770992/curated_task_registry_v1.jsonl` | 278 候选中 60 Task；20/域；38 ELIGIBLE、22 CONDITIONAL | 选择概率/权重保留；Retail 20/20 CONDITIONAL，不能把条件性评分当完整官方评分 |
| WP2 | `artifacts/wp1_wp6_root_cause_audit_v1/task_evidence_matrix.jsonl` 与 run manifests | 383 manifest；324 有效 run（251 Study、73 Sentinel）；59 非有效/中断 | run、attempt、request、response 各自计数；不因行为结果重采 |
| WP3 | `runs/wp3_full_frozen_v3` 每 run JSONL/构建报告 | 6,625 决策帧（Agent 3,640，User 2,942，Evaluator 43）；7,280 转移记录（Agent 决策 3,640、Closed-loop 3,640）；2,975 环境 delta；Study Agent 决策 2,831 | 全部帧 `context_truncation_status=UNKNOWN`；43 帧 Memory PARTIAL。转移记录完整不等于环境有变化或可估计转移核 |
| WP4 | `data/embeddings/emb_v001/embedding_manifest.json` | 4,114 有效 2048 维向量；3,640 决策索引；8,499 atom-chunk 链接 | 实际为获批 DMX `qwen3.7-text-embedding` epoch，不是旧 README 的 v4；语义测量不是行为样本 |
| WP5/R1 | `artifacts/wp6_r1_full_corpus_support_resolution_v1/summary.json` | 3,445 自然候选对；Type-B-Clean 0；2 Type-A 候选未验证 | 自然历史效应不可识别；受控编辑不得补入自然对照 |
| WP6 历史基线 | `artifacts/wp6_task_anchor_outcome_coverage_v1/{summary.json,branch_rows.jsonl}` | 232 闭环分支、25 Task、43 锚点；139 自然终止、80 调用截尾、13 技术中断；129/139 有适用完整官方评分 | 此为 10/24 去重快照，不含后来实验；80 截尾均不作终局失败 |
| WP6 后续 | `reports/post_2026_10_15_experiment_synthesis_2026_11_02.md` 及其所列原始制品 | 10/29 去重观察覆盖 55/60 Task；P1 9 Task/108 单步；P2 6 Task/72 闭环；双域 4 Task/48 闭环；11/02 五试点各 12 分支 | 后续 cohort 相互重叠，本轮未构造全版本统一 branch 去重表，**不能**将这些分支数加到 232 或当新独立 Task |

本轮新增的派生索引位于 `phase2/WP7/artifacts/v1/`：60 行 `cohort_ledger.jsonl`、6,625 行 `decision_ledger.jsonl`、7,280 行 `transition_ledger.jsonl`、232 行历史基线 `branch_ledger_baseline_20261024.jsonl`。它们仅保留身份、状态和源引用，不复制原始对话或工具参数值。构建脚本 `phase2/WP7/build_first_round_ledgers.py`，运行时使用同进程工作区 guard；断言 60 Task、324 run、6,625 个唯一 decision ID、7,280 个唯一 transition ID、232 基线 branch 均通过。`cohort_ledger` 的 WP6 字段明确标记 `as_of_20261027`，后续覆盖状态为 `NOT_RECONCILED_IN_V1`，防止旧矩阵冒充最新全量。

本轮尚未完成全部后续 WP6 版本的逐 branch 去重与 checkpoint/transition 精确连接。因此 WP7 全历史统一证据账本的 Gate 为 `PARTIAL`；可用的 WP3 与历史基线索引已完成，后续版本不得在未去重前投入 Phase II 转移核估计。
