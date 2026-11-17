# Re-tag brief (→ CCAR-P Professional)

We are re-pointing the study app at the **Claude Certified Architect – Professional (CCAR-P)** exam.
Read `content/SPEC.md` first: it lists the 7 domains and 38 objectives (P1.1–P7.3) and the accuracy rules.

The existing questions were written for other blueprints (Foundations `D*` codes, or the older Developer bank).
You are given a set of questions. For EVERY one, decide:

1. **Keep or drop.** Keep it if it squarely tests one CCAR-P objective as worded in SPEC.md. Drop it if it is
   version/API trivia (exact flags, field names, beta headers, model-specific parameter behaviour), pure
   implementation mechanics a professional architect wouldn't decide, or only loosely related to any objective.
   Expect Claude Code configuration questions to be numerous: keep the ones about *team* setup, shared config,
   workflows and debugging (P7), drop the rest — P7 is only 7% of the exam.
   Drop any question whose key you doubt (say why).
2. For kept questions set `subskill` to the best objective code (e.g. `"P3.2"`). Keep every other field as is,
   including `scenario` when present (the app shows the scenario description as context).
   Questions without `scenario` must be self-contained: if the stem leans on missing context, add one short
   sentence of context. Never change options, answer keys or explanations.

## Output
Write `content/pro/retag/<your label>.json`:
```json
{"questions": [ /* kept questions, full objects, updated */ ],
 "dropped": [ {"id": "AI2-004", "reason": "..."} ]}
```
Validate: `python3 -I -c "import json;d=json.load(open('content/pro/retag/<label>.json'));print(len(d['questions']),len(d['dropped']))"`.
Edit no other file. Keep scratch files in your own new directory under the scratchpad.
Final message: kept count per objective code, dropped count, any doubted keys.
