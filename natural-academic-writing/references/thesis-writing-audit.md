# Thesis Writing Audit

Use this procedure to draft, revise, or audit formal Indonesian academic writing. Read [thesis mode](thesis-mode.md), the applicable [voice preferences](voice-profile.md#thesis--proposal-voice), and any local writing guide, glossary, examples, or template.

## Set the scope

- Identify the manuscript version and requested action. For a new draft, map the section's role, claims, and supporting evidence before writing. For a targeted revision, read the passage and its surrounding context. For a full audit, track every paragraph and sentence, table cell, caption, and relevant figure label in scope.
- Read the latest applicable user decisions and source records. Use the local glossary for current wording and the primary evidence for technical meaning, dates, and claim limits. Record any source gaps or artifacts you cannot assess.
- A keyword search can help locate occurrences. Establish coverage by reading each relevant unit in context. Trace affected wording across sections, including figures and tables, and list any proposed follow-up outside the authorized edit scope.

## Four review passes

| Pass | What to check |
| --- | --- |
| Actor, action, and object | Identify who or what acts, what the action does, and which item or condition it affects. Give `ini` or `tersebut` a clear referent. Make each verb fit its object. Choose a concise passive when the actor is immaterial. |
| Relationships between ideas | Make the cause, qualification, comparison, or sequence explicit when the evidence supports it. Split crowded clauses and join short sentences when they express one relationship more clearly together. Check whether each paragraph has one main function and whether its transition advances the argument. |
| Terminology and format | Confirm the meaning of a term in context and use the current glossary consistently. Check the first relevant occurrence of each abbreviation in document order, including tables. Confirm expansions and explain relevant functions. Preserve names of technologies and code identifiers. Apply EYD V and local italic, punctuation, and citation rules. |
| Evidence and claim limits | Distinguish a plan, an observation, a risk, and an interpretation. Check citations, quantities, metric definitions and units, negation, modality, conditions, sample and version, and chronology. Preserve the distinction between simulation and physical observations. Identify any unsupported detail or change in what the method promises to measure. |

Reread the revised sentence with its neighbors and compare it with the original and the available evidence. When a substantive problem needs a change to the research question, method, scope, or findings, mark it separately with its evidence and proposed correction. Keep unresolved claims out of copy-ready prose. Apply the review rules already approved for the task.

## Worked examples

These constructed examples illustrate editing decisions. Use your manuscript's actual evidence, citations, and terminology.

| Issue | Before | After | Reason and limit |
| --- | --- | --- | --- |
| Vague referent and condition | “Jika kondisi tersebut terjadi, penyesuaian dilakukan oleh sistem.” | “Jika pembacaan sensor tidak tersedia, program menggunakan nilai terakhir yang tercatat.” | Name the condition and action when the source identifies both. Keep “tidak tersedia” distinct from “sensor gagal”. |
| One verb for different objects | “Data suhu dan perintah kalibrasi diperoleh melalui aplikasi.” | “Aplikasi membaca data suhu dan mengirim perintah kalibrasi.” | The two objects require different actions. Sending a command alone establishes no successful calibration. |
| One relationship split across sentences | “Prosedur memeriksa konfigurasi yang sudah tercatat. Konfigurasi terbaru masih perlu diperiksa pada setiap stasiun.” | “Prosedur memeriksa konfigurasi yang sudah tercatat, sedangkan konfigurasi terbaru masih perlu diverifikasi pada setiap stasiun.” | Present the procedure alongside its limit. Preserve “masih perlu”. |
| Ambiguous terminology | “Antarmuka dipakai untuk melihat tren kelembapan.” | “Pengguna melihat tren kelembapan pada tampilan pemantauan.” | Use the term that fits the object. In code or service documentation, “antarmuka” may refer to an API or an interface instead. |
| Method and observable evidence | “Uji membuktikan pencatatan berjalan tanpa gangguan.” | “Pengujian memeriksa apakah jumlah catatan bertambah selama periode pengamatan.” | State the planned check and its indicator. Limit any eventual finding to what was observed during the test. |
| Metric and sample | “Studi mengukur kapasitas pemrosesan pada beberapa perangkat.” | “Studi mengukur *throughput* dalam sampel per detik menggunakan empat perangkat yang disimulasikan.” | Use the definition, unit, and test conditions established by the source. Keep the citation attached to the measurement. |
| Scope of a conclusion | “Hasilnya berlaku untuk semua stasiun pemantauan.” | “Hasil tersebut berlaku pada dua stasiun yang diuji dengan konfigurasi penelitian.” | If evidence covers only two stations, flag the original as a substantive overgeneralization. Offer the narrower wording separately when the task authorizes style edits only. |
| Figure reference | “Gambar 2 menunjukkan cara program memilih data.” | “Program menyaring pembacaan yang belum lengkap sebelum menghitung rata-rata. Urutan penyaringan ditunjukkan pada Gambar 2.” | Lead with the idea and verify that the figure shows the described process. Start the caption with its number if required. |

## Check across the document and the rendered output

- Follow changed terms and names through prose, headings, schedules, tables, captions, and diagram labels. Preserve quantities, time allocations, criteria, and citations when a label changes. Check the source diagram and the rendered figure when both are available and affected.
- Match the treatment of abbreviations and italics against the target format. Prefer the [official EYD guidance](https://ejaan.kemendikdasmen.go.id/) for spelling and punctuation and the institution's guide for document-specific requirements. Label a clarity or voice suggestion as such.
- For a copy-ready deliverable, keep audit notes, internal source IDs, and routine review timestamps outside the manuscript. Preserve dates the reader needs to interpret the evidence. Render Markdown when real italic, headings, lists, and tables are required. Check the rendered text and structure against its source. When transfer is in scope, verify the formatting in the destination document as well. Follow the project's own render or publication workflow when it applies.

## Report the result

For an audit, report the reviewed version, scope, and source limits. Group recurring issues while retaining their locations. Give each actionable finding a location, before and proposed after wording, a specific reason, and any fact or condition that constrains the edit. Distinguish evidence or meaning issues, clarity, language conventions, and voice preferences so the reader can prioritize them. Keep audit-only findings as proposals. For an authorized revision, apply and recheck the affected text and assets. Use technical checks to verify structure and formatting, and assess prose and claims by reading them against the evidence.
