# CCAR-P Study Program — Content Spec

You are writing original exam-prep content for the **Claude Certified Architect – Professional (CCAR-P)** exam
(Anthropic, exam guide v1.0, July 2026). The learner is an experienced Claude builder.
Target candidates are mid-to-senior solution architects, AI/ML engineers and tech leads (3+ years architecture or
platform engineering, 6+ months running Claude or a comparable LLM in production, end-to-end delivery), often in
regulated sectors. Questions ask for the best **architectural, operational or stakeholder decision**, and reward
fixing the root cause over adding a compensating control.

## Real exam format (match it)
- **63 scored items, 120 minutes**, multiple choice (1 of 4) and multiple response ("Select TWO" of 5,
  "Select THREE" of 6). Each item states how many to pick. No partial credit.
- **Standalone items** — no shared scenario bank. Each stem carries its own context.
- Scaled score 100–1000, pass = 720. Score report shows percent correct per domain.

## Domains & objectives (codes are fixed — use exactly these)
Objective weights are the domain weight split evenly (the guide only publishes domain weights).

### P1 Solution Design & Architecture — 17%
| Code | Objective |
|---|---|
| P1.1 | Translate business problems into Claude-based AI solutions |
| P1.2 | Design end-to-end architectures (input → processing → output → feedback loops) |
| P1.3 | Select appropriate architectural patterns (workflow, agentic, augmented LLM) |
| P1.4 | Design multi-agent systems and orchestration strategies |
| P1.5 | Apply decomposition techniques for complex problem solving |
| P1.6 | Align solutions to business value pillars (efficiency, transformation, productivity, cost, performance SLAs) |

### P2 Claude Models, Prompting & Context Engineering — 13%
| Code | Objective |
|---|---|
| P2.1 | Select appropriate Claude models based on trade-offs |
| P2.2 | Design system prompts, templates, and guardrails |
| P2.3 | Apply prompt engineering techniques (zero-shot, few-shot, chain-of-thought) |
| P2.4 | Optimise context windows and manage token usage |
| P2.5 | Implement prompt reuse strategies (caching, modular prompts, Skills) |

### P3 Integration — 19%
| Code | Objective |
|---|---|
| P3.1 | Evaluate tool/agent configuration for capability bloat |
| P3.2 | Analyse authentication and authorisation requirements to identify security gaps |
| P3.3 | Evaluate accuracy-latency trade-offs and justify configuration decisions |
| P3.4 | Analyse observability challenges and select monitoring strategies at scale |
| P3.5 | Design a RAG pipeline with appropriate chunking and indexing strategies |
| P3.6 | Apply retrieval strategies matched to data shape and query pattern |
| P3.7 | Evaluate connection protocols and select the integration mechanism (MCP, API/CLI, agent-to-agent) |
| P3.8 | Evaluate progressive discovery vs. monolithic context strategy |

### P4 Evaluation, Testing & Optimisation — 16%
| Code | Objective |
|---|---|
| P4.1 | Define evaluation metrics (accuracy, latency, cost, safety, security) |
| P4.2 | Design evaluation datasets and test frameworks using mixed methodologies |
| P4.3 | Conduct A/B testing and iterative improvements |
| P4.4 | Diagnose system issues (prompt failure, hallucinations, model mismatch) |
| P4.5 | Optimise token usage, latency, and cost-performance trade-offs |
| P4.6 | Monitor system performance using logging and observability tools |

### P5 Governance, Safety & Risk Management — 14%
| Code | Objective |
|---|---|
| P5.1 | Implement guardrails and safety controls |
| P5.2 | Identify risks, limitations, and failure modes of LLM systems |
| P5.3 | Apply human-in-the-loop validation strategies |
| P5.4 | Ensure compliance with regulations (e.g., GDPR, HIPAA, FedRAMP) |
| P5.5 | Address ethical AI considerations (bias, fairness, transparency) |

### P6 Stakeholder Communication & Lifecycle Management — 14%
| Code | Objective |
|---|---|
| P6.1 | Conduct structured discovery and requirement gathering |
| P6.2 | Communicate architectural decisions and trade-offs |
| P6.3 | Manage stakeholder feedback loops and expectation alignment (including SLAs) |
| P6.4 | Document architectures and provide implementation guidance |
| P6.5 | Support lifecycle phases (discovery, design, handoff, monitoring, iteration) |

