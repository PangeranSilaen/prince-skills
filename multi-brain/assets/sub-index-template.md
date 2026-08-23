# Multi Brain Bucket: `bucket-name`

Scope: short, durable description of what belongs in this bucket.

## Current State

<!-- Add only currently authoritative facts, decisions, constraints, and invariants. -->

## Open Loops

<!-- Add only actionable unfinished items. -->

## Recent Events

<!-- Format: YYYY-MM-DDTHH:MM+HH:MM | kind | AgentName | concise durable event -> optional context pointer -->

## Rules

- Read `Current State` and `Open Loops` before chronology.
- Keep current state declarative and authoritative.
- Use `ACTIVE`, `SUPERSEDED`, `CLOSED`, or `HISTORICAL` when lifecycle clarity matters.
- Keep recent events short; use deep context for evidence and rationale.
- Prefer 8-12 recent events maximum.
- Run maintenance above 6 KiB; roll up history above 8 KiB.
- Never store secrets or raw credential-bearing output.
