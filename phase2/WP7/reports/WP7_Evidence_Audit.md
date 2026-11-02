# WP7 Historical Evidence Audit：第一轮结论（2026-11-02）

## 研究状态

核心证据为 60 个冻结 Task、324 个有效 WP2 run、2,831 个 Study Agent 决策、6,625 个跨角色 WP3 帧、7,280 个 WP3 转移记录。WP3 转移中一半是 Agent 决策边、一半是 Closed-loop 边；其结构完整不等于 7,280 次环境改变，也不等于有足够重复邻域来估计 (K(x'\mid x))。用于状态构造的 Agent 有效输入引用已存在，但全部帧的上下文截断状态为 UNKNOWN；Memory 43 帧 PARTIAL。应把这些不确定性带入 WP10 状态质量标记。

历史自然对照仍无严格 Type-B-Clean（0/3,445 候选），因此自然历史效应 `UNIDENTIFIED`。人工历史信息三臂与真实闭环的局部路径变化是 `EXPLORATORY`/有限 `SUPPORTED`，不能反向证明自然效应或已获得 Markov 状态。样本最有信息的现象不是单纯终局成功：Retail 地址写入往往发生在 Agent3–6，Telecom 漫游一条 B 路径短暂 true→false→true 而终态相同；固定 Agent2、只看最终 DB 会漏掉机制。反过来，User 介入首步 B 特异信号在另一组独立 Task 未复现，必须同权保留负例。

## 有效性与流失

- WP1：60/60 来源、horizon、入样概率可追溯；原总体仅冻结 60 Task，Retail 全部 CONDITIONAL，外推/评分资格有限。
- WP2：383 manifest 中 324 有效；59 非有效/中断不得混入行为分母。Attempt、response、run、decision 严格分列。
- WP3：6,625/6,625 decision ID 唯一、7,280/7,280 transition ID 唯一；Agent 3,640、User 2,942、Evaluator 43。历史全体 No-Future/No-Oracle 结论沿用 `artifacts/wp1_wp6_root_cause_audit_v1/wp3_validation.json`，本轮只复核索引与来源，**未重新跑**原始请求逐字段审计。
- WP4：4,114 有效语义向量是测量，不是独立轨迹；不得与 Phase II 拟议 v4 坐标直接合并。
- WP5：自然配对缺乏共同支持，不能放宽硬匹配制造 Type B。
- WP6：10/24 基线 232 分支中 139 自然终止、80 调用截尾、13 技术中断；后续实验多 cohort 重叠，55/60 是“曾有某种观察”，不是 55 个局部核可识别 Task。分支有效性需逐锚点复核双恢复、下一请求、环境隔离；单纯本轮索引不提供新恢复证明。

## 第一轮 Gate

资产盘点、终点字典、历史主张分级和基线层级索引 `PASSED`。全部 WP6 后续分支与 checkpoint/transition 跨版本统一去重、环境变化可估计集合、完整独立 Task 覆盖的动态更新仍 `PARTIAL`。当前数据可支持 WP10 的离线状态候选设计；**不能**直接作为 WP12 局部核/Policy Field 的确认性样本，亦不启动 WP9。

实际测试：同进程工作区 guard 后，标准库索引构建运行 1 次成功；60 Task、324 run、6,625 decision、7,280 transition、232 历史 branch 断言全部通过。未安装包、未调用付费 API、未下载 benchmark、未修改旧样本。项目根目录无 `.git`，所以不能给出主项目 commit/干净状态；第三方 tau2 固定 commit 可读。新制品仅 `phase2/WP7/`、`phase2/WP8/` 与工作区报告。下一版须将后续 cohort 以原始 branch UID 去重并建立 checkpoint/transition 的完整连接，保留所有截尾与失败，不覆盖 v1。
