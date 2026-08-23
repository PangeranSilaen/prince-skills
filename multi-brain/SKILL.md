---
name: multi-brain
description: Maintain lightweight, durable repository memory shared across AI agents. Use when initializing or maintaining `.multibrain`, resuming prior repository work, recording decisions or verified state future agents need, correcting stale memory, or selectively recalling earlier work. Do not use as a general activity log for trivial or one-off work.
compatibility: Requires repository file read/write access. Python 3.10+ is optional for deterministic maintenance commands.
metadata:
  version: "2.0"
---

# Multi Brain

## Purpose

Maintain shared repository memory that answers two questions efficiently:

1. What is true and important **now**?
2. Where can an agent selectively read the history or evidence behind it?

Keep memory state-first, bounded, evidence-aware, and cheap to scan. Multi Brain is a routing and recovery aid, not a replacement for current source code, tests, runtime evidence, or Git/GitHub state.

## When To Use

Use Multi Brain when work creates durable knowledge that another session or agent is likely to need, including:

- resuming work started by another agent;
- recording a durable decision, verified state change, constraint, root cause, blocker, or expensive-to-rediscover finding;
- correcting or superseding stale memory;
- initializing shared repository memory;
- maintaining or compacting an existing `.multibrain/` store.

Do not write memory merely because work happened. Skip trivial edits, routine successful commands, temporary observations, and one-off tasks with no future handoff value.

## Memory Write Gate

Write new memory only when at least one is true:

- a durable decision was made;
- verified project state changed in a way future work depends on;
- a reusable constraint or invariant was discovered;
- a root cause, blocker, or failure mode was verified;
- a previous assumption or memory entry was proven wrong;
- an open loop remains for a future agent;
- rediscovering the information would be materially expensive.

Prefer updating current state over appending another event when the new information simply replaces older truth.

## Source Of Truth

When memory conflicts with current evidence, prefer the more authoritative source:

1. current runtime evidence, source code, tests, and active configuration;
2. current repository documentation and current Issue/PR state;
3. Multi Brain `Current State`;
4. historical Multi Brain context or archived events.

Re-verify volatile facts when they matter, including branch/HEAD, PR status, running services, database state, credentials/access, test status, and environment configuration.

## Read Workflow

### 1. Read The Master Index

Read `.multibrain/session.md` first when it exists.

Treat it only as a stable directory of named buckets. Do not turn it into a work log and do not update it for every event.

### 2. Select The Minimum Relevant Memory

Choose the one bucket that best matches the task. Open a second bucket only when the task clearly crosses scopes.

Inside a v2 bucket, read in this order:

1. `Current State`
2. `Open Loops`
3. `Recent Events` only when chronology matters
4. pointed context files only when deeper evidence or rationale is required

For an unrelated task, reading `session.md` alone is enough.

### 3. Re-verify Volatile State

Before acting on volatile claims, verify them against the current repository/runtime instead of trusting historical memory.

## Write Workflow

### 1. Pass The Memory Write Gate

Do not write anything until the result qualifies as durable memory.

### 2. Update Current Truth First

Update `Current State` when the authoritative project state changed. Keep it concise and declarative.

Use lifecycle labels when helpful:

- `ACTIVE` — currently authoritative and relevant;
- `SUPERSEDED` — replaced by newer evidence or a newer decision;
- `CLOSED` — completed and no longer an open loop;
- `HISTORICAL` — retained only as past evidence.

When new evidence supersedes older context, make the new authoritative pointer obvious. Preserve old evidence unless there is a separate reason to delete it.

### 3. Maintain Open Loops

Add, update, or close only actionable unfinished items. Avoid copying an entire Issue tracker into Multi Brain.

### 4. Add A Short Recent Event Only When Useful

Events are breadcrumbs, not reports. Keep each event concise and point to deeper context when detail matters.

Recommended format:

```md
- 2026-08-24T01:30+08:00 | state | Codex | verified auth lockout root cause -> .multibrain/context/2026-08-24T0130+0800-codex-auth-lockout.md
```

Use ISO 8601 timestamps with a numeric UTC offset. Keep filenames filesystem-safe by omitting `:` characters.

### 5. Write Deep Context Selectively

