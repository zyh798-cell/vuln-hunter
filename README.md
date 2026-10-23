# vuln-hunter

A Codex / OpenAI-style **skill** that turns a coding agent into a disciplined vulnerability assessor.

It authorization-gates every run: no active probing without a confirmed scope memo, static analysis first when source is available, verification to kill false positives, and a remediation-ready report as the deliverable.

## Structure

```
vuln-hunter/
├── SKILL.md                    # entrypoint: gate, workflow, hard rules
├── references/
│   ├── workflow.md             # stage-by-stage procedure + authorization criteria
│   └── tools.md                # toolchain: nuclei, ZAP, ffuf, semgrep, gosec, bandit, trivy
├── assets/
│   ├── scope-memo.md           # the authorization document a run must start with
│   └── report-template.md      # findings → remediation report shape
└── scripts/
    ├── check_scope.py          # validates a machine-readable scope file
    └── example-scope.json      # example of a passing scope
```

## Install (Codex skill)

The folder is installable as-is. Put it in your skills directory:

```
mkdir -p ~/.codex/skills && cp -r vuln-hunter ~/.codex/skills/
```

or install from this repo with the skill-installer pattern:

```
python scripts/install-skill-from-github.py --repo <you>/<repo> --path vuln-hunter
```

Then invoke with `$vuln-hunter`.

## What it does

1. Requires a filled, confirmed scope memo before any active test.
2. Recon → scan → verify → report, static analysis preferred when the target's source is in the working directory.
3. Produces `report.md`: severity-ranked findings with reproducible evidence and minimal remediation, ordered by risk.

## Rules that do not change

- No scanning/probing outside confirmed scope.
- No destructive tests, no persistence, no payload building, no exfiltration of secrets found.
- Findings go to the target's owner only.

## License

MIT — see `LICENSE`.

> **Responsible use:** this skill is for systems you own or have explicit written authorization to test. Unauthorized testing of systems you do not control is illegal in most jurisdictions.
