# Session Handoff Lifecycle

Read this reference when deciding where a handoff should live, how it interacts with durable memory, or when it is safe to delete.

## Mental Model

A session handoff is a message in transit between two agent sessions. It is not a repository knowledge base.

```text
current session
  -> ephemeral handoff
  -> receiving session
       -> current context
       -> durable memory only for knowledge worth keeping
  -> handoff deleted
```

The design goal is that deleting the handoff after consumption does not damage long-term project continuity.

## Storage Precedence

### 1. Existing project policy

If repository instructions explicitly define a temporary handoff location and that location is untracked, follow it.

Do not use a documented permanent handoff archive merely because it exists unless the user explicitly wants archival handoffs.

### 2. Repo-local `.handoff/`

Default for ordinary coding-agent workflows.

Benefits:

- discoverable from the project working directory;
- portable across local agent clients using the same checkout;
- easy to remove;
- can be locally excluded without changing tracked repository files.

In Git repositories, prefer `/.handoff/` in `.git/info/exclude`. Do not modify tracked `.gitignore` solely for temporary handoffs.

### 3. System temp

Use system temp when:

- repository policy forbids any local temporary directory;
- `.handoff/` is already tracked;
- the repository must remain byte-for-byte untouched outside the active task;
- the working tree is read-only but a shared system temp area is available.

The prompt starter must contain the exact accessible path. Do not use system temp when the receiving agent runs on a different machine/container that cannot access it.

### 4. Chat-only self-contained handoff

Use when filesystem continuity between sessions is unavailable or uncertain.

In this mode, the copy-paste prompt carries the required transition state directly. Keep it concise and apply the same secret-safety and source-of-truth rules.

## `.git/info/exclude`

Using `.git/info/exclude` is preferred because it is local repository metadata and does not create a project-wide policy change for an ephemeral workflow.

A helper may append:

```text
# session-handoff ephemeral artifacts
/.handoff/
```

Do not repeatedly add duplicate lines. Do not rewrite unrelated exclude rules.

Leaving this local exclude rule in place after cleanup is acceptable because it prevents future accidental handoff commits and does not alter repository history. The handoff files themselves remain temporary.

## Consumption Protocol

The receiving agent should:

1. read the whole handoff;
2. load referenced durable sources selectively;
3. verify volatile facts needed for immediate work;
4. resolve obvious drift between the checkpoint and current sources of truth;
5. promote genuinely new durable knowledge to Multi Brain/docs only when appropriate;
6. delete the handoff;
7. start the recommended action.

Do not postpone cleanup until the end of the next long session. Once the transfer succeeded, the transport artifact has completed its job.

## Multi Brain Boundary

When Multi Brain exists:

### Multi Brain stores

- authoritative current state;
- durable decisions and constraints;
- verified root causes;
- costly-to-rediscover knowledge;
- meaningful open loops reusable across sessions.

### Session Handoff stores

- why a session transition is happening;
- a point-in-time git/test/runtime checkpoint;
- immediate unfinished work;
- local working-tree notes;
- the exact next action;
- pointers to durable sources.

### Avoid duplication

Bad:

```text
handoff contains a 200-line copy of the auth investigation already stored in
.multibrain/context/...
```

Good:

```text
Current auth conclusion: read .multibrain/indexes/auth.md.
For evidence behind the lockout root cause, follow its ACTIVE context pointer.
Next action: reproduce the remaining frontend error on current HEAD.
```

## Volatile State

A handoff is a checkpoint. These facts can become stale quickly:

- branch/HEAD;
- open/merged PR state;
- CI status;
- test baseline;
- running process/service state;
- DB rows/counts;
- deployment state;
- device/network state.

The receiving agent should re-check any volatile fact before acting on it when drift would matter.

## Cleanup Safety

Delete only the handoff artifact that was intentionally created for the transition.

A cleanup helper should refuse arbitrary paths and should not recursively delete unrelated directories.

If multiple handoff files exist, do not assume all are stale. Remove the consumed file and report the others through `status` for deliberate review.
