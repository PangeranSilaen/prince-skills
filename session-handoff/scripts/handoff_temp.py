#!/usr/bin/env python3
"""Safe mechanics for ephemeral session-handoff artifacts."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

EXCLUDE_COMMENT = "# session-handoff ephemeral artifacts"
EXCLUDE_RULE = "/.handoff/"
TOPIC_RE = re.compile(r"[^a-z0-9-]+")


class HandoffError(RuntimeError):
    pass


def repo_root(value: str) -> Path:
    root = Path(value).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise HandoffError(f"repository path does not exist or is not a directory: {root}")
    return root


def run_git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def is_git_repo(repo: Path) -> bool:
    result = run_git(repo, "rev-parse", "--is-inside-work-tree")
    return result.returncode == 0 and result.stdout.strip() == "true"


def ensure_repo_root(repo: Path) -> Path:
    if not is_git_repo(repo):
        return repo
    result = run_git(repo, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        raise HandoffError(result.stderr.strip() or "unable to resolve Git repository root")
    return Path(result.stdout.strip()).resolve()


def tracked_handoff_paths(repo: Path) -> list[str]:
    if not is_git_repo(repo):
        return []
    result = run_git(repo, "ls-files", ".handoff")
    if result.returncode != 0:
        raise HandoffError(result.stderr.strip() or "unable to inspect tracked .handoff paths")
    return [line for line in result.stdout.splitlines() if line.strip()]


def git_exclude_path(repo: Path) -> Path:
    result = run_git(repo, "rev-parse", "--git-path", "info/exclude")
    if result.returncode != 0:
        raise HandoffError(result.stderr.strip() or "unable to resolve .git/info/exclude")
    raw = Path(result.stdout.strip())
    if raw.is_absolute():
        return raw.resolve()
    return (repo / raw).resolve()


def ensure_local_exclude(repo: Path) -> None:
    if not is_git_repo(repo):
        return
    exclude = git_exclude_path(repo)
    exclude.parent.mkdir(parents=True, exist_ok=True)
    text = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
    lines = text.splitlines()
    if EXCLUDE_RULE in lines:
        return
    block = f"{EXCLUDE_COMMENT}\n{EXCLUDE_RULE}\n"
    with exclude.open("a", encoding="utf-8") as handle:
        if text and not text.endswith("\n"):
            handle.write("\n")
        handle.write(block)


def slugify(value: str) -> str:
    value = value.strip().lower().replace("_", "-").replace(" ", "-")
    value = TOPIC_RE.sub("-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    if not value:
        raise HandoffError("topic must contain at least one letter or number")
    return value[:64]


def timestamp() -> str:
    return datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%z")


def managed_repo_dir(repo: Path) -> Path:
    return repo / ".handoff"


def managed_system_dir(repo: Path) -> Path:
    safe_name = slugify(repo.name or "project")
    return Path(tempfile.gettempdir()).resolve() / "session-handoff" / safe_name


def prepare(repo: Path, topic: str, system_temp: bool) -> Path:
    repo = ensure_repo_root(repo)
    slug = slugify(topic)

    if not system_temp:
        tracked = tracked_handoff_paths(repo)
        if tracked:
            raise HandoffError(
                ".handoff contains tracked repository files; use --system-temp instead of mixing ephemeral handoffs with tracked content"
            )
        ensure_local_exclude(repo)
        target_dir = managed_repo_dir(repo)
    else:
        target_dir = managed_system_dir(repo)

    target_dir.mkdir(parents=True, exist_ok=True)
    base = f"{timestamp()}-{slug}"
    path = target_dir / f"{base}.md"
    counter = 2
    while path.exists():
        path = target_dir / f"{base}-{counter}.md"
        counter += 1

    path.write_text(
        "# Temporary Session Handoff\n\n"
        "<!-- session-handoff:ephemeral -->\n\n"
        "Lifecycle: `EPHEMERAL — delete after successful consumption`\n",
        encoding="utf-8",
    )
    return path.resolve()


def relative_display(repo: Path, path: Path) -> str:
    try:
        return path.relative_to(repo).as_posix()
    except ValueError:
        return str(path)


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def validate_cleanup_target(repo: Path, raw_path: str) -> Path:
    candidate = Path(raw_path).expanduser()
    if not candidate.is_absolute():
        candidate = repo / candidate
    candidate = candidate.resolve()

    repo_dir = managed_repo_dir(repo).resolve()
    system_dir = managed_system_dir(repo).resolve()
    if not (is_within(candidate, repo_dir) or is_within(candidate, system_dir)):
        raise HandoffError("cleanup path is outside managed session-handoff directories")
    if candidate.suffix.lower() != ".md":
        raise HandoffError("cleanup only accepts .md handoff files")
    return candidate


def cleanup(repo: Path, raw_path: str) -> Path:
    repo = ensure_repo_root(repo)
    target = validate_cleanup_target(repo, raw_path)
    if not target.exists():
        raise HandoffError(f"handoff does not exist: {target}")
    if not target.is_file():
        raise HandoffError(f"handoff path is not a file: {target}")

    text = target.read_text(encoding="utf-8", errors="replace")
    if "<!-- session-handoff:ephemeral -->" not in text:
        raise HandoffError("refusing cleanup: ephemeral session-handoff marker not found")

    parent = target.parent
    target.unlink()
    try:
        parent.rmdir()
    except OSError:
        pass
    return target


def list_handoffs(repo: Path) -> list[Path]:
    repo = ensure_repo_root(repo)
    paths: list[Path] = []
    for directory in (managed_repo_dir(repo), managed_system_dir(repo)):
        if directory.exists():
            paths.extend(sorted(p.resolve() for p in directory.glob("*.md") if p.is_file()))
    return paths


def verify_ignored(repo: Path, path: Path) -> bool | None:
    if not is_git_repo(repo) or not is_within(path, repo):
        return None
    rel = path.relative_to(repo).as_posix()
    result = run_git(repo, "check-ignore", "-q", rel)
    return result.returncode == 0


def command_prepare(repo: Path, args: argparse.Namespace) -> int:
    path = prepare(repo, args.topic, args.system_temp)
    resolved_repo = ensure_repo_root(repo)
    ignored = verify_ignored(resolved_repo, path)
    print(f"prepared: {relative_display(resolved_repo, path)}")
    if ignored is True:
        print("git: ignored locally")
    elif ignored is False:
        print("WARN: handoff path is not ignored by Git")
    else:
        print("git: not applicable")
    return 0


def command_status(repo: Path) -> int:
    resolved_repo = ensure_repo_root(repo)
    paths = list_handoffs(resolved_repo)
    if not paths:
        print("no active temporary handoffs")
        return 0
    for path in paths:
        ignored = verify_ignored(resolved_repo, path)
        state = "ignored" if ignored is True else "NOT IGNORED" if ignored is False else "non-repo temp"
        print(f"{relative_display(resolved_repo, path)} | {state}")
    return 0


def command_cleanup(repo: Path, args: argparse.Namespace) -> int:
    removed = cleanup(repo, args.path)
    print(f"deleted: {removed}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage ephemeral Session Handoff files safely.")
    parser.add_argument("--repo", default=".", help="Repository/project root (default: current directory)")
    sub = parser.add_subparsers(dest="command", required=True)

    prepare_parser = sub.add_parser("prepare", help="Create a unique temporary handoff file")
    prepare_parser.add_argument("--topic", required=True, help="Short topic slug or phrase")
    prepare_parser.add_argument(
        "--system-temp",
        action="store_true",
        help="Use the OS temp directory instead of <repo>/.handoff/",
    )

    sub.add_parser("status", help="List active managed handoff files")

    cleanup_parser = sub.add_parser("cleanup", help="Delete one consumed handoff safely")
    cleanup_parser.add_argument("--path", required=True, help="Managed handoff file to delete")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        repo = repo_root(args.repo)
        if args.command == "prepare":
            return command_prepare(repo, args)
        if args.command == "status":
            return command_status(repo)
        if args.command == "cleanup":
            return command_cleanup(repo, args)
        parser.error(f"unknown command: {args.command}")
    except HandoffError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
