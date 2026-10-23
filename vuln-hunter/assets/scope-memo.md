# Scope Memo

Confirm every field before any active testing. Leave none blank.

- **Client / Owner**: name and role of the person or organization that authorizes this test
- **Authorizer in contact**: name + channel (for disputes mid-test)
- **Authorization window**: start/end dates and times (timezone), and whether re-confirmation is needed after expiry
- **In-scope assets**: exact hosts, IPs, URL prefixes, API endpoints. Be explicit — "our whole site" is not a scope
- **Out-of-scope**: exclusions, third-party integrations, production data stores, load/DoS limits
- **Allowed techniques**: non-destructive only by default; list any exceptions explicitly
- **Data handling**: secrets/PII are recorded by location and risk only, never exfiltrated or stored in the report
- **Reporting channel**: where findings go (owner, bug bounty, internal ticket)
- **Emergency contact**: who to reach if something unexpected happens mid-test
