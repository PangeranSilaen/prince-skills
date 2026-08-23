# Multi Brain

Multi Brain is a portable Agent Skills-compatible workflow for durable shared repository memory across coding agents such as OpenCode, Claude Code, Codex, and similar tools.

Version 2 keeps the original selective-read idea but changes the memory model from chronology-first to **state-first**. Agents should be able to learn what is authoritative now without rereading months of activity history.

## Core Model

```text
.multibrain/
├── session.md                 # stable directory of topic buckets
├── indexes/
│   ├── agents.md              # Current State + Open Loops + Recent Events
│   ├── auth.md
│   └── deploy.md
├── context/                   # deeper evidence and rationale
└── archive/                   # rolled-up historical chronology
```

The intended read path is:

```text
session.md -> relevant bucket -> current state/open loops -> selective context
```

History is still preserved, but it no longer has to be read before an agent can understand the current project state.

## Why v2

Long-running real-world usage exposed several weaknesses in the original log-oriented model:

- a small number of very long entries could make a bucket expensive to read despite an entry-count cap;
- older findings could silently become stale or be superseded by newer evidence;
- updating `session.md` after every event created unnecessary shared-file churn;
- mechanical consistency depended entirely on the LLM following Markdown conventions;
- Multi Brain could drift toward becoming a second changelog rather than durable project memory.

v2 addresses those issues with state-first buckets, lifecycle semantics, byte-size budgets, an explicit memory write gate, source-of-truth rules, secret-safety guidance, deterministic maintenance tooling, and regression eval fixtures.

## Bucket Shape

Each v2 bucket is intentionally small:

```md
# Multi Brain Bucket: `auth`

Scope: authentication, authorization, login state, and auth-specific decisions.

## Current State

- ACTIVE — ...

## Open Loops

- ...

## Recent Events

- 2026-08-24T01:30+08:00 | decision | Codex | ... -> .multibrain/context/...
```

The important distinction is:

- **Current State** answers what is true now.
- **Open Loops** answers what remains actionable.
- **Recent Events** provides a short breadcrumb trail.
- **Context** contains deeper evidence or rationale only when needed.
- **Archive** keeps rolled-up history away from the hot read path.

## Memory Write Gate

Do not store every completed action. Write memory only for durable decisions, verified state changes, reusable constraints, root causes/blockers, corrections to stale assumptions, meaningful open loops, or knowledge that would be expensive to rediscover.

This prevents Multi Brain from becoming a verbose activity log.

## Size Budgets

Recommended defaults:

| Area | Budget |
| --- | --- |
| `session.md` | target <= 4 KiB |
| bucket | target <= 6 KiB |
| bucket maintenance warning | > 6 KiB |
| bucket rollup required | > 8 KiB |
| `Current State` | preferably <= 8 bullets |
| `Open Loops` | preferably <= 8 bullets |
| `Recent Events` | preferably 8-12 entries |
| context note | normally 1-4 KiB |

Size is used as the primary maintenance signal because entry count alone does not predict token cost.

## Helper Script

The optional Python helper handles deterministic mechanics while leaving semantic summarization to the agent:

```bash
python scripts/multibrain.py --repo . init
python scripts/multibrain.py --repo . status
python scripts/multibrain.py --repo . doctor
python scripts/multibrain.py --repo . record --bucket auth --agent codex --kind decision --summary "Use exact-model capability gating"
python scripts/multibrain.py --repo . migrate
```

### `init`

Creates the v2 directory structure and non-destructively adds a marked startup block to root agent instructions when appropriate. Repeated runs are intended to be safe.

### `status`

Shows bucket sizes, event counts, and whether maintenance is recommended.

### `doctor`

Checks required paths, session bucket pointers, context pointers, legacy bucket format, and size budgets.

### `record`

Prepends one concise event to `Recent Events`. The agent must first decide that the Memory Write Gate is satisfied; the script does not decide what deserves memory.

### `migrate`

Mechanically upgrades legacy v1 bucket files by preserving their original body under `Historical Log (v1)` and adding empty v2 state sections. It deliberately does not fabricate a semantic `Current State` summary.

## Lifecycle And Authority

Useful lifecycle labels are:

- `ACTIVE` — current authoritative state;
- `SUPERSEDED` — replaced by newer evidence/decision;
- `CLOSED` — finished and no longer an open loop;
- `HISTORICAL` — retained only for history/evidence.

Multi Brain itself is not the ultimate source of truth. Current runtime evidence, source code, tests, configuration, and live Git/GitHub state outrank memory when they conflict.

## Secret Safety

Assume `.multibrain/` may be committed. Never persist passwords, API tokens, cookies, private keys, secret `.env` values, credential-bearing URLs, or raw logs that contain secrets. Record safe locations or retrieval instructions instead of secret values.

## Included Files

- `SKILL.md` — agent workflow and behavioral contract
- `scripts/multibrain.py` — deterministic maintenance helper
- `assets/session-template.md` — stable master index template
- `assets/sub-index-template.md` — v2 state-first bucket template
- `assets/context-template.md` — deep context template
- `assets/agents-snippet.md` / `assets/claude-snippet.md` — marked root bootstrap blocks
- `references/memory-layout.md` — memory/lifecycle model
- `references/maintenance.md` — budgets, migration, rollup, and integrity rules
- `evals/` — regression and trigger scenarios for future skill revisions
- `tests/` — helper-script regression tests

## Compatibility

The skill remains Markdown-first and can still be used without Python. Existing v1 memory is not automatically destroyed or rewritten. Use `migrate` only when you intentionally want a legacy bucket converted to the v2 shape.
