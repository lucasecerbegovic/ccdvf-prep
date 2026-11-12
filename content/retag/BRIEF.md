# Re-tag brief (Developer → Architect)

The question bank in `content/part*.json` was written for the **Claude Certified Developer (CCDV-F)** blueprint.
We are re-orienting the app to the **Claude Certified Architect – Foundations (CCAR-F)** exam.
Read `content/SPEC.md` first: it defines the 6 scenarios (S1–S6) and the 30 task statements (D1.1–D5.6).

You are given ONE source file. For EVERY question in it, decide:

1. **Keep or archive.** Keep only if the question squarely tests one CCAR-F task statement as written in SPEC.md
   (a design decision an architect makes about agents, tools/MCP, Claude Code configuration, prompting/structured
   output, or context/reliability). Archive questions about general software engineering, HTTP transport/SSE,
   retries/backoff mechanics, API keys/secrets/IAM, cost arithmetic, model trivia, requirements gathering,
   lifecycle/ops, third-party agent frameworks, MCP server *authoring* internals, Managed Agents product details,
   or anything only loosely related. When in doubt, archive — new questions will be written for gaps.
2. For kept questions:
   - set `subskill` to the best task code (e.g. `"D2.2"`),
   - add `"scenario"` (`"S1"`…`"S6"`) — the scenario whose system the question best fits,
   - **lightly reframe the stem's first sentence(s)** so it reads as part of that scenario's system
     (e.g. "A support-resolution agent built on the Agent SDK…", "In the team's CI pipeline, `claude -p`…").
     Keep the tested decision, the options, the answer key and the explanations exactly equivalent.
     Do not reframe if it would change what is being tested — then pick the closest scenario as-is.
   - re-check the answer key against SPEC.md accuracy rules; if you find a wrong or now-doubtful key, archive it
     and say why.
   - keep `id`, `difficulty`, `select`, `options`, `answer`, `explanations`, `code`, `ref` (fix `ref` only if it
     is clearly wrong).
3. Also read the file's `lessons`. Don't rewrite them; just list which lesson keyPoints/traps are still useful
   source material for which task codes (short notes).

## Output
Write `content/retag/<source basename>` (same filename as the source) as JSON:
```json
{
  "questions": [ /* kept questions, full objects, updated */ ],
  "archived": [ {"id": "AI2-004", "reason": "general REST/SDLC, not on CCAR-F"} ],
  "lessonNotes": [ {"task": "D1.5", "note": "AW.1 keyPoints 4–6 on hooks are accurate and reusable"} ]
}
```
Validate it parses: `python3 -I -c "import json;d=json.load(open('content/retag/<file>'));print(len(d['questions']),len(d['archived']))"`.
Do not edit any other file. In your final message report: kept count per task code, kept count per scenario,
archived count, and any answer keys you doubted.
