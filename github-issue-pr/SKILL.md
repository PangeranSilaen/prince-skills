---
name: github-issue-pr
description: Create or update GitHub Issues and Pull Requests across repositories using local templates and repository conventions, configurable language rules, draft-PR workflows, credential-safety rules, and UTF-8/mojibake verification.
---

# GitHub Issue & PR

Use this workflow for Issue and Pull Request bodies across projects. Keep the skill as the procedural layer; repository-specific policy stays in `AGENTS.md` or the repository's contributor documentation.

## Workflow

1. Read the matching template before composing the body when one is available:
   - `issue_template.md` for Issues.
   - `pr_template.md` for Pull Requests.
   - Also check repository-specific template directories such as `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE/`.
2. Follow the repository's documented language and formatting conventions. If no convention is documented, use the user's language or the project's established language. Keep technical terms, identifiers, commands, paths, API names, and error messages unchanged.
3. Write the title and body to a temporary UTF-8 file. Prefer the agent's file-writing tool or Python with explicit `encoding="utf-8"`. Do not pass non-ASCII body text directly through PowerShell pipes or shell commands that may reinterpret encoding.
4. Create or update GitHub content with `--body-file`, using the current repository rather than a hard-coded owner or project name:
   - Issue: `gh issue create` / `gh issue edit`.
   - PR: `gh pr create` / `gh pr edit`.
   - Follow repository policy for draft PRs. If drafts are required, create the PR with `--draft`; do not mark it ready without explicit user approval.
5. Verify the remote body when the repository provides a verification script. For example:
   `python <repository-verification-script> --repo <owner>/<repo> --kind <issue|pr> --number <number> --body-file <path>`
   If no script is available, retrieve the remote body with `gh api` and verify the content and encoding directly.
6. Report the Issue/PR link and verification result. Remove temporary body files before handoff if they are inside the repository.

## Content rules

- Never include real credentials, tokens, passwords, private IP credentials, or secrets. Use placeholders when examples are required.
- Use `Closes #<issue>` only when the PR fully resolves that Issue. For partial work use `Refs #<issue>` or `Related to #<issue>` so merging does not close the Issue prematurely.
- Follow the repository's policy for draft PRs and review readiness. Do not change a draft to ready for review without explicit user approval.
- For handoff Issues, put the current status in `## Context` and represent remaining work as checkboxes under `## Acceptance criteria`, when those sections are part of the applicable template.
- Treat the API response as the encoding source of truth. Terminal rendering can be misleading, especially on Windows.

## Encoding verification

Use the repository's verification script when available. It should authenticate through the existing `gh` session, capture raw `gh api` bytes, decode the JSON as UTF-8, reject common mojibake markers, and optionally compare the remote body with the local body file. Do not assume a fixed repository owner, repository name, language, template path, or project-specific workflow.
