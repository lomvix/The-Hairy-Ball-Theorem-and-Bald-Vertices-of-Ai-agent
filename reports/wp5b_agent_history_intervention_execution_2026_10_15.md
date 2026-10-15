# WP5-B Agent 历史遮蔽受控试点：执行与结果（2026-10-15）

## 实施与预算

按用户批准的冻结 `runs/wp5b_history_intervention_plan_v1/request_plan.parquet` 执行 **12 个锚点 × 3 臂 × 6 次 = 216 次 Agent-only 请求**。A 为原始请求，B 只遮蔽最近用户消息前的一条 Agent 纯文本话语，C 只改写初始化 Agent 问候语。执行前完成 12/12 锚点人工语境复核；序号 1、7、8 被单列为高语境依赖，但仍适合解释为“历史缺失敏感性”人工干预，见 `reports/wp5b_history_intervention_manual_review_2026_10_15.md`。未执行任何工具、User Simulator 或环境转移；原始 WP2/WP5/WP6 文件未改动。

授权硬上限为 **240 API attempts、2,000,000 输入 tokens、50,000 输出 tokens**。实际 216 次 attempt，覆盖全部计划行；**210 次 HTTP 200 成功，6 次传输状态不明**（无 HTTP 状态、用量未知），未重试，也无未闭合在途 attempt。成功响应的 provider-reported usage 为 **1,305,615 输入 / 32,982 输出 tokens**；对 6 次未知请求按预留量计入 **55,038 输入 / 12,288 输出 tokens**。因此停止时的**已观测或保守预留**账本为 **1,360,653 输入 / 45,270 输出 tokens**，低于全部三项硬上限；这不是能核实的实际账单。DMX 的精确货币价格仍为 `UNKNOWN`，不从 token 数伪造费用。

执行分初始 6 次通路验证、并发续跑、单路尾段完成。并发预留曾两次提前触发输出门禁；修正调度器为“等待在途结果结算再重判”后继续，最后 15 条在保留 1,000 输出 token 额外安全缓冲下串行完成。三次暂停均未修改冻结请求、预算上限或已开始 attempt 的归属。6 个传输不明的计划序号为 **28、55、66、123、198、200**；其中 B 臂 2 次、C 臂 4 次、A 臂 0 次。它们可能已到达服务端，因此不以新 attempt 填补，也不把缺失记为行为失败。

原始证据在 `runs/wp5b_history_intervention_execution_v1/`：`authorization.json` 固定计划 SHA-256 `4a9a1beaf2792f3ea82b966c9f9aa6ec5e11f21511f14b453e2b9b2eb308e0d7`、人工复核 SHA-256 与硬上限；`journal/` 为追加式 attempt 开始/结果账本，`attempts/` 和 `responses/` 保存逐次结果与成功时的完整原始响应。请求从工作区内 `<LOCAL_SECRET_FILE>` 在内存中读取凭证；生成的响应在写入前替换密钥字面值。请求超时 180 秒；技术性未知没有自动重发。

## 离线研究结果

最终派生数据在 `runs/wp5b_history_intervention_analysis_v2/`：216 行逐请求 `branch_outcomes.parquet`、36 行锚点×臂 `anchor_arm_distribution.parquet`、12 行锚点配对 `pairwise_effects.parquet`，连同三表 SHA-256 manifest。先前 `analysis_v1` 是 201 次 attempt 时的中途快照，保留但不作为最终结论。最终有 **67/72 个三臂同轮小组全部成功**，其中 TEST 35、CURATION_DIAGNOSTIC 32；其余 5 个小组至少有一次传输不明。

| 观察口径 | 结果 |
| --- | ---: |
| 成功响应，A/B/C | 72 / 70 / 68 |
| 67 个完整小组中，三臂的“调用工具／直接回复”粗动作相同 | **67/67** |
| 完整小组中，A 与 B 的较细动作类别相同 | 64/67 |
| 完整小组中，A 与 C 的较细动作类别相同 | 66/67 |
| 完整小组中，A 与 B / A 与 C 的全文动作签名相同 | 37/67 / 40/67 |
| 210 次成功响应的不同 response ID / 不同 choice payload | 210 / 191 |

全部较细动作类别差异都来自**同一个 CURATION_DIAGNOSTIC airline 锚点**：B 相对 A 有 3 个同轮不同，C 相对 A 有 1 个；主要是搜索航班的工具选择或调用次数变化。它不是 3 个独立任务的证据，也不是 held-out TEST 的确认结果。12 个锚点的三臂粗动作分布 TV 均为 0，但样本小、配对锚点人为筛选，且重复响应存在相同 choice payload，**不能推断总体或局部严格行为充分性**。一个探索性 airline 锚点的 B 臂成功回答平均 1,769 输出 tokens，A 为约 961、C 为约 808；B 臂 4 次成功只有 1 个不同 choice payload，不能将这 4 次当作独立重复。回答长度的变化与下一步粗动作稳定可同时存在。

没有 response ID 复用，但 210 次响应只有 191 个不同 choice payload；不同 ID 也不自动证明独立推理。C 臂缺失 4 次、B 臂 2 次，缺失并非三臂均衡；配对分析只用完整同轮小组，不将缺失插补成基线。此实验固定用户和工具消息、改变历史 Agent 文本，是**人工反事实请求的下一步响应敏感性**；不能解释为自然执行轨迹中的历史效应，也不能提供 Closed-loop 任务成功率。

## 测试、工作区与 Gate

实现为 `src/behavioral_state/history_intervention_runtime.py`、`src/behavioral_state/history_intervention_analysis.py`，新增相应 `tests/behavioral_state/` 测试。guard 后执行入口：`.venv/Scripts/python.exe -m src.behavioral_state.history_intervention_runtime --workspace . --keys <LOCAL_SECRET_FILE> --workers 6`；尾段使用 `--workers 1`。离线分析入口为 `.venv/Scripts/python.exe -m src.behavioral_state.history_intervention_analysis --workspace .`。预检验证 36 个不同请求负载与原始请求来源，严格保留非 Agent 消息及工具 schema；版本化分析拒绝覆盖。最终全项目 guarded 测试 **238 passed**，另有 3 条既有 Pydantic 警告。

工作区根目录 `<WORKSPACE_ROOT>` 在 D:，非 reparse point，预检可用空间 227,727,052,800 bytes；根目录无 Git，pinned τ² checkout commit 为 `fc0055dc4e0a316c3f83133267fbd6faaa770992`。TEMP/TMP、Python bytecode、pip/HF 缓存、所有请求响应/日志/派生表均在项目根目录内。Python 3.12.4、PyArrow 14.0.2；没有下载或安装。

**Gate：冻结的 Agent-only 三臂采集 = PASSED（216 行均尝试，210 成功，6 不明）；WP5-B 严格行为充分性确认 = UNIDENTIFIED。** 现有证据描述了粗动作稳定与一个探索性工具选择差异，不证明约化状态充分；有效 Closed-loop 恢复仍为 0。若继续，宜先做零付费的工具参数/回答内容机制审查和按任务聚类的不确定性分析，再决定是否值得另立新的、独立授权的样本计划。
