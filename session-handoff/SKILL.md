---
name: session-handoff
description: Create a temporary, structured transfer package when the user wants to continue a long or interrupted task in a fresh AI session. Use for explicit handoff/resume requests, context-window rollover, or moving active work to another agent. The handoff is ephemeral: preserve only transition state, reference durable repository memory instead of duplicating it, keep the artifact untracked, and instruct the receiving agent to delete it after successful consumption.
compatibility: Requires file read/write access for file-based handoffs. Git is optional. Works without Multi Brain, but integrates with it when present.
metadata:
  version: "2.0"
---

# Session Handoff

Create a small, accurate bridge from the current session to the next one. A handoff is **temporary transport**, not durable project documentation.

## Core Contract

A good handoff answers only what the receiving agent needs to resume safely:

1. What is the task and why is it being handed off?
2. What is verified true right now?
3. What remains unfinished?
4. What should the next agent do first?
5. Which durable project sources should it read instead of trusting copied history?

The normal lifecycle is:

```text
snapshot -> create temporary handoff -> give prompt starter
-> next agent reads -> re-verifies volatile state
-> syncs genuinely new durable knowledge -> deletes handoff -> resumes work
```

Do not turn the handoff into a second changelog, project wiki, or long-term memory system.

## When To Use

Use this skill when the user explicitly wants to:

- continue in a new chat/session;
- hand work to another agent or client;
- package state because the current context is too long;
- pause a complex task and resume later with minimal rediscovery.

Do not trigger merely because a session is long. Do not create a handoff for an ordinary pause unless continuity across sessions is actually requested.

## Output Contract

Produce:

1. one temporary handoff artifact when the next session can access the same filesystem; and
2. one concise copy-paste prompt starter in the current chat.

If the user explicitly asks for a prompt-only handoff, or the next session cannot access the same filesystem, do **not** create a repository file. Produce a self-contained prompt handoff in chat instead, while keeping the same content discipline and secret-safety rules.

## Workflow

### 1. Read repository guidance first

Inspect applicable `AGENTS.md`, `CLAUDE.md`, project docs, and active skills before writing the handoff. Do not copy those files into the handoff. Reference them and carry forward only session-specific constraints that are not obvious from the repository itself.

When Multi Brain exists, read only the relevant current-state bucket(s). See [references/lifecycle.md](references/lifecycle.md) for the exact division of responsibility.

### 2. Capture a minimal final snapshot

Verify only state that materially affects resumption. Common examples:

- current branch and HEAD;
- clean/dirty working tree and important uncommitted paths;
- active Issue/PR and whether it is draft/merged/blocked;
- relevant test command and latest result;
- runtime, database, deployment, or device state only when the current task depends on it.

Record exact identifiers such as commit SHA, PR number, test counts, or important file paths. Do not dump entire command outputs when a compact exact summary preserves the same operational meaning.

Label uncertain or unavailable facts explicitly as `INFERRED` or `NOT TESTED`; do not present them as verified.

### 3. Distill before writing

Apply this retention test to every candidate detail:

Keep it only when the next agent would otherwise need to rediscover it before safely continuing.

Prefer pointers over duplication:

- repository rules -> point to `AGENTS.md` / `CLAUDE.md`;
- durable current state -> point to Multi Brain when present;
- Issue/PR history -> point to the Issue/PR;
- implementation detail -> point to relevant files/commits;
- long forensic evidence -> point to durable context rather than copying it.

A handoff should normally target roughly 3-8 KiB. Above ~12 KiB, re-check for copied history, duplicated durable memory, raw logs, or unnecessary boilerplate.

### 4. Prepare an ephemeral location

Default to a repository-local `.handoff/` directory because it is easy for the receiving agent to locate while remaining outside durable project content.

When `scripts/handoff_temp.py` is available, prefer:

```bash
python <skill-dir>/scripts/handoff_temp.py --repo . prepare --topic <short-topic>
```

The helper creates a unique `.handoff/*.md` path and, in Git repositories, adds `/.handoff/` to the repository's local `.git/info/exclude` rather than modifying tracked `.gitignore`.

