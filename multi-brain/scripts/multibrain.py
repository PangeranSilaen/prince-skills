#!/usr/bin/env python3
"""Deterministic maintenance helper for Multi Brain v2.

The script handles structure and integrity. It deliberately does not perform
semantic summarization; agents remain responsible for deciding what knowledge
is durable and what the authoritative current state means.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable

SESSION_WARN_BYTES = 4 * 1024
BUCKET_WARN_BYTES = 6 * 1024
BUCKET_ERROR_BYTES = 8 * 1024
MAX_EVENT_SUMMARY = 320
MARKER_START = "<!-- multi-brain:start -->"
MARKER_END = "<!-- multi-brain:end -->"
V2_SECTIONS = ("## Current State", "## Open Loops", "## Recent Events")
POINTER_RE = re.compile(r"->\s+(\.multibrain/[^\s)]+)")
BUCKET_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class MultiBrainError(RuntimeError):
    pass


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_asset(name: str) -> str:
    path = skill_root() / "assets" / name
    return path.read_text(encoding="utf-8")


def repo_root(value: str) -> Path:
    root = Path(value).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise MultiBrainError(f"repository path does not exist or is not a directory: {root}")
    return root


def multibrain_root(repo: Path) -> Path:
    return repo / ".multibrain"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def ensure_file(path: Path, content: str) -> bool:
    if path.exists():
        return False
    write_text(path, content)
    return True


def ensure_dirs(repo: Path) -> None:
    root = multibrain_root(repo)
    for name in ("indexes", "context", "archive"):
        (root / name).mkdir(parents=True, exist_ok=True)


def contains_unmarked_multibrain(text: str) -> bool:
    if MARKER_START in text or MARKER_END in text:
        return False
    return bool(re.search(r"(?im)^#{1,6}\s+Multi Brain(?:\s|$)", text))


def upsert_marked_block(path: Path, block: str, create_when_missing: bool) -> str:
    block = block.strip() + "\n"
    if not path.exists():
        if not create_when_missing:
            return "skipped (file absent)"
        write_text(path, block)
        return "created"

    text = path.read_text(encoding="utf-8")
    start = text.find(MARKER_START)
    end = text.find(MARKER_END)

    if (start == -1) != (end == -1):
        return "warning: incomplete Multi Brain marker pair; left unchanged"

    if start != -1 and end != -1:
        if end < start:
            return "warning: invalid Multi Brain marker order; left unchanged"
        end += len(MARKER_END)
        prefix = text[:start].rstrip()
        suffix = text[end:].lstrip("\n")
        updated = (prefix + "\n\n" if prefix else "") + block + suffix
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            return "updated"
        return "unchanged"

    if contains_unmarked_multibrain(text):
        return "warning: existing unmarked Multi Brain guidance detected; merge manually"

    updated = block + ("\n" if text.strip() else "") + text
    path.write_text(updated, encoding="utf-8")
    return "updated"


def add_session_bucket(session: Path, bucket: str, scope: str) -> bool:
    text = session.read_text(encoding="utf-8")
    target = f".multibrain/indexes/{bucket}.md"
    if target in text:
        return False

    line = f"- `{bucket}` — {scope.strip()} -> {target}"
    if "## Buckets" in text:
        before, after = text.split("## Buckets", 1)
        new_after = after.rstrip() + "\n\n" + line + "\n"
        session.write_text(before + "## Buckets" + new_after, encoding="utf-8")
    else:
        session.write_text(text.rstrip() + "\n\n## Buckets\n\n" + line + "\n", encoding="utf-8")
    return True


def command_init(repo: Path) -> int:
    ensure_dirs(repo)
    root = multibrain_root(repo)

    created_session = ensure_file(root / "session.md", read_asset("session-template.md"))
    indexes = root / "indexes"
    bucket_files = sorted(indexes.glob("*.md"))

    created_agents = False
    if not bucket_files:
        template = read_asset("sub-index-template.md")
        content = template.replace("`bucket-name`", "`agents`").replace(
            "Scope: short, durable description of what belongs in this bucket.",
            "Scope: shared notes for agent workflows, prompts, skills, and repository-wide agent behavior.",
        )
        write_text(indexes / "agents.md", content)
        created_agents = True
        add_session_bucket(
            root / "session.md",
            "agents",
            "shared notes for agent workflows, prompts, skills, and repository-wide agent behavior",
        )

    agents_result = upsert_marked_block(repo / "AGENTS.md", read_asset("agents-snippet.md"), True)
    claude_result = upsert_marked_block(repo / "CLAUDE.md", read_asset("claude-snippet.md"), False)

    print(f"session.md: {'created' if created_session else 'present'}")
    print(f"starter agents bucket: {'created' if created_agents else 'not needed'}")
    print(f"AGENTS.md: {agents_result}")
    print(f"CLAUDE.md: {claude_result}")
    return 0


def section_lines(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    try:
        start = lines.index(heading) + 1
    except ValueError:
        return []
    result: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        result.append(line)
    return result


def count_events(text: str) -> int:
    return sum(1 for line in section_lines(text, "## Recent Events") if line.lstrip().startswith("- "))


def format_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    return f"{size / 1024:.1f} KiB"


def bucket_health(size: int) -> str:
    if size > BUCKET_ERROR_BYTES:
        return "ROLLUP REQUIRED"
    if size > BUCKET_WARN_BYTES:
        return "maintenance recommended"
    return "healthy"


def command_status(repo: Path) -> int:
    root = multibrain_root(repo)
    session = root / "session.md"
    if not session.exists():
        print("Multi Brain is not initialized.")
        return 1

    buckets = sorted((root / "indexes").glob("*.md")) if (root / "indexes").exists() else []
    contexts = sorted((root / "context").glob("*.md")) if (root / "context").exists() else []
    archives = sorted((root / "archive").glob("*.md")) if (root / "archive").exists() else []

    print(
        f"Multi Brain: {len(buckets)} bucket(s), {len(contexts)} context note(s), "
        f"{len(archives)} archive note(s)"
    )
    print(f"session.md: {format_size(session.stat().st_size)}")

    for bucket in buckets:
        text = bucket.read_text(encoding="utf-8")
        size = bucket.stat().st_size
        legacy = not all(section in text for section in V2_SECTIONS)
        suffix = ", legacy-v1 shape" if legacy else ""
        print(
            f"{bucket.stem:20} {format_size(size):>10}  {count_events(text):>2} recent event(s)  "
            f"{bucket_health(size)}{suffix}"
        )
    return 0


def clean_pointer(raw: str) -> str:
    return raw.rstrip(".,;]")


def iter_pointers(text: str) -> Iterable[str]:
    for match in POINTER_RE.finditer(text):
        yield clean_pointer(match.group(1))


def marker_problems(path: Path, repo: Path) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    starts = text.count(MARKER_START)
    ends = text.count(MARKER_END)
    rel = path.relative_to(repo)
    problems: list[str] = []
    if starts != ends:
        problems.append(f"{rel} has an incomplete Multi Brain marker pair")
    elif starts > 1:
        problems.append(f"{rel} has {starts} Multi Brain blocks; expected at most one")
    return problems


def command_doctor(repo: Path) -> int:
    root = multibrain_root(repo)
    errors: list[str] = []
    warnings: list[str] = []

    required = [root / "session.md", root / "indexes", root / "context", root / "archive"]
    for path in required:
        if not path.exists():
            errors.append(f"missing required path: {path.relative_to(repo)}")

    session_targets: list[str] = []
    session = root / "session.md"
    if session.exists():
        size = session.stat().st_size
        if size > SESSION_WARN_BYTES:
            warnings.append(f"session.md is {format_size(size)}; target is <= 4 KiB")
        text = session.read_text(encoding="utf-8")
        for pointer in iter_pointers(text):
            if pointer.startswith(".multibrain/indexes/"):
                session_targets.append(pointer)
                target = repo / pointer
                if not target.exists():
                    errors.append(f"broken session bucket pointer: {pointer}")
        duplicates = sorted({target for target in session_targets if session_targets.count(target) > 1})
        for duplicate in duplicates:
            errors.append(f"duplicate session bucket pointer: {duplicate}")

    referenced_context: set[Path] = set()
    indexes = root / "indexes"
    if indexes.exists():
        for bucket in sorted(indexes.glob("*.md")):
            rel_pointer = f".multibrain/indexes/{bucket.name}"
            if session.exists() and rel_pointer not in session_targets:
                warnings.append(f"unindexed bucket file: {rel_pointer}")

            text = bucket.read_text(encoding="utf-8")
            size = bucket.stat().st_size
            if size > BUCKET_ERROR_BYTES:
                errors.append(
                    f"{bucket.relative_to(repo)} is {format_size(size)}; semantic rollup required above 8 KiB"
                )
            elif size > BUCKET_WARN_BYTES:
                warnings.append(
                    f"{bucket.relative_to(repo)} is {format_size(size)}; maintenance recommended above 6 KiB"
                )

            missing_sections = [section for section in V2_SECTIONS if section not in text]
            if missing_sections:
                warnings.append(
                    f"{bucket.relative_to(repo)} uses legacy/non-v2 shape; run migrate then derive current state"
                )

            for pointer in iter_pointers(text):
                target = repo / pointer
                if pointer.startswith(".multibrain/context/"):
                    referenced_context.add(target.resolve())
                    if not target.exists():
                        errors.append(f"broken context pointer in {bucket.name}: {pointer}")

    context_dir = root / "context"
    if context_dir.exists():
        orphans = [p for p in context_dir.glob("*.md") if p.resolve() not in referenced_context]
        if orphans:
            warnings.append(
                f"{len(orphans)} unreferenced context note(s) found; review before deleting because they may be historical evidence"
            )

    for instructions in (repo / "AGENTS.md", repo / "CLAUDE.md"):
        errors.extend(marker_problems(instructions, repo))

    if errors:
        for item in errors:
            print(f"ERROR: {item}")
    if warnings:
        for item in warnings:
            print(f"WARN: {item}")
    if not errors and not warnings:
        print("PASS: Multi Brain structure and pointers look healthy")
    elif not errors:
        print("PASS WITH WARNINGS: no blocking integrity errors")

    return 1 if errors else 0


def safe_bucket(value: str) -> str:
    value = value.strip().lower()
    if not BUCKET_RE.fullmatch(value):
        raise MultiBrainError("bucket must match [a-z0-9][a-z0-9-]*")
    return value


def ensure_v2_bucket(repo: Path, bucket: str, scope: str | None) -> Path:
    root = multibrain_root(repo)
    path = root / "indexes" / f"{bucket}.md"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if not all(section in text for section in V2_SECTIONS):
            raise MultiBrainError(f"bucket {bucket!r} is legacy/non-v2; run migrate before record")
        return path

    ensure_dirs(repo)
    session = root / "session.md"
    ensure_file(session, read_asset("session-template.md"))
    resolved_scope = (scope or f"shared durable memory for {bucket}").strip()
    content = read_asset("sub-index-template.md")
    content = content.replace("`bucket-name`", f"`{bucket}`")
    content = content.replace(
        "Scope: short, durable description of what belongs in this bucket.",
        f"Scope: {resolved_scope}",
    )
    write_text(path, content)
    add_session_bucket(session, bucket, resolved_scope)
    return path


def prepend_recent_event(text: str, event: str) -> str:
    lines = text.splitlines()
    try:
        heading_index = lines.index("## Recent Events")
    except ValueError as exc:
        raise MultiBrainError("bucket has no '## Recent Events' section") from exc

    insert_at = heading_index + 1
    while insert_at < len(lines) and not lines[insert_at].strip():
        insert_at += 1
    lines.insert(insert_at, event)
    return "\n".join(lines).rstrip() + "\n"


def validate_context_pointer(repo: Path, raw: str) -> str:
    pointer = raw.replace("\\", "/")
    if pointer.startswith("./"):
        pointer = pointer[2:]
    if not pointer.startswith(".multibrain/context/") or not pointer.endswith(".md"):
        raise MultiBrainError("context pointer must be a .md file under .multibrain/context/")

    context_root = (repo / ".multibrain" / "context").resolve()
    target = (repo / pointer).resolve()
    try:
        target.relative_to(context_root)
    except ValueError as exc:
        raise MultiBrainError("context pointer escapes .multibrain/context/") from exc
    if not target.exists() or not target.is_file():
        raise MultiBrainError(f"context pointer does not exist: {pointer}")
    return pointer


def command_record(repo: Path, args: argparse.Namespace) -> int:
    bucket = safe_bucket(args.bucket)
    summary = " ".join(args.summary.split())
    if not summary:
        raise MultiBrainError("summary cannot be empty")
    if len(summary) > MAX_EVENT_SUMMARY:
        raise MultiBrainError(f"summary exceeds {MAX_EVENT_SUMMARY} characters; put detail in context")

    agent = " ".join(args.agent.split())
    if not agent:
        raise MultiBrainError("agent cannot be empty")

    context_pointer = ""
    if args.context:
        pointer = validate_context_pointer(repo, args.context)
        context_pointer = f" -> {pointer}"

    bucket_path = ensure_v2_bucket(repo, bucket, args.scope)
    timestamp = datetime.now().astimezone().isoformat(timespec="minutes")
    event = f"- {timestamp} | {args.kind} | {agent} | {summary}{context_pointer}"

    text = bucket_path.read_text(encoding="utf-8")
    updated = prepend_recent_event(text, event)
    bucket_path.write_text(updated, encoding="utf-8")

    size = bucket_path.stat().st_size
    print(f"recorded event in {bucket_path.relative_to(repo)} ({format_size(size)})")
    if size > BUCKET_ERROR_BYTES:
        print("WARN: bucket exceeds 8 KiB; semantic rollup required")
    elif size > BUCKET_WARN_BYTES:
        print("WARN: bucket exceeds 6 KiB; maintenance recommended")
    return 0


def migrate_bucket(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    if all(section in original for section in V2_SECTIONS):
        return False

    bucket = path.stem
    migrated = f"""# Multi Brain Bucket: `{bucket}`

