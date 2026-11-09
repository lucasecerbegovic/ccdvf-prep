# CCDV-F Study Program — Content Spec

You are writing original exam-prep content for the **Claude Certified Developer – Foundations (CCDV-F)** exam
(Anthropic, delivered by Pearson VUE; exam guide v1.0 effective July 2026).
The learner is an experienced Claude builder (API, Agent SDK, MCP, Claude Code) cramming for 2–3 weeks.

## Real exam format (match it)
- 53 scenario-based items, 120 minutes, multiple choice (1 correct of 4) and multiple response
  ("Select TWO" / "Select THREE", of 5–6 options). Each item states how many to pick. No partial credit.
- Scaled score 100–1000, pass = 720. Candidates: AI engineers, tech leads, senior SWEs (1–5 yrs, 6+ months with LLMs, Python/TS).

## Domains & sub-skills (codes are fixed — use exactly these)
| Code | Sub-skill | Weight | Topics |
|---|---|---|---|
| AI.1 | Claude Application Design | 8.6% | Claude's behaviour across Claude Code, Desktop, claude.ai, the API and SDKs; content boundaries; schema design; session hygiene; plugin management |
| AI.2 | Software Engineering Foundations | 7.4% | REST APIs, JSON, async programming, version control, SDLC integration, code review, refactoring (in Claude-app contexts) |
| AI.3 | Claude API Mechanics | 6.8% | Messages API, tools, streaming, vision/PDF, thinking, prompt caching, Bedrock/Vertex/Foundry access, Message Batches, realtime vs batch |
| AI.4 | Configuration Management | 4.1% | CLAUDE.md, settings.json, model version pinning, prompt versioning, plugin dependencies |
| AI.5 | Understanding Requirements | 3.4% | Functional + infrastructure requirements from business needs and solution architecture |
| AI.6 | Systems Life Cycle | 2.8% | Developing, implementing, operating and maintaining LLM systems (monitoring, rollouts, deprecations) |
| MSO.1 | Technical Fundamentals | 6.1% | SDK integration, REST-wrapping SDKs, retries/timeouts, streaming transports (SSE), websockets |
| MSO.2 | LLM Fundamentals | 5.2% | Tokens, context windows, sampling, non-determinism, next-token generation; fast mode, adaptive thinking, effort levels; zero/one/few-shot |
| MSO.3 | Cost & Token Management | 2.8% | Usage tracking, cost modelling, prompt caching, cache breakpoints, batch discount, token counting |
| MSO.4 | Model Selection & Trade-offs | 2.7% | Opus / Sonnet / Haiku use cases; quality-latency-cost trade-offs; breaking changes across releases; pinning |
| AW.1 | Agent Construction with Claude | 5.3% | Claude Agent SDK, custom loops & harnesses, Tool Runner, self-hosted vs Anthropic-hosted (Managed Agents), hooks |
| AW.2 | Agent Patterns & Frameworks | 4.9% | Tool-use loops, subagents, memory, context management; third-party frameworks (Strands, LangGraph, PydanticAI) |
| AW.3 | Agent Architecture | 4.5% | Workflow vs agent decision, orchestrator/supervisor hierarchies, subagents, routing, prompt chaining, parallelization, evaluator-optimizer |
| PCE.1 | Prompt Engineering | 4.6% | Clarity, few-shot examples, system vs user placement, XML tags, output constraints, iteration, input sanitisation |
| PCE.2 | Context Engineering | 3.8% | Window management, tool output pruning, compaction, context editing, isolation via subagents, long-doc placement |
| PCE.3 | Output Handling | 2.6% | Structured outputs, response validation, defensive parsing, scepticism toward confident output, stop_reason handling |
| TM.1 | Tool Implementation | 4.4% | Tool definitions/descriptions, input_schema, strict, tool_result & is_error, parallel tool use, client vs server tools, approval patterns |
| TM.2 | Agentic Customization | 4.1% | Choosing among built-in tools, custom tools, Agent Skills, MCP servers, plugins, subagents |
| TM.3 | MCP Server Development | 2.1% | Authoring/deploying MCP servers; tools, resources, prompts; stdio vs Streamable HTTP; auth; MCP connector |
| SS.1 | AI Application Security | 3.2% | Prompt injection (direct/indirect), jailbreaks, untrusted input, data leakage, PII, authn/authz |
| SS.2 | Guardrails & Safe Deployment | 2.3% | Content policy, layered guardrails, least privilege, IAM, human-in-the-loop, refusal handling |
| SS.3 | Identity, Secrets & Key Management | 1.6% | API keys across environments, workspaces, secret managers, rotation, WIF/OAuth, never in prompts/repos |
| SS.4 | Claude Hooks | 1.0% | PreToolUse/PostToolUse etc. hooks to block destructive actions, exit codes / decisions |
| CC.1 | Claude Code Operation | 3.1% | Rules, Skills, slash commands, subagents, memory; sessions; headless (-p) & auto modes; CLAUDE.md hierarchy; settings.json precedence; permissions |
| ETD.1 | Debugging & Error Handling | 2.6% | HTTP error types (400/401/403/404/413/429/500/529), retries/backoff, trace analysis, integration-layer vs model-output problems |

