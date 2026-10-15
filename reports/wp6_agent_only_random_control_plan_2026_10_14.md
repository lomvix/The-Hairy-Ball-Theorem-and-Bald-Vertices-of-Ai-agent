# WP6 Agent-only 随机对照子计划（2026-10-14）

## 结果与范围

已从 WP5 冻结的 1,465 条精确有效请求中，按 3 个当前模型 × 3 个域分层，冻结 **10 条随机对照锚点**：每格均匀抽 1 条，另均匀抽中 1 个格子再抽第 2 条。种子为 `20261014`，无根据结果重抽、排除或调换。10 条覆盖 9 个不同任务，阶段分布 EARLY 5、MIDDLE 1、LATE 4。若将来构成 24-anchor pilot，这 10 条占 41.7%，满足随机对照 ≥40% 的硬约束；余下 14 条定向锚点**尚未冻结**，故这不是完整 WP6 Pilot 计划。

有效产物：`runs/wp6_agent_only_random_control_v1/random_control_frame.parquet`（全部 1,465 条候选及概率）、`anchor_selection_v001.json`（抽样种子与入选 ID）、`branch_plan.parquet`（10×8=80 条仅规划的 Agent-only 重复）、`manifest.json` 和 `validation_v1.json`。配置为 `configs/wp6/agent_only_random_control_v1.yaml`。校验返回 PASS、0 错误；完整测试套件 214 passed，另有 3 个既有 Pydantic 警告。

## 入样概率与预算事实

对任何候选，设其模型×域格子有 `N_cell` 条；其作为随机对照被纳入的概率严格为 `10/(9×N_cell)`：基础均匀抽样概率 `1/N_cell`，再加该格子以 `1/9` 概率获得第二个名额所增加的 `1/N_cell`。每条候选均在 frame 中记录格子大小、分数式与数值概率；80 条计划记录继承其锚点的随机对照入样概率。此概率只适用于 **RANDOM_CONTROL 分析角色**，不能冒充尚未设计的定向锚点总体入样概率。

规划中的 80 次重复，按这些相同基准请求的历史 token usage 逐条乘 8，估计输入约 **608,984 tokens**、输出约 **15,792 tokens**。这是历史用量的机械外推；模型/服务时段变化与重试会改变实际消耗，**不是硬预算或价格报价**。DMX 当前单价及本轮付费上限未核实；配置与计划均标记 `NOT_AUTHORIZED_NOT_STARTED`，不会从 branch seed 覆盖原始 provider seed 或采样参数。

## 未解决问题和下一步

- 需要另行按预注册规则冻结剩余 14 条定向锚点，优先补足 MIDDLE、结构事件和几何候选覆盖；不能用 WP6 后续响应或未来结果反向选点。WP5 几何配对只是候选，不是已证实的 aliasing。
- 需要确定实际 DMX 价格、逐请求 token/attempt 硬上限、熔断和付费授权后，才可执行 Agent-only；执行时只读取冻结的精确请求，不运行工具。当前 API attempts、branch runs 和付费 tokens 均为 0。
- Closed-loop 继续标记未验证，不能用 Agent-only 抽样替代 User 服务端隐状态和完整分叉恢复检查，也不能据此推进 WP5-B 闭环确认。