Rules:

- never commit a handoff;
- never add `.handoff/` to tracked `.gitignore` solely for this workflow;
- if `.handoff/` is already tracked or repository policy forbids local temp files, use system temp or chat-only handoff instead;
- do not ask the user to choose a location when a safe default is available.

See [references/lifecycle.md](references/lifecycle.md) for fallback rules and cleanup semantics.

### 5. Write the handoff

Use [assets/handoff-template.md](assets/handoff-template.md). Omit irrelevant sections instead of filling the document with `N/A` boilerplate.

Required properties:

- current-state-first, not chronological;
- explicit `VERIFIED`, `INFERRED`, and `NOT TESTED` where useful;
- clear next action;
- concise open loops;
- exact pointers to durable sources;
- no secrets;
- no raw chain-of-thought or conversation transcript.

### 6. Reconcile with Multi Brain

If Multi Brain exists:

- do not copy durable knowledge into the handoff merely for completeness;
- update Multi Brain only when this session produced genuinely new durable knowledge that passes its Memory Write Gate;
- keep volatile transition state only in the handoff;
- let the handoff point to relevant Multi Brain bucket/context paths.

The handoff may be deleted. Multi Brain must remain useful after that deletion.

### 7. Produce the prompt starter

Use [assets/prompt-starter-template.md](assets/prompt-starter-template.md) as a pattern, then customize it to the actual task.

The receiving agent must be instructed to:

1. read the handoff fully;
2. read referenced repository instructions/current durable memory as needed;
3. re-verify volatile state before relying on the snapshot;
4. sync any genuinely new durable knowledge if necessary;
5. delete the temporary handoff after successful consumption;
6. continue the recommended next action without asking the user to re-explain known context.

### 8. Final checks

Before reporting completion:

- re-open the handoff and verify important identifiers;
- confirm the handoff is untracked when Git is present;
- confirm no credentials/secrets were copied;
- ensure the document has a concrete next action;
- ensure durable knowledge is not trapped only inside the temporary artifact;
- ensure the prompt starter includes cleanup.

Do not auto-commit or create a changelog entry merely because a handoff was produced.

## Secret Safety

Never place passwords, API tokens, session cookies, private keys, secret `.env` values, credential-bearing URLs, recovery codes, or production credentials in a handoff.

This applies to local-development credentials too. Record safe retrieval locations or instructions instead of values.

Treat raw logs as sensitive until reviewed. Include only the minimal redacted evidence needed to resume.

## Receiving-Agent Cleanup Protocol

A receiving agent should delete the handoff **after** all of these are true:

- the file was read successfully;
- critical repository guidance and referenced durable memory were loaded;
- volatile state needed for the next action was re-verified;
- any new durable knowledge worth preserving was written to its proper durable source.

Then remove the artifact before substantive work continues.

When the helper is available:

```bash
python <skill-dir>/scripts/handoff_temp.py --repo . cleanup --path <handoff-path>
```

The helper refuses to delete arbitrary paths outside the managed temporary handoff area.

## Anti-Patterns

- Permanent handoff files under `docs/` or the repository root by default.
- Committing handoffs "for history".
- Updating `CHANGELOG.md` just because a session ended.
- Dumping full chat history or raw terminal output.
- Copying `AGENTS.md`, Multi Brain, Issues, or PR descriptions into the handoff.
- Treating a stale handoff snapshot as authoritative without re-verification.
- Storing credentials because they are "only local".
- Asking the user to re-state context that the handoff or repository can resolve.
- Leaving the handoff behind after the next agent has consumed it.

## Resources

- Read [references/lifecycle.md](references/lifecycle.md) when choosing storage, integrating with Multi Brain, or handling cleanup/fallbacks.
- Use [assets/handoff-template.md](assets/handoff-template.md) to write the temporary artifact.
- Use [assets/prompt-starter-template.md](assets/prompt-starter-template.md) for the receiving-session prompt.
- Use `scripts/handoff_temp.py` for deterministic prepare/status/cleanup mechanics when Python is available.
- Use `evals/` as regression scenarios when changing activation or behavior.
