# Answer-key review brief

You are an independent reviewer for exam-prep questions (Claude Certified Architect – Foundations).
`content/SPEC.md` explains the format. You did not write these questions; assume nothing about them is right.

For EVERY question assigned to you, work it yourself before reading the key:
1. Read the stem and options, decide your own answer, then compare with `answer`.
2. Check every factual claim the key and its explanation depend on against official sources:
   local reference `/private/tmp/claude-501/bundled-skills/2.1.321/b5dc1eb8612cbaaae146f93aa7df0067/claude-api/`
   and live docs (WebFetch): code.claude.com/docs, platform.claude.com/docs, modelcontextprotocol.io,
   anthropic.com/engineering. Note: on current models, forced `tool_choice` (`any`/`tool`) returns 400.
3. Classify each question:
   - `ok`
   - `wrong_key` — the keyed answer is wrong or another option is equally/more correct (ambiguous)
   - `bad_fact` — key is right but an explanation/stem states something false or unverifiable
   - `weak` — fine facts but a distractor is arguably also correct, or the stem gives the answer away

## Fixing
Only fix `wrong_key`, `bad_fact` and `weak` items, and only when you have doc evidence (URL + short quote/paraphrase).
Edit the question in place in your assigned file(s): change `answer`, rewrite an option/explanation/stem as needed,
keeping `select`/option-count rules. If a question can't be repaired cleanly, set `"retired": true` on it
(the build drops retired questions). Keep `id`, `subskill`, `scenario`. Don't touch questions classified `ok`.
After editing, validate: `python3 -I content/build.py` must exit 0 (other reviewers may be editing other files
at the same time — ignore errors in files that are not yours).

## Report
Write `content/review/<your label>.json`:
`{"reviewed": N, "findings": [{"id","file","class","problem","evidence_url","evidence","fix"}]}` — only non-ok items.
Final message: counts per class, and the ids you changed or retired with one line each.
Keep scratch files in your own new directory under the scratchpad, not its root.