Create `.multibrain/context/*.md` only when future agents benefit from evidence or rationale beyond the bucket summary.

Useful content:

- goal and outcome;
- authoritative decision and rationale;
- evidence and verification;
- relevant files or identifiers;
- constraints and invalidated assumptions;
- follow-up items.

Record distilled rationale, not private chain-of-thought or a transcript of the session.

## Size Budgets

Treat size as the primary maintenance signal; entry count alone is insufficient.

Recommended budgets:

- `session.md`: target <= 4 KiB;
- each bucket: target <= 6 KiB, maintenance recommended above 6 KiB, rollup required above 8 KiB;
- `Current State`: preferably <= 8 bullets;
- `Open Loops`: preferably <= 8 bullets;
- `Recent Events`: preferably 8-12 active entries;
- one event summary: preferably <= 320 characters before its pointer;
- context note: normally 1-4 KiB, larger only when the investigation genuinely needs it.

When a bucket exceeds budget, preserve authoritative current state and recent useful events, then roll older chronology into `.multibrain/archive/` or an intentionally compressed historical context note. Never discard still-authoritative evidence merely to meet a size target.

## Secret Safety

Assume `.multibrain/` may be committed.

Never persist passwords, API tokens, session cookies, private keys, secret `.env` values, credential-bearing URLs, or raw logs containing secrets. Record safe locations or retrieval instructions instead, such as `development credentials are available in .cred`, without copying secret values.

## Concurrency And Stability

Keep `session.md` stable to reduce write collisions between agents working in different buckets. Update it only when a bucket is created, removed, renamed, or its scope materially changes.

Prefer one durable bucket per cohesive domain. Use short, stable names such as `auth`, `deploy`, `ui`, `agents`, or `nvr-perf`.

## Initialization

When the user asks for `multi brain init`, bootstrap non-destructively:

- create `.multibrain/session.md` if missing;
- create `.multibrain/indexes/`, `.multibrain/context/`, and `.multibrain/archive/`;
- create a starter `agents` bucket when no bucket exists;
- inspect root agent instruction files such as `AGENTS.md` and `CLAUDE.md`;
- add or update the marked Multi Brain startup block without replacing repository-specific guidance.

Prefer the deterministic helper when Python is available:

```bash
python <skill-dir>/scripts/multibrain.py --repo . init
```

The command is intended to be idempotent. Existing unmarked Multi Brain guidance should not be duplicated; inspect and merge it deliberately instead.

## Maintenance Commands

When `scripts/multibrain.py` is available, prefer it for mechanical operations:

```bash
python <skill-dir>/scripts/multibrain.py --repo . status
python <skill-dir>/scripts/multibrain.py --repo . doctor
python <skill-dir>/scripts/multibrain.py --repo . record --bucket auth --agent codex --kind decision --summary "Use exact-model capability gating"
python <skill-dir>/scripts/multibrain.py --repo . migrate
```

`doctor` checks structure, pointers, size budgets, and obvious integrity problems. `record` only performs deterministic event insertion after the agent has already decided the Memory Write Gate is satisfied. `migrate` preserves legacy v1 content under a historical section and adds empty v2 state sections; it does not invent a semantic summary.

## Root Instruction Files

Use marked blocks for deterministic maintenance:

```md
<!-- multi-brain:start -->
## Multi Brain
...
<!-- multi-brain:end -->
```

Never destructively replace unrelated `AGENTS.md` or `CLAUDE.md` content.

## Relationship With Session Handoff

Multi Brain and `session-handoff` serve different purposes:

- Multi Brain stores durable repository knowledge reusable across many sessions.
- Session Handoff packages the transition state of one specific long session.

A handoff should reference durable Multi Brain knowledge instead of duplicating it. When a handoff reveals genuinely new durable knowledge, update Multi Brain once before finishing.

## Resources

- Read `references/memory-layout.md` for the v2 runtime structure and lifecycle model.
- Read `references/maintenance.md` for budgets, rollup, migration, and integrity guidance.
- Use templates under `assets/` for new stores and context notes.
- Use `scripts/multibrain.py` for deterministic bootstrap and maintenance when available.
- Use `evals/` as regression scenarios when changing this skill.
