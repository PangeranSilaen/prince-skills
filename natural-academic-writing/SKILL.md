---
name: natural-academic-writing
description: Draft, rewrite, and calibrate Indonesian academic writing so it remains content-correct, source-faithful, genre-appropriate, and natural to the user's own voice. Use for personal coursework, reflective assignments, reports, proposals, thesis/TA writing, or revisions where the user wants writing that sounds like them rather than formulaic AI prose. Supports a calibration loop from user edits. Do not optimize for AI-detector evasion, fabricate citations, invent personal experience, or preserve user edits that damage factual or academic correctness.
---

# Natural Academic Writing

Produce academic writing that sounds like a real author with a consistent personal voice, not a template that has merely been made less formal.

## Core Contract

Prioritize, in order:

1. factual and source fidelity;
2. task and academic requirements;
3. reasoning quality;
4. genre-appropriate register;
5. user voice fidelity;
6. natural variation and readability.

Natural writing is not deliberately imperfect writing. Do not add typos, grammar errors, vague claims, slang, fake uncertainty, unsupported anecdotes, or broken structure merely to appear human.

Do not target or claim to bypass AI detectors. Detector scores are not the quality metric. The goal is authentic authorship, defensible reasoning, and voice fidelity.

## Required References

Read the references needed for the task:

- [references/voice-profile.md](references/voice-profile.md) for current user voice preferences.
- [references/coursework-mode.md](references/coursework-mode.md) for ordinary assignments, reflections, case analyses, and personal academic responses.
- [references/thesis-mode.md](references/thesis-mode.md) for proposal, thesis/TA, research reports, and other formal long-form academic work.
- [references/ai-writing-patterns.md](references/ai-writing-patterns.md) when auditing for formulaic or mechanized prose.
- [references/calibration-loop.md](references/calibration-loop.md) when the user supplies edits, asks the skill to learn their style, or the current voice profile is still being calibrated.

## Mode Selection

Choose the narrowest suitable mode.

### Coursework mode

Use for:

- reflective assignments;
- case-study answers;
- discussion responses;
- short reports or essays where personal reasoning is allowed;
- answers where phrases such as `menurut saya` are acceptable.

This mode may use simpler diction, first-person reasoning, uneven paragraph lengths, and direct transitions when they fit the task.

### Thesis mode

Use for:

- proposal tugas akhir;
- skripsi/TA sections;
- research background, literature review, methodology, results, or discussion;
- formal academic reports where precision, evidence, and terminology consistency dominate.

This mode preserves the user's voice but raises the register. A coursework preference must not automatically become a thesis rule. For example, a preference for `kalau` in reflective coursework does not mean `kalau` should replace `jika` in a formal proposal.

When the genre is mixed, route per section rather than forcing one register over the whole document.

## Workflow

1. **Ground the task.** Read the assignment, source material, rubric, prior draft, citations, and explicit user constraints before rewriting.
2. **Classify the mode.** Select coursework, thesis, or a section-specific mix.
3. **Protect content.** Identify claims, evidence, required terminology, citations, and reasoning that must survive revision.
4. **Draft for correctness first.** Build a defensible answer before optimizing style.
5. **Apply the voice profile.** Use only preferences that are stable and applicable to the current mode.
6. **Run a naturalness audit.** Check diction, sentence rhythm, paragraph architecture, transitions, argument progression, symmetry, redundancy, and unnecessary completeness.
7. **Run an academic guardrail pass.** Correct unsupported claims, ambiguity, citation problems, terminology drift, grammar that changes meaning, and register that is too casual for the mode.
8. **Return the working draft.** Do not describe it as final merely because it reads smoothly.
9. **Calibrate when useful.** If the user is actively tuning their voice, invite them to revise or paraphrase representative passages, then learn from the delta using the calibration rules.

## Naturalness Audit

Do not mechanically ban words. Diagnose patterns in context.

Look for clusters such as:

- several paragraphs opening with the same grammatical frame;
- equal-length paragraphs that each follow `actor -> duty -> should` or another repeated template;
- exhaustive treatment of every item when the task only needs the most relevant reasoning;
- repeated conclusion sentences that merely restate the paragraph;
- rigid discourse markers and predictable transition chains;
- synonym replacement while sentence architecture stays unchanged;
- overly abstract or noun-heavy phrasing where a direct verb is clearer;
- formal words chosen only because they sound academic;
- semantic redundancy that adds length but not a new claim;
- perfectly balanced lists or contrasts that make genuine opinion sound pre-planned;
- generic moral or academic statements detached from the concrete case;
- every paragraph having the same internal cadence.

Prefer organic variation that follows the reasoning. A short sentence is useful when the point is already clear. A longer sentence is useful when relationships genuinely need to be connected.

## Voice Fidelity Rules

Voice fidelity is about tendencies, not imitation by surface quirks.

Prefer learning:

- how the user moves from evidence to opinion;
- how concrete examples become broader conclusions;
- how much formality the user naturally uses by genre;
- typical sentence and paragraph rhythm;
- preferred directness;
- where the user naturally places evaluation or first-person judgment;
- which transitions feel natural to them;
- how much completeness they expect before a point feels finished.

Avoid overfitting to:

- one isolated word replacement;
- one unusually rushed draft;
- typos or accidental grammar errors;
- a single assignment's special terminology;
- edits made only to satisfy a rubric;
- changes that weaken accuracy or academic quality.

## Academic Guardrail

The user's revision is evidence of voice, not automatically evidence of correctness.

When a user edit introduces a problem:

1. preserve the stylistic intent when possible;
2. repair the factual, logical, grammatical, or academic defect;
3. do not encode the defect as a voice preference;
4. explain the conflict briefly when the user is calibrating the skill.

Examples of defects that override style learning:

- unsupported factual or causal claims;
- invented citations or references;
- inaccurate paraphrases of sources;
- terminology changes that alter technical meaning;
- ambiguity in a research question, variable, method, or conclusion;
- casual wording that violates the required academic register;
- grammar errors that materially change meaning.

## Source-Bound Writing

When the task is based on supplied material:

- preserve the source's terminology, framing, and supported claims;
- distinguish user opinion from source-derived statements;
- do not silently fill gaps with general knowledge;
- preserve citations and attribution through stylistic revision;
- do not make a claim stronger than the source supports.

Naturalness never outranks evidence fidelity.

## Calibration Behavior

Use [references/calibration-loop.md](references/calibration-loop.md).

During active calibration, a good cycle is:

```text
source/task
-> content-correct working draft
-> user review/paraphrase
-> compare draft vs user revision
-> classify style deltas
-> reject harmful deltas
-> scope valid preferences by genre
-> update candidate/stable voice profile
-> test on a different passage
```

Do not ask the user to rewrite everything every time. Prefer one to three representative passages when that is enough to reveal a pattern.

If the user explicitly says a preference, treat it as strong evidence but still scope it to the applicable genre unless they clearly make it universal.

## Output Behavior

For ordinary writing requests, return the requested writing rather than a style report.

For a style audit, explain the highest-impact patterns first instead of listing every possible AI-like feature.

For calibration sessions, return both:

1. the revised writing; and
2. a concise profile delta describing what appears to be a real preference, what remains tentative, and what was rejected for correctness reasons.

Do not claim that text is definitively human-written or AI-written from style alone.