# Security Policy

## Responsible use

This project is an authorization-gated vulnerability assessment skill. It is intended for use on systems you own or operate, or where you have explicit written authorization from the system owner to test.

- Use only against in-scope targets with confirmed authorization.
- No destructive tests, no persistence, no payload building, no exfiltration of data found during a test.
- If you discover a 0-day or otherwise undisclosed vulnerability in a third-party product, follow that product's responsible disclosure process. Do not publish raw PoCs publicly without the vendor's consent.

## Reporting a vulnerability in this repository

Do **not** open a public issue for security problems.

1. Email: `<your-email>`.
2. Include: a brief description of the issue, minimal reproduction steps (against your own or authorized systems only), and the affected file or component.
3. Response target: 5 business days for acknowledgement, 30 days for a fix.
4. We coordinate disclosure with the reporter before any public release.

## Bug reports

For non-security bugs or feature requests, open a normal GitHub issue using the template.

## Scope

This policy covers the code in this repository. Toolchains referenced in `references/tools.md` (nuclei, ZAP, ffuf, semgrep, etc.) are maintained by their respective projects and are out of scope here.
