# Authorization

The skill refuses active testing until it has a confirmed scope memo. Minimum acceptable evidence, in order of strength:

1. A signed written authorization or contract naming the targets, owner, and period.
2. A `scope.json` that passes `scripts/check_scope.py` and has been explicitly confirmed by the user in conversation.
3. The user states they own or control the target and it is their own local or owned asset (localhost, owned domains, owned infrastructure). For anything internet-facing that is not clearly the user's own asset, demand option 1.

Things that are NOT sufficient: the target being public, well-known, or a "demo site", or the user saying "it's probably fine".

# Stages

## 1. Scoping

- Record in-scope assets (hosts, IPs, URL prefixes, API versions) and out-of-scope exclusions (third-party dependencies, adjacent tenants, production data stores, etc.).
- Record timing windows and impact limits: no tests outside the window, no requests expected to break availability.
- Decide which vulnerability classes are in scope. Default is non-destructive checks only: authentication flaws, injection, misconfiguration, outdated software, unsafe defaults.
- Write the memo to `scope-memo.md` (from `assets/scope-memo.md`), and optionally a machine-readable `scope.json` if a second assessor or a CI job should validate it.

## 2. Recon (passive first)

- Inventory the attack surface: listening ports, routes/endpoints, JS-referenced endpoints, exposed admin paths, error pages, response headers.
- Fingerprint technology: frameworks and library versions from JS bundles, meta tags, and headers. Version info drives the scan stage.
- Prefer non-disruptive methods: local source code when available beats black-box; black-box beats intrusive scanning. If the target's source code is in the working directory, static analysis of it is the fastest and safest path to real findings.

## 3. Scan (active, in-scope only)

- Choose tools per target type; see `references/tools.md` for the default toolchain and concrete command patterns.
- Run low-volume, high-signal checks first; escalate to full scanner runs only when the time window allows.
- Log raw output to `findings/<asset>-<tool>.log` so every finding stays reproducible.

## 4. Verify

- For each candidate finding: re-confirm reachability and impact inside the scope. Typical verification is a minimal reproducing request, a source-code path trace, or a config check.
- Kill false positives aggressively (WAF noise, scanner heuristics, benign configuration). A finding without reproducible evidence is not in the report.
- State impact honestly: reachable from where, with what access level, and what an attacker can actually do.

## 5. Report

- One `report.md` per engagement, from `assets/report-template.md`.
- Order findings by risk, not by tool. Each finding has: title, severity, affected asset, evidence (request/response or code path), root cause, and the minimal remediation that closes it.
- Close with a prioritized remediation plan: what to fix this week, this month, and why.
- Keep the report readable by a non-expert: severity in plain terms, no unexplained jargon.
