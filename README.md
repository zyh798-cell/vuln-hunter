<div align="center">

# 🎯 Vuln-Hunter

### **AI-Ready | Autonomous Vulnerability Hunting Skill Package**

⚡ **专为 AI Agent 设计的轻量级自动化渗透测试与漏洞挖掘技能包**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![AI Skill](https://img.shields.io/badge/Agent%20Skill-Claude%20%2F%20Codex-orange.svg)](#)
[![Security](https://img.shields.io/badge/domain-Cybersecurity-red.svg)](#)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[English](README_EN.md) | [简体中文](README.md)

---

</div>

## 📖 简介 (Overview)

> [!IMPORTANT]
> **Vuln-Hunter** 是一个模块化的 AI Agent 技能包（Skill Package）。它结合了自动化指令编排与多工具链调用，让大语言模型（如 Claude Code, Codex, AutoGPT 等）具备**自动化授权评估、代码静态审计（SAST）、动态探测（DAST）与漏洞报告生成**的闭环执行能力。

---

## ✨ 核心特性 (Key Features)

<div align="center">

| 阶段 | 功能模块 | 说明 |
| :--- | :--- | :--- |
| 🛡️ **Scope Check** | **授权范围校验** | 内置脚本强制前置校验，防止越权检测 |
| 🔍 **Static Scan** | **白盒静态审计** | 协同 Semgrep / Bandit / Gosec 等工具快速定位源码漏洞 |
| 🌐 **Dynamic Scan**| **黑盒/动态探测** | 整合 Nuclei 等工具进行服务发现与 Payload 验证 |
| 📊 **AI Report**   | **智能报告生成** | 自动剔除误报，输出符合 CVSS 标准的结构化修复建议 |

</div>

---

## 🚀 快速开始 (Quick Start)

### 1. 克隆仓库
```bash
git clone [https://github.com/zyh798-cell/vuln-hunter.git](https://github.com/zyh798-cell/vuln-hunter.git)
cd vuln-hunter
```

### 2. 安装工具链（按需）

```powershell
pip install bandit                        # Python 静态审计
winget install AquaSecurity.Trivy         # 依赖 / 配置 / 密钥扫描
# Nuclei 不在 winget 源：从 https://github.com/projectdiscovery/nuclei/releases
# 下载 windows_amd64.zip 解压并加入 PATH；首次拉取模板前按需设置代理：
$env:HTTP_PROXY="http://127.0.0.1:<代理端口>"; $env:HTTPS_PROXY="http://127.0.0.1:<代理端口>"; nuclei -update-templates
```

### 3. 运行评估

将 `vuln-hunter/` 整个文件夹放入你的 Agent 技能目录（Codex / Claude Code 等），然后在对话中触发：

`"Run an authorization-gated vulnerability assessment of the target in scope: <target>"`

Agent 将严格按 [SKILL.md](vuln-hunter/SKILL.md) 的四阶段流程执行：
**① 准备与授权校验**（强制 `scripts/check_scope.py`，exit 0 方可继续）→ **② 静态优先 / 动态门控扫描** → **③ 结果二次校验与去误报** → **④ 结构化报告生成**（输出至 `./output/vuln_hunter_report.md`）。每次阶段切换输出 `[Vuln-Hunter Status]` 状态行；工具失败自动退避（最多重试 1 次），无法恢复时降级为纯静态分析。

---

## 🧪 测试范围与证据 (Testing & Evidence)

| 项目 | 说明 |
| :--- | :--- |
| 测试日期 | 2026-10-25（Round 1）/ 2026-10-26（Round 2） |
| 代码版本 | Round 2 证据锚定 commit `5c3fe2a` |
| 已验证 | 授权门控双向、bandit SAST（0 问题）、trivy 密钥扫描（0 泄露）、工具缺失自动降级、checks bundle 下载失败回退、报告产出、阶段状态行 |
| 测试结论 | 0 漏洞发现；门控 / 退避 / 降级 / 报告全链路按 SKILL.md 设计工作 |
| 证据 | [evidence/2026-10-26/](evidence/2026-10-26/) 全文运行日志 · [测试记录（含未验证清单）](evidence/2026-10-26/TEST-RECORD.md) · [报告 v2](output/vuln_hunter_report.md) |

---

## ⚠️ 已知限制 (Known Limitations)

- **退避机制为指令层策略**：定义于 [SKILL.md](vuln-hunter/SKILL.md)（最多重试 1 次 / 总计 2 次尝试、等待间隔 5s/10s、429 立即停止、自动降级纯静态），约束 Agent 行为而非硬编码逻辑；超时、429、报告写入失败等故障注入场景尚未全部实测，见[测试记录](evidence/2026-10-26/TEST-RECORD.md)「尚未验证」清单。
- **动态扫描未实测**：nuclei DAST 需授权目标，当前仅完成引擎与模板就绪验证。
- **平台**：全部测试在 Windows 11 完成；nuclei 不在 winget 源，需从 GitHub Releases 手动安装。
- **在线依赖**：trivy misconfig 检查包需联网下载，失败时自动回退内置检查。

---

## 📜 授权声明 (Authorization)

本技能包仅适用于**已获书面授权**的资产。所有动态测试前强制运行 `scripts/check_scope.py` 校验授权范围，未授权目标一律拒绝执行。详见 [vuln-hunter/SKILL.md](vuln-hunter/SKILL.md) 与 [docs/SECURITY.md](docs/SECURITY.md)。