### P7 Developer Productivity & Operational Enablement — 7%
| Code | Objective |
|---|---|
| P7.1 | Configure Claude tools and environments for teams (e.g., Claude Code) |
| P7.2 | Improve developer workflows using AI-assisted tooling |
| P7.3 | Support debugging and operational issue resolution |

## Accuracy rules (critical)
1. **Verify every fact** against official sources before you use it. Local reference:
   `/private/tmp/claude-501/bundled-skills/2.1.321/b5dc1eb8612cbaaae146f93aa7df0067/claude-api/`
   (`SKILL.md`, `shared/*.md`). Live docs (WebFetch): platform.claude.com/docs (models, prompting, caching,
   tool use, structured outputs, batches, citations, embeddings, evals/"define success criteria", "reduce
   hallucinations", data retention/ZDR, Bedrock/Vertex), code.claude.com/docs, modelcontextprotocol.io
   (incl. authorization), anthropic.com/engineering ("Building effective agents", "Contextual retrieval",
   "Effective context engineering", "Writing tools for agents", multi-agent research system),
   trust.anthropic.com / privacy pages for compliance claims.
2. Prefer **durable concepts** over version trivia. Speak in model tiers (Opus / Sonnet / Haiku). Do not invent
   prices, limits or certifications; put numbers in the stem if the question needs them. Never claim Anthropic
   holds a specific compliance certification or offers a specific contract (BAA, FedRAMP level) unless the
   official page says so — frame compliance questions around the architect's controls (data minimisation,
   residency, retention, access, audit, DPIA, human review), not vendor paperwork trivia.
3. Forced `tool_choice` (`any`/`tool`) returns 400 on current models — never key an answer on it.
4. If you are not sure a fact is true, don't use it. A wrong answer key is the worst possible defect.

## Question quality rules
- **Context first**: 2–5 sentences of realistic, self-contained context (organisation, constraint, symptom),
  then a precise ask ("What should the architect do FIRST?", "Which approach BEST…?", "What is the MOST
  likely cause?"). Vary industries (finance, healthcare, retail, public sector, SaaS, education).
- Test **judgment**: ~70% scenario-judgment, ~20% "which is correct" with config/code/metrics, ~10% concept.
- **Distractors are plausible**: compensating controls instead of root-cause fixes, over-engineering,
  prompt-only fixes where a deterministic control is needed, bigger model / bigger context as a cure-all,
  technically right but ignores the stakeholder/business constraint. No joke options, no "all of the above".
- **Length parity**: the correct option must not be systematically the longest.
- ~20% multi-response ("Select TWO" with 5 options, "Select THREE" with 6). State it at the end of the stem.
- Difficulty: 1 / 2 / 3 ≈ 20% / 50% / 30%. Every option gets an explanation (1–3 sentences). Original content only.

## Output format
```json
{
  "lessons": [
    {
      "subskill": "P3.5",
      "title": "Design a RAG pipeline",
      "summary": "2–3 sentences: what the exam tests here.",
      "keyPoints": ["6–10 dense, exam-relevant facts. May use `inline code` and **bold**."],
      "traps": ["3–5 exam traps."],
      "code": {"lang": "python", "src": "optional snippet ≤ 15 lines"},
      "docs": [{"title": "Contextual retrieval", "url": "https://www.anthropic.com/engineering/contextual-retrieval"}],
      "drill": "One 10–15 minute hands-on exercise."
    }
  ],
  "questions": [
    {
      "id": "P3-5-001",
      "subskill": "P3.5",
      "difficulty": 2,
      "stem": "...",
      "select": 1,
      "options": ["A", "B", "C", "D"],
      "answer": [2],
      "explanations": ["why A wrong", "why B wrong", "why C right", "why D wrong"],
      "ref": "https://... (official doc URL)"
    }
  ]
}
```
- `subskill` holds the objective code. `scenario` (S1–S6) is optional and only kept on questions carried over from
  the Foundations bank; the app then shows that scenario's description as context. New questions omit it.
- `answer` holds 0-based indexes; `answer.length === select`; `explanations.length === options.length`.
- Single-select: exactly 4 options. Select TWO: 5. Select THREE: 6.
- `id`: unique; new questions use `P<domain>-<objective>-<3-digit seq>`; carried-over questions keep their id.
- Add `"retired": true` to drop a question from the build without deleting it.
