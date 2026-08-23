#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

MOJIBAKE_MARKERS = ("\ufffd", "Ã", "Â", "â€", "â†")


def fetch_body(repo: str, kind: str, number: int) -> str:
    endpoint = "issues" if kind == "issue" else "pulls"
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}/{endpoint}/{number}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr.decode("utf-8", errors="replace"))
        raise SystemExit(result.returncode)

    try:
        payload = json.loads(result.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"failed to decode GitHub API response as UTF-8 JSON: {exc}") from exc

    return payload.get("body") or ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify GitHub Issue/PR body UTF-8 integrity.")
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--kind", required=True, choices=("issue", "pr"))
    parser.add_argument("--number", required=True, type=int)
    parser.add_argument("--body-file", type=Path, help="Optional local UTF-8 body file for exact comparison")
    args = parser.parse_args()

    remote = fetch_body(args.repo, args.kind, args.number)
    found = [marker for marker in MOJIBAKE_MARKERS if marker in remote]

    if found:
        print("FAIL: suspicious mojibake markers found:", ", ".join(repr(x) for x in found))
        return 1

    if args.body_file is not None:
        local = args.body_file.read_text(encoding="utf-8")
        if remote != local:
            print("FAIL: GitHub body differs from the local UTF-8 body file")
            return 1

    print("PASS: GitHub body is clean UTF-8" + (" and matches local body file" if args.body_file else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
