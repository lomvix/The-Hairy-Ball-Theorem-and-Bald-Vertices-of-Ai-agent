# WP6 Agent-only 24-anchor Pilot 计划（2026-10-14）

## 阶段结果

已冻结 **24 条真实锚点、192 条 Agent-only 重复请求的未执行计划**。三个域各 8 条；当前模型覆盖 Claude 7、Gemini 8、GPT 9；阶段为 EARLY 11、MIDDLE 7、LATE 6；共有 17 个不同 task。组成：随机对照 10 条（41.7%）、结构性“紧跟工具结果”6 条（25%）、几何近态候选 3 对共 6 条（25%）、基准自然运行成功/失败分歧 2 条（8.3%）。几何配对只属于 WP5 预筛候选，不表示已证实状态混叠。

冻结产物在 `runs/wp6_agent_only_pilot_v1/`：`branch_plan.parquet`、`targeted_branch_plan.parquet`、`targeted_selection_frame.parquet`、`anchor_selection_v001.json`、`manifest.json`、最终 `validation_v2.json`。全体随机候选及概率仍在 `runs/wp6_agent_only_random_control_v1/random_control_frame.parquet`；定向候选池在 `runs/wp6_targeted_pool_v1/targeted_frame.parquet`。配置为 `configs/wp6/agent_only_random_control_v1.yaml` 与 `configs/wp6/agent_only_targeted_v1.yaml`。

## 选择机制与概率边界

随机层先从全部 1,465 条精确请求中按模型×域九格抽样，每格 1 条，加 1 个随机 bonus 格；该角色对每条候选的入样概率为 `10/(9×N_cell)`，不使用未来结果。已冻结随机层之后，定向层才从剩余 1,455 条中按互斥优先级分类：基准自然运行分歧、WP5 几何候选、紧跟工具结果、其它。预注册的模型×域名额为 3 个候选 pair、6 个结构单点、2 个分歧单点。

定向单点在各自层内均匀抽样，其概率为 `1/N_stratum`；几何层均匀抽 1 对，每对概率为 `1/N_pairs`，某端点若出现在多对候选中，其端点入样概率为 `degree/N_pairs`。计划明确区分随机角色的**无条件**概率与给定已冻结随机层后的定向**条件**概率；不能把二者混成一个总体权重。基准成功/失败结果只用于最后一个*定向层的选点标签*，绝未注入 Agent 当前请求/状态，且不会被当作无偏总体估计。WP6 分叉未来结果完全未参与选点。

## 实际验证和预算

- 随机子计划校验 `validation_v1.json`：PASS、0 错误。完整 24-anchor 计划的首次校验误把数据类别 `GEOMETRIC_ALIAS_CANDIDATE` 与分析角色 `GEOMETRIC_PAIR_CANDIDATE` 视为同名，留下 `validation_v1.json` 失败记录；修正映射后的 `validation_v2.json`：PASS、0 错误，3 对 pair 均完整，24×8 行数与概率均匹配。
- 新增随机/定向概率单元测试；完整受工作区 guard 约束的项目测试：**216 passed、3 个既有 Pydantic 警告**。
- 按选中锚点当时相同请求的已记录 token usage 机械乘 8，历史等量估算为输入 **1,436,688 tokens**、输出 **25,760 tokens**。这不含重试或服务端计量变化，**不是已批准的 hard cap、价格或实际消耗**。计划无 provider seed 覆盖，不改变冻结请求采样参数。
- 实际 API attempts、付费 tokens、branch runs 均为 **0**。计划标记 `NOT_AUTHORIZED_NOT_STARTED`；Closed-loop 仍未放行。

## 尚未解决的执行门槛

需要先确定当前 DMX 单价/可计费模型、逐请求与全批次的 attempt/input/output token 硬上限和熔断策略，并获得明确的 WP6 付费授权；否则只能继续 Mock/离线工作。正式 Agent-only 执行器还需证明仅重发精确有效请求、收到动作立即停止且绝不执行工具，并将原始响应和失败追加记录在工作区内。User 服务端隐状态未解决，因此即便 Agent-only Pilot 将来完成，也不能把它当作 Closed-loop 保真或 WP5-B 闭环充分性证据。
