---
name: claim-validation
description: Validate claims against user-specified evidence, identify unsupported or overstated statements, trace each finding to its source, and propose precise corrections. Designed for explicit/manual validation requests involving paragraphs, tables, reports, interviews, papers, articles, datasets, or other evidence. Default output is an easy-to-read Indonesian validation table.
metadata:
  version: "1.0"
---

# Claim Validation

Audit claims against the evidence the user actually designates. The goal is not to find as many errors as possible, but to distinguish what is well supported, what is only partly supported, what is uncertain, and what needs revision.

## Core Contract

When this skill is invoked:

1. treat the user's selected source set as the evidence boundary;
2. extract the substantive claims that need validation;
3. compare each claim with the strongest relevant evidence;
4. preserve uncertainty, scope, timing, and source wording;
5. identify contradictions or missing support;
6. explain the result in clear Indonesian;
7. give a concrete correction whenever a claim needs work;
8. make every finding easy to trace back to the source.

Do not silently use general knowledge or external sources to rescue a claim when the user asks for validation against a specific source set.

## Source Boundary

First determine what counts as evidence.

Examples:

- "validasi berdasarkan wawancara ini" -> use the interview as the evidence boundary.
- "cek tabel ini terhadap bab sebelumnya" -> use the specified earlier sections.
- "validasi paragraf ini terhadap paper tersebut" -> use that paper.
- "cek juga dengan sumber eksternal" -> the boundary may expand to external research.

Keep these two questions separate:

- **Source validity:** is the claim supported by the evidence the user specified?
- **Real-world truth:** is the claim true according to broader external evidence?

Do not conflate them. A statement can be plausible in the real world but still unsupported by the selected source.

## Claim Extraction

Validate substantive claims, not every sentence mechanically.

A claim is usually worth checking when it asserts or implies:

- a factual condition;
- a quantity, status, capability, or implementation state;
- a cause or consequence;
- a comparison;
- a generalization;
- a priority or severity;
- a policy being implemented;
- a plan already being executed;
- a conclusion drawn from evidence.

For tables, keep the original row numbers when available.

For paragraphs, split only when separate factual claims require different evidence or different verdicts.

## Validation Workflow

### 1. Read enough source context

Do not validate from isolated keyword matches when surrounding context may change meaning.

Read the relevant paragraph, table row, section, interview answer, result, figure, or nearby context needed to understand:

- who or what the statement applies to;
- whether it is observed, assumed, proposed, planned, or implemented;
- the relevant time period;
- any qualifiers or exceptions;
- whether another source section contradicts it.

### 2. Compare claim strength with evidence strength

Actively check for these common problems:

- assumption presented as fact;
- plan presented as current implementation;
- policy presented as proven operational behavior;
- recommendation presented as an existing condition;
- possibility presented as certainty;
- partial evidence generalized to the whole organization or system;
- one system's condition generalized to all systems;
- historical evidence presented as current without support;
- correlation presented as causation;
- missing or inconsistent numbers;
- internal contradiction between sections;
- claim stronger than the wording of the source;
- absence of documentation treated as proof of absence.

Read [references/validation-rubric.md](references/validation-rubric.md) for verdict definitions and correction rules.

### 3. Trace the evidence

For each finding, provide the most useful human locator available.

Prefer a locator such as:

```text
BAB VII -> 1.4 Dependencies -> Tabel 7.1 -> hlm. 36 -> Database Layer
```

For other source types:

```text
Results -> Table 3 -> p. 8 -> paragraph 2
Wawancara Tim PDT -> pertanyaan 6
Artikel -> bagian "Methodology" -> paragraf 3
```

When the tool provides line citations, page citations, URLs, or file citations, include them as supporting references, but do not replace the human-readable locator with opaque IDs alone.

### 4. Decide the verdict

Use one of these by default:

- **VALID KUAT**
- **VALID DENGAN CATATAN**
- **BUKTI TIDAK CUKUP**
- **KONTRADIKTIF**
- **TIDAK VALID**

Do not inflate uncertainty into an error. "Not proven" is not the same as "proven false."

### 5. Give an actionable correction

Never stop at "kurang valid."

For each claim that needs work, choose the smallest sufficient action:

- **Pertahankan** when no revision is needed.
- **Perhalus wording** when the evidence supports a weaker formulation.
- **Ganti frasa** when only one phrase overstates the evidence.
- **Ganti kalimat** when the whole sentence needs correction.
- **Tulis ulang klaim** when its framing is structurally wrong.
- **Hapus** when unsupported and unnecessary.
- **Cari evidence tambahan** when the claim may be useful but current evidence is insufficient.

Whenever possible, show the exact change:

```text
Sekarang:
"OIKN tidak memiliki automatic failover."

Ganti menjadi:
"Kemampuan automatic failover pada lingkungan virtualisasi belum terkonfirmasi dengan jelas."
```

Do not rewrite more than necessary.

## Default Output

Respond in Indonesian and keep the explanation easy to follow.

Use a Markdown table by default:

| No. / Klaim | Status | Bukti yang Bisa Dilacak | Analisis | Perbaikan |
| --- | --- | --- | --- | --- |

For a long audit, keep the table concise enough to scan, then add a short summary below covering:

- which claims are safe to keep;
- which claims need revision first;
- any cross-source contradiction;
- any limitation in the evidence;
- any recommendation that is analytical rather than directly sourced.

If the user asks for another format, follow that request.

## Evidence Discipline

Preserve the distinction between:

- **observed**;
- **stated by interviewee/source**;
- **assumed**;
- **planned**;
- **recommended**;
- **implemented**;
- **tested/verified**.

Do not upgrade one category into another.

Examples:

- "diasumsikan belum tersedia" does not justify "tidak tersedia";
- "akan diterapkan" does not justify "sudah diterapkan";
- "kebijakan menggunakan failover" does not prove failover is operational;
- "belum dijelaskan dalam dokumen" does not prove the capability does not exist.

When evidence conflicts, surface the conflict instead of choosing whichever statement is more convenient.

## Priorities, Scores, and Judgement Labels

If the target contains labels such as High, Critical, Sangat Tinggi, compliant, mature, effective, or similar judgement terms:

1. look for an explicit scoring method, rubric, matrix, threshold, or source statement;
2. if one exists, validate against it;
3. if none exists, describe the label as an analytical judgement rather than a sourced fact;
4. do not invent a formula after the fact.

## External Research

Only expand beyond the user's selected material when:

- the user explicitly asks for broader verification or research; or
- external evidence is necessary to answer the requested question and the user has not restricted the source set.

Clearly separate external findings from source-bound findings.

## Final Quality Check

Before answering, confirm that:

- every negative verdict has a reason;
- every important claim has traceable evidence;
- uncertainty in the source remains uncertainty in the answer;
- contradictions are surfaced;
- unsupported claims are not silently repaired using outside knowledge;
- suggested wording is no stronger than the evidence;
- the user can quickly locate the proof and apply the correction.
