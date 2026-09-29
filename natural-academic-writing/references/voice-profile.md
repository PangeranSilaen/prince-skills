# Voice Profile

This file stores durable writing preferences learned from explicit user feedback and repeated calibration. It is not a list of tricks for making AI text look human.

## Scope

Current calibration is strongest for **Indonesian academic coursework**, especially reflective answers and case analyses. Thesis/proposal preferences are less calibrated and should be treated more conservatively.

## Stable Preferences

### Direct but still academic

Prefer clear everyday academic Indonesian over unnecessarily bureaucratic phrasing.

In reflective coursework, the user explicitly prefers forms such as:

- `kalau` over `apabila` when the sentence remains appropriate for the assignment;
- direct verbs over nominalized or bureaucratic constructions;
- straightforward explanations over formal padding.

This preference is **mode-scoped**. In thesis/proposal writing, use the academically appropriate form such as `jika` when `kalau` would be too conversational.

### Conversational academic glue

In reflective coursework, the user's natural prose often uses small connective words to keep the reasoning flowing rather than relying on formal discourse markers.

Commonly comfortable forms include:

- `juga`, `sebenarnya`, `sudah`, and `itu` as light connective or emphasis words;
- `tapi`, `cuma`, `punya`, `pakai`, `lanjut`, and `kelihatan` when the assignment register permits a conversational academic tone;
- familiar technical English such as `code quality`, `deploy`, `release`, or `resource` when those are the natural domain terms.

Do not mechanically inject these words. Their value is in matching the user's natural sentence flow, not in increasing their frequency. Keep standard grammar and academically important terminology intact.

### Opinion should sound owned

When the task invites personal reasoning, the user is comfortable with:

- `menurut saya`;
- a clearly stated personal judgment;
- concrete consequences before abstract labels;
- acknowledging responsibility without hiding behind detached formal language.

Do not turn this into repetitive first-person framing. The point is ownership, not inserting `menurut saya` into every paragraph.

### Concrete causal reasoning

The user's natural reasoning often moves from a concrete event to its possible consequences, then to the broader ethical or academic point.

Typical pattern:

```text
specific condition
-> plausible consequence
-> broader implication
-> personal/academic judgment
```

Prefer this over immediately replacing the chain with abstract category labels when the concrete explanation carries the argument better.

### Organic paragraph structure

The user strongly dislikes prose that is `too neat` or obviously templated.

Avoid making every paragraph:

- the same length;
- begin with the actor or concept name;
- contain one definition, one explanation, and one identical closing sentence;
- end with a mini-conclusion whether it is needed or not.

Let paragraph shape follow the importance and complexity of the point.

The user explicitly prefers **fewer, denser paragraphs** over many short AI-like paragraphs when the reasoning is still one coherent flow. Do not impose a paragraph quota:

- one paragraph is enough when the answer is already complete;
- two or three paragraphs are natural when the argument genuinely changes phase;
- a coherent paragraph may reach roughly 180–230 words without being split;
- never lengthen an answer only to reach a paragraph or word target.

The user also finds colon-led pseudo-lists inside ordinary prose less natural. When no real list is needed, prefer an integrated sentence using forms such as `yakni`, `seperti`, or ordinary clause structure.

### Natural completeness

Do not force every possible stakeholder, effect, or subpoint into the answer merely to look comprehensive.

The user tends to prefer identifying the important point, explaining why it matters, and expanding only where the reasoning genuinely benefits.

Completeness is still required when the rubric explicitly asks for exhaustive coverage.

## Candidate Preferences

These are supported by the first calibration case but need more examples before becoming global rules.

### Uneven sentence rhythm

Likely preference: mix short direct sentences with longer explanatory sentences instead of maintaining a uniformly polished cadence.

### Fewer polished summary paragraphs

Likely preference: avoid adding a concluding paragraph after every subsection when the preceding reasoning already makes the conclusion obvious.

### Less lexical display

Likely preference: choose the ordinary precise word instead of a more formal synonym merely to sound academic.

### Argument before label

Likely preference: in reflective assignments, explain the reasoning first when useful, then name the ethical/technical category, rather than beginning every paragraph with a textbook label.

## Negative Preferences

Avoid by default unless the genre genuinely needs them:

- overly ceremonial or bureaucratic diction;
- repetitive `dalam kondisi tersebut`, `dari seluruh rangkaian`, `dengan demikian`, or similar framing when a simpler transition works;
- repeated `tidak hanya ... tetapi juga ...` constructions;
- highly symmetrical actor-by-actor paragraphs;
- polished recap sentences that add no new reasoning;
- abstract wording that hides the human consequence of a case;
- replacing the user's opinion with generic textbook morality;
- fragmenting one coherent answer into several short paragraphs merely for visual balance;
- forcing inline inventories after a colon when ordinary prose would carry the same meaning more naturally.

These are not banned phrases. Repetition and context determine whether they become a problem.

## Calibration Record

### Calibration 001 — Ethics coursework case analysis

Observed comparison:

- an earlier highly structured version was judged substantially less natural;
- a later version with simpler diction, more varied paragraph shapes, less symmetry, and more direct personal reasoning was judged much closer to a real average student's writing;
- the user explicitly noted that `apabila` felt less natural than `kalau` for this kind of assignment;
- the user wants future drafts to be reviewed and optionally paraphrased by them, with the resulting edits used as calibration evidence;
- the user explicitly does **not** want the system to copy errors blindly when their revision conflicts with sound academic writing.

This calibration supports the stable preferences above for coursework mode. It is not enough to define the user's full thesis-writing voice.

### Calibration 002 — Ethics anti-pattern coursework

Observed comparison:

- the user revised a representative answer and then explicitly asked for the same style tendencies to be applied to the remaining answers;
- the revision repeatedly added light connective words such as `juga`, `sebenarnya`, and `sudah`, and preferred direct coursework forms such as `kelihatan`, `tapi`, and `asal-asalan`;
- the user naturally retained common technical English such as `code quality` and `deploy` rather than translating every technical term;
- the user explicitly stated that answers should not be forced beyond one paragraph when one paragraph is enough;
- the user explicitly prefers keeping a coherent thought in fewer, denser paragraphs, including paragraphs around 180–230 words when appropriate, instead of splitting it into many short paragraphs;
- the user explicitly finds colon-led inline inventories less natural in ordinary prose and prefers integrated wording such as `yakni` or `seperti`;
- the user accepted the calibrated application across different answers as substantially closer to the desired style;
- the user's nonstandard `mempengaruhi` edit was treated as a correctness conflict and was **not** learned as a voice preference; the stylistic direction is preserved while standard morphology remains authoritative.

This calibration promotes paragraph density, conversational academic glue, and selective technical-English retention to stable coursework preferences. It remains scoped to Indonesian coursework and should not be transferred mechanically to thesis/proposal writing.