---
name: vuln-hunter
description: Run authorization-gated vulnerability assessment against targets the user owns or is explicitly authorized to test. Use for vulnerability scanning, static security analysis, security audit, and remediation-ready findings reports. Not for attacking, probing, or scanning targets without verified written authorization, and not for building offensive payloads or exploits.
metadata:
  short-description: Authorization-gated vulnerability assessment
  workflow: "4 phases: authorize -> scan (static+dynamic) -> verify -> report"
---

# vuln-hunter

A disciplined vulnerability-assessment skill for coding agents. It enforces an authorization gate before any active test, prefers static analysis when the target's source is available, verifies findings to kill false positives, and ships a remediation-ready report as the deliverable.

## Four-phase workflow (strictly ordered)

| Phase | Name | Exit gate |
| ----- | ---- | --------- |
| 1 | Preparation & Authorization Validation | `scripts/check_scope.py` exits 0 on a confirmed, in-window scope |
| 2 | Static & Dynamic Security Scanning | candidate findings logged under `findings/`, all tied to in-scope assets |
| 3 | Result Secondary Verification & False Positive Removal | every candidate confirmed with reproducible evidence or explicitly killed |
| 4 | Structured Report Generation | `./output/vuln_hunter_report.md` delivered to the owner |

Each phase's exit gate must pass before the next phase starts. Never loop inside a phase, and never re-enter an earlier phase without new, user-confirmed information.

## Status feedback (mandatory)

At **every phase transition** — and whenever the run degrades, skips, or halts — print one line to the terminal:

```
[Vuln-Hunter Status] <Phase n/4 | DEGRADED | HALTED> — <one-line state summary>
```

The line must state, at minimum: the current phase, the execution mode (`static` / `static+dynamic` / `static-only (degraded)`), and the asset or counter in progress. This lets the operator tell progress from a hang at a glance.

## Phase 1 — Preparation & Authorization Validation

Exit gate: a confirmed, in-window, machine-validated scope. **No dynamic/active test may start before this gate passes.**

1. Build the scope from [assets/scope-memo.md](assets/scope-memo.md); every field must be filled, none left blank. Minimum acceptable evidence, strongest first:
   - (a) a signed written authorization naming the targets, owner, and period;
   - (b) a `scope.json` that passes `scripts/check_scope.py` **and** was explicitly confirmed by the user in conversation;
   - (c) the user's own clearly owned asset (localhost, owned domains, owned infrastructure).
   Anything internet-facing that is not clearly the user's own asset requires (a). Details: [references/workflow.md](references/workflow.md) "Authorization".
2. **Mandatory first action of the run** — validate the scope file and require exit code 0:

   ```bash
   python scripts/check_scope.py <scope.json>
   ```

3. **Hard stop on failure.** If `check_scope.py` exits non-zero, do not run any active check. Show the errors to the user, fix the scope file, and re-run until it exits 0. Passive recon and static analysis of local source may proceed only against in-scope assets.
4. No `scope.json` yet? Create one (see `scripts/example-scope.json`), have the user confirm every field explicitly, then run step 2. Verbal confirmation alone is never sufficient for active testing.
5. Re-run `check_scope.py` if the authorization window expires mid-run or the scope changes. Outside the window: stop active work.

On exit:

```
[Vuln-Hunter Status] Phase 1/4 complete — scope validated (check_scope.py exit 0). Next: Phase 2, mode static+dynamic.
```

## Phase 2 — Static & Dynamic Security Scanning

Read [references/workflow.md](references/workflow.md) and [references/tools.md](references/tools.md) before the first scan.

1. **Static first.** If the target's source is available locally, start there (semgrep / bandit / gosec plus manual sink review). Fastest, safest, no network interaction, usually the highest yield.
2. **Dynamic second, only through the gate.** Active checks (nuclei, ZAP, ffuf, nmap, …) run only after Phase 1's gate passes, only against in-scope assets, and only with rate-limited, low-volume settings. Log raw output to `findings/<asset>-<tool>.log`.
3. **Order:** passive recon → manual review of high-risk routes (login, upload, search, logout, CSRF-adjacent) → broad scanner runs.
4. Every tool invocation follows the Backoff Strategy below; a failed tool never blocks the phase — it is skipped, recorded, and the scan continues.

