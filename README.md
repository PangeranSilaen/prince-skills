# prince-skills

Personal collection of reusable AI agent skills for coding and knowledge-work workflows. The repository is primarily designed around `SKILL.md`-compatible agents such as OpenCode, Claude Code, and similar tooling.

## Skills

| Skill | Status | Purpose |
| --- | --- | --- |
| [`compactor`](./compactor/) | Active | Losslessly compress prompts, instructions, and other text while preserving operational meaning and constraints. |
| [`session-handoff`](./session-handoff/) | Active | Transfer active work into a fresh AI session through an ephemeral, untracked handoff that is deleted after successful consumption. |
| [`multi-brain`](./multi-brain/) | Active | Maintain state-first, selective repository memory across multiple agents with bounded buckets, deeper evidence, lifecycle semantics, and optional integrity tooling. |
| [`github-issue-pr`](./github-issue-pr/) | Active, AksaLoka-specific | Create and update GitHub Issues and PRs using AksaLoka conventions, templates, draft workflow, secret-safety rules, and UTF-8 verification. |
| [`glm-ocr`](./glm-ocr/) | Legacy / Not in use | OCR through `ocr.z.ai`. Kept for reference, but no longer part of the active workflow. |

## Skill Notes

### compactor

Losslessly reduces text size and token usage without silently dropping facts, requirements, technical details, conditions, identifiers, or strong constraints. Intended for compaction rather than ordinary lossy summarization.

### session-handoff

Creates an ephemeral transition package for moving active work into a fresh agent session. Version 2 keeps the handoff outside durable repository history, defaults to a locally ignored `.handoff/` artifact when filesystem continuity exists, points to durable sources such as Multi Brain instead of duplicating them, requires re-verification of volatile state, and tells the receiving agent to delete the handoff after successful consumption.

### multi-brain

Provides durable shared repository memory across agents using `.multibrain/session.md` as a stable bucket directory, state-first files under `.multibrain/indexes/`, selective evidence under `.multibrain/context/`, and historical rollups under `.multibrain/archive/`. Version 2 adds a Memory Write Gate, `ACTIVE`/`SUPERSEDED` lifecycle semantics, source-of-truth rules, byte-size budgets, secret-safety guidance, deterministic `init`/`status`/`doctor`/`record`/`migrate` tooling, and regression evals.

### github-issue-pr

A repository-specific workflow originally used by AksaLoka. It standardizes Issue and Pull Request bodies, Indonesian-language conventions, draft PR behavior, credential safety, and remote UTF-8/mojibake verification. Templates and the verification script are included with the skill.

### glm-ocr

> **Status: Legacy / Not in use**

This skill is retained as a reference implementation, but it is no longer used in the regular workflow. In practice, the `ocr.z.ai` authentication token proved too short-lived and too dependent on active browser login sessions. Reliable use required keeping multiple Chrome profiles/accounts open, and closing a relevant profile could invalidate the associated token and force re-authentication. That operational overhead made the workflow too fragile and inefficient for routine agent use.

The existing skill files remain available for anyone who still wants to experiment with the approach.

## Installation

Copy the desired skill directory into the skills directory used by your agent. Common examples:

```text
# OpenCode / generic agent skills
~/.agents/skills/<skill-name>/

# Claude Code
~/.claude/skills/<skill-name>/
```

Some skills are universal while others intentionally contain repository-specific conventions. Review the target skill's `SKILL.md` before reusing it in another project.

## License

MIT
