# Session Handoff

Session Handoff is a portable Agent Skills-compatible workflow for moving active work from one AI session to another without turning handoff documents into permanent repository clutter.

Version 2 treats a handoff as an **ephemeral transport artifact**:

```text
old session -> temporary handoff -> new session -> delete handoff
                                      |
                                      +-> durable knowledge goes to Multi Brain/docs only when warranted
```

## Why v2

The original workflow successfully preserved context, but it encouraged handoff documents to behave like permanent project documentation:

- it searched `docs/handoffs/` and other repository locations by default;
- it could create long 300-500 line documents;
- it suggested updating changelogs after a handoff;
- it allowed local credentials in the handoff;
- it duplicated decisions, project rules, and history that often already had durable sources;
- it had no receiving-agent cleanup protocol.

Those behaviors make sense for archival handoff reports, but not for routine session rollover.

## v2 Principles

- **Temporary by default.** A handoff exists only until the next agent consumes it.
- **Untracked by default.** Repo-local handoffs live under `.handoff/` and are locally excluded with `.git/info/exclude`.
- **State-first.** Capture what is true now, what remains, and what to do next.
- **Pointers over copies.** Reference `AGENTS.md`, Multi Brain, Issues/PRs, files, and commits instead of reproducing them.
- **Re-verify volatile state.** Git, PRs, tests, DB/runtime, and deploy state can drift after the handoff was written.
- **Secret-safe.** No credentials, including local-development credentials.
- **No repository ceremony.** Do not commit a handoff or modify changelogs merely because a session ended.

## Default Runtime Location

```text
<repo>/.handoff/<timestamp>-<topic>.md
```

In Git repositories the helper adds this local exclusion, without touching tracked `.gitignore`:

```text
# session-handoff ephemeral artifacts
/.handoff/
```

After successful consumption, the receiving agent deletes the handoff file. Keeping the local exclude rule is harmless and protects future handoffs from accidental commits.

## Helper

```bash
python session-handoff/scripts/handoff_temp.py --repo . prepare --topic auth-debug
python session-handoff/scripts/handoff_temp.py --repo . status
python session-handoff/scripts/handoff_temp.py --repo . cleanup --path .handoff/20260824T021500+0800-auth-debug.md
```

The helper owns only deterministic mechanics. The agent still decides what information belongs in the handoff.

## Package

```text
session-handoff/
├── SKILL.md
├── README.md
├── assets/
│   ├── handoff-template.md
│   └── prompt-starter-template.md
├── references/
│   └── lifecycle.md
├── scripts/
│   └── handoff_temp.py
├── tests/
│   └── test_handoff_temp.py
└── evals/
    ├── evals.json
    └── trigger-evals.json
```

## Multi Brain Integration

Multi Brain is durable repository memory. Session Handoff is a one-time transition checkpoint.

A receiving agent should be able to delete the handoff after consumption without losing durable project knowledge. If that is not true, the handoff contains knowledge that belongs somewhere durable instead.
