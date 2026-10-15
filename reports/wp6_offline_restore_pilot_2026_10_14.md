# WP6 离线恢复试点（2026-10-14）

## 结论

在 pinned tau2 `fc0055dc4e0a316c3f83133267fbd6faaa770992` 上，airline、retail、telecom 各一条已归档的真实首轮 Agent 决策锚点，均通过两个独立官方 orchestrator 实例的本地状态恢复核验。状态是 `LOCAL_FIRST_TURN_RESTORE_PASS_EXTERNAL_SESSION_UNVERIFIED`，**不是** WP6 完整闭环分叉通过，也不能据此运行付费采样。

首轮有效证据：`runs/wp6_offline_restore_v2/first_agent_{airline,retail,telecom}_gpt61.json`。`v1` 是较早的检查集，保留作审计；首轮以 `v2` 为准。实施脚本：`scripts/wp6_offline_restore_pilot.py`。

## 方法与实际结果

- 选用 WP5 冻结 inventory 中当前模型 `openai/gpt-6.1-sol-cdx` 的三个真实、精确映射锚点；只选第一次 User 发言后的 Agent 决策，轨迹前缀无工具调用或待执行工具效果。
- 对每条锚点核验 WP2 run manifest 中六个归档文件的 SHA-256，包括初始化快照、决策环境、Agent/User 状态、轨迹前缀和有效请求；用 Pydantic 严格重建归档 Agent/User/轨迹对象，并核对官方 `to_litellm_messages` 结果与当时实际请求消息相同。
- 各自建立两个不同的官方 tau2 orchestrator 对象，从原始任务初始化，确认官方 Agent/User 环境数据库哈希与归档初始化和决策快照匹配；再恢复归档状态、轨迹与决策轮次。每个实例的官方策略提示词、User 提示词、工具 schema、Agent/User 状态、请求消息和推断的 User→Agent 轮次全部相符，两个环境与数据库对象互不共享。
- `airline`、`retail`、`telecom`：各 2 个独立实例、每实例 9 项检查全 True；各 6 个归档文件哈希通过。合计 3 条真实锚点、6 个实例。网络连接在脚本内被禁止；实际 API attempts、branch runs、付费 tokens 均为 0。
- 最终完整受工作区 guard 约束的测试套件：`204 passed, 3 warnings`（已有的 Pydantic `model_` 命名空间警告），约 7.36 秒。

## 含环境变更的中途锚点

从同一冻结 inventory 选出 retail task 59 的真实 Agent 决策 `decision_4fdd7308f156ffff2c7fabf3af49475d63b19455de189a3b15f1eb6bb68fd50d`，其 14 条轨迹包含 4 条工具调用消息和一次 `modify_pending_order_address`；归档决策数据库哈希不同于任务初始化哈希。该任务无 task-level initial state。

`scripts/wp6_middle_environment_replay.py` 在两个独立官方 orchestrator 上执行 `initialize()`，再以完整归档轨迹调用 `environment.set_state(..., strict=True)`；两次均无严格重放错误，决策 Agent 数据库哈希均与归档一致，Agent/User 提示词、工具 schema、Agent 请求消息、User 状态和轨迹 roundtrip 均匹配。有效证据：`runs/wp6_offline_restore_v4/middle_retail_mutating_tool_gpt61.json`。归档六文件哈希通过；网络被禁用，0 API attempts、0 branch runs、0 付费 tokens。

先前的 `v2` 中途试验因未执行官方 `initialize()` 而在提示词比较上失败；`v3` 补上初始化后通过；`v4` 再明确限制无 task-level initial state，避免对带初始化动作的任务错误地重复应用初始化效果。旧结果全部保留。当前成功仅覆盖这一条 retail 工具路径，不能外推到其它任务/域。

## 边界与未解决问题

首轮试点覆盖无工具前缀；另有一条含实际环境变更的 retail 中途前缀通过严格重放。Agent/User 状态仍从归档快照反序列化，尚未证明任意中途轨迹均可严格恢复。服务提供商内部的 User 模型会话/隐状态不可观察且未受控；即使本地签名相等，也不能称为完整闭环保真。尚未执行偏离动作、User 后续反应、分叉后的工具副作用或终局评估，也未分配 WP6 抽样概率。

下一阶段应扩展零付费严格前缀重放到 airline/telecom、带初始化状态和更多工具路径；检查失败必须降级为 Agent-only。只有明确处理 User 服务端隐状态与可重复分叉策略，并另行确定调用预算后，才能安排 WP6 的实际 branch pilot。
