# Multi Brain v2 Memory Model

## Design Goal

Optimize for fast recovery of authoritative project state without deleting useful historical evidence.

The hot read path should answer:

1. Which memory domain matches this task?
2. What is authoritative now?
3. What remains open?
4. Which deeper evidence is worth opening?

Chronology is secondary.

## Runtime Layout

```text
.multibrain/
├── session.md
├── indexes/
│   ├── agents.md
│   ├── auth.md
│   └── deploy.md
├── context/
│   └── YYYY-MM-DDTHHMM+HHMM-agent-topic.md
└── archive/
    └── <rolled-up historical notes>
```

Root instruction files such as `AGENTS.md` or `CLAUDE.md` may contain a marked startup block that points agents to the Multi Brain read flow.

## Layer 1: `session.md`

`session.md` is a stable directory, not a diary.

Each entry should contain only:

- a short bucket name;
- a durable scope description;
- a relative pointer to the bucket file.

Example:

```md
- `auth` — authentication, authorization, login state, and auth-specific decisions -> .multibrain/indexes/auth.md
```

Do not add per-event timestamps. Updating `session.md` for every bucket event creates needless write collisions between agents working in unrelated domains.

Change `session.md` only when a bucket is created, removed, renamed, or materially re-scoped.

## Layer 2: State-First Buckets

Each file in `.multibrain/indexes/` should be a compact working-memory view for one cohesive domain.

Recommended shape:

```md
# Multi Brain Bucket: `auth`

Scope: authentication, authorization, login state, and auth-specific decisions.

## Current State

- ACTIVE — password verification uses ...
- ACTIVE — lockout semantics are ...

## Open Loops

- Verify ...

## Recent Events

- 2026-08-24T01:30+08:00 | correction | Codex | previous lockout assumption superseded -> .multibrain/context/...
```

### Current State

This is the most important section. It should contain concise facts, decisions, constraints, and invariants that are currently authoritative.

Avoid chronology words such as "then", "later", or "after that" unless they are needed for the state itself.

### Open Loops

Keep only unfinished items that materially help the next agent act. Close or remove items when they are no longer actionable.

Do not mirror every GitHub Issue. Link to the Issue when the tracker itself is the better source of detail.

### Recent Events

Use events as breadcrumbs for recent changes to state, not as mini reports.

Recommended kinds:

- `decision`
- `state`
- `blocker`
- `correction`
- `handoff`

Keep event summaries short and point to context when deeper evidence matters.

## Layer 3: Context

Context files contain durable evidence and rationale that would be expensive to rediscover.

Good reasons to create context:

- a root-cause investigation;
- a decision with important trade-offs;
- non-obvious runtime evidence;
- a compatibility constraint;
- a handoff that has reusable technical substance;
- a correction that supersedes earlier evidence.

Bad reasons:

- a routine command succeeded;
- a small edit happened;
- a normal test passed with no durable implication;
- the information is already obvious from current source code.

Context should record distilled rationale and evidence, not private chain-of-thought or conversation transcripts.

## Layer 4: Archive

`.multibrain/archive/` exists to remove old chronology from the hot read path without pretending it never happened.

Archive material may be:

- a preserved legacy v1 log;
- a semantic rollup of older events;
- a historical checkpoint that is no longer authoritative but still useful as evidence.

Archive should normally be opened only during historical investigation.

## Lifecycle Semantics

Use lifecycle labels when they reduce ambiguity:

### `ACTIVE`

The statement is currently authoritative.

### `SUPERSEDED`

Newer evidence or a newer decision replaced this statement. Preserve a pointer to the replacement when useful.

### `CLOSED`

The item was completed or intentionally ended and is no longer an open loop.

### `HISTORICAL`

The item is retained for evidence or chronology but should not guide current behavior by itself.

A context file may remain immutable historical evidence while the bucket's `Current State` points to a newer authoritative context.

## Authority Hierarchy

Memory must not overrule fresher evidence.

Use this default precedence when sources conflict:

1. current runtime evidence, source code, tests, and active configuration;
2. current repository docs plus current Issue/PR state;
3. Multi Brain `Current State`;
4. historical context and archive material.

Re-verify volatile facts before relying on them for actions.

## Size Model

Entry count is a poor proxy for token cost because one event can become a paragraph.

Recommended limits:

| Item | Recommendation |
| --- | --- |
| `session.md` | target <= 4 KiB |
| bucket | target <= 6 KiB |
| bucket warning | > 6 KiB |
| bucket rollup | > 8 KiB |
| `Current State` | <= 8 bullets when practical |
| `Open Loops` | <= 8 bullets when practical |
| `Recent Events` | 8-12 entries |
| event summary | <= ~320 chars before pointer |
| context | normally 1-4 KiB |

These are maintenance budgets rather than data-loss rules. Preserve important evidence even when a complex investigation legitimately exceeds them.

## Multi-Agent Concurrency

The architecture intentionally reduces shared-file writes:

```text
Agent A -> indexes/auth.md
Agent B -> indexes/ui.md
Agent C -> indexes/deploy.md
```

All three can work without touching `session.md` unless bucket topology changes.

When multiple agents work in the same bucket, prefer updating current truth instead of adding overlapping duplicate events.

## Secret Boundary

Assume all Multi Brain Markdown may be committed.

Never store secret values. Record safe references such as:

```text
development credentials are available in .cred
```

rather than copying the credential itself.

## Relationship To Session Handoff

Multi Brain stores durable repository knowledge across many sessions. A session handoff is a transition snapshot for one particular session boundary.

A handoff should reference Multi Brain when durable knowledge already exists instead of reproducing the same history. Only genuinely new durable findings should be written back to Multi Brain.