Exit gate: every candidate finding is recorded under `findings/` and tied to an in-scope asset.

On exit (or on degradation):

```
[Vuln-Hunter Status] Phase 2/4 complete — N candidate findings, mode static+dynamic. Next: Phase 3.
[Vuln-Hunter Status] DEGRADED — <tool> unavailable (<reason>). Continuing in static-only mode.
```

## Phase 3 — Result Secondary Verification & False Positive Removal

Exit gate: every candidate finding is either confirmed with reproducible evidence or explicitly killed.

1. Re-confirm each candidate inside scope: a minimal reproducing request, a source-code path trace, or a config check.
2. Kill false positives aggressively (WAF challenge pages, scanner heuristics, benign configurations). A finding without reproducible evidence does not enter the report.
3. State impact honestly: reachable from where, with what access level, and what an attacker can actually do.
4. Secrets, credentials, PII, and database contents are recorded by location and risk only — never exfiltrated, retained, or printed.

On exit:

```
[Vuln-Hunter Status] Phase 3/4 complete — N findings verified, M false positives removed. Next: Phase 4.
```

## Phase 4 — Structured Report Generation

Exit gate: `./output/vuln_hunter_report.md` delivered to the target's owner.

1. Produce the report at **`./output/vuln_hunter_report.md`** (create the `output/` directory if missing), following [assets/report-template.md](assets/report-template.md).
2. Order findings by risk, not by tool. Each finding: title, severity, affected asset, evidence, root cause, minimal remediation.
3. Include a **limitations** section: checks skipped or degraded (per the Backoff Strategy below), coverage gaps, and anything cut short by the authorization window.
4. Close with a prioritized remediation plan (fix this week / this month / why). Keep it readable by a non-expert.

On exit:

```
[Vuln-Hunter Status] Phase 4/4 complete — report written to ./output/vuln_hunter_report.md.
```

## Anti-hang & Backoff Strategy (mandatory)

Progress over persistence. A failing tool or API never justifies a loop.

- **Max one retry.** Any command or tool call that fails (non-zero exit, timeout, connection error, 5xx) may be retried **at most once**. After the second failure, stop using that tool for this run: mark the check `skipped (tool failure)` in `findings/` and continue with the remaining checks.
- **No identical retries.** A retry must change something (narrower target, lower rate, smaller sub-check). Otherwise skip straight to recording the failure.
- **Explicit timeouts.** Every tool call gets a timeout; exceeding it counts as a failure and follows the one-retry rule.
- **429 / rate-limit means stop, not retry.** On HTTP 429 Too Many Requests or an explicit rate-limit signal: halt that tool immediately, record the limit, and continue elsewhere. Never re-issue the same request.
- **Environment failures degrade, never loop.** If Docker is missing or its daemon is not running, a tool errors out, or the 429 case above triggers: do **not** keep retrying the same call. Drop the offending tool, degrade the run to **pure static code analysis** mode, and finish Phases 3–4 with static-only evidence.
- **Degrade, don't stall.** In static-only mode, print the `DEGRADED` status line, complete the remaining phases, and state the degradation prominently in the report's limitations.
- **Hard time budget.** The authorization window is a cap. If it is about to close, stop active work and report coverage as-is.
- Every failure and skip is recorded in `findings/` so the report can account for it.

## Rules that do not change

- Never scan, probe, or interact with targets outside the confirmed scope.
- Destructive or high-impact actions (data modification, DoS-style tests, social engineering, physical) are out of scope; refuse and document instead.
- Do not exfiltrate, retain, or print secrets, credentials, PII, or database contents discovered during a test — record the location and risk only.
- Never build or drop persistent access, webshells, implants, or anything that survives the test.
- Findings go to the target's owner through the normal conversation; no third-party disclosure.
- If scope evidence is in doubt, stop active work and re-confirm.

## Outputs

- `scope-memo.md` (or `scope.json`) — the confirmed authorization.
- `findings/` — raw tool logs plus failure/skip notes.
- `./output/vuln_hunter_report.md` — the deliverable, following [assets/report-template.md](assets/report-template.md).
