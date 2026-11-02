# WP7 行为终点字典 v1

旧报告的 L0–L4 在不同设计中可能指不同层级，Phase II 不再以数字简称作为变量名。以下所有标签必须保存观察窗、来源和缺失原因；`UNKNOWN` 不得编码为 0。

| 名称 | 定义/提取 | 主要来源 | 自动/人工 | 缺失处理 |
|---|---|---|---|---|
| ACT_CLASS | 单次完整 Agent 决策的粗动作类：工具、通信、结束等；多个同响应 tool call 仍是一决策 | WP3 decision/action、实际 response | 规则自动，边界人工抽检 | 响应无效或未到达记 TECHNICAL_FAILURE |
| TOOL_CALL | 决策提出的规范化工具名及顺序；提案与执行分列 | WP3 action、tool execution | 自动，别名人工核对 | 无工具可为明确 `NONE`，未观测不可填 NONE |
| TOOL_ARGUMENTS | 与调用对应的规范化参数、类型和目标对象，不公开敏感值 | WP3 action/执行记录 | 自动，复杂对象人工复核 | 提案/实际执行不一致另标 PARTIAL |
| COMMUNICATION_SEMANTICS | Agent 对 User 的可执行建议、询问、确认及其语义目标 | Agent 可见输出；不以 User 后验解释 Agent 意图 | 自动候选+盲人工复核 | 无通信与未捕获通信分开 |
| ENVIRONMENT_TRANSITION | 相邻决策/工具步骤的实际 Agent DB、User DB、外部状态变化，含中间反向变化 | WP3 delta、WP6 前后快照/工具结果 | 结构化自动+路径人工复核 | 无变化须有两侧快照；缺侧标 PARTIAL/UNKNOWN |
| FIRST_RELEVANT_ACTION | 预先指定任务字段的首个相关 Agent 动作及 Agent 序号 | 冻结任务目标+WP3/WP6 action | 规则自动+语义复核 | 未到达/自然结束/截尾分开；不得事后改规则 |
| FIRST_RELEVANT_STATE_CHANGE | 首个实际相关环境字段变更及执行者 Agent/User/Tool | 预先指定字段+环境 delta | 自动+执行语义复核 | 终态相同也保留中间变化；缺快照 UNKNOWN |
| FINAL_STATE | 自然终止时的可观测最终 Agent DB/User DB/工具状态 | WP2/WP6 终态快照 | 自动+来源核对 | 截尾不填“无变化”或最终失败 |
| TERMINAL_OUTCOME | 自然终止、成功、失败、预算/上下文截尾、技术中断等；评分另列适用性 | WP2/WP6 summary、适用的官方 evaluator | 自动+人工审计 | 官方评分不适用与缺失分开，不能把未评分算失败 |

所有终点应追加 `task_uid,trajectory_uid,decision_id,branch_uid,transition_id,actor,observation_window,source_ref,validity,missing_reason,protocol_epoch`。Agent 策略、User 工具和环境响应必须分开。No-Future/No-Oracle：状态输入只取该决策前真实可见内容，未来 User/Tool、gold 和最终评分仅供标签/评估，不能进入输入特征。
