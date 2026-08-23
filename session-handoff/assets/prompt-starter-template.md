Read the temporary session handoff at `<HANDOFF_PATH>` in full before doing substantive work.

Then:
1. Read the repository instructions and durable sources referenced by the handoff as needed.
2. Re-verify volatile state that affects the next action (for example branch/HEAD, PR status, tests, runtime/DB state). Treat the handoff snapshot as a checkpoint, not an eternal source of truth.
3. Preserve any genuinely new durable knowledge in the repository's proper memory/docs system when warranted; do not duplicate information that is already durable.
4. Delete `<HANDOFF_PATH>` after successful consumption. It is intentionally ephemeral and must not be committed.
5. Continue directly with the `Next Action` from the handoff. Do not ask me to re-explain context that the handoff or repository already answers.

Reply in `<LANGUAGE>` and clearly separate anything that is VERIFIED, INFERRED, or NOT TESTED when that distinction matters.