## Accuracy rules (critical)
1. **Verify every fact** against official sources before you use it. Local reference (fast, current as of Nov 2026):
   `/private/tmp/claude-501/bundled-skills/2.1.321/b5dc1eb8612cbaaae146f93aa7df0067/claude-api/` —
   especially `SKILL.md`, `shared/*.md` (tool-use-concepts, prompt-caching, agent-design, error-codes, models,
   cost-optimization, live-sources), `python/claude-api/*.md`, `typescript/claude-api/*.md`.
   Live docs (WebFetch): platform.claude.com/docs, code.claude.com/docs (Claude Code + Agent SDK),
   modelcontextprotocol.io (MCP spec), anthropic.com/engineering ("Building effective agents", "Writing tools for agents",
   "Effective context engineering").
2. The exam blueprint is from **July 2026**. Prefer **durable concepts** (why caching is a prefix match, why to return
   is_error tool results, when a workflow beats an agent) over version trivia. When a question needs model specifics,
   speak in tiers (Opus = most capable/most expensive, Sonnet = balanced, Haiku = fastest/cheapest) or features that
   are stable. Do NOT write questions whose answer hinges on a Nov-2026-only detail (e.g. one specific model's default
   effort level). Do not invent prices; if a question needs numbers, give them in the scenario.
3. If you are not sure a fact is true, don't use it. A wrong answer key is the worst possible defect.

## Question quality rules (make it feel like the real thing)
- **Scenario first**: 2–5 sentences of realistic context (company, constraint, symptom) then a precise ask
  ("What should the developer do FIRST?", "Which approach BEST meets the requirements?", "What is the MOST likely cause?").
- Test **judgment and application**, not recall of trivia. Mix: ~60% scenario-judgment, ~25% "what happens / which is
  correct" with code or config, ~15% concept checks.
- **Distractors are plausible**: each wrong option is something a competent dev might actually do (over-engineering,
  the outdated way, right idea wrong place, fixes the symptom not cause). No joke options. No "all of the above".
- **Length parity**: the correct option must not be systematically the longest/most detailed. Vary which is longest.
- **Balance answer positions** across A–D (and A–F).
- ~20% of items multi-response: "Select TWO" (5 options) or "Select THREE" (6 options). State it at the end of the stem.
- Code snippets: mix Python and TypeScript (roughly half each where code is used), current SDK shapes
  (`client.messages.create`, `output_config`, `thinking: {type: "adaptive"}`, etc.). Keep snippets ≤ 15 lines.
- Difficulty: 1 = straightforward, 2 = typical exam, 3 = hard (two options look right). Aim ~25% / 50% / 25%.
- Every option gets an explanation (1–3 sentences): why it's right, or the specific reason it's wrong.
- Original content only. Do not copy questions from third-party practice sites.

## Output format
Write ONE JSON file (UTF-8, valid JSON, no comments) at the path given in your task:
```json
{
  "lessons": [
    {
      "subskill": "AI.3",
      "title": "Claude API Mechanics",
      "summary": "2–3 sentence framing of what the exam tests here.",
      "keyPoints": ["8–12 dense, exam-relevant facts. May use `inline code`."],
      "traps": ["4–6 'exam traps': things experienced builders get wrong or where best practice differs from habit."],
      "code": {"lang": "python", "src": "optional illustrative snippet ≤ 15 lines"},
      "docs": [{"title": "Prompt caching", "url": "https://platform.claude.com/docs/..."}],
      "drill": "One 10–15 minute hands-on exercise the learner can do."
    }
  ],
  "questions": [
    {
      "id": "AI3-001",
      "subskill": "AI.3",
      "difficulty": 2,
      "stem": "Scenario text... Which approach BEST ...?",
      "code": {"lang": "typescript", "src": "optional"},
      "select": 1,
      "options": ["option A text", "option B text", "option C text", "option D text"],
      "answer": [2],
      "explanations": ["why A wrong", "why B wrong", "why C right", "why D wrong"],
      "ref": "https://... (official doc URL most relevant)"
    }
  ]
}
```
- `answer` holds 0-based option indexes; `answer.length === select`; `explanations.length === options.length`.
- single-select: exactly 4 options. Select TWO: 5 options. Select THREE: 6 options.
- `id`: sub-skill code without the dot + 3-digit sequence (e.g. `MSO2-014`).
- Lesson `keyPoints`/`traps` are condensed (≈10 min read total). Markdown is limited to `inline code` and **bold**.

When done, run `python3 -c "import json;d=json.load(open(PATH));print(len(d['lessons']),len(d['questions']))"` to confirm the file parses,
and report counts per sub-skill plus any facts you were unsure about and left out.
