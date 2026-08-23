from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "handoff_temp.py"
spec = importlib.util.spec_from_file_location("handoff_temp", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class HandoffTempTests(unittest.TestCase):
    def git(self, repo: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def make_git_repo(self, root: Path) -> Path:
        repo = root / "repo"
        repo.mkdir()
        self.git(repo, "init")
        self.git(repo, "config", "user.email", "test@example.com")
        self.git(repo, "config", "user.name", "Test")
        (repo / "README.md").write_text("# test\n", encoding="utf-8")
        self.git(repo, "add", "README.md")
        self.git(repo, "commit", "-m", "init")
        return repo

    def test_prepare_repo_local_is_ignored_and_cleanup_removes_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_git_repo(Path(tmp))
            path = module.prepare(repo, "Auth Debug", system_temp=False)
            self.assertTrue(path.exists())
            self.assertIn("session-handoff:ephemeral", path.read_text(encoding="utf-8"))
            rel = path.relative_to(repo).as_posix()
            ignored = subprocess.run(["git", "-C", str(repo), "check-ignore", "-q", rel])
            self.assertEqual(ignored.returncode, 0)
            self.assertEqual(self.git(repo, "status", "--short"), "")

            removed = module.cleanup(repo, rel)
            self.assertEqual(removed, path)
            self.assertFalse(path.exists())

    def test_prepare_does_not_duplicate_local_exclude_rule(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_git_repo(Path(tmp))
            module.prepare(repo, "one", system_temp=False)
            module.prepare(repo, "two", system_temp=False)
            exclude = module.git_exclude_path(repo).read_text(encoding="utf-8")
            self.assertEqual(exclude.splitlines().count(module.EXCLUDE_RULE), 1)

    def test_cleanup_rejects_path_outside_managed_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            outside = repo / "important.md"
            outside.write_text("do not delete", encoding="utf-8")
            with self.assertRaises(module.HandoffError):
                module.cleanup(repo, str(outside))
            self.assertTrue(outside.exists())

    def test_cleanup_rejects_unmarked_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            target = repo / ".handoff" / "notes.md"
            target.parent.mkdir()
            target.write_text("ordinary notes\n", encoding="utf-8")
            with self.assertRaises(module.HandoffError):
                module.cleanup(repo, str(target))
            self.assertTrue(target.exists())

    def test_tracked_handoff_content_requires_system_temp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_git_repo(Path(tmp))
            tracked = repo / ".handoff" / "tracked.md"
            tracked.parent.mkdir()
            tracked.write_text("tracked\n", encoding="utf-8")
            self.git(repo, "add", ".handoff/tracked.md")
            self.git(repo, "commit", "-m", "track handoff dir")
            with self.assertRaises(module.HandoffError):
                module.prepare(repo, "new handoff", system_temp=False)

            temp_path = module.prepare(repo, "new handoff", system_temp=True)
            self.assertTrue(temp_path.exists())
            module.cleanup(repo, str(temp_path))

    def test_non_git_project_still_supports_repo_local_temp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            path = module.prepare(repo, "plain project", system_temp=False)
            self.assertTrue(path.exists())
            self.assertTrue(path.is_relative_to(repo / ".handoff"))
            module.cleanup(repo, str(path))


if __name__ == "__main__":
    unittest.main()
