from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "multibrain.py"
SPEC = importlib.util.spec_from_file_location("multibrain_cli", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
mb = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mb)


class MultiBrainTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        tmp = tempfile.TemporaryDirectory()
        repo = Path(tmp.name)
        return tmp, repo

    def test_init_is_byte_idempotent_and_doctor_passes(self) -> None:
        tmp, repo = self.make_repo()
        self.addCleanup(tmp.cleanup)

        self.assertEqual(mb.command_init(repo), 0)
        first_session = (repo / ".multibrain" / "session.md").read_bytes()
        first_agents = (repo / "AGENTS.md").read_bytes()

        self.assertEqual(mb.command_init(repo), 0)
        second_session = (repo / ".multibrain" / "session.md").read_bytes()
        second_agents = (repo / "AGENTS.md").read_bytes()

        self.assertEqual(first_session, second_session)
        self.assertEqual(first_agents, second_agents)
        agents_text = second_agents.decode("utf-8")
        self.assertEqual(agents_text.count(mb.MARKER_START), 1)
        self.assertEqual(agents_text.count(mb.MARKER_END), 1)
        self.assertTrue((repo / ".multibrain" / "archive").is_dir())
        self.assertEqual(mb.command_doctor(repo), 0)

    def test_record_creates_bucket_and_updates_stable_session_directory(self) -> None:
        tmp, repo = self.make_repo()
        self.addCleanup(tmp.cleanup)
        mb.command_init(repo)

        args = type(
            "Args",
            (),
            {
                "bucket": "auth",
                "agent": "Codex",
                "kind": "decision",
                "summary": "Use exact-model capability gating",
                "context": None,
                "scope": "authentication and authorization decisions",
            },
        )()

        self.assertEqual(mb.command_record(repo, args), 0)
        bucket = (repo / ".multibrain" / "indexes" / "auth.md").read_text(encoding="utf-8")
        session = (repo / ".multibrain" / "session.md").read_text(encoding="utf-8")

        self.assertIn("| decision | Codex | Use exact-model capability gating", bucket)
        self.assertIn(".multibrain/indexes/auth.md", session)
        self.assertEqual(session.count(".multibrain/indexes/auth.md"), 1)
        self.assertEqual(mb.command_doctor(repo), 0)

    def test_doctor_fails_on_broken_context_pointer(self) -> None:
        tmp, repo = self.make_repo()
        self.addCleanup(tmp.cleanup)
        mb.command_init(repo)

        bucket_path = repo / ".multibrain" / "indexes" / "agents.md"
        text = bucket_path.read_text(encoding="utf-8")
        event = (
            "- 2026-08-24T01:30+08:00 | state | Codex | broken pointer test "
            "-> .multibrain/context/missing.md"
        )
        bucket_path.write_text(mb.prepend_recent_event(text, event), encoding="utf-8")

        self.assertEqual(mb.command_doctor(repo), 1)

    def test_context_pointer_cannot_escape_context_directory(self) -> None:
        tmp, repo = self.make_repo()
        self.addCleanup(tmp.cleanup)
        mb.command_init(repo)
        (repo / ".multibrain" / "escape.md").write_text("not context", encoding="utf-8")

        with self.assertRaises(mb.MultiBrainError):
            mb.validate_context_pointer(repo, ".multibrain/context/../escape.md")

    def test_migrate_preserves_legacy_body_without_inventing_state(self) -> None:
        tmp, repo = self.make_repo()
        self.addCleanup(tmp.cleanup)
        mb.ensure_dirs(repo)
        root = repo / ".multibrain"
        (root / "session.md").write_text("# Multi Brain\n", encoding="utf-8")
        legacy = root / "indexes" / "legacy.md"
        legacy.write_text(
            "# Named Sub-Index: `legacy`\n\n## Entries\n\n- old verified observation\n",
            encoding="utf-8",
        )

        self.assertEqual(mb.command_migrate(repo), 0)
        migrated = legacy.read_text(encoding="utf-8")

        self.assertIn("## Current State", migrated)
        self.assertIn("## Open Loops", migrated)
        self.assertIn("## Recent Events", migrated)
        self.assertIn("## Historical Log (v1)", migrated)
        self.assertIn("- old verified observation", migrated)
        self.assertNotIn("ACTIVE — old verified observation", migrated)

    def test_doctor_requires_rollup_for_oversized_bucket(self) -> None:
        tmp, repo = self.make_repo()
        self.addCleanup(tmp.cleanup)
        mb.command_init(repo)

        bucket_path = repo / ".multibrain" / "indexes" / "agents.md"
        bucket_path.write_text(
            bucket_path.read_text(encoding="utf-8") + ("x" * (mb.BUCKET_ERROR_BYTES + 100)),
            encoding="utf-8",
        )

        self.assertEqual(mb.command_doctor(repo), 1)

    def test_doctor_detects_duplicate_session_pointer(self) -> None:
        tmp, repo = self.make_repo()
        self.addCleanup(tmp.cleanup)
        mb.command_init(repo)

        session_path = repo / ".multibrain" / "session.md"
        session_path.write_text(
            session_path.read_text(encoding="utf-8")
            + "\n- `agents-copy` — duplicate -> .multibrain/indexes/agents.md\n",
            encoding="utf-8",
        )

        self.assertEqual(mb.command_doctor(repo), 1)


if __name__ == "__main__":
    unittest.main()
