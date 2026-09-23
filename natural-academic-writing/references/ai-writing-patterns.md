# AI Writing Patterns

Use this reference as an audit aid, not as a detector or a blacklist.

The patterns below are supported by comparative writing research, but none of them proves that a specific passage was written by AI. Genre, proficiency, editing, and assignment design can produce similar features in human writing.

## Evidence-Supported Patterns

### Repetitive syntactic structure

A 2026 Indonesian study of student academic papers associated with generative-AI use reported repetitive sentence structures, rigid discourse markers, and semantic redundancy as recurring features.

Practical audit question:

> Do several nearby sentences or paragraphs reuse the same grammatical frame even when the ideas differ?

Do not `fix` this by randomizing syntax. Vary structure only when the reasoning supports a different shape.

### Rigid or formulaic discourse organization

Research comparing ChatGPT and student argumentative writing has found more routinized or formulaic rhetorical patterns in model-generated examples, while students showed greater structural variety.

Practical audit question:

> Are examples, contrasts, explanations, or paragraph transitions introduced through the same visible pattern every time?

### Stable genre-insensitive style

A 2025 PNAS study found substantial differences between human and instruction-tuned LLM writing across grammatical, lexical, and rhetorical features, including difficulty matching the stylistic variation associated with human genre conventions. Instruction-tuned models showed a distinct noun-heavy, informationally dense style.

Practical audit question:

> Does a reflective assignment, thesis paragraph, report, and explanatory answer all sound as if they came from the same polished register?

This is one reason the skill uses separate coursework and thesis modes.

### Academic vocabulary used as display rather than precision

A 2024 corpus comparison of ChatGPT-generated and human-authored social-science academic writing reported overuse of infrequent academic vocabulary and excessively flowery language in ChatGPT output. It also found patterns consistent with synonym substitution inside syntactically similar structures.

Practical audit questions:

> Is the more formal word actually more precise?

> Did wording change while the sentence architecture stayed mechanically identical?

### Formulaic bundles and exemplification

Comparative work on argumentative writing has reported more formulaic language-pattern behavior in ChatGPT essays and more routinized exemplification patterns than in student writing.

Practical audit question:

> Are examples being used because they advance the argument, or because every claim is being expanded through the same `for example -> explanation -> conclusion` routine?

### Semantic redundancy

Redundancy is especially noticeable when a paragraph repeatedly restates the same judgment using slightly different academic phrasing without adding a new condition, consequence, piece of evidence, or interpretation.

Practical audit question:

> If one sentence is removed, is any substantive information actually lost?

If not, the paragraph may be polished but mechanically padded.

## Patterns Observed in the Current Calibration

These are consistent with the research above but come from the user's own evaluation of drafts:

- actor-by-actor paragraphs with nearly identical structure felt artificial;
- very balanced paragraph lengths felt over-produced;
- repeated `X memiliki tanggung jawab... seharusnya...` framing felt templated;
- highly formal words reduced perceived naturalness when a simpler word fit the assignment;
- repeated mini-conclusions made the answer feel more generated;
- concrete causal reasoning sounded more authentic than abstract category lists alone.

Treat these as voice evidence, not universal facts about AI writing.

## What Not to Do

Do not respond to these patterns by deliberately adding:

- typos;
- grammar mistakes;
- random fragments;
- fake personal anecdotes;
- unsupported uncertainty;
- unnecessary slang;
- arbitrary sentence-length variation;
- meaningless lexical diversity.

The goal is not statistical camouflage. It is prose whose structure follows a real argument and a real genre.

## AI Detector Boundary

Do not use detector scores as the optimization target.

OpenAI discontinued its public AI-text classifier in 2023 because of its low accuracy. Turnitin's current guidance also states that its AI-writing model can misidentify human-written, AI-generated, and AI-paraphrased text and should not be used as the sole basis for adverse action against a student.

Therefore:

- do not promise `undetectable` writing;
- do not rewrite solely to lower a detector score;
- do not encode detector-specific tricks into the voice profile;
- judge quality through source fidelity, reasoning, genre fit, voice, and readability.

## Sources

1. Habiburrahman & Harsono. `Pola Kebahasaan AI Generatif dalam Karya Ilmiah Mahasiswa: Repetisi Sintaksis, Rigiditas Penanda Wacana, dan Redundansi Semantis.` Pena: Jurnal Pendidikan Bahasa dan Sastra, 16(3), 2026. https://doi.org/10.22437/pena.v16i3.56207
2. Reinhart, A. et al. `Do LLMs write like humans? Variation in grammatical and rhetorical styles.` Proceedings of the National Academy of Sciences, 122(8), 2025. https://doi.org/10.1073/pnas.2422455122
3. `A corpus-driven comparative analysis of AI in academic discourse: Investigating ChatGPT-generated academic texts in social sciences.` Lingua, 312, 2024, 103838. https://doi.org/10.1016/j.lingua.2024.103838
4. Jiang, F. (Kevin) & Hyland, K. `Does ChatGPT argue like students? Bundles in argumentative essays.` Applied Linguistics, 46(3), 2025, 375–391. https://ueaeprints.uea.ac.uk/id/eprint/96245/
5. `Exemplification in ChatGPT and student argumentative writing: A local grammar analysis.` Linguistics and Education, 93, 2026, 101533. https://doi.org/10.1016/j.linged.2026.101533
6. OpenAI. `New AI classifier for indicating AI-written text` — notes that the classifier was discontinued because of low accuracy. https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/
7. Turnitin Guides. `Using the AI Writing Report` — states that AI-writing detection may misidentify text and should not be the sole basis for adverse action. https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report

## Evidence Caveats

- Several cited studies focus on English, so transfer to Indonesian should be treated as a writing-audit hypothesis rather than a universal linguistic law.
- The 2026 Indonesian study used a corpus selected partly through AI-probability criteria, so its features should not be treated as proof of authorship for an individual document.
- Model behavior changes over time. Prefer broad writing principles such as structural variety, genre fit, and non-redundancy over model-specific word lists.
- A highly structured human writer can display these same patterns. Style evidence is descriptive, not an authorship verdict.