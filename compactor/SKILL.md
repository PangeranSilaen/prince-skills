---
name: compactor
description: Losslessly compact user-provided text, prompts, instructions, or draft responses into a shorter, denser, copy-paste-ready form while preserving meaning, technical details, constraints, conditions, identifiers, and dependencies. Use when the user asks to compact, shorten, condense, reduce tokens/newlines, remove filler, or make text more efficient without losing important information. Do not use for ordinary summarization where information may intentionally be omitted.
---

# Compactor

Compact content for maximum information density without changing its meaning or operational intent.

## Core Principle

Correctness and semantic fidelity take priority over brevity.

Remove words, not information.

## Workflow

1. Identify the actual intent and required output.
2. Identify information that must survive compression.
3. Remove filler, repetition, unnecessary transitions, and redundant explanations.
4. Merge statements that can be combined without ambiguity.
5. Shorten wording while preserving modality, conditions, dependencies, and ordering.
6. Preserve structure when changing it could reduce clarity or break syntax.
7. Verify that the compacted version still expresses every material requirement from the source.

## Must Preserve

Preserve anything that can affect meaning, correctness, or execution, including:

- facts, names, numbers, dates, versions, paths, URLs, commands, and identifiers
- explicit requirements and constraints
- negations such as "do not", "never", "only", and "except"
- conditions, exceptions, dependencies, and prerequisites
- required sequence or ordering
- technical decisions and implementation details
- user preferences that affect the requested task

Never silently weaken `must`, `never`, `only`, or other strong constraints.

Do not invent information or resolve ambiguity by guessing.

## Compression Rules

Prefer:
- shorter equivalent wording
- merged related statements
- direct imperative language
- fewer headings and blank lines
- removing repeated context already expressed clearly

Remove:
- greetings and conversational filler
- unnecessary confirmations
- repeated explanations
- rhetorical transitions
- examples that add no unique information
- meta-commentary about the rewriting process

Do not remove information merely because it looks verbose.

## Structured Content

For code, shell commands, JSON, YAML, configuration, tables, or other syntax-sensitive content:

- preserve syntax required for validity
- preserve meaningful line breaks
- do not rewrite executable content merely to save tokens unless explicitly requested
- compact surrounding prose instead

Readability and validity take priority over minimizing newlines.

## Output Contract

Return only the compacted content.

Wrap the entire result in one fenced code block (code snippet) for easy copying. Do not add introductions, explanations, or closing remarks outside the fence.

Use the same language as the input unless the user requests otherwise.

Minimize unnecessary blank lines, but retain line breaks that preserve syntax, structure, or clarity.

If the content itself contains triple-backtick fences, use a longer outer fence so the complete result remains safely copyable.

If the source is already near-minimal, preserve it instead of forcing further compression.

## Priority Order

When goals conflict, use this order:

1. Semantic fidelity
2. Explicit constraints
3. Technical correctness
4. Copy-paste usability
5. Brevity
6. Fewer newlines
