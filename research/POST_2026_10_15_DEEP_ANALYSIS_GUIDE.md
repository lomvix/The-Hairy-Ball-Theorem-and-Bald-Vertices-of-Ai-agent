# 10/15 后深入分析材料与复核路线

版本：2026-11-02 初稿。配套综述：`reports/post_2026_10_15_experiment_synthesis_2026_11_02.md`。本文件只公开可复核的问题、聚合数、版本化来源名称和分析规则；原始 benchmark 请求/响应、任务文本、数据库快照、用户资料、密钥和 embedding 均保留在本地，不随本文件发布。

## 研究问题与三个不可合并的估计对象

| 线 | 比较对象 | 需要的证据 | 目前判断 |
| --- | --- | --- | --- |
| 自然历史 | 相同当前条件下的两条**真实**不同历史 | 不同 run 来源、完整非 Agent 可见面/环境/Memory 支持、各来源独立恢复及重复 | 3,445 候选中严格 Type-B-Clean 0；效应不可识别。 |
| 受控输入 | 同一恢复点 A 原始、B 遮蔽、C 保留事实改写 | 三臂资格、全重复表达编辑、User/环境不变、A 基线波动、C 文本扰动对照 | 已有局部行为与环境机制，跨 Task/域净效应待确认。 |
| 状态预测 | 冻结的约化状态 X 与更充分的可见状态 X+ 对未来 L2/L3 的预测 | 未用于造状态的 Task、完整 Agent 序号、User/工具步骤与删失、Task 级误差 | 尚无独立前瞻确认；不能从受控分叉直接称 X 充分。 |

## 版本化证据地图（本地私有数据不上传）

| 用途 | 首选冻结来源 | 核对点 |
| --- | --- | --- |
| 60-Task 来源、WP2 流失、WP3/4 测量 | `artifacts/wp1_wp6_root_cause_audit_v1/`、`artifacts/wp1_wp6_wp2_attrition_v1/`、`artifacts/wp1_wp6_wp4_measurement_audit_v1/` | Task 权重、251/73 有效 run、2,831 Study Agent 决策与 6,625 跨角色帧分开；qwen3.7 epoch 不跨版本比较。 |
| 10/24 R2 原始分支与评分 | `artifacts/wp6_all_useful_sample_statistical_audit_v4/`、`artifacts/wp6_task_anchor_outcome_coverage_v1/` | v1–v3 统计草稿不作最终分母；232 唯一分支与 129 个已评分自然终止单列。 |
| 10/27 预注册再采样 | `runs/wp1_wp6_preregistered_plan_v3/`、`artifacts/wp1_wp6_final_task_matrix_v2/`、`artifacts/wp1_wp6_agent_only_analysis_v1/`、`artifacts/wp1_wp6_closed_loop_analysis_v4/` | `final_task_matrix_v1` 有生成计数错误，不引用；A–B/A–C 与 Type C 分层。 |
| 10/29 混合样本总索引 | `artifacts/wp1_wp6_sample_gap_analysis_v1/` | 683 行为混合设计索引，不与其组成 cohort 再相加；使用修正后的完整 Agent1–4 序号。 |
| 10/30 信息优先 P1/P2 | `artifacts/wp1_wp6_information_results_v3/p1/`、`p2/` | 9/6 Task、108/72 分支、110/378 attempts；P2 只以 4 个完整 Task 作三臂主比较。 |
| 双域 48 分支与 User 路径 | `artifacts/wp1_wp6_dual_domain_information_mechanism_v2/`、`runs/wp1_wp6_dual_domain_information_execution_v1/` | 首次相关动作、重新获得事实、Agent 直接 DB 与 User 工具 DB 分开；后期 23 条截尾。 |
| 11/02 单 Task 复制 | 五份 `reports/wp1_wp6_rank{27,32,37,4,33}_*_pilot_2026_11_02.md` 对应的 `runs/*pilot_execution_v1/` 与 `artifacts/*pilot_analysis_v1/` | 逐项区分结果盲选、字段合法性、A/C 对照和首次可达时点；不把 4 次重复当 4 Task。 |
| 最近有界筛选 | `artifacts/wp1_wp6_telecom_request_only_screen_v1/result.json` 及 Airline/信息锚点筛选报告 | 只对冻结首 run/短名单下结论，失败原因不能外推为整个 Task 永不合格。 |

## 建议先做的四项深入分析

1. **构造唯一、不可加错的研究样本账本。**以 `task_uid → run_uid → decision_id → checkpoint_id → arm → seed_label → branch_uid → request/step` 为层级，给每行标记设计、自然/干预来源、是否已在旧 cohort 计数、是否被后续选择。分别输出 Task、锚点、配对组、分支和 attempt 分母。对 55/60 覆盖、各域未观察 Task、自然 Clean 0 与 Parent Token 保守账本作断言。公开只出聚合表，私有 ID 不发布。
2. **重审“信息遮蔽强度”而非只看字符串。**每锚点记录事实来源、Agent 可见历史内全部重复、当前受保护消息是否重述、保留的 ID/选项能否反推、B 的语境/字段是否合法、C 是否保留机器可检索实体字面、首次新 User/工具反馈何时重新提供事实。将 Retail 旧商品映射、Retail 地址、Telecom 设备状态、User 程序性能力与 Airline 结构化日期分层，不能把这些异质编辑汇成一个处理强度。
3. **重算事件锚定的局部未来。**保留固定 Agent1/2/3/4 终点作横向比较；另在付费前定义“首次与目标事实有关的可执行工具／User 操作及相邻 DB 转移”。分别编码 L2 工具/规范化参数、自然语言中的建议、User 实际调用、Agent DB、User DB、暂时逆向切换、最终目标字段及自然终止/上限截尾。不存在的后续端点记缺失，不能填成相同。对 10/29 重放使用已更正的完整 Agent 序号。
4. **Task 级不确定性与反例审阅。**A–B 与 A–C 逐 Task 差异及二者之差，与 A 臂自身重复波动并列；Task 级 bootstrap、离群 Task 留一、时间块分层、对 2 个 P2 技术停止和后期截尾作界限。针对 Retail 地址两 Task 做结果盲选/窗口敏感性；针对 Telecom 漫游的暂时 off→on 做预定义路径编码后在新独立 Task 前瞻检验，不能拿事后编码的 1/4 报总体风险率。对于 Airline 日期占位符案例单列“非合法值输入”实验，不纳入严格三臂净效应。

完成上述离线复核后，才能冻结新的独立 Task 采样和 X/X+ 状态预测协议。优先找不被当前消息重述、也不会在首次工具/User 响应中立刻重新获得的旧事实；保持三域与自然历史各自原 Gate，不因已观察结果替换 Task。若严格自然支持仍为 0，明确写“不可识别”，不要扩大同一锚点调用数来代替支持。

## 最小交付表与判定规则

建议私有版输出五张表：`cohort_ledger`（不可重计）、`anchor_qualification`（事实/重复/合法性）、`branch_endpoints`（完整 Agent 序号及 Agent/User 作用）、`task_level_contrasts`（A–B、A–C、A 基线）、`missingness_and_censoring`（自然终止/技术/上限/评分资格）。每表必须有来源 manifest/hash 和版本；新结果不得覆盖旧原始数据。公开版只保留按域、Task 及机制类别的聚合摘要，不附逐条 benchmark 内容。

判定次序：先检查自然共同支持；再检查干预资格与对照是否真保留事实；再检查主终点是否在可观察窗口内；最后才估计差异及区间。若任何前提失败，报告 `UNIDENTIFIED` 或探索性局部效应，不把不显著解释为状态充分。最终应形成三个独立结论：自然历史作用、受控历史信息敏感性、多步约化状态预测支持。

