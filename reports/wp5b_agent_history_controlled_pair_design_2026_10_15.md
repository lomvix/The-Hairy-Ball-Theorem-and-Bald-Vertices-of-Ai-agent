# WP5-B 先前 Agent 历史受控配对：离线可行性计划（2026-10-15）

## 本轮结果

本轮**只冻结设计，不执行 API**。来源是已归档 WP5 `handoff_v5` 的 1,465 个 Agent-only 可用锚点：506 个满足最近用户消息前紧邻一条非空、无工具调用的 Agent 纯文本消息，且最近用户消息至少 40 字符。按事先固定的决策 ID 哈希排序，在 TEST 与 CURATION_DIAGNOSTIC 各域选 2 个不同任务，共 **12 个任务/12 个锚点**；TEST 的 6 个任务是主要分析集，CURATION_DIAGNOSTIC 的 6 个只用于探索，不与 TEST 混报。该选取只使用请求结构、任务分组和哈希，不使用未来动作、自然运行成功率或 WP6 结果。

每个锚点准备三臂，三臂的模型、采样设置、工具 schema、策略、全部用户与工具消息保持不变：

| 臂 | 唯一变动 | 目的 |
| --- | --- | --- |
| A 原始 | 无；引用冻结原请求 | 同时间块基线与随机波动 |
| B 历史遮蔽 | 将最近用户消息前的一条纯文本 Agent 消息改为固定的“先前助手消息已省略”标记 | 测被省略 Agent 历史的局部敏感性 |
| C 问候语改写 | 只改初始化 Agent 问候语的措辞 | 作为请求文本变化的安慰剂式对照 |

每臂每锚点计划 6 次，**216 条 Agent-only 请求**；重复轮次内把三臂排成相邻的小组，臂先后顺序随轮次轮换：每臂各 72 次，作为小组首位各 24 次。这样可减少长时间漂移与某一臂的固定顺序混淆，但不能控制 DMX 内部缓存、路由或隐状态。`C` 也不是可证明无效的完美安慰剂，只能比较“微小文本变化”与“实质遮蔽”的差别。

冻结计划在 `runs/wp5b_history_intervention_plan_v1/`：506 行候选清单、12 行入选锚点、216 行请求计划、24 份仅改一处 Agent 文本的版本化请求、manifest。原始请求不复制、不改写；A 臂直接引用原文件。27 个计划产物的 manifest SHA-256 全部复核通过；逐行核验 216/216 个请求引用与哈希正确，非 Agent 负载一致，且除预定 Agent 文本外无字段变动；216 行均标 `NOT_AUTHORIZED`。原 WP5 handoff manifest SHA-256 为 `15b13fa65c979b205b112769d3ae463b69111331dcfe27c2297b45d455de8cff`。

## 样本量与费用边界

按相同源请求的已归档 provider usage 简单外推，216 次约需 **1,315,080 输入 / 21,294 输出 tokens**；加 25% 规划余量为 **1,643,850 输入 / 26,618 输出 tokens**。历史用量不是本次账单或保证上界，尤其遮蔽文本可能改变模型的输出长度；精确 DMX 价格未知，故货币费用为 `UNKNOWN`。如后续获授权执行，建议独立设置硬上限，例如 **最多 240 attempts、200 万输入、5 万输出 tokens**，并在超过任一上限时停止；这只是建议，**不是本轮授权**。既往 WP6 未用完的额度不转入本计划。

主要分析应按任务/锚点聚类，而非把 216 次当独立任务：预先比较同一锚点的 A–B 与 A–C 粗下一步动作分布和完整动作签名，报告原始调用数、不同响应 ID/choice payload 数、缺失与传输不确定，并用任务级重采样评估不确定性。若重复响应严重复用，需降低有效样本解释；即使观察到差异，也只能称为**人工编辑请求的局部 Agent-only 敏感性**，不能推广为自然历史的充分性、Closed-loop 结果或任务成功率。

## 尚需解决的问题与 Gate

当前结构筛选只要求最近用户消息长度至少 40 字符，**不能证明其在遮蔽后仍语境连贯**。12 个锚点的人工语义复核状态保持 `PENDING`；其中一些用户回复显然依赖先前助手提供的信息或问题。正式执行前，应逐条确认遮蔽是否仍对应可解释的问题，或将不连贯者预先排除并发布新版本。TEST 只有 6 个独立任务，属于试点而非总体行为充分性的高精度确认。当前有效 Closed-loop 检查点仍为 0；不能用本计划代替 WP6 恢复验证。

实现为 `src/behavioral_state/history_intervention.py`、`scripts/wp5b_plan_history_intervention.py` 和 `tests/behavioral_state/test_history_intervention.py`。guard 后复现：`.venv/Scripts/python.exe scripts/wp5b_plan_history_intervention.py --output runs/<新的版本目录>`；既有目录拒绝覆盖。工作区预检见 `reports/workspace_guard_report.md`。项目根目录在 D:、无根 `.git`；pinned τ² commit 为 `fc0055dc4e0a316c3f83133267fbd6faaa770992`。Python 3.12.4，PyArrow 14.0.2。最终全项目测试 **234 passed，3 条既有 Pydantic 警告**。新增 API attempt、下载、安装、Closed-loop 执行均为 **0**。

**Gate：受控 Agent-history 请求计划 = PARTIAL（设计已冻结；人工语境复核与付费授权未完成）；WP5-B 严格充分性确认 = UNIDENTIFIED。**
