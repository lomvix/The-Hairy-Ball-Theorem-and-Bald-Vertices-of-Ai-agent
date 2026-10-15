# WP5 可观测状态 v2.1：历史信息缺口与配对重筛（2026-10-15）

## 实施范围

本轮是 **WP5-A 的离线补充审计**，不是覆盖已冻结 `B0_CURRENT`，也不是 WP5-B 的分叉充分性确认。读取冻结 WP5 `handoff_v5` 的 2,831 个 Study 决策及 3,445 个同条件跨运行配对，为每条已归档 Agent 有效请求发布逐角色消息指纹，并对原配对重新标注可比性。没有读取未来动作或 WP6 分叉结果来选配对；新增 API attempt、下载和采样均为 **0**。

成果在 `runs/wp5_observable_v2_1/`：`observable_states.parquet`（2,831 行）、`pair_comparisons.parquet`（3,445 行）、`manifest.json`。来源清单 SHA-256 为 `15b13fa65c979b205b112769d3ae463b69111331dcfe27c2297b45d455de8cff`；两张表 SHA-256 分别为 `c64c3a8af35d6f081eb2ab9f3c1962610a651d70af839bd79ee8014fad64e3ae` 和 `cf701d8c128372a23334ffc26393a93c7de71cce8ba5953eba16ea82aa531aa1`。先前试算目录 `runs/wp5_observable_v2/` 保留为审计痕迹；其中宽松数字模式把订单号误称为电话线索，因此 **v2.1 是本轮唯一采用版本**。

新表示保留最后与更早用户消息、最近与全部工具观察、策略消息、完整非 Agent 消息序列、先前 Agent 序列的独立 SHA-256 指纹。`request_goal_evidence_hash` 仅是排除极短字面确认语后的用户文本序列指纹，**不是语义目标分类**；身份线索仅标记用户可见文本中的邮箱字面模式，**不是身份已核验**。确认状态只标注最近用户消息是否匹配有限的肯定/否定字面词表，不能推断真实授权或用户意图。完整非 Agent 指纹另分为含请求局部 `tool_call_id` 的精确版本与不含该 ID 的消息负载版本。所有字段都来自该决策时刻实际归档请求，不引入隐藏 User Scenario 或未来结果。

## 实际结果

| 重筛条件 | 配对数 |
| --- | ---: |
| 冻结同条件跨运行配对 | 3,445 |
| 原 WP5 几何候选 | 273 |
| 候选中最后用户消息相同 | 37 |
| 候选中最后用户消息与最近工具结果均相同 | 30 |
| 上述 30 组再要求更早用户消息序列相同 | **0** |
| 全部配对中完整非 Agent 消息负载相同、先前 Agent 消息不同 | **0** |
| 全部配对中完整非 Agent 消息逐项精确相同 | 2；两组 Agent 序列也相同，B1 历史距离为 0 |

273 个几何候选覆盖 25 个任务，但相同最新用户消息及工具观察的 30 组只来自 5 个任务。候选中的策略消息指纹全部相同；仅 8 组的更早用户消息序列相同，而且它们不在上述 30 组之内。273 组的“目标证据”全文指纹均不相同。由此可见，冻结 B0 的近邻/零距**没有**隔离出“只有先前 Agent 历史不同”的对照。已有两组完整非 Agent 观察相同的自然配对，也缺少 Agent 历史差异，不能用于检验历史因果作用。邮箱字面线索出现于 15/2,831 个状态；最近用户消息的有限字面确认词表只命中 2 个肯定表达。因此这些词法标注覆盖很窄，不能据此宣称身份/确认状态已被充分建模。

## 方法、测试与 Gate

实现：`src/behavioral_state/observable_v2.py`、`scripts/wp5_build_observable_v2.py`，新增 `tests/behavioral_state/test_observable_v2.py`。复现命令是在项目根目录先执行 `scripts/Initialize-WorkspaceGuard.ps1`，再用 `.venv/Scripts/python.exe scripts/wp5_build_observable_v2.py --output runs/<新的版本目录>`；既有版本拒绝覆盖。冻结表会对照原 manifest 验证 SHA-256，输出写入和临时文件均限制于 `<WORKSPACE_ROOT>`。项目根目录无 Git 仓库；pinned τ² checkout commit 仍为 `fc0055dc4e0a316c3f83133267fbd6faaa770992`。本轮未改 benchmark。Python 3.12.4、PyArrow 14.0.2；测试命令 `.venv/Scripts/python.exe -m pytest -q` 在 guard 后运行。

新定向测试 **4/4**，包括订单号不得被当成联系方式；最终全项目 **231 passed、3 条既有 Pydantic 警告**。工作区写入边界预检见 `reports/workspace_guard_report.md`。没有付费请求，因此新增接口费用为 0。

**Gate：WP5 可观测状态缺口审计 PASSED；WP5-B 严格行为充分性确认仍为 UNIDENTIFIED。** 下一步若要辨识先前 Agent 历史的作用，应先冻结“同一用户/工具/策略可见输入，仅改变先前 Agent 话语”的受控成对请求及阴性对照，并明确同一模型、路由、采样和时间块约束；当前归档自然配对不能替代这一步。Closed-loop 恢复尚未证明，不能把 Agent-only 的下一步动作等同任务结果。新增付费分叉需要独立计划和预算授权。
