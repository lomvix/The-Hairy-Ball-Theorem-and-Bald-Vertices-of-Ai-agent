# WP8 官方 Benchmark 资料核查（2026-11-02）

本轮仅查阅官方网页/代码与本地固定 tau2 副本；未下载或运行新 Benchmark。网页 `main` 是浮动版本，后续实施必须锁 commit、资产 manifest 和任务版本。

| 项目 | 官方已核实 | 尚未知/执行限制 | 首轮判断 |
|---|---|---|---|
| tau2 | [官方仓库](https://github.com/sierra-research/tau2-bench)，本地固定 `fc0055dc4e0a316c3f83133267fbd6faaa770992`；Airline/Retail/Telecom 的交互、工具及任务评分见[官方域说明](https://github.com/sierra-research/tau2-bench/blob/main/src/tau2/domains/README.md)。本地 `pyproject.toml` 标 MIT；已有 WP1 reset/replay、WP2/3 轨迹。 | 后续采样的长窗口仍需同版本恢复验证；任务类型并非天然“长时域”。 | 保留可控多轮对照；6 个新试点候选来自既有 60 Task，不替换总体。 |
| ALE | [官方代码/README](https://github.com/rdi-berkeley/agents-last-exam)：v1.1 有 122 active Task，框架 Apache-2.0、Task 数据 CC-BY-4.0；任务为可执行 `main.py`，使用桌面/CLI 沙箱、隐藏参考与评分；官方统一轨迹记录每步、工具和观察。[完整任务列表](https://github.com/rdi-berkeley/agents-last-exam/blob/main/selected_tasks/full.txt) 与 [Docker 允许清单](https://github.com/rdi-berkeley/agents-last-exam/blob/main/selected_tasks/docker_support.txt) 可核对 ID。 | 当前 Windows 工作区没有核实 KVM/Docker/云 VM 写入隔离、各任务资产大小、任务级 reset/Memory 可见性、价格；某些任务需嵌套 Docker/QEMU，不得运行。 | 9 个官方 ID 仅作待审候选，优先 Docker 清单内多工作流；不能视为可运行最终名单。 |
| UltraHorizon | [官方论文](https://arxiv.org/abs/2509.21766)与[官方仓库](https://github.com/StarDewXXX/UltraHorizon)列出 Mystery Grid、Sequence Explore、Alien Genetics Laboratory 三环境；示例 `parallel_run.py --env seq --steps 50`，官方说明 `steps` 不是工具调用数，且长轨迹 API 成本高。 | 仓库首页/根目录未见 LICENSE，**许可 UNKNOWN**；场景 ID、任务定义、版本锁定、独立 reset、Memory/trace 粒度、判分器及安全隔离须逐项验证。官方给出的无 prefix cache 50-step 示例输入量约每运行 1M–10M，不是本地测量，不能据此承诺完整试点成本。 | 仅列三环境家族，不下载、不运行；许可与 reset 未核实前不进入付费试点。 |
| Odysseys | [官方代码](https://github.com/ljang0/Odysseys)与[论文](https://arxiv.org/abs/2604.24964)公开 200 个跨站网页任务、rubric；使用实时互联网/OSWorld 浏览器与截图轨迹，代码库显示 MIT。 | 实时网站状态漂移，任务级环境复现和外部副作用控制难；逐任务版权/站点规则未审。 | 首轮暂缓。 |

核查维度结论：tau2 的 task definition、tool、日志、reset 有本地固定版本证据；ALE 的官方 task definition、harness、trace 与 license 已证实，但本工作区可执行性和实际 reset 未证；UltraHorizon 有代码/场景/官方成本警告，但 license 与关键状态接口 UNKNOWN。Memory 支持不能仅凭论文讨论“记忆”认定为可观测结构化 memory event；checkpoint 不能仅凭脚本 resume 认定为单决策快照。以上限制决定 WP8 Gate 为 `PARTIAL`，不能直接启动 WP9。