Scope: migrated legacy bucket; refine this scope during semantic review.

## Current State

<!-- Derive authoritative current state from the preserved v1 history. -->

## Open Loops

<!-- Derive only actionable unfinished work from the preserved v1 history. -->

## Recent Events

<!-- Add only new durable events after migration. -->

## Historical Log (v1)

{original.rstrip()}
"""
    write_text(path, migrated)
    return True


def command_migrate(repo: Path) -> int:
    indexes = multibrain_root(repo) / "indexes"
    if not indexes.exists():
        raise MultiBrainError(".multibrain/indexes does not exist; run init first")

    migrated: list[str] = []
    for path in sorted(indexes.glob("*.md")):
        if migrate_bucket(path):
            migrated.append(path.name)

    if migrated:
        print("migrated legacy bucket(s): " + ", ".join(migrated))
        print("semantic review still required: populate Current State and Open Loops from preserved history")
    else:
        print("no legacy buckets required migration")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Maintain Multi Brain v2 repository memory")
    parser.add_argument("--repo", default=".", help="repository root (default: current directory)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="initialize Multi Brain non-destructively")
    sub.add_parser("status", help="show a compact memory inventory")
    sub.add_parser("doctor", help="validate structure, pointers, and size budgets")
    sub.add_parser("migrate", help="mechanically preserve and wrap legacy v1 buckets")

    record = sub.add_parser("record", help="prepend one durable event to a v2 bucket")
    record.add_argument("--bucket", required=True)
    record.add_argument("--agent", required=True)
    record.add_argument(
        "--kind",
        default="state",
        choices=("decision", "state", "blocker", "correction", "handoff"),
    )
    record.add_argument("--summary", required=True)
    record.add_argument("--context", help="existing .multibrain/context/*.md pointer")
    record.add_argument("--scope", help="scope used only when creating a new bucket")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        repo = repo_root(args.repo)
        if args.command == "init":
            return command_init(repo)
        if args.command == "status":
            return command_status(repo)
        if args.command == "doctor":
            return command_doctor(repo)
        if args.command == "record":
            return command_record(repo, args)
        if args.command == "migrate":
            return command_migrate(repo)
        parser.error(f"unknown command: {args.command}")
    except (OSError, MultiBrainError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
