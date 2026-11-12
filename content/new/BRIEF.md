# New-content brief (CCAR-F)

Read `content/SPEC.md` first and follow every rule in it (accuracy, question quality, output format).

You own ONE domain. Write:
1. **One lesson per task statement** in your domain (format in SPEC.md). Source material: the old Developer
   lessons in `content/part*.json` (`lessons`) and the `lessonNotes` in `content/retag/part*.json` that point
   at your task codes. Reuse what's accurate, rewrite it for the architect framing, drop off-blueprint material.
2. **New questions** so that your domain reaches its target, with the scenario mix given in your task.
   - First read every already-kept question for your domain in `content/retag/part*.json`
     (filter `subskill` starting with your domain code) so you do NOT duplicate a tested decision.
   - Spread new questions across task statements so each task ends up as close to even as possible
     (existing + new), favouring tasks that are currently thin.
   - Each question's `scenario` must be one of S1–S6 and its stem must read as part of that scenario's system.
   - ~20% multi-response, difficulty mix ~20/50/30, vary which option is longest, mix config/code snippets in.
   - ids: `D<d>-<t>-<seq>` e.g. `D5-3-001`.
3. **Verify** facts against the local claude-api reference and the live docs named in SPEC.md
   (Claude Code docs at code.claude.com/docs are essential for D1.5, D1.7, D2.5 and all of D3).
   Leave out anything you can't confirm.

Write `content/new/<your domain lowercased>.json` (e.g. `content/new/d3.json`) as
`{"lessons": [...], "questions": [...]}`. Validate structure with:
`python3 -I -c "import json;d=json.load(open('content/new/d3.json'));q=d['questions'];assert all(len(x['answer'])==x['select'] and len(x['explanations'])==len(x['options']) and len(x['options'])=={1:4,2:5,3:6}[x['select']] for x in q);print(len(d['lessons']),len(q))"`
Write in batches (e.g. save after each task statement) so partial work is never lost.
Edit no other file. Final message: counts per task code and per scenario, and any facts you left out as unverified.
