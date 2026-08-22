---
name: session-handoff
description: Create a structured handoff document and prompt starter when the current AI session is too long and the user wants to continue in a new session with full context preserved. Use when the user says "buat handoff", "handoff session", "lanjut new session", "session terlalu panjang", "compaction lalu handoff", "sesi baru", "context window penuh", "bikin handoff doc", or any request to package current session state for resumption elsewhere. Also activates when user explicitly mentions wanting prompt caching to work in next session, when context is approaching limits, or when wrapping up a long debugging/feature session that the user wants to pause and continue later. Produces both a markdown handoff doc AND a copy-paste prompt starter for the new session. Works with any project structure — auto-detects available tools, directories, and conventions (AGENTS.md, CLAUDE.md, etc).
---

# Session Handoff

When a session gets long and the user wants to continue in a new chat, this skill packages everything needed for an agent in the new session to be immediately productive — without the user having to re-explain context.

## When to Use

Trigger this skill when the user signals **session fatigue** or **context overflow**:

- Direct: "bikin handoff", "handoff doc", "lanjut new session", "context udah panjang"
- Indirect: "sesi sudah terlalu panjang", "biar prompt caching tetap jalan di sesi baru", "compaction"
- Implicit: long sessions (>50 turns) where the user is wrapping up multiple PRs / investigations and starts asking about session state

Don't trigger this for short clarification requests or normal pauses — only when the user explicitly signals they want to start fresh.

## Output Contract

Produce TWO artifacts:

1. **Handoff doc** — a markdown file that the next agent reads first. Location auto-detected from project structure (see Step 2)
2. **Prompt starter** — a ready-to-paste block in the current chat that the user copies into the new session

Both are required. The user paste prompt starter → new agent reads handoff doc → new agent confirms understanding → resumes work.

## Step-by-Step Process

### Step 1: Take a final state snapshot

