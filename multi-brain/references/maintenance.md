# Multi Brain Maintenance

## Principle

Automate mechanics, not meaning.

Scripts may validate paths, normalize timestamps, insert bounded events, detect legacy structure, and report oversize files. They should not invent semantic summaries or delete history merely to satisfy a size limit.

## Routine Maintenance

Use:

```bash
python scripts/multibrain.py --repo . status
python scripts/multibrain.py --repo . doctor
```

`status` is a fast inventory. `doctor` is the stronger integrity check.

Recommended moments to run `doctor`:

- after `multi brain init`;
- after migration from v1;
- after a large investigation writes several memory notes;
- before handing a repository to another agent when memory quality matters;
- while changing the Multi Brain skill itself.

## Budget Policy

Default thresholds used by the helper:

- `session.md`: warning above 4 KiB;
- bucket healthy up to 6 KiB;
- bucket maintenance warning above 6 KiB;
- bucket rollup error above 8 KiB.

The 8 KiB threshold means the hot bucket needs semantic maintenance, not that the file should be truncated automatically.

## Semantic Rollup Procedure

When a bucket exceeds budget:

1. Read the complete bucket and any context needed to distinguish authoritative state from history.
2. Rewrite `Current State` so it contains only present authoritative facts/decisions/invariants.
3. Remove closed or obsolete items from `Open Loops`.
4. Keep only the most useful 8-12 recent events.
5. Move older chronology into `.multibrain/archive/<bucket>-<date>-rollup.md` or an equivalent historical context note.
6. Mark older claims `SUPERSEDED` or `HISTORICAL` when they remain visible and could otherwise mislead an agent.
7. Re-run `doctor`.

Do not compress away a still-authoritative constraint merely because it is old.

## Correcting Stale Memory

When new evidence contradicts old memory:

1. verify the new evidence using the strongest available source;
2. update `Current State` first;
3. mark or describe the prior claim as `SUPERSEDED` where ambiguity remains;
4. point to the new authoritative context when deeper evidence is needed;
5. add one concise `correction` event only when the change itself is worth preserving.

Avoid silently editing historical evidence to make it look as though the old conclusion was never held. Historical notes may instead receive a clear superseded notice.

## Legacy v1 Migration

The helper provides a conservative migration:

```bash
python scripts/multibrain.py --repo . migrate
```

For each bucket that lacks v2 sections, the command:

- preserves the existing content;
- creates `Current State`, `Open Loops`, and `Recent Events` sections;
- stores the original legacy body under `Historical Log (v1)`;
- does not invent current-state bullets.

After mechanical migration, an agent should read the legacy log and populate `Current State` plus `Open Loops` semantically.

Migration is intentionally not automatic during `init`.

## Root Instruction Maintenance

The helper owns only marked blocks:

```md
<!-- multi-brain:start -->
...
<!-- multi-brain:end -->
```

If an existing repository already contains unmarked Multi Brain instructions, `init` should avoid duplicating them and report that manual merge is appropriate.

Never replace unrelated repository instructions.

## Pointer Integrity

Pointers in `session.md` and `Recent Events` should use relative repository paths.

`doctor` checks obvious `-> .multibrain/...` targets. Broken pointers should be repaired or explicitly removed when the target was intentionally retired.

Orphan context files are not automatically deleted because they may be historical evidence. Review them before cleanup.

## Secret Hygiene

Before committing memory, inspect summaries/context for accidental:

- passwords;
- access/API tokens;
- cookies or authorization headers;
- private keys;
- secret `.env` values;
- URLs containing credentials;
- raw diagnostic output that embeds secrets.

Prefer references to safe secret locations rather than secret values.

## Tooling Failure Mode

If the helper script is unavailable or incompatible with the environment, follow the same rules manually in Markdown. Multi Brain remains a Markdown-first protocol; Python is an optional deterministic maintenance layer rather than a runtime dependency.
