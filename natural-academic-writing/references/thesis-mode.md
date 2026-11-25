# Thesis Mode

Use this mode for proposal tugas akhir, skripsi/TA, research reports, journal-style sections, and other formal academic writing where evidence, terminology, and logical precision matter more than conversational naturalness.

## Goal

Preserve the user's recognizable directness and reasoning style while producing prose that is acceptable in a formal academic document.

Use a formal, straightforward register. For drafting and revision, use the [writing procedure and worked examples](thesis-writing-audit.md) alongside this reference.

## Register

Prefer standard formal Indonesian without unnecessary bureaucracy.

Typical choices:

- prefer `jika` over `kalau` in formal analytical prose;
- use first person only when the institution, supervisor, or section convention allows it;
- prefer direct active or neutral constructions when they are clearer than heavy passive phrasing;
- keep technical terms consistent across sections;
- use precise ordinary words before rare formal synonyms;
- avoid casual intensifiers and spoken fillers.

Do not assume that `lebih formal` means `lebih panjang`.

## Evidence Discipline

Every substantive claim must have an appropriate basis.

Before stylistic revision, identify:

- claims supported by citations;
- claims derived from the user's own data or analysis;
- methodological statements, including which steps are planned and which have been performed;
- definitions, technical terminology, and the versions or conditions under which observations were made;
- claims that are currently unsupported or too strong.

During rewriting:

- preserve citation-to-claim alignment;
- do not strengthen `may`, `can`, `associated with`, or similar cautious claims into certainty;
- do not invent references to make a paragraph feel complete;
- keep attribution close to the claim it supports, including after joining or splitting sentences;
- preserve the source's unit of analysis, definition and unit of each metric, and limits of the sample, setup, or simulation;
- use partial evidence for the specific claim it establishes. Keep failed requests, unsupported functions, and unverified support distinct when the evidence makes those distinctions;
- flag missing evidence and distinguish the historical baseline, the current implementation, and any planned change or evaluation.

## Paragraph Architecture

A thesis paragraph should have a clear job, but not every paragraph needs the same visible template.

Possible paragraph functions include:

- establish context;
- define a problem;
- synthesize prior work;
- identify a gap;
- explain a design or method choice;
- interpret a result;
- state an implication or limitation.

Let the function determine the structure. Avoid repeating the same `topic sentence -> three supporting sentences -> concluding sentence` shape across an entire section.

### Paragraph density and word count

The user's preference for **fewer, denser paragraphs** is a valid editorial signal, but the approximately **180–230 words per paragraph** noted in the voice profile is **coursework calibration evidence**, not a target for thesis prose. Do not apply a paragraph minimum, maximum, or word quota unless an authoritative project rule explicitly requires one.

For proposals, keep sentences that develop the same claim or evidence-to-inference chain together. Start a new paragraph when its function changes, for example from explaining a concrete integration problem to motivating a design decision. A paragraph may be long when its internal logic is clear, or short when a method step or limitation requires precision. The goal is coherent argument units, not visual symmetry or deliberate unevenness.

Never pad a paragraph with generic context or mechanically separate it merely to reach an imagined count. Review each paragraph for one defensible primary claim, adequate support, readable sentence links, and correct citation placement.

## Natural Academic Flow

Prefer logical continuity over decorative transitions.

A transition is useful when it shows a real relationship such as:

- cause;
- contrast;
- narrowing;
- consequence;
- comparison;
- chronology;
- evidence-to-interpretation.

Do not add connectors merely because adjacent paragraphs need to look linked. Repetition of the key technical noun is sometimes clearer than forced synonym replacement.

## User Voice in Formal Writing

Carry over stable cross-mode tendencies such as:

- directness;
- concrete reasoning before broad conclusions;
- dislike of empty recap sentences;
- preference for words that are precise without sounding ceremonial;
- paragraph length that follows content rather than visual symmetry.

Do **not** automatically carry over coursework-specific habits such as:

- conversational `kalau`;
- frequent `menurut saya`;
- rhetorical questions;
- informal evaluative wording;
- personal reflection where an objective research statement is required.

## Section-Specific Guidance

### Background / Latar Belakang

Build pressure gradually from context to concrete problem to consequence to gap to research relevance.

Avoid:

- generic openings about technology developing rapidly unless they are necessary and supported;
- repeating the same problem in different wording;
- claiming novelty without literature evidence;
- inflated statements such as `sangat penting`, `sangat dibutuhkan`, or `memberikan dampak signifikan` without support.

