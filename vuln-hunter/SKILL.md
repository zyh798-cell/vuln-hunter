---
name: vuln-hunter
description: Run authorization-gated vulnerability assessment against targets the user owns or is explicitly authorized to test. Use for vulnerability scanning, static security analysis, security audit, and remediation-ready findings reports. Not for attacking, probing, or scanning targets without verified written authorization, and not for building offensive payloads or exploits.
metadata:
  short-description: Authorization-gated vulnerability assessment
---

# vuln-hunter

A disciplined vulnerability-assessment skill for coding agents. It enforces an authorization gate before any active test, prefers static analysis when the target's source is available, verifies findings to kill false positives, and ships a remediation-ready report as the deliverable.

## Gate (mandatory, before any active test)

1. Require a filled scope memo. If none exists, create one from [assets/scope-memo.md](assets/scope-memo.md) and have the user confirm every field. See [references/workflow.md](references/workflow.md) "Authorization" for the minimum acceptable evidence.
2. If a machine-readable scope file exists, validate it first:

   ```bash
   python scripts/check_scope.py <scope.json>
   ```

3. No confirmed scope, no active probing. Passive recon on public data (DNS, public endpoints) is allowed only after the same confirmation and only against in-scope assets.

## Workflow

Read [references/workflow.md](references/workflow.md) before starting a run. Stages:

1. **Scoping** — in-scope assets, out-of-scope exclusions, timing window, impact limits.
2. **Recon** — passive first: endpoints, routes, exposed files, headers, tech fingerprint.
3. **Scan** — active checks only inside confirmed scope: vulnerability scanners, known-CVE templates, safe checks. Tool commands and caveats: [references/tools.md](references/tools.md).
4. **Verify** — re-confirm each candidate finding; every reported finding needs reproducible evidence.
5. **Report** — produce `report.md` from [assets/report-template.md](assets/report-template.md): severity-ranked findings, evidence, root cause, concrete remediation, priority order.

## Rules that do not change

- Never scan, probe, or interact with targets outside the confirmed scope.
- Destructive or high-impact actions (data modification, DoS-style tests, social engineering, physical) are out of scope; refuse and document instead.
- Do not exfiltrate, retain, or print secrets, credentials, PII, or database contents discovered during a test — record the location and risk only.
- Never build or drop persistent access, webshells, implants, or anything that survives the test.
- Findings go to the target's owner through the normal conversation; no third-party disclosure.
- If scope evidence is in doubt, stop active work and re-confirm.

## Outputs

- `scope-memo.md` (or `scope.json`) — the confirmed authorization.
- `report.md` — the deliverable, using [assets/report-template.md](assets/report-template.md).
