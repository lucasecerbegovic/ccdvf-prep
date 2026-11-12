# CCAR-F Study Program — Content Spec

You are writing original exam-prep content for the **Claude Certified Architect – Foundations (CCAR-F)** exam
(Anthropic, exam guide v1.0 effective July 2026).
The learner is an experienced Claude builder (API, Agent SDK, MCP, Claude Code) cramming for 2–3 weeks.
The exam targets **solution architects and tech leads who design production Claude systems** (about 6+ months
hands-on with the Claude API, Agent SDK, Claude Code and MCP). Questions ask for the best *design decision*,
not syntax recall.

## Real exam format (match it)
- **60 scored items, 120 minutes**, multiple choice (1 correct of 4) and multiple response
  ("Select TWO" of 5, "Select THREE" of 6). Each item states how many to pick. No partial credit.
- Items are grouped under **scenarios**: each sitting draws **4 scenarios at random from a bank of 6**,
  about 15 items per scenario.
- Scaled score 100–1000, pass = 720.

## Scenarios (codes are fixed)
Every question belongs to exactly one scenario. The stem must read naturally as part of that scenario
(the company/system described below), adding its own specific situation.

| Code | Scenario | The system |
|---|---|---|
| S1 | Customer Support Resolution Agent | An Agent SDK agent that resolves support tickets end to end: looks up customers/orders via MCP tools, issues refunds within policy, escalates to humans, keeps state across a multi-turn conversation. |
| S2 | Code Generation with Claude Code | A team using Claude Code to build and change features in a real codebase: CLAUDE.md, plan mode, skills/commands, iterative refinement, tests as the feedback loop. |
| S3 | Multi-Agent Research System | A coordinator agent that decomposes research questions and delegates to search/analysis/synthesis subagents, then assembles a cited report. |
| S4 | Developer Productivity with Claude | An internal platform giving engineers Claude-powered tooling: shared team config, MCP servers for internal systems, custom tools, exploring unfamiliar/large codebases. |
| S5 | Claude Code for Continuous Integration | Claude Code running non-interactively in CI/CD (`claude -p`, structured output, PR review, automated fixes), with permissions, hooks and cost controls. |
| S6 | Structured Data Extraction | A pipeline that extracts structured fields from documents (invoices, contracts, forms) with JSON schemas, validation/retry loops, batch processing and human review. |

## Domains & task statements (codes are fixed — use exactly these)
Task-statement weights are the domain weight split evenly (the guide only publishes domain weights).

### D1 Agentic Architecture & Orchestration — 27%
| Code | Task | Topics |
|---|---|---|
| D1.1 | Agentic loops | The tool-use loop (`stop_reason` `tool_use` → execute → `tool_result` → repeat until `end_turn`); loop termination, max turns/budget limits; workflow vs agent decision; when *not* to use an agent |
| D1.2 | Coordinator and subagent patterns | Orchestrator–worker / hub-and-spoke; the coordinator owns decomposition, routing and synthesis; subagents don't talk to each other directly; parallel vs sequential subagents; evaluator–optimizer |
| D1.3 | Subagent invocation and context passing | Subagents start with **fresh, isolated context** — pass everything they need explicitly in the task prompt; return condensed results, not full transcripts; Agent SDK `agents` definitions (description, prompt, tools); restricting subagent tools |
| D1.4 | Workflow enforcement and handoff | Enforcing required steps/order deterministically (code, hooks, tool gating) instead of hoping the prompt is followed; prerequisites (verify identity before refund); structured handoff summaries to humans or other agents |
| D1.5 | Agent SDK hooks | PreToolUse / PostToolUse / Stop / SessionStart etc.; blocking or modifying tool calls, normalising tool output, enforcing policy (e.g. refund limits) in code; hooks are deterministic, prompts are probabilistic |
| D1.6 | Task decomposition | Fixed prompt chains vs dynamic decomposition; splitting by independent sub-questions; per-file then cross-file passes; avoiding over-narrow decomposition that misses coverage |
| D1.7 | Session state, resumption and forking | Resuming a session (`resume`/`--resume`/`--continue`), forking to explore alternatives, when to start fresh with a summary instead of resuming stale context; persisting state outside the context window |

