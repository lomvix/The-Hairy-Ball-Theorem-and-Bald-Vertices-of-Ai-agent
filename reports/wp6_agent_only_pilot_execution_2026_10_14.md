# WP6 Agent-only Pilot 执行报告（2026-10-14）

## 范围与结论

已按冻结的 `runs/wp6_agent_only_pilot_v1/branch_plan.parquet` 完成 **24 锚点 × 8 次 = 192 次 Agent-only 请求**，没有扩展到 Closed-loop，没有执行任何工具或推进 User/Environment。随机对照为 10/24 锚点（41.7%），三个域各 8 锚点；Claude 7、Gemini 8、GPT 9 锚点。计划本身未被改写。

本次授权硬上限为最多 240 次 API attempt、2,000,000 输入 tokens、80,000 输出 tokens（含重试）。实际为 **192 attempt / 192 成功 / 0 重试 / 0 不明用量 / 0 未闭合 attempt**，报告的 provider usage 合计 **1,809,204 输入、19,618 输出 tokens**。剩余额度不自动转作新计划。三个模型在 DMX 公共价格页面的精确单价未能验证，故真实货币费用为 `UNKNOWN`，不以 token 量伪造价格。

## 写入边界与实现

真实项目根目录 `<WORKSPACE_ROOT>`，位于 D:，本轮预检剩余 119,995,793,408 bytes；根目录没有 Git 仓库、不是 reparse point。进程级 guard 把 TEMP/TMP/TMPDIR、pip/uv/HF 缓存及 Python bytecode 路径设于项目内。固定 tau2 commit 为 `fc0055dc4e0a316c3f83133267fbd6faaa770992`，工作树干净。无下载、安装或工作区外研究写入。

新增 `src/branching/agent_only_runtime.py`：逐次验证 WP2 原始请求来源哈希，重建相同的模型、消息、工具 schema、tool_choice、temperature/reasoning_effort/seed；用 `requests` 发一次合法推理，收到响应立即停止，不接入 benchmark 工具执行器。串行与最多 4 路实际并发的调度使用同一工作区内的 append-only attempt journal，发起前预留预算，返回后按实测 usage 结算；技术失败最多准备一次可审计重试，但本轮没有重试。任何 provider seed override 均未应用。原始响应完整保存，凭证只在内存中注入；最终扫描执行、分析及 canonical 前缀产物共 777 个文件，API key 原文命中 0。

原始执行证据：`runs/wp6_agent_only_execution_v1/authorization.json`、`journal/`、`attempts/`、`responses/`。授权 sidecar 固定本轮上限与计划 SHA-256 `1eac550ea7e12ddfc256dfaf3cda07bff169fbd2f5dae06a3ed82d282b97e197`。

## 实际质量核验

- 24 个锚点各恰有 8 条有效响应；三个域各 8 锚点。192 个 `attempts` 与 192 个原始 `responses` 对应，全部有 usage、HTTP 200，工具执行文件为 0。请求的返回模型别名与各源 WP2 调用一致：Claude 返回 `claude-sonnet-5-5`、GPT 返回 `gpt-6.1-sol`、Gemini 返回 `gemini-3.8-flash`；192 条别名核验 0 不符。
- `runs/wp6_agent_only_analysis_v1/branch_runs.parquet` 有 192 行；`agent_action_distributions.parquet` 有 27 行，各锚点频率和为 1。按固定粗分类，21/24 锚点的 8 次响应属于单一类别，另 3 锚点有两类；按完整动作签名（含工具参数/文本）13/24 锚点仅 1 种，其余锚点有 3–8 种。这是描述性结果，不等于行为充分性已证实。
- 6 组 Claude 响应 ID 复用，合计涉及 15 次 attempt；组内原始 choice payload 相同，但 15 次各自有不同的 `x-request-id`。其余 GPT/Gemini 没有该 header：总计 56/192 次有可见且唯一的 provider request header，183/192 个响应 ID 唯一。不能排除代理缓存、确定性重放或服务端私有状态的影响，独立随机 draw 数量 `UNIDENTIFIED`。
- `calculate` 工具的 intended effect 未被固定 tau2 域工具装饰器分类，共 8 次标记 `UNKNOWN`，不隐式猜成读取或写入。所有工具选择的**观测效果**都是 `NOT_EXECUTED`；不得把动作意图当成数据库变化。
- 全项目 guarded tests：**221 passed，3 条既有 Pydantic warnings**。本轮新增 Agent-only 单步、恢复不重复调用、并发账本、动作归类与 Wilson 区间测试 5 条均通过。

## 产物与门禁

`runs/wp6_agent_only_analysis_v1/branch_manifest.json` 声明 `agent_only_status=COMPLETE`、`closed_loop_branches=0`，并保存两个 Parquet 的 SHA-256。`agent_action_distributions.parquet` 的 K=8 均标 `LOW_SUPPORT`；Wilson 区间仅作有限样本描述，不把重复 tool call 当独立试验单位。

Agent-only 原始采集和描述性分布已完成；**WP6 整体仍为 PARTIAL**。初版 `branch_runs.parquet` 的 `canonical_trace_ref` 为 null，保留其生成时的状态。随后新增 `runs/wp6_agent_only_canonical_v1/` 单步因果前缀：192 条 branch lineage、583 个 WP3 v1 schema 事件、192 个动作、8 个质量标记；783 个对象通过 WP3 Pydantic schema 验证，事件父边与序号核查 0 错误，4 份 Parquet 的 manifest 哈希均一致。事件仅有 MODEL_REQUEST、MODEL_RESPONSE、AGENT_MESSAGE、Agent 提议的 TOOL_CALL；工具结果、环境变化及闭环转移均为 0。它复用了 WP3 的 schema、事件构造器和工具 ontology，**没有**运行 WP3 的完整自然轨迹 builder，故应称作 `AGENT_ONLY_ONE_RESPONSE_PREFIX`，不冒充完整 canonical run。

Closed-loop 因外部 User provider 隐状态无法核验，维持 `BLOCKED_BY_STATE_RECOVERY`；本轮没有授权 Closed-loop，不能据 Agent-only 结果推进 WP5-B 闭环充分性确认。
