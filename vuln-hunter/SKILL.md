---
name: vuln-hunter
description: Run authorization-gated security assessment against targets the user controls or is explicitly authorized to test. Use for vulnerability scanning, security audit, pentest-style validation, and finding reports. Not for attacking, scanning, or probing targets without verified written authorization, or for building offensive payloads and exploits.
metadata:
  short-description: Authorization-gated vulnerability assessment
---

# vuln-hunter

Turns Codex into a disciplined vulnerability assessor: enumerate attack surface, scan for known weaknesses, verify findings to kill false positives, and ship a remediation-ready report.

The whole workflow is authorization-gated. Defense-first posture: the deliverable is a report the target's owner can act on, not raw tool output.

## Gate (mandatory, before any active testing)

1. Require a filled scope memo. If none exists, create one from [assets/scope-memo.md](assets/scope-memo.md) and have the user confirm every field. See [references/workflow.md](references/workflow.md) "Authorization" for the minimum acceptable evidence.
2. If a machine-readable scope file exists, validate it before proceeding:

   ```bash
   python scripts/check_scope.py <scope.json>
   ```

3. No confirmed scope, no active probing. Passive recon on public data (DNS, public endpoints) is allowed only after the same confirmation and only against in-scope assets.

## Workflow

Read [references/workflow.md](references/workflow.md) before starting a run. Stages:

1. **Scoping** — enumerate in-scope assets, out-of-scope exclusions, timing windows, impact limits.
2. **Recon** — passive first: endpoints, routes, exposed files, headers, tech fingerprint.
3. **Scan** — active checks only inside the confirmed scope: vulnerability scanners, known-CVE templates, safe checks. Tool commands and caveats: [references/tools.md](references/tools.md).
4. **Verify** — re-check each candidate finding to confirm it is real and reachable. Every reported finding needs reproducible evidence.
5. **Report** — produce the report from [assets/report-template.md](assets/report-template.md): severity-ranked findings, evidence, root cause, concrete remediation, priority order.

## Rules that do not change

- Never scan, probe, or interact with targets outside the confirmed scope.
- Destructive or high-impact actions (data modification, DoS-style tests, social engineering, physical) are out of scope for this skill; refuse and document instead.
- Do not exfiltrate, retain, or print secrets, credentials, PII, or database contents discovered during a test — record the location and risk only.
- Never build or drop persistent access, webshells, implants, or anything that survives the test.
- Findings are reported to the target's owner through the usual conversation; no third-party disclosure.
- If scope evidence is in doubt, stop active work and re-confirm.

## Outputs

- `scope-memo.md` (or `scope.json`) — the confirmed authorization.
- `report.md` — the deliverable, using [assets/report-template.md](assets/report-template.md).