### D2 Tool Design & MCP Integration — 18%
| Code | Task | Topics |
|---|---|---|
| D2.1 | Tool interface design | Tool descriptions as the main selection signal; clear names, input formats, examples, boundaries between similar tools; consolidating vs splitting tools; returning only high-signal fields |
| D2.2 | Structured errors for MCP tools | `isError` / `is_error` results; distinguishing transient vs validation vs business-rule vs permission errors; retryable flags and actionable messages so the agent can recover; never return an empty success on failure |
| D2.3 | Tool distribution and tool choice | Too many tools degrades selection — give each agent/subagent a scoped tool set; `tool_choice` `auto` / `none`; guaranteed structured output via structured outputs (`output_config.format`) or `strict` tools — forced `tool_choice` (`any` / `tool`) is rejected with a 400 on current models, so never key an answer on it |
| D2.4 | MCP server integration | Configuring servers in `.mcp.json` (project, shared via git) vs user scope; env-var expansion for secrets; stdio vs Streamable HTTP; tools vs resources vs prompts; choosing an existing server vs building one |
| D2.5 | Built-in tools | Claude Code / Agent SDK built-ins: Read, Write, Edit, Bash, Grep, Glob, WebSearch/WebFetch, Task/Agent; picking Grep for content search vs Glob for paths; Edit's unique-match requirement and Read+Write fallback |

### D3 Claude Code Configuration & Workflows — 20%
| Code | Task | Topics |
|---|---|---|
| D3.1 | CLAUDE.md hierarchy | User (`~/.claude/CLAUDE.md`), project (`./CLAUDE.md` or `.claude/CLAUDE.md`, committed), local/personal, and subdirectory CLAUDE.md files loaded on demand; `@import`; what belongs where; diagnosing "teammate doesn't get the instruction" (it's in user scope) |
| D3.2 | Slash commands and skills | Project commands/skills in `.claude/` (shared) vs `~/.claude/` (personal); skills with `SKILL.md` frontmatter (description drives auto-invocation), `allowed-tools`, `context: fork`; when to use a skill vs CLAUDE.md vs a command |
| D3.3 | Path-specific rules | `.claude/rules/*.md` with `paths:` glob frontmatter so conventions load only for matching files (e.g. `**/*.test.ts`); vs subdirectory CLAUDE.md |
| D3.4 | Plan mode vs direct execution | Plan mode for large, ambiguous or multi-file/architectural changes; direct execution for small well-scoped fixes; Explore subagent to keep discovery out of main context |
| D3.5 | Iterative refinement | Concrete input/output examples, test-driven iteration (write tests, let Claude iterate to green), interview-style clarification, giving all interacting issues in one message vs sequentially |
| D3.6 | Claude Code in CI/CD | `claude -p` (non-interactive) with `--output-format json` / `--json-schema`; permission settings / `--allowedTools` for unattended runs; CLAUDE.md as CI context; a separate session to review generated code; avoiding re-reviewing unchanged code |

### D4 Prompt Engineering & Structured Output — 20%
| Code | Task | Topics |
|---|---|---|
| D4.1 | Prompts with explicit criteria | Explicit, concrete criteria instead of vague instructions ("be conservative"); defining what to flag and what to skip to cut false positives; severity definitions with examples |
| D4.2 | Few-shot prompting | Few-shot examples for ambiguous cases, output format consistency, and handling of edge cases; diverse examples showing reasoning; when few-shot beats more instructions |
| D4.3 | Structured output with JSON schemas | Tool use with `input_schema` or structured outputs to guarantee syntactically valid JSON; schema design: required vs optional/nullable fields, enums with "other"+detail, avoiding forced fabrication; syntax vs semantic correctness |
| D4.4 | Validation and retry loops | Validate semantics in code; retry with the specific validation error fed back; know when retry can't help (information absent from source); self-correction fields (e.g. stated vs computed totals) |
| D4.5 | Message Batches API | 50% cost, up to 24 h processing, no latency SLA; good for overnight/bulk non-blocking work, bad for blocking/interactive paths; `custom_id` correlation; resubmitting only failed items; no multi-turn tool loops inside one request |
| D4.6 | Multi-pass review | Independent review instance (not the generator self-reviewing in the same context); per-file local passes + cross-file integration pass; attention dilution in one giant pass |

### D5 Context Management & Reliability — 15%
| Code | Task | Topics |
|---|---|---|
| D5.1 | Context across long conversations | Persistent "case facts" block outside summarised history; progressive summarisation loses numbers/dates; trimming verbose tool output to relevant fields; lost-in-the-middle and placing key info at start/end |
| D5.2 | Escalation and ambiguity | Escalate on explicit customer request, policy gaps, or inability to progress — not on sentiment or self-reported confidence; ask for clarification when multiple matches; honour explicit human-agent requests immediately |
| D5.3 | Error propagation | Subagents return structured error context (what failed, partial results, alternatives) to the coordinator; distinguish "access failed" from "no results found"; don't silently swallow errors or abort the whole workflow |
| D5.4 | Large codebase context | Explore with Grep/Glob then targeted Read; scratchpad/notes files across context boundaries; subagents for isolated exploration; `/compact`; summarising findings before a new phase |
| D5.5 | Human review and confidence | Field-level confidence calibrated against labelled data; stratified sampling of high-confidence outputs; aggregate accuracy hides per-document-type failures; routing low-confidence items to humans |
| D5.6 | Information provenance | Preserve claim → source mappings through synthesis; carry dates/publication info so conflicts can be explained; annotate conflicting sources rather than picking one silently |

## Accuracy rules (critical)
1. **Verify every fact** against official sources before you use it. Local reference:
   `/private/tmp/claude-501/bundled-skills/2.1.321/b5dc1eb8612cbaaae146f93aa7df0067/claude-api/`
   (`SKILL.md`, `shared/*.md`, `python/`, `typescript/`). Live docs (WebFetch):
   code.claude.com/docs (Claude Code: memory, skills, slash commands, hooks, settings, headless/CLI reference,
   subagents, MCP; Agent SDK), platform.claude.com/docs (Messages API, tool use, structured outputs, batches,
   prompt engineering), modelcontextprotocol.io, anthropic.com/engineering ("Building effective agents",
   "Writing tools for agents", "Effective context engineering", "How we built our multi-agent research system").
2. Prefer **durable architectural concepts** over version trivia. Speak in model tiers (Opus / Sonnet / Haiku).
   Do not invent prices or limits; put numbers in the scenario if the question needs them.
3. If you are not sure a fact is true, don't use it. A wrong answer key is the worst possible defect.

## Question quality rules
- **Scenario first**: the stem opens inside the scenario's system (2–5 sentences: the specific situation,
  constraint, symptom), then a precise ask ("What should the architect do FIRST?", "Which change BEST…?",
  "What is the MOST likely cause?").
