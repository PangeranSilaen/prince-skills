# Astra Guidance Provenance

Use this reference only when routing or prompt design depends on current GPT-6 Astra behavior or capabilities.

Last reviewed: **2026-09-14**.

## Official OpenAI guidance

Primary sources:
- `https://developers.openai.com/api/docs/guides/latest-model`
- `https://developers.openai.com/api/docs/models/gpt-6-astra`

At the review date, official guidance establishes that GPT-6 Astra:
- is more likely to ask focused questions when missing input could materially change the outcome;
- is sensitive to instructions in skills and files such as `AGENTS.md`, so conflicting or stale instructions should be audited;
- tends toward detailed, formatted output, so desired style and structure should be specified;
- can benefit from explicit guidance about when to delegate work to subagents;
- may test more broadly than necessary on small coding tasks, so verification scope should be calibrated;
- supports reasoning efforts `low`, `medium`, `high`, `xhigh`, and `max`.

These are model/product facts. Re-check official documentation when a task materially depends on current model behavior, supported reasoning levels, or host capability.

## Workflow policy, not official model guidance

The following rules are deliberate workflow choices for this skill:
- `Astra Medium` is the default Astra route for mature-evidence synthesis, comparison, planning, and structured writing.
- `Astra High` is reserved for contradiction-heavy reasoning, difficult comparative decisions, consequential trade-offs, or deep red-team work.
- `xhigh` and `max` are not selected automatically.
- retrieval, source hardening, bulk reading, deterministic transformations, and routine verification normally stay on the non-Astra path.
- every Astra artifact remains a working artifact until independently audited.
- actual Astra invocation requires explicit user approval unless standing authorization already covers the run.

OpenAI documentation does **not** establish Medium as universally optimal for these task classes. These routing rules should be revised only when observed evaluations or user workflow needs justify the change.

## Meaning of Sol in this skill

`Sol` means the **current browser ChatGPT GPT-5.6 Sol orchestrator** coordinating the user's workflow.

It does not mean selecting `gpt-5.6-sol` inside Codex, an API client, or another executor environment. A Codex-hosted Sol is a different execution path and must not be silently substituted for the browser orchestrator.

## Approval provenance

The Astra invocation approval gate is a user-workflow requirement, not an OpenAI model limitation. It exists because an Astra run consumes a separately managed quota and the user retains control over when that quota is spent.
