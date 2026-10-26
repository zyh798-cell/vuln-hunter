# vuln-hunter 测试记录（Test Record）

- **测试轮次**：Round 1（2026-10-25）/ Round 2（2026-10-26）
- **代码版本**：Round 2 证据锚定 commit `5c3fe2a35aa20898da343347072c8b3d74b504c6`（SKILL.md 四阶段重构后）
- **执行环境**：Windows 11 / Git Bash + PowerShell / WorkBuddy agent
- **工具版本**：nuclei v3.11.1 · trivy 0.76.1 · bandit 1.9.4 · Python 3.13（见 `00-tool-versions.log`）
- **证据目录**：`evidence/2026-10-26/`（本轮全文运行日志，带时间戳与版本头；Round 1 日志未落盘，以对话记录与本表为准）

## 一、已实测场景

| # | 场景 | 预期行为 | 实际结果 | 通过 |
|---|------|---------|---------|------|
| T1 | `check_scope.py` + 合法 `scope.json` | exit 0，输出 in-scope 数量与确认人 | `scope OK: 2 in-scope asset(s), confirmed by Alice…`，exit 0 | ✅ |
| T2 | `check_scope.py` + 非法 scope（5 个空字段 + dos 技术） | exit 非 0，逐项列出错误，拒绝破坏性技术 | exit 1，列出 6 项错误，含 `destructive techniques present but not allowed: ['dos']` | ✅ |
| T3 | 工具链可用性探测 | 如实识别缺失工具 | Round 1：扫描器全缺仅 nmap；Round 2：nuclei / trivy / bandit 就位 | ✅ |
| T4 | 扫描器全缺 → 自动降级 | 按 Backoff Strategy 降级纯静态分析，不重试不卡死 | Round 1 自动降级纯静态，Grep sink 审查完成，0 发现 | ✅ |
| T5 | bandit SAST 全量扫描 | 0 issue 或如实报告 | 42 行代码，Low/Medium/High 全部 0（`03-bandit-sast.log`） | ✅ |
| T6 | trivy secret 密钥泄露扫描 | 0 泄露或如实报告 | 0 secrets（`04-trivy-secret.log`） | ✅ |
| T7 | trivy checks bundle 下载失败 | 回退内置检查并继续，不死循环 | `Falling back to embedded checks` 后扫描正常完成 | ✅ |
| T8 | 报告产出路径 `./output/vuln_hunter_report.md` | 目录缺失自动创建，两轮均产出 | Round 1 / Round 2 均生成（`05-report-v2-snapshot.md`） | ✅ |
| T9 | GitHub 线上生效验证 | raw SKILL.md 含新章节 | HTTP 200，Backoff/Status/报告路径 11 处匹配 | ✅ |
| T10 | 阶段切换状态行 `[Vuln-Hunter Status]` | 每次阶段切换输出 | 两轮测试均已按格式输出 | ✅ |

## 二、故障注入场景（尚未验证）⏳

> 退避机制为 SKILL.md 内的 Agent 行为条款（指令层策略），非硬编码程序逻辑。以下场景**不应**以 T7 的单次成功推及，需逐一注入验证。

| # | 场景 | 预期行为（SKILL.md 条款） | 状态 |
|---|------|--------------------------|------|
| F1 | 工具调用超时 | 计为失败；等待 10s 后单次重试；再失败即跳过并记录 | ⏳ 未注入 |
| F2 | HTTP 429 Too Many Requests | **立即**停用该工具，禁止重试（不适用 5s 等待间隔） | ⏳ 未注入 |
| F3 | Docker 缺失 / 守护进程未运行 | 降级纯静态代码分析并完成后续阶段 | ⏳ 未直接注入（T4 工具缺失已验证同一下降路径） |
| F4 | 报告文件写入失败 | 重试 1 次（间隔 5s）后转对话完整输出报告并记录（v1.1 新增条款） | ⏳ 未注入 |
| F5 | 授权窗口中途过期 | 停止全部动态工作，如实报告已覆盖范围 | ⏳ 未注入 |
| F6 | 首次失败后立即重试（违规路径） | 应被「等待间隔强制」条款阻止 | ⏳ 未注入 |
| F7 | 工具第二次失败后继续余下检查 | 标记 `skipped (tool failure)`，其余检查照常完成 | ⏳ 未注入 |

## 三、结论与边界

- **已验证**：授权门控双向（放行/拒绝）、静态扫描链（bandit/trivy/Grep sink）、降级触发、报告产出、线上发布一致性。
- **未验证**：上表 F1–F7 全部故障注入场景；nuclei DAST 真实目标评估（需授权）。
- **下一步**：搭建可注入故障的受控环境（如本地 mock 命令返回非零/模拟 429），逐项跑 F1–F7 并补充本表。