### Literature Review

Synthesize sources by relationship, not one source per paragraph by default.

Prefer:

```text
claim/theme
-> evidence across sources
-> agreement, difference, limitation, or gap
```

Compare the mechanisms, evidence, and limits that matter to the argument. Explain what the proposal takes from a source and why. Identify reused findings when they affect whether two studies provide independent evidence.

### Methodology

Clarity and reproducibility outrank stylistic variation.

Keep:

- variables;
- procedures;
- tools;
- versions;
- thresholds;
- formulas;
- sampling logic;
- evaluation criteria

exact and consistent. For each planned test, name the activity, input, reference or expected condition, and observable evidence where supported by the design. Describing an observation criterion preserves the possibility of success, failure, or an inconclusive outcome. Claims about time, effort, or ease require evidence for that dimension.

### Results and Discussion

Separate observation from interpretation when needed.

Do not:

- restate every table value in prose;
- claim causes from descriptive associations;
- add a polished implication after every result;
- hide limitations because they make the narrative less neat.

## Naturalness Audit for Thesis Writing

Flag patterns such as:

- every paragraph beginning with a formal connector;
- repeated `penelitian ini bertujuan untuk...`, `berdasarkan hal tersebut...`, `oleh karena itu...` when unnecessary;
- long nominalized phrases that can be expressed with a direct verb;
- synonym rotation that changes established technical terminology;
- excessive hedging or excessive certainty;
- paragraphs that all have nearly identical length and cadence;
- repeated summaries of the same research gap;
- claims written more confidently than the evidence allows.

## Reviewer-comment calibration for proposal writing

An author's margin comment or manual rewrite is stronger calibration evidence than a positive reaction to a generated draft. Start with one to three representative paragraphs from distinct proposal functions (e.g., background, literature synthesis, and methodology), preserve their original source mapping, and compare the generated and user-edited versions. Record the **specific** style deltas (diction, syntax, paragraph boundary, emphasis) separately from factual/citation corrections. Apply stable preferences only to their supported genre and section; re-test on another passage before generalizing.

If the user expresses concern that the result feels mechanical, diagnose the relevant pattern. Avoid cosmetic tricks, AI-detector targets, forced human errors, or universal blacklists. A similarity/plagiarism report, even a 0% result, is not a measure of authorial voice or source attribution correctness.

For a *proposal-only* document, describe plans prospectively where appropriate while keeping known prior work and existing systems historically accurate. Do not recast already completed implementation as work that has never happened, nor invent evaluation results, source support, or supervisor approval.

## Supervisor and Institutional Rules

Local academic rules override stylistic preference.

When the user provides:

- a campus template;
- supervisor feedback;
- faculty writing rules;
- citation style requirements;
- a previously approved section;

use them as the primary register and structure constraints. Calibrate the user's voice inside those boundaries rather than fighting them.

## Idiomatic syntax and translationese

Build the sentence around the relationship the reader needs to understand: what acts or changes, what is affected, and under which supported condition. Choose natural Indonesian clause order and direct verbs, including concise passive verbs when institutional rules require them. Keep nominalizations that name a precise concept; unpack stacks of abstract nouns that obscure the action.

Generic editorial example: “Pelaksanaan identifikasi perbedaan dilakukan untuk pemberian dukungan terhadap proses integrasi” can become “Perbedaan diidentifikasi untuk mendukung proses integrasi.” This is a constructed example, not a source claim. Check the original evidence before adding an actor or a causal connection.

Keep established technical English when it gives the clearest precise meaning. On the first relevant occurrence in document order, including tables, introduce a verified expansion or original term and explain its role when needed. Keep official names and code identifiers intact. Apply EYD V and the institution's italic, abbreviation, and punctuation rules. Distinguish a language-rule correction from an editorial preference. Split layered clauses when their references become unclear. Retain conditions, negations, uncertainty, and citation scope when splitting. Paragraphs may compare several studies or develop one mechanism; do not impose one-paper-per-paragraph or repeated opening/closing templates.

Read the revision independently of the English source, then compare its scientific meaning back to the evidence. Report changes to research scope, findings, method, or chronology separately from stylistic edits. A smooth sentence is not evidence of a valid claim.

When the supplied evidence contradicts a sentence, do not present that sentence as clean, copy-ready prose. Preserve the original in the audit and identify the proposed content correction separately. If project governance reserves the substantive choice for the user, mark the affected span as pending rather than silently approving a stronger claim.