- Test **design judgment**: ~70% scenario-judgment, ~20% "what happens / which is correct" with config or code,
  ~10% concept checks.
- **Distractors are plausible**: over-engineering, prompt-only fixes where a deterministic control is needed,
  right idea wrong layer, fixes the symptom not the cause, bigger model / bigger context as a cure-all.
  No joke options, no "all of the above".
- **Length parity**: the correct option must not be systematically the longest. Vary which is longest.
- ~20% multi-response ("Select TWO" with 5 options, "Select THREE" with 6). State it at the end of the stem.
- Code/config snippets ≤ 15 lines: CLAUDE.md, `.claude/settings.json`, `.mcp.json`, SKILL.md frontmatter,
  hook scripts, CLI invocations, Python/TypeScript SDK calls.
- Difficulty: 1 = straightforward, 2 = typical exam, 3 = hard (two options look right). Aim ~20% / 50% / 30%.
- Every option gets an explanation (1–3 sentences).
- Original content only.

## Output format
```json
{
  "lessons": [
    {
      "subskill": "D1.3",
      "title": "Subagent invocation and context passing",
      "summary": "2–3 sentences: what the exam tests here.",
      "keyPoints": ["6–10 dense, exam-relevant facts. May use `inline code` and **bold**."],
      "traps": ["3–5 exam traps."],
      "code": {"lang": "json", "src": "optional snippet ≤ 15 lines"},
      "docs": [{"title": "Subagents", "url": "https://code.claude.com/docs/..."}],
      "drill": "One 10–15 minute hands-on exercise."
    }
  ],
  "questions": [
    {
      "id": "D1-3-001",
      "subskill": "D1.3",
      "scenario": "S3",
      "difficulty": 2,
      "stem": "...",
      "code": {"lang": "json", "src": "optional"},
      "select": 1,
      "options": ["A", "B", "C", "D"],
      "answer": [2],
      "explanations": ["why A wrong", "why B wrong", "why C right", "why D wrong"],
      "ref": "https://... (official doc URL most relevant)"
    }
  ]
}
```
- The field is still called `subskill`; it holds the task-statement code.
- `answer` holds 0-based indexes; `answer.length === select`; `explanations.length === options.length`.
- Single-select: exactly 4 options. Select TWO: 5. Select THREE: 6.
- `id`: unique; new questions use `D<domain>-<task>-<3-digit seq>`; retained questions keep their old id.
