# Default toolchain

Pick the minimum that fits the target. All commands below are patterns; substitute in-scope targets only. Prefer local, non-disruptive checks over network hammering.

## Web application (black-box)

- `nuclei -u <url> -t http/ -severity medium,high,critical -rl targets.txt` — template-driven checks, good signal, low noise. Start with medium+ severity; drop to low only in long windows.
- `owasp-zap-fast-scan.sh <url>` (from ZAP CLI: `zap-baseline-scan.sh <url>` in older releases) — fast baseline: auth, headers, common misconfig.
- `ffuf -w <wordlist> -u <url>/FUZZ -mc 200,301,401,403 -fo results.txt` — directory/param discovery. Use small wordlists first (`top-1000.txt`); full dictionary runs only when the time window allows and the target can absorb load.
- Manually review: login, upload, search, logout, and CSRF-adjacent routes are where most real bugs live.

## Web application (white-box / source available)

Static analysis first — it is faster and non-disruptive:

- `semgrep --config auto --lang python <path>` (swap `--lang` per language) — broad, low false-positive surface.
- `gosec -exclude generated <path>/...` for Go, `bandit -r <path>` for Python.
- Grep for the classic sink patterns and hand-check each hit: SQL string concatenation into `query`/`execute`, `eval`/`exec` on user data, unescaped template interpolation, `innerHTML` + user input, deserialization of untrusted data, `child_process`/`os.system` with user input.

## Networks / infrastructure

- `nuclei -u <host> -t network/` plus `nmap -Pn -sV -p- <host> --open` for service fingerprint. Versioned services drive CVE template selection.
- `trivy fs --scanners vuln .` against a local checkout, or `trivy image <img>` for container images.

## Configuration and defaults

- `nuclei -t http/misconfiguration/` catches a lot of exposed panels, debug endpoints, and default credentials.
- Hand-check `.env`-adjacent leaks, verbose error modes, and overly permissive CORS in response headers.

## Notes

- Rate-limit everything: `-rate-limit`/`--threads`/`--concurrency` flags exist for a reason; defaults that are safe for a shared host are usually too fast for a production target.
- Log raw output: `findings/<asset>-<tool>.log`. A finding is only reportable if its evidence is reproducible from these logs.
- WAF false positives are common with `ffuf` (challenge pages that return 200). Confirm with a direct follow-up request before reporting a "hidden" path.
- No destructive tests: skip DoS, SQL `DROP`, log tampering, and anything that mutates production data.
