# Calibration Loop

Use this reference when the user wants the skill to learn from their revisions or when the current voice profile is still uncertain.

## Principle

Treat user revisions as **evidence about preference**, not as commands to imitate every surface change.

The calibration loop should discover durable choices while filtering out accidents, task-specific edits, and academically harmful changes.

## Default Cycle

```text
1. produce a content-correct working draft
2. ask the user to review/paraphrase representative passages when calibration is useful
3. compare original draft vs user revision
4. classify each meaningful delta
5. validate it against academic correctness and task rules
6. scope the preference by genre/context
7. update candidate/stable profile evidence
8. test the learned preference on a different passage
```

Do not force the user to rewrite the whole document. One to three representative passages are often enough to reveal a pattern.

## Delta Classification

Classify edits into one or more categories:

### Diction

Examples:

- formal synonym -> ordinary precise word;
- `apabila` -> `kalau` in reflective coursework;
- nominal phrase -> direct verb.

### Syntax

Examples:

- long sentence split into two;
- repeated subject-first structure varied;
- subordinate clause moved later because it reads more naturally.

### Rhythm

Examples:

- shorter sentence inserted after a dense explanation;
- paragraph lengths made less uniform;
- repeated cadence removed.

### Argument architecture

Examples:

- concrete consequence moved before the abstract category;
- less important stakeholder compressed;
- opinion introduced only after the case facts are explained.

### Register

Examples:

- overly formal -> student-natural;
- coursework wording -> more formal thesis wording;
- unnecessary first-person language removed from research prose.

### Content correction

Examples:

- misunderstood theory corrected;
- unsupported claim removed;
- citation narrowed to match the source.

Content corrections are not voice preferences unless they also reveal a separate stylistic tendency.

## Evidence Strength

Use the following default model:

```text
explicit user preference statement
-> stable preference immediately, scoped to the stated context

same preference observed in 2+ independent revisions
-> stable preference for the matching mode

one observed revision without explicit explanation
-> candidate preference

contradictory revisions
-> context-dependent; identify the condition rather than choosing one globally
```

A stable preference can still be revised when later evidence shows it was overgeneralized.

## Scope Before Generalization

Record the narrowest scope supported by evidence.

Possible scopes:

- universal;
- Indonesian writing;
- academic writing;
- coursework only;
- reflective coursework only;
- thesis/proposal only;
- specific section such as background or discussion;
- one assignment/rubric only.

Example:

`apabila -> kalau` from a reflective ethics assignment supports a coursework preference. It does **not** justify a universal ban on `apabila`, and it does not imply that `kalau` is preferred in a thesis proposal.

## Academic Validation Gate

Before learning from a revision, ask:

1. Does the edit preserve the intended claim?
2. Does it remain supported by the source/evidence?
3. Does it preserve required terminology?
4. Does it fit the assignment or section register?
5. Does it introduce ambiguity?
6. Does it damage grammar enough to change meaning?
7. Does it conflict with a rubric, template, supervisor instruction, or citation rule?

When an edit fails this gate, preserve the user's stylistic direction when possible but repair the defect.

### Example

User edit:

```text
Penelitian ini membuktikan bahwa X menyebabkan Y.
```

Source only supports an association.

Do not learn `more confident causal wording` as a voice preference. Restore the evidentially correct claim while retaining any harmless diction/rhythm changes surrounding it.

## Comparing Draft and Revision

Focus on meaningful deltas, not raw edit count.

A useful calibration report should answer:

- What did the user repeatedly simplify?
- What structure did they remove?
- What did they make more concrete?
- Where did they add personal judgment?
- Which transitions disappeared?
- Which details did they keep despite shortening?
- Which edits were required by correctness rather than style?

Do not overinterpret punctuation or one-off typo fixes.

## Profile Delta Format

During explicit calibration, summarize learning compactly:

```text
Stable:
- [preference] — scope: [mode/context] — evidence: [explicit/repeated]

Candidate:
- [preference] — needs another example

Rejected as voice signal:
- [edit] — reason: factual/academic/grammar/rubric conflict
```

When repository mutation is authorized and the installed skill is writable, update `references/voice-profile.md` with durable findings. Otherwise return the proposed delta for the user or maintaining agent to apply.

## Avoid Overfitting

Do not make the profile increasingly complicated after every draft.

Prefer a small number of explanatory tendencies over dozens of word bans.

Bad profile growth:

```text
never use apabila
never use namun
never use oleh karena itu
never use selain itu
```

Better profile:

```text
In reflective coursework, prefer direct everyday academic transitions and avoid stacking formal discourse markers when the relationship is already obvious.
```

The better rule generalizes while still allowing context-sensitive exceptions.

## Calibration Completion

A profile is sufficiently calibrated for a mode when:

- the user accepts drafts with only local edits across several different tasks;
- new revisions mostly confirm existing preferences rather than reveal new global patterns;
- the skill can distinguish voice from correctness without user intervention;
- the same rules work across different topics within the mode.

Calibration is never permanently finished. Treat the profile as a living but conservative model of the user's writing preferences.