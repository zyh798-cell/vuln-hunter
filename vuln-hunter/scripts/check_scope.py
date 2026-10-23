"""Validate a machine-readable scope file before any active testing.

Usage: python check_scope.py <scope.json>
Exits 0 when the scope is complete and confirmed, non-zero otherwise.
"""
import json
import sys

REQUIRED = [
    "client",
    "in_scope",
    "out_of_scope",
    "window",
    "confirmed_by",
]

ALLOWED_TECHNIQUES_DEFAULT = {"non_destructive"}


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <scope.json>", file=sys.stderr)
        return 2

    try:
        data = json.load(open(sys.argv[1], encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"scope file unreadable: {exc}", file=sys.stderr)
        return 1

    errors = []
    for field in REQUIRED:
        value = data.get(field)
        if not value:
            errors.append(f"missing or empty field: {field}")

    techniques = data.get("techniques") or ALLOWED_TECHNIQUES_DEFAULT
    destructive = {t for t in techniques if t in {"dos", "destructive", "mutation", "social_engineering"}}
    if destructive:
        errors.append(f"destructive techniques present but not allowed by this skill: {sorted(destructive)}")

    if errors:
        print("scope not acceptable:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"scope OK: {len(data['in_scope'])} in-scope asset(s), confirmed by {data['confirmed_by']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
