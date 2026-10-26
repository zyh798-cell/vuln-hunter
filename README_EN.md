<div align="center">

# 🎯 Vuln-Hunter

### **AI-Ready | Autonomous Vulnerability Hunting Skill Package**

⚡ **A lightweight cybersecurity testing skill package designed for AI Agents.**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![AI Skill](https://img.shields.io/badge/Agent%20Skill-Claude%20%2F%20Codex-orange.svg)](#)

[English](README_EN.md) | [简体中文](README.md)

</div>

---

## 📖 Overview

**Vuln-Hunter** is a modular AI Agent skill package. It orchestrates security tools and guides LLMs (such as Claude Code, Codex, AutoGPT) to execute authorized security assessments, SAST code audits, and report generation.

---

## 🚀 Usage

### 1. Install toolchain (as needed)

```powershell
pip install bandit                        # Python static analysis
winget install AquaSecurity.Trivy         # dependency / config / secret scanning
# Nuclei is not on winget: grab windows_amd64.zip from
# https://github.com/projectdiscovery/nuclei/releases, extract, add to PATH.
# Set a proxy before the first template sync if needed:
$env:HTTP_PROXY="http://127.0.0.1:<proxy-port>"; $env:HTTPS_PROXY="http://127.0.0.1:<proxy-port>"; nuclei -update-templates
```

### 2. Run an assessment

Drop the `vuln-hunter/` folder into your agent's skills directory, then prompt:

`"Run an authorization-gated vulnerability assessment of the target in scope: <target>"`

The agent follows the four-phase workflow in [SKILL.md](vuln-hunter/SKILL.md):
**① Preparation & Authorization Validation** (mandatory `scripts/check_scope.py`, exit 0 required) → **② Static-first / dynamic-gated scanning** → **③ Result verification & false-positive removal** → **④ Structured report** (written to `./output/vuln_hunter_report.md`). Every phase transition prints a `[Vuln-Hunter Status]` line; tool failures back off automatically (max 1 retry) and degrade to pure static analysis when unrecoverable.

---

## 🧪 Testing & Evidence

| Item | Detail |
| :--- | :--- |
| Test dates | 2026-10-25 (Round 1) / 2026-10-26 (Round 2) |
| Code version | Round 2 evidence anchored at commit `5c3fe2a` |
| Verified | Authorization gate (both directions), bandit SAST (0 issues), trivy secret scan (0 leaks), tool-missing degradation, checks-bundle download fallback, report output, phase status lines |
| Result | 0 findings; gate / backoff / degradation / reporting all behave as designed in SKILL.md |
| Evidence | [evidence/2026-10-26/](evidence/2026-10-26/) full run logs · [Test record (incl. untested list)](evidence/2026-10-26/TEST-RECORD.md) · [Report v2](output/vuln_hunter_report.md) |

---

## ⚠️ Known Limitations

- **Backoff is an instruction-level policy**: defined in [SKILL.md](vuln-hunter/SKILL.md) (max 1 retry / 2 attempts total, 5s/10s wait intervals, immediate stop on 429, auto-degrade to static-only). It constrains agent behavior rather than being hard-coded logic; fault-injection scenarios (timeouts, 429, report-write failure) are not yet fully tested — see the [test record](evidence/2026-10-26/TEST-RECORD.md).
- **Dynamic scanning untested**: nuclei DAST requires an authorized target; only engine/template readiness has been verified.
- **Platform**: all tests ran on Windows 11; nuclei is not on winget and must be installed from GitHub Releases.
- **Online dependency**: trivy's misconfig checks bundle is downloaded at runtime and falls back to embedded checks offline.

---

## 📜 Authorization

This skill package is for **authorized assets only**. Every dynamic test requires `scripts/check_scope.py` to validate the scope first; unauthorized targets are refused. See [vuln-hunter/SKILL.md](vuln-hunter/SKILL.md) and [docs/SECURITY.md](docs/SECURITY.md).
