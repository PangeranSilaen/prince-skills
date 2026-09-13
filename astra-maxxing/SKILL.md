---
name: astra-maxxing
description: Decide whether substantial reasoning work should stay with the browser Sol orchestrator or use GPT-6 Astra, choose an appropriate Astra effort, build a bounded executor prompt, and audit Astra output. Use for model-routing decisions around complex synthesis, planning, writing, or research; when the user asks to use or compare Astra; or when reviewing Astra output. Do not use for ordinary prompt rewriting or to send retrieval-heavy work to Astra by default.
---

# Astra Maxxing

Use GPT-6 Astra where frontier reasoning materially helps, not merely because it is available.

`maxxing` means maximizing useful work per call: quality, evidence discipline, quota efficiency, reproducibility, and auditability. It does **not** mean automatically selecting the highest reasoning effort.

## Core Contract

Treat Astra as a reasoning executor, not as a source of truth.

For each task, determine:

1. whether Astra should be used at all;
2. which reasoning effort is justified;
3. what evidence/context Astra should receive or read;
4. what Astra may and may not do;
5. what artifact it should return; and
6. how an independent orchestrator will audit the result.

Default workflow:

```text
TASK
-> classify work type + evidence maturity
-> retrieve/harden evidence first when needed
-> choose non-Astra / Astra Medium / Astra High
-> generate executor prompt
-> obtain invocation approval when required
-> Astra produces WORKING_DRAFT
-> orchestrator audits independently
-> revise, accept for scope, or block
-> optional commit/PR/publish only under the surrounding workflow
```

## Route Per Stage, Not Per Project

Large projects usually contain both Astra-worthy and non-Astra work. Route the current stage instead of assigning the entire project to one model.

Classify evidence maturity first:

- **Raw** — search results, unreviewed files, unread full text, unverified claims, or unknown current state.
- **Partial** — some material is verified, but a gap could still change the recommendation.
- **Decision-ready** — decision-driving claims are traceable, material gaps are explicit, and relevant contradictions are known.

`Decision-ready` does not mean sources agree. It means disagreement and uncertainty are explicit enough to reason over.

## Routing

### Non-Astra path

Use a non-Astra path, typically the current browser ChatGPT GPT-5.6 Sol orchestrator plus appropriate tools, for:

- discovery, search, bulk PDF/full-text reading, and extraction;
- source, DOI, citation, code, test, runtime, or Git verification;
- mechanical repository work and deterministic transformations;
- routine edits or low-complexity writing;
- tasks where missing evidence matters more than additional reasoning.

If evidence is raw, harden it first and route again. In this skill, Sol means the current browser ChatGPT GPT-5.6 Sol orchestrator, not a Sol model selected inside Codex or another executor environment.

### Astra Medium — default Astra route

Use Medium for reasoning-heavy work over sufficiently mature context, including:

- synthesis across verified evidence;
- comparing alternatives and trade-offs;
- planning and decision-package construction;
- structured writing where multiple constraints interact;
- prompt-sensitive reasoning and redrafting;
- turning a compact evidence package into a reviewable recommendation.

Medium is a workflow default, not an official claim that it is optimal for every task.

### Astra High — escalate for reasoning difficulty, not importance alone

Use High only when at least one material difficulty remains after evidence hardening, for example:

- valid sources materially contradict one another;
- many constraints interact and local fixes can create downstream conflicts;
- the decision is hard to reverse and alternatives must be compared adversarially;
- a final red-team requires deep counterfactual or contradiction analysis.

Before choosing High, state the expected reasoning difficulty in one sentence.

Do not escalate merely because a document is long, the task is important, the user asks for a longer answer, or Medium produced an inconvenient conclusion.

### No automatic xhigh/max

Do not automatically route to `xhigh` or `max`. Add a higher tier only when repeated evaluation on a defined task family shows that High is insufficient after evidence, prompt, and tool use are already sound.

## Evidence and Tool Boundaries

Match evidence to the claim being made.

- Search/discovery results support discovery and screening, not detailed factual claims by themselves.
- Curated libraries and full text support reading and source management when provenance is preserved.
- Code graphs, indexes, and semantic code tools are navigation aids.
- Source code and configuration support implementation-state claims within their scope.
- Tests support only the behavior and revision actually exercised.
- Runtime observations support observed behavior under the recorded conditions.
- Git/history supports chronology and change-state claims.
- Astra output is synthesis or recommendation, not independent evidence.

Astra may read primary sources selectively when synthesis requires it. Do not make Astra perform broad retrieval merely to avoid a separate hardening pass.

## Executor Prompt

When generating an Astra prompt, read [references/executor-contract.md](references/executor-contract.md).

Prefer pointers to authoritative repository files over copying long context when the executor can access those files. Inline the task, critical constraints, decision-driving gaps, and any information the executor cannot retrieve itself.

Specify instruction priority and action boundaries clearly. Repository guidance such as `AGENTS.md` may be read for project rules and context without implying permission for unrelated local mutation.

The prompt must distinguish routine assumptions Astra may make from consequential decisions that remain human checkpoints.

## Invocation Approval Gate

Selecting Astra and invoking Astra are separate actions. The skill may recommend Astra, choose an effort level, and prepare the executor prompt without consuming Astra quota.

Before actually starting a GPT-6 Astra run, obtain explicit user approval unless the user has already granted clear standing authorization for Astra invocation within the current scope. A general request to continue project work, create a skill, or use available tools does not by itself authorize consuming Astra quota.

When approval is required, present the proposed model, effort, task, and execution environment first. Do not silently substitute a Codex-hosted Sol or other executor for the browser Sol orchestrator.

## Artifact Status

Unless the surrounding task explicitly authorizes otherwise:

- Astra output starts as `WORKING_DRAFT`;
- Astra may return `READY_FOR_AUDIT` or `BLOCKED`;
- it does not become accepted repository state merely because Astra wrote it;
- commit, PR, publish, merge, deployment, or external synchronization remain separate actions governed by the surrounding workflow.

If the user forbids writes, return the artifact in chat instead of creating a file.

## Session Policy

Use the same Astra session when the goal, evidence revision, and instruction environment remain coherent and the request is a tightly coupled follow-up.

Prefer a fresh Astra session when:

- task semantics change materially;
- a new evidence package invalidates prior premises;
- the previous session is polluted by tool failures, stale instructions, or unrelated work;
- context is large enough that inherited assumptions are harder to audit than reconstructing the task from authoritative pointers.

Compact when the task is still the same and the context is valid but redundant. Use a handoff when moving across sessions or environments. Compaction does not repair semantically stale context.

## Audit Contract

The orchestrator audits against the task contract and primary evidence, not Astra's confidence or prose quality.

Check:

1. **Scope and actions** — what changed, where, and whether actions stayed authorized.
2. **Provenance** — decision-driving claims trace to the stated evidence and revision.
3. **Reasoning** — alternatives, counterevidence, assumptions, and uncertainty are handled consistently.
4. **Verification** — test/runtime/tool claims match evidence actually available.
5. **Output contract** — requested structure, status, unresolved decisions, and human checkpoints remain visible.

Return one status:

- `ACCEPTED_FOR_SCOPE` — the artifact satisfies the stated contract for that version and scope;
- `REVISION_REQUIRED` — identify concrete defects, evidence, and correction conditions;
- `BLOCKED` — required evidence, access, or human decision is missing.

`ACCEPTED_FOR_SCOPE` is not authorization to merge, publish, or deploy.

For corrections, send a defect list and the evidence delta. Do not use "think harder" as a substitute for diagnosis, and do not automatically escalate reasoning effort after every defect.

## Official Guidance Provenance

For model-specific behavior or current capability claims, read [references/guidance-provenance.md](references/guidance-provenance.md). Refresh official guidance when the answer materially depends on current Astra behavior, model options, or host capability.

Do not turn temporary model behavior, one benchmark, community prompt folklore, or one user's anecdote into a permanent rule without evidence.

## Evaluation

Behavioral cases live in `evals/evals.json`. Evaluate routing changes against paired cases such as raw vs hardened evidence and low-risk vs contradiction-heavy decisions.

Prefer observed behavioral failures over accumulating speculative rules.
