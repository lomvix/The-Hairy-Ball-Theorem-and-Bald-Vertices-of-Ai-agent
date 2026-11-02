# Phase II 第一轮交付与下一阶段执行计划

范围仅 WP7 Historical Evidence Audit 与 WP8 Long-Horizon Benchmark Curation。已读 `agent.md`/`AGENTS.md`、README、集成契约、Codex 执行指南、CHANGELOG 与 `work_packages/PHASE2_MASTER_TASKBOOK.md`。旧 README/契约中“WP7 临界点、WP8 修复迁移”属于 WP1–WP6 旧编号；本轮以用户明确指定的 Phase II 总任务书重新定义 WP7/WP8，**不**执行旧编号的临界点或修复研究。

交付：`phase2/WP7/reports/` 四份审计/字典/主张报告与 `artifacts/v1/` 的 60 Task、6,625 决策、7,280 转移、232 历史基线分支索引；`phase2/WP8/reports/` 的官方资料核查、18 行任务筛选矩阵、候选选择及预算草案。两组报告的详细限制以各文件为准。没有任何新模型/embedding/判分 API 调用，付费 0 attempt、0 tokens；旧 WP1–WP6 原始数据和报告未变。

路径与 Git：工作区根在 D 盘，写入保护见 `reports/workspace_guard_report.md`。主项目无 `.git`，因此 Git 状态 `UNKNOWN`，不能提交 commit 或声称干净；第三方 tau2 工作副本固定 commit `fc0055dc4e0a316c3f83133267fbd6faaa770992`，单次安全目录只读状态无条目。系统 TEMP/TMP 原本在 C 盘；执行派生索引时同进程调用项目守卫，将 temp/cache 指到工作区。没有全局 Git 配置修改或工作区外研究文件写入。

阶段测试：派生脚本一次成功，断言 60/60 Task、324 run、6,625/6,625 唯一 decision、7,280/7,280 唯一 transition、232 基线 branch、6 个 tau2 预选 UID 和 18 行筛选矩阵通过。`pyarrow` 在当前工作区解释器中不可用，故改读已冻结的 JSONL 镜像，不安装依赖。未重跑 No-Future/No-Oracle 原始逐字段校验、未运行新 benchmark 环境、未验证新任务 reset。

可复核 SHA-256：WP1 registry `968e2742ebae4ea74044276203b5388f98dbe0d4dcaa4246c14df2a6e680f73b`；旧 60 Task 根因矩阵 `4ec537c2e86c37c2d9080a3e4cafaee5c97905e2f14be1281ff227cdc379ada6`；新 cohort ledger `17a4f33a8dfce244aa0c8cca5ada332d5e58f100a4762855a2d6c33ed6574cc2`、decision ledger `2fc72b862318b6e4053a1a4180832c70eec465d152f616ff27bbd9e8a22b7513`、transition ledger `7391d25130fa56e573c609b2d0e2363211380420bdaa74272de1b6fc57f494d5`；WP8 矩阵 `005727f0ea105408e80ced8102457c7916f542be18a2d9f5486211121a7f9026`。ALE/UltraHorizon 尚未本地 pinned，不能填虚构 commit。

Gate：WP7 第一轮 `PARTIAL`（后续 WP6 cohort 尚未统一去重链接）；WP8 第一轮 `PARTIAL`（ALE 任务级资产/环境、UltraHorizon 许可和重置未证实）；WP9 `NOT_STARTED`。自然 Type-B-Clean 仍 0；受控历史输入敏感性仅探索性；多步约化状态充分性仍未建立。

下一阶段只建议在负责人确认后执行：①补齐 WP6 后续版本的 branch/checkpoint/transition 去重关联，保留截尾与来源；②逐项审阅 ALE 九任务和 UltraHorizon 场景，核查许可证、资产体积、沙箱写入、日志/Memory/reset；③冻结最终任务名单、模型及真实价格、每 Task run 数、付费 attempt/token/人民币上限和工作区输出路径；④本地零付费 dry-run 通过后再考虑 WP9 小规模采集。当前**等待研究负责人确认**，不启动 WP9。
