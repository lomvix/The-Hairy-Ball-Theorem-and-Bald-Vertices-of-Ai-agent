# WP6 跨模型、跨域离线恢复阶段报告（2026-10-14）

## 实施结论

已对冻结 WP5 锚点中的 9 条真实“工具调用后环境数据库发生变更”的 Agent 决策做离线保真探针，覆盖 `gpt-6.1-sol-cdx`、`claude-sonnet-5-5-cc`、`gemini-3.8-flash` × airline、retail、telecom。每条锚点在两个独立官方 tau2 orchestrator 实例中均通过严格初始化后轨迹重放；合计 18 次本地恢复、54 个归档工件 SHA-256 核验通过。telecom 的 3 条任务带 task-level 初始化状态，均通过“先初始化、再只重放后续轨迹”的边界检查。

结构化证据为 `runs/wp6_offline_replay_matrix_v1/checkpoint_audit.parquet` 和 `manifest.json`；逐条原始核验结果在 `runs/wp6_offline_restore_v7/`（GPT）和 `runs/wp6_offline_restore_v8/`（Claude、Gemini）。这是一组**能力探针**，按可用的数据库变更路径有目的地选取，并非预注册的 WP6 随机 branch 样本；未赋 selection probability，不得用于估计总体恢复率。

## 实际测试结果

- 9/9 锚点均为 `LOCAL_STRICT_PREFIX_REPLAY_PASS_EXTERNAL_SESSION_UNVERIFIED`；每条两个隔离实例的初始/决策数据库哈希、官方 Agent/User 提示词、工具 schema、归档 Agent 请求消息、User 状态与轨迹 roundtrip 核验均通过，严格重放无异常。
- 初始化边界新增纯函数检查及 5 个正/负例测试，覆盖前缀不匹配、初始化未完成的工具调用、以及在工具结果处截断等情形。WP6 定向测试：14 passed；完整受工作区 guard 约束的项目测试：209 passed、3 个既有 Pydantic 警告。
- 0 API attempts、0 branch runs、0 paid tokens；没有下载或安装，也没有把原始 benchmark 文本、密钥写入矩阵报告。

## 未解决问题与下一步门槛

服务端 User 模型会话/隐状态仍不可观察、不可恢复；Agent/User 对象由归档快照重建，本轮未执行偏离后的 User/Agent 交互，也未证明任意任务和工具路径都可重放。因此 9/9 仅是**本地严格前缀重放**，完整 Closed-loop 保真通过数仍为 **0**；审计表统一标记 `REVIEW_EXTERNAL_SESSION`。

进入正式 WP6 分叉之前，应分别确定 Agent-only 与 Closed-loop 的可执行范围：Agent-only 可基于已归档的精确有效请求单独规划，但须先冻结随机对照比例、选择概率、每锚点次数与独立付费预算；Closed-loop 还需要解决 User 服务端隐状态控制或给出严格的降级方案，并做真正偏离动作后的隔离验证。不得将此次 9 条有目的探针当作 24-anchor Pilot 或自然分叉证据。
