# WP7 研究主张审计 v1

证据等级：`CONFIRMED`（独立支持与有效复现）、`SUPPORTED`（局部有效但外推有限）、`EXPLORATORY`（机制/小样本）、`UNIDENTIFIED`（共同支持或观测不足）、`INVALID`（违反对照/定义）。本轮未将任何关键理论主张升为 CONFIRMED。

| 主张 | 等级 | 审计理由 |
|---|---|---|
| 自然历史在相同当前状态下仍影响 Agent | UNIDENTIFIED | 3,445 自然候选中严格 Type-B-Clean=0；不能把人工遮蔽冒充自然对照 |
| Agent 对历史事实遮蔽的输入敏感性 | EXPLORATORY | 10/30 P1 9 Task、P2 6 Task 和四 Task 双域闭环有局部路径差异；三臂 C 对照自身会变化、Task 支持少，且部分候选编辑不完全剥夺事实 |
| Agent-only 同请求动作波动 | SUPPORTED（观察层） | 多锚点重复有可见动作变异，但 response ID 复用/条件变化限制独立随机推断；不能替代闭环 |
| 局部闭环行为/环境转移差异 | SUPPORTED（限定锚点） | 已有真实 User/工具分支及 Level-3 应用层恢复；分支多集中于 Telecom、截尾高，不能外推到全 60 Task |
| 原约化状态具多步行为充分性 | UNIDENTIFIED | 尚无冻结 X/X+ 后在独立 Task 的前瞻多步预测/转移核确认；近 embedding 不等于相同状态 |
| 光滑行为流形、向量场临界点或拓扑指数 | UNIDENTIFIED | 尚无稳定局部几何、切空间、漂移与拓扑前提验证；不能从失败或 kNN 图直接推出 |

应同等保留负例：User 介入 9 Task/54 闭环首步 A–B 5/18 vs A–C 1/18 的表面信号，在另 9 个独立 Task 的 108 单步复制中变为 5/36 vs 5/36；原信号未复现。Retail rank 15 的严格本地资格 3/3 与 15/15 测试是实现/资格证据，不是行为效应。Telecom rank 33 一条遮蔽臂路径出现漫游 true→false→true 的暂时逆向转移，三臂终态相同；这只是 1 个 Task 中 1 条探索性机制样本，不能报发生率。详见 `reports/post_2026_10_15_notable_sample_cases_2026_11_02.md`。
