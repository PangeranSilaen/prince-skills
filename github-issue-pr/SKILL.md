---
name: github-issue-pr
description: Create or update GitHub Issues and Pull Requests for AksaLoka using the repository templates, Indonesian-language convention, draft-PR workflow, credential-safety rules, and UTF-8/mojibake verification. Use whenever an agent writes or changes an Issue or Pull Request body in this repository.
---

# GitHub Issue & PR

Use this workflow for Issue and Pull Request bodies. Keep the skill as the procedural layer; global repository policy stays in `AGENTS.md`.

## Workflow

1. Read the matching template before composing the body:
   - `issue_template.md` for Issues.
   - `pr_template.md` for Pull Requests.
2. Write the title and explanatory text in Indonesian. Keep technical terms, identifiers, commands, paths, API names, and error messages unchanged.
3. Write the body to a temporary UTF-8 file. Prefer the agent's file-writing tool or Python with explicit `encoding="utf-8"`. Do not pass non-ASCII body text directly through PowerShell pipes or `--body`.
4. Create or update GitHub content with `--body-file`:
   - Issue: `gh issue create` / `gh issue edit`.
   - PR: `gh pr create --draft` / `gh pr edit`.
5. Verify the remote body with:
   `python .agents/skills/github-issue-pr/scripts/verify_github_body.py --repo PangeranSilaen/aksaloka --kind <issue|pr> --number <number> --body-file <path>`
6. Report the Issue/PR link and verification result. Remove temporary body files before handoff if they are inside the repository.

## Content rules

- Never include real credentials, tokens, passwords, private IP credentials, or secrets. Use placeholders when examples are required.
- Use `Closes #<issue>` only when the PR fully resolves that Issue. For partial work use `Refs #<issue>` or `Related to #<issue>` so merge does not close the Issue prematurely.
- PRs must start as drafts and may become ready for review only after explicit user approval, as required by `AGENTS.md`.
- For handoff Issues, put the current status in `## Context` and represent remaining work as checkboxes under `## Acceptance criteria`.
- Treat the API response as the encoding source of truth. Terminal rendering can be misleading on Windows.

## Encoding verification

`scripts/verify_github_body.py` authenticates through the existing `gh` session, captures raw `gh api` bytes, decodes the JSON as UTF-8, rejects common mojibake markers, and optionally compares the remote body exactly with the local UTF-8 body file.
