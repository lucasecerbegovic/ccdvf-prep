# New-content brief (CCAR-P)

Read `content/SPEC.md` first and follow every rule in it (accuracy, quality, output format). New questions
have no `scenario` field: each stem is self-contained.

You own one or more domains. Write:
1. **One lesson per objective** in your domain(s). Source material you may reuse where accurate: lessons in
   `content/new/*.json` (Foundations) and `content/archive_ccdvf/*.json` (older Developer exam). Rewrite for the
   Professional framing (architect decisions, stakeholder and business context, root cause over compensating
   control). Keep each lesson ≈10 minutes.
2. **New questions** exactly to the per-objective counts in your task. First read every kept question for your
   objectives in `content/pro/retag/*.json` (filter by `subskill`) so you don't duplicate a tested decision.
   ~20% multi-response, difficulty ~20/50/30, vary which option is longest, vary industries.
   ids: `P<d>-<o>-<seq>` e.g. `P6-2-001`.
3. **Verify** every fact against the sources named in SPEC.md; leave out anything you can't confirm. For P5.4
   compliance: test the architect's controls and reasoning (data minimisation, residency, retention, access
   control, audit trails, DPIA, human review, vendor due diligence), never a claim about what certifications or
   contracts Anthropic holds unless an official Anthropic page states it. For P6 stakeholder topics, answers rest
   on sound practice (clarify success criteria first, quantify trade-offs, set realistic SLAs from measured
   evals, document decisions as ADRs, staged rollout with feedback loops) — no invented "official" frameworks.

Write `content/pro/new/<label>.json` as `{"lessons": [...], "questions": [...]}`; save after each objective so
partial work survives. Validate:
`python3 -I -c "import json;d=json.load(open('content/pro/new/<label>.json'));q=d['questions'];assert all(len(x['answer'])==x['select'] and len(x['explanations'])==len(x['options']) and len(x['options'])=={1:4,2:5,3:6}[x['select']] for x in q);print(len(d['lessons']),len(q))"`
Edit no other file. Scratch files go in your own new directory under the scratchpad.
Final message: lessons written, new questions per objective, facts left out as unverified.