Run these checks **before** writing the handoff (use what's available in the project):

```
- git status --short (if using git)
- git branch --show-current
- git log --oneline -8
- gh pr list or equivalent PR tool (if used)
- DB count/records snapshot (if database-backed work was done)
- Test suite baseline (npm test, pytest, php artisan test, etc.)
```

Save these outputs verbatim into the handoff. Don't paraphrase counts, hashes, or commit IDs — accuracy matters when the next agent verifies state. Skip any check that's not applicable to your project.

### Step 2: Determine handoff doc location

**Auto-detect the best location** by checking what's available in the project:

1. **Check AGENTS.md / CLAUDE.md first** — if it specifies a handoff/docs location, use that
2. **Check for existing docs folder** — `docs/handoffs/`, `docs/`, or any `docs/` subfolder already used
3. **Fallback to root** — `.handoffs/` at project root
4. **Ask user** — if nothing detected, ask where they prefer

Filename format: `YYYY-MM-DD-<short-topic-slug>.md` (e.g. `2026-05-14-db-safety-hardening-complete.md`).

Don't overthink this — the location matters less than the content. Pick one and move on.

### Step 3: Write the handoff doc

Use this template. **Make sections conditional** — skip or mark "N/A" if not applicable to your project. Don't force content that doesn't exist. The next agent should only see relevant information, not boilerplate for everything.

```markdown
# Handoff — <YYYY-MM-DD>: <Topic Headline>

> Dokumen ini ditulis di akhir sesi panjang (<one-line context>). Sesi berikutnya buka di chat baru karena context window sudah panjang. Dokumen ini cukup detail untuk agent baru langsung produktif tanpa baca history.

## TL;DR

<2-4 sentences max. What was done, what's the current state, what's next.>

## Status Git Saat Handoff

```
Branch: <current branch> (<clean | dirty>, <sync state>)
HEAD: <hash> <commit subject>

Recent merges/commits:
  <hash> (#PR) <subject>
  ...
```

**Untracked files:** <list, with note about whether to ignore/commit/etc.>

## Konteks Singkat: Apa Yang Terjadi Di Sesi Ini

<Narrative 3-6 paragraphs. Cover:
- Why the session started (initial task)
- Major pivots or discoveries  
- What was completed (PRs merged, files changed, decisions made)
- What was left undone and why>

## State Database / Infrastructure

<Counts, server states, deployment status. If none, write "Tidak ada database/infra work yang dilakukan">

## Login / Access Credentials

<Local-only credentials for testing. Never include production secrets. If none, write "Tidak ada credentials digunakan">

## Test Suite Baseline

<Last test run counts. Note pre-existing failures so next agent doesn't chase ghosts.>

## Open Tasks (Priority Order)

<% If there are open tasks %>
### 1. <Task title> (<HIGH|MEDIUM|LOW>)

URL: <issue/PR url if any>

**Context:** <1-3 sentences about what user reported or why this matters>

**Investigasi yang diperlukan:** <what to look at first>

**Reference files:** <bullet list of likely-relevant paths>

### 2. ... (repeat)
<% else %>
Tidak ada open tasks untuk dilanjutkan.
<% endif %>

## Constraints & Konvensi yang HARUS Diingat

<Pull from AGENTS.md/CLAUDE.md/project-specific docs. Critical rules only — don't dump entire file. Examples:
- Forbidden commands
- PR/branch conventions
- Tool preferences (e.g., "use Read not cat")
- Communication style preferences>

<% If project has defined skills/conventions that should be auto-triggered %>
## Skills / Tools Project-Scope

<List skills the next agent should activate proactively for this project's domain.>
<% endif %>

## Tech Stack Ringkas

<One line per layer: language version, framework, DB, build tool, etc.>

## File Yang Mungkin Sering Disentuh (Reference Cepat)

<% If key files were frequently worked on %>
| Path | Tujuan |
|------|--------|
| ... | ... |
<% else %>
Tidak ada file khusus yang dominan dalam sesi ini.
<% endif %>

## Saran Order Berikut (Recommended)

<Numbered list, opinionated. The next agent should be able to pick task #1 and start without re-deciding.>

<% If production/deploy work was involved %>
## Production / Deploy Info

<SSH targets, deploy paths, environment quirks. Flag anything destructive.>
<% else %>
Tidak ada production/deploy work yang dilakukan.
<% endif %>

---

**Catatan untuk agent baru:** <interaction style notes — language preference, decision-making style, recommended use of tools, anything unique to the user that helps the next agent maintain rapport>
```

Match the language of the doc to what the user has been speaking in this session. If user wrote Indonesian, write the handoff in Indonesian (technical terms like "branch", "commit", "PR" stay English).

### Step 4: Write the prompt starter

Provide this as a code block in the current chat reply. The user copies it into the new session.

**Generic template** (customize based on what you detected in Step 1):

```
Halo, gw lanjut dari sesi sebelumnya (<DATE>) yang sudah panjang. Konteks lengkap ada di file `<HANDOFF_PATH>` di project ini.

Tolong lo baca file handoff itu dulu (full, jangan skim) sebelum reply apapun. Setelah itu konfirmasi:
1. State git + branch + last commits sesuai handoff
2. State <DB/infra jika applicable> (counts) sesuai handoff  
3. Open tasks + priority order
4. Constraints critical yang harus diingat

Setelah itu, langsung mulai task #1 dari "Saran Order Berikut" di handoff (<TASK_TITLE>). <PROCESS_NOTES — e.g., "TDD properly", "pakai question tool dengan label RECOMMENDED", "bahasa Indonesia">.

Konteks kenapa handoff: <ONE_LINE — e.g., "sesi sebelumnya panjang karena ngerjain X+Y+Z, semua sudah merged. Mau lanjut task baru tapi context window sudah gede.">
```

**Customize the `<PROCESS_NOTES>`** based on what worked well in this session. Examples:
- If using databases: `"cek DB state juga"`
- If testing is important: `"run tests before changes"`
- User preference: `"gunakan Bahasa Indonesia untuk semua response"`

If the user's AGENTS.md has specific instructions, mention those too.

### Step 5: Update changelogs (if project has any)

If the project tracks `CHANGELOG.md`, `.opencode/CHANGELOG.md`, or similar, add an entry summarizing the session. Even if gitignored, this helps the next agent. Skip if no such file exists — not all projects need this.

### Step 6: Final reply to user

Tell the user:

1. Where the handoff doc is written (full path)
2. Show the prompt starter as a code block they can copy
3. Final state check (git clean, DB intact, tests stable)
4. Note about prompt caching (per-conversation, so new session = new cache, but the structured doc minimizes re-discovery time)
5. Anything left unstaged that they need to decide on

Keep the reply tight — they're about to switch sessions, so the message should be skim-friendly, not a wall of prose.

## Anti-Patterns

- **Don't dump conversation history verbatim.** The handoff is a *digest*, not a transcript. The next agent doesn't need every message — just the decisions, state, and next steps.
- **Don't skip the snapshot step.** Without git/test/DB state, the next agent has to re-discover, which defeats the purpose.
- **Don't write "see chat history".** The new session won't have access to the old chat. Everything important must be in the doc.
- **Don't auto-commit the handoff** unless the user explicitly asks. Many projects gitignore handoff docs intentionally — let the user decide.
- **Don't make the prompt starter generic.** Tailor it to the specific user (language, decision style, tools they prefer). A generic starter loses session-specific context that took the current agent time to learn.
- **Don't include secrets or production credentials.** Local dev creds OK; anything that grants production access stays out.

## When to Be Brief vs Detailed

**Brief handoff (under 200 lines):**
- Single-task session
- One PR merged, no major pivots
- No infrastructure or production touched

**Detailed handoff (300-500 lines):**
- Multiple PRs or investigations
- Forensic / debugging sessions where root cause matters for context
- Production touches or deployment decisions
- Multiple open issues being tracked

A handoff over 500 lines is usually too long — split into multiple sub-pages or trim aggressively.

## Verification Before Finishing

Before telling the user "you can switch sessions now":

- [ ] Handoff doc written and readable (re-open it, scan for typos / missing sections)
- [ ] Prompt starter customized for the specific user / project
- [ ] Final state snapshot matches the handoff body (no drift) — **skip checks that don't apply** (e.g., if no DB work, don't verify DB counts)
- [ ] Any unstaged changes flagged to user
- [ ] If project has CHANGELOG, entry added

If any check fails, fix it before announcing "ready". The next agent's context quality depends on this doc being accurate.
