# WP8 试点采样协议与预算草案（未授权执行）

本轮付费 API attempt、输入/输出 tokens、下载、模型运行均为 **0**。下述是进入 WP9 前的可行性预算，不自动继承历史 WP1–WP6 授权，也不是预计实际费用。每个选中 Task 至少两个独立 run，同 Task 重复不能当独立 Task；Agent 决策数、User 调用、工具步骤、attempt、响应各自记账。

| 条件性试点 | Task/场景 × run | 观察窗/请求规划上限 | 输入/输出 token 规划量 | 前置 Gate |
|---|---:|---|---|---|
| tau2 | 6 × 2 = 12 run | 每 run 最多 12 Agent + 12 User 请求；总计划至多 288，技术重试预留后最多 346 attempt | 暂拟硬上限 300 万输入、40 万输出 | 固定 commit、六 Task 资格、长窗口评分与双恢复、User/环境状态隔离 |
| ALE | 9 × 2 = 18 run | 暂以每 run 40 个 Agent 决策作截尾窗口，计划至多 720 个模型请求、最多 864 attempt；工具/MCP 步骤另计 | 暂拟硬上限 1,100 万输入、180 万输出，**非官方实测** | 九 Task 定义与资产、CPU/Docker 允许条件、本机或受控沙箱的工作区内写入、可观测逐决策日志、单价 |
| UltraHorizon | 优先 1 环境×1 run 校准；目标候选 3 环境×2 run | 官方 50-step 示例并非 50 次 LLM/工具调用，不能先定可信 attempt 上限 | 官方无 prefix-cache 示例约 **每 run 输入 100 万–1,000 万**；六 run 仅粗外推 600 万–6,000 万输入，输出与判分成本 UNKNOWN | License、场景/重置/日志、模型与判分器价格、单 run 实测令牌/写入后才可设正式硬上限 |

tau2 与 ALE 数字是**内部规划假设**，不是从官方 benchmark 得出的成本预测；不包含 judge、额外 Agent、沙箱/云 VM、存储与网络费用。以模型实际单价 (p_{in},p_{out})（每百万 token）估算费用：`(input_tokens × p_in + output_tokens × p_out)/1,000,000 + sandbox/judge/storage`。当前无已核验的模型/判分器价格和 ALE/UltraHorizon 运行画像，人民币金额为 `UNKNOWN`，不能把上表当已批准费用。若要一个保守父级技术容量，tau2+ALE 暂拟最多 1,400 万输入、220 万输出；UltraHorizon 独立审批，不与前两项自动合池。

执行顺序草案：先完成 18 行任务级资格卡和官方版本锁；在**工作区内**验证下载/资产大小、沙箱与 cache/tmp 路径；零 API dry-run 核对单 Agent 决策、工具/环境转移、Memory 可见性、reset 与 trace；再请负责人确认最终 Task 清单、run 次数、模型、真实单价/总费用、每段 token/attempt 硬上限和输出路径。确认后才进入 WP9 的少量 pilot，按 Task/时间块交错执行。技术重试计 attempt，未知用量按上限预留；行为失败不重采。明确编码 NATURAL_TERMINATION/TASK_SUCCESS/TASK_FAILURE/BUDGET_CENSORED/CONTEXT_CENSORED/TECHNICAL_INTERRUPTION/MANUAL_STOP。

建议未来原始请求/响应、任务资产、日志分别留在工作区内 `data/phase2/raw/`、`datasets/phase2/`、`logs/phase2/`，派生分析在 `phase2/WP9/`；这只是待批准路径，不在本轮创建。若任何 VM/容器/云运行会把研究文件写到项目外（尤其 C 盘或云端未批准卷），该候选直接暂停，不靠事后搬回补救。
