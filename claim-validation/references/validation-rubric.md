# Validation Rubric

Use this reference when assigning verdicts and proposing corrections.

## Verdicts

### VALID KUAT

Use when the claim is directly and clearly supported by the evidence with matching scope, timing, and certainty.

Typical action: **Pertahankan**.

### VALID DENGAN CATATAN

Use when the central idea is supported but one or more details require caution.

Common reasons:

- the source uses qualified wording such as "diasumsikan", "diperkirakan", "dapat", or "belum terkonfirmasi";
- the claim is slightly broader than the evidence;
- the timing is unclear;
- the evidence is indirect;
- the conclusion is reasonable but partly analytical.

Typical action: **Perhalus wording**, **ganti frasa**, or add a qualifier.

### BUKTI TIDAK CUKUP

Use when the claim may be true, but the selected evidence does not establish it.

Examples:

- documentation is silent;
- only a proposal exists;
- only one component was observed but the claim covers the whole system;
- the source says something is unclear, not absent.

Typical action: **Cari evidence tambahan** or rewrite the claim as an uncertainty.

### KONTRADIKTIF

Use when relevant evidence conflicts internally or directly opposes the claim.

Do not hide the conflict by choosing one source without explanation.

Typical action:

1. show both locations;
2. explain exactly what conflicts;
3. recommend validation with the authoritative source, owner, interviewee, or current system;
4. align the document only after confirmation.

### TIDAK VALID

Use when the selected evidence clearly disproves the claim or the claim materially misstates the source.

Typical action: **Ganti kalimat**, **tulis ulang klaim**, or **hapus**.

## Strength Mismatches

### Assumption -> Fact

Source:
"Diasumsikan virtualisasi belum didukung failover otomatis."

Unsafe:
"Automatic failover tidak tersedia."

Safer:
"Kemampuan automatic failover belum terkonfirmasi dengan jelas."

### Plan -> Implementation

Source:
"Backup akan dilakukan setiap minggu."

Unsafe:
"Backup dilakukan setiap minggu."

Safer:
"Backup mingguan direncanakan, tetapi pelaksanaannya perlu diverifikasi."

### Policy -> Operational State

Source:
"Kebijakan pemulihan menggunakan multi-ISP."

Unsafe:
"Pusat data sudah menggunakan multi-ISP."

Safer:
"Kebijakan pemulihan menetapkan penggunaan multi-ISP, tetapi implementasi aktual perlu diverifikasi."

### Missing Documentation -> Nonexistence

Source:
"Keberadaan alternate site belum dijelaskan."

Unsafe:
"OIKN tidak memiliki alternate site."

Safer:
"Keberadaan dan kesiapan alternate site belum terdokumentasi dengan jelas."

### Partial Scope -> Generalization

Source:
"Monitoring server menggunakan Zabbix."

Unsafe:
"Seluruh infrastruktur dimonitor secara terpusat dengan Zabbix."

Safer:
"Monitoring server menggunakan Zabbix, sementara cakupan monitoring terhadap komponen lain perlu diverifikasi."

## Correction Priority

Prefer the smallest correction that restores source fidelity.

1. **Pertahankan**
2. **Perhalus wording**
3. **Ganti frasa**
4. **Ganti kalimat**
5. **Tulis ulang klaim**
6. **Hapus**
7. **Cari evidence tambahan**

Do not rewrite an entire paragraph when changing one qualifier is enough.

## Traceability Standard

Evidence should be locatable by a human without relying only on tool-specific IDs.

Good:

```text
BAB IV -> 4.10 Event Management dan Incident Management -> hlm. 25 -> paragraf pembuka
```

Good for interviews:

```text
Notulensi wawancara Tim PDT -> pertanyaan 6 -> jawaban tentang DCMS
```

Good for papers:

```text
Results -> Table 2 -> p. 7 -> row "Latency"
```

When exact paragraph or sentence numbering is unavailable, describe the nearest stable section, table, row, or quoted phrase.

## Analytical Judgements

Labels such as "Tinggi", "Critical", "mature", or "effective" are valid as sourced facts only when supported by a stated method, matrix, threshold, or explicit source judgement.

Otherwise say clearly that they are the analyst's judgement.

Example:

```text
Status: VALID DENGAN CATATAN
Catatan: Kondisi gap didukung sumber, tetapi label "Sangat Tinggi" tidak memiliki formula atau matriks prioritas yang dijelaskan. Perlakukan label tersebut sebagai penilaian tim.
```
