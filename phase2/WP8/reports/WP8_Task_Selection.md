# WP8 第一轮任务筛选与候补清单

机器可读矩阵：`WP8_Task_Suitability_Matrix.csv`，18 行（tau2 6、ALE 9、UltraHorizon 3 环境家族）；10 指标各取 0/1/2/UNKNOWN。当前仅 tau2 的可观测结果和本地可重复性按 WP1/pinned 证据赋 2；其余未完成任务级审阅的指标保留 UNKNOWN，**不**凭任务名、难度标签或模型失败率填分。评分仅作筛选，不是质量榜单。

tau2 候选使用固定哈希 `SHA256("20261102:PHASE2_WP8_PILOT_V1|" + task_uid)`，在预设的 Airline horizon 0/2、Retail 0/2、Telecom 1/2 六层各取哈希最小者，保留原 WP1 选择概率和条件性资格。不看后续成功/失败选任务。短名单在 `artifacts/v1/tau2_pilot_shortlist.jsonl`，对应 Airline 原任务 ID 15、37；Retail 101、49；Telecom 两个 MMS 场景（具体 UID 在短名单）。这是预选，不是已批准 WP9 样本；Airline 37 曾在另一历史编辑实验出现非法占位符，WP8 不能借此当新有效历史机制样本，亦不因此事后替换。

ALE 的九个官方 v1.1 ID 已写入矩阵，分布于 business_finance、computing_math、education_info、engineering；均见[官方完整任务清单](https://github.com/rdi-berkeley/agents-last-exam/blob/main/selected_tasks/full.txt)及[Docker 支持清单](https://github.com/rdi-berkeley/agents-last-exam/blob/main/selected_tasks/docker_support.txt)。选择这些是为覆盖不同工作流并降低环境依赖门槛，**不是**已完成逐任务长时域/Memory/安全/资产审查。它们包括 ETL、checkpoint consolidation、feature parity、MARC、Verilog、SUMO 等不同结构；不得从名称直接推断独立决策深度或恢复需求。

UltraHorizon 先列官方三个环境家族（Mystery Grid、Sequence Explore、Alien Genetics Laboratory），不是三个已锁定的 task/scenario ID；若场景粒度/许可证/重置证据不满足，则保持 0 个可执行候选。Odysseys 暂缓。每个候选要补做任务级卡片：原始任务定义与许可、输入资产大小、行动/工具接口、环境 reset/隔离、可观测 Memory、可验证中间进展、外部副作用、安全约束、估算决策长度及参考版本。只可按这些预先定义的资格条件剔除或替换，记录全部剔除原因，不按新模型表现补位。

筛选 Gate：`PARTIAL`。tau2 六个 UID 已冻结为待审清单；ALE 九个 ID 和 UltraHorizon 三家族仍须逐任务/场景审阅。任何付费试点要在负责人确认最终名单、协议、预算和存储路径后才能执行。
