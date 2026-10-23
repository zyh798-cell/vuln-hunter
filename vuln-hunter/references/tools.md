# Default toolchain

Pick the minimum that fits the target. The commands below are patterns; substitute in-scope targets only. Prefer local, non-disruptive checks over network hammering.

## Web application (black-box)

- `nuclei -u <url> -t http/ -severity medium,high,critical -rl targets.txt` — template-driven checks, good signal, low noise. Start at medium+ severity; drop to low only in long windows.
- ZAP fast scan: `zap-baseline-scan.sh <url>` (older releases) or `owasp-zap-fast-scan.sh <url>` — auth, headers, common misconfiguration.
- `ffuf -w <wordlist> -u <url>/FUZZ -mc 200,301,401,403 -fo results.txt` — directory and parameter discovery. Use small wordlists first (`top-1000.txt`); full dictionary runs only when the window allows and the target can absorb the load.
- Manually review login, upload, search, logout, and CSRF-adjacent routes: most real bugs live there.

## Web application (white-box / source available)

Static analysis first — faster and non-disruptive:

- `semgrep --config auto --lang python <path>` (swap `--lang` per language) — broad, low false-positive surface.
- `gosec -exclude generated <path>/...` for Go; `bandit -r <path>` for Python.
- Grep classic sink patterns and hand-check each hit: SQL string concatenation into query/execute, eval/exec on user data, unescaped template interpolation, innerHTML plus user input, deserialization of untrusted data, child_process/os.system with user input.

## Networks / infrastructure

- `nuclei -u <host> -t network/` plus `nmap -Pn -sV -p- <host> --open` for service fingerprint. Service versions drive CVE template selection.
- `trivy fs --scanners vuln .` against a local checkout; `trivy image <img>` for container images.

## Configuration and defaults

- `nuclei -t http/misconfiguration/` catches exposed panels, debug endpoints, and default credentials.
- Hand-check .env-adjacent leaks, verbose error modes, and overly permissive CORS in response headers.

## Notes

- Rate-limit everything: `-rate-limit`/`--threads`/`--concurrency` flags exist for a reason. Defaults that are safe for a shared host are usually too fast for a production target.
- Log raw output to `findings/<asset>-<tool>.log`. A finding is reportable only if its evidence is reproducible from these logs.
- WAF false positives are common with ffuf (challenge pages that return 200). Confirm with a direct follow-up request before reporting a "hidden" path.
- No destructive tests: skip DoS, SQL DROP, log tampering, and anything that mutates production data.
