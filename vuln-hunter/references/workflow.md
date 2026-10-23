# Authorization

The skill refuses active testing until it has a confirmed scope memo. Minimum acceptable evidence, in order of strength:

1. A signed written authorization or contract naming the targets, owner, and period.
2. `scope.json` that passes `scripts/check_scope.py` and has been explicitly confirmed by the user in-conversation.
3. The user states they own/control the target and the target is their own local or owned asset (localhost, owned domains, owned infrastructure). For anything internet-facing that is not clearly the user's own asset, demand option 1.

Things that are NOT sufficient: a target being public, being well-known, being a "demo site", or the user saying "it's probably fine".

# Stages

## 1. Scoping

- Record in-scope assets (hosts, IPs, URL paths, API versions) and out-of-scope exclusions (third-party dependencies, adjacent tenants, production data stores, etc.).
- Record timing windows and impact limits: no tests outside the window, no requests expected to break availability.
- Decide which vulnerability classes are in scope: default is non-destructive checks only (auth flaws, injection, misconfiguration, outdated software, unsafe defaults).
- Write the memo to `scope-memo.md` (use `assets/scope-memo.md`), and optionally a machine-readable `scope.json` if a second assessor or CI job should validate it.

## 2. Recon (passive first)

- Inventory the attack surface: listening ports, routes/endpoints, JS-referenced endpoints, exposed admin paths, error pages, headers.
- Fingerprint technology: frameworks, library versions (from JS bundles, meta tags, headers) — version info drives the scan stage.
- Prefer non-disruptive methods: local source code when available beats black-box; black-box beats intrusive scanning. If the target's source code is in the working directory, static analysis of it is the fastest and safest path to real findings.

## 3. Scan (active, in-scope only)

- Choose tools per target type; see `references/tools.md` for the default toolchain and concrete command patterns.
- Run low-volume, high-signal checks first; escalate to full scanner runs only if time permits and the window allows.
- Log every raw output to a file named `findings/<asset>-<tool>.log` so findings stay reproducible.

## 4. Verify

- For each candidate finding: re-confirm reachability and impact inside the scope. Typical verification: minimal reproducing request, source-code path trace, or config check.
- Kill false positives aggressively (WAF noise, scanner heuristics, benign configuration). A finding without reproducible evidence is not in the report.
- Note impact honestly: "reachable from where, with what access level, and what could an attacker do".

## 5. Report

- One `report.md` per engagement using `assets/report-template.md`.
- Order findings by risk, not by tool. Each finding: title, severity, affected asset, evidence (request/response or code path), root cause, and a concrete remediation with the minimal change that closes it.
- Close with a prioritized remediation plan: what to fix this week, this month, and why.
- Keep the report useful to a non-expert: severity in plain terms, no unexplained jargon.
