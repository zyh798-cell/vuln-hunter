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

