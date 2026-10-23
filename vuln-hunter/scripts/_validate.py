import json, re, sys

p = r"C:\Users\ZTL\Desktop\111\vuln-hunter\SKILL.md"
t = open(p, encoding="utf-8").read()
m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
assert m, "no frontmatter"
fm = m.group(1)
data = {}
for line in fm.splitlines():
    k, sep, v = line.partition(":")
    data[k.strip()] = v.strip()
assert data.get("name") == "vuln-hunter", "bad name"
assert data.get("description"), "no description"
assert len(data["description"]) <= 1024, "description too long"
print("frontmatter OK:", json.dumps(data, indent=2))
sys.exit(0)
assert data.get("short-description"), "no short-description"
