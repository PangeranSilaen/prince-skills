# Temporary Session Handoff

<!-- session-handoff:ephemeral -->

Created: `<ISO-8601 timestamp>`
Topic: `<short topic>`
Lifecycle: `EPHEMERAL — delete after successful consumption`

## Resume Here

<2-5 sentences: current objective, current state, and the first action the receiving agent should take.>

## Verified Snapshot

- `VERIFIED` Git: `<branch> @ <short/full SHA>; clean|dirty; sync state if known>`
- `VERIFIED` Issue/PR: `<number/status/url or omit>`
- `VERIFIED` Tests: `<command -> result or omit>`
- `VERIFIED` Runtime/DB/Deploy: `<only task-relevant facts or omit>`

## Active Open Loops

1. `<highest-priority unfinished item>`
2. `<next item only if genuinely active>`

## Decisions / Findings Needed To Resume

- `<distilled decision/root cause/constraint that is not already obvious from a durable source>`
- `<mark INFERRED or NOT TESTED when appropriate>`

## Durable Sources To Read

- `<AGENTS.md / CLAUDE.md / Multi Brain bucket / Issue / PR / source file>` — `<why it matters>`

## Working Tree Notes

<Only uncommitted/untracked paths and what to do with them. Omit when clean.>

## Next Action

`<one concrete action the receiving agent can start immediately after verification + cleanup>`

## Cleanup

After reading this file, loading referenced durable sources, re-verifying volatile state, and preserving any genuinely new durable knowledge, delete this handoff before continuing substantive work.
