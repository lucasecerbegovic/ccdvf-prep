"""Merge question sources, validate, balance answer positions, allocate diagnostic + sealed scenario mocks.
Usage: python3 -I build.py   (run from anywhere; paths are relative to this file)
Sources: retag/part*.json (questions kept from the old Developer bank) and new/*.json (lessons + new questions).
Writes ../app/bank.json and prints a report.
"""
import json, glob, os, random, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "app", "bank.json")
SOURCES = sorted(glob.glob(os.path.join(HERE, "retag", "part*.json"))) + sorted(glob.glob(os.path.join(HERE, "new", "*.json")))

MOCK_N, PER_SCENARIO, SCENARIOS_PER_MOCK = 60, 15, 4
SEALED_MOCKS = 4  # mocks 3-6; mocks 1-2 are drawn from the practice bank at start time
PRACTICE_RESERVE = 12  # per scenario, never sealed

DOMAINS = [
    ("D1", "Agentic Architecture & Orchestration", 27),
    ("D2", "Tool Design & MCP Integration", 18),
    ("D3", "Claude Code Configuration & Workflows", 20),
    ("D4", "Prompt Engineering & Structured Output", 20),
    ("D5", "Context Management & Reliability", 15),
]
TASK_NAMES = {
    "D1": ["Agentic loops", "Coordinator and subagent patterns", "Subagent invocation and context passing",
           "Workflow enforcement and handoff", "Agent SDK hooks", "Task decomposition",
           "Session state, resumption and forking"],
    "D2": ["Tool interface design", "Structured errors for MCP tools", "Tool distribution and tool choice",
           "MCP server integration", "Built-in tools"],
    "D3": ["CLAUDE.md hierarchy", "Slash commands and skills", "Path-specific rules", "Plan mode vs direct execution",
           "Iterative refinement", "Claude Code in CI/CD"],
    "D4": ["Prompts with explicit criteria", "Few-shot prompting", "Structured output with JSON schemas",
           "Validation and retry loops", "Message Batches API", "Multi-pass review"],
    "D5": ["Context across long conversations", "Escalation and ambiguity", "Error propagation",
           "Large codebase context", "Human review and confidence", "Information provenance"],
}
DW = {c: w for c, _, w in DOMAINS}
TASKS = [(f"{d}.{i+1}", n, round(DW[d] / len(ns), 2)) for d, ns in TASK_NAMES.items() for i, n in enumerate(ns)]
TW = {c: w for c, _, w in TASKS}
SCENARIOS = [
    ("S1", "Customer Support Resolution Agent",
     "An Agent SDK agent resolves support tickets end to end. It looks up customers and orders through MCP tools, "
     "issues refunds within policy, escalates to human agents, and keeps state across long multi-turn conversations."),
    ("S2", "Code Generation with Claude Code",
     "A product team uses Claude Code to build and change features in a large production codebase, relying on "
     "CLAUDE.md, plan mode, custom skills and commands, and tests as the feedback loop."),
    ("S3", "Multi-Agent Research System",
     "A coordinator agent breaks research questions into parts, delegates them to search, analysis and synthesis "
     "subagents, and assembles a cited report."),
    ("S4", "Developer Productivity with Claude",
     "A platform team gives engineers Claude-powered tooling: shared team configuration, MCP servers for internal "
     "systems, custom tools, and help exploring large, unfamiliar codebases."),
    ("S5", "Claude Code for Continuous Integration",
     "Claude Code runs non-interactively in the CI/CD pipeline to review pull requests, generate tests and propose "
     "fixes, under tight permission, reliability and cost constraints."),
    ("S6", "Structured Data Extraction",
     "A pipeline extracts structured fields from invoices, contracts and forms using JSON schemas, validation and "
     "retry loops, batch processing, and human review of uncertain results."),
]
SC = [c for c, _, _ in SCENARIOS]

rng = random.Random(20261112)
errors, warnings = [], []
lessons, questions = {}, []
seen_ids = set()

for path in SOURCES:
    name = os.path.relpath(path, HERE)
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        errors.append(f"{name}: unparseable ({e})"); continue
    for l in d.get("lessons", []):
        if l.get("subskill") in TW: lessons[l["subskill"]] = l
        else: warnings.append(f"{name}: lesson for unknown task {l.get('subskill')}")
    for q in d.get("questions", []):
        qid = q.get("id"); p = f"{name}:{qid}"; ok = True
        if q.get("subskill") not in TW: errors.append(f"{p} bad task code {q.get('subskill')}"); ok = False
        if q.get("scenario") not in SC: errors.append(f"{p} bad scenario {q.get('scenario')}"); ok = False
        opts, ans, ex, sel = q.get("options", []), q.get("answer", []), q.get("explanations", []), q.get("select", 1)
        if len(opts) != {1: 4, 2: 5, 3: 6}.get(sel, -1): warnings.append(f"{p} select-{sel} with {len(opts)} options")
        if len(ans) != sel or len(set(ans)) != sel: errors.append(f"{p} answer/select mismatch"); ok = False
        if any((not isinstance(a, int)) or a < 0 or a >= len(opts) for a in ans): errors.append(f"{p} answer index out of range"); ok = False
        if len(ex) != len(opts): errors.append(f"{p} explanations != options"); ok = False
        if not q.get("stem"): errors.append(f"{p} empty stem"); ok = False
        if qid in seen_ids: qid = qid + "b"; q["id"] = qid; warnings.append(f"{p} duplicate id renamed")
        if ok: seen_ids.add(qid); questions.append(q)

# --- balance answer positions (single-select only; skip items whose text references option letters)
letter_ref = re.compile(r"\b(option|answer|choice)\s+[A-F]\b|\([A-F]\)", re.I)
pos_before = Counter(q["answer"][0] for q in questions if q["select"] == 1)
singles = [q for q in questions if q["select"] == 1]
rng.shuffle(singles)
target = 0
for q in singles:
    if letter_ref.search(q["stem"] + " ".join(q["options"]) + " ".join(q["explanations"])): continue
    want = target % 4; target += 1
    cur = q["answer"][0]
    if cur == want: continue
    for arr in (q["options"], q["explanations"]):
        arr[cur], arr[want] = arr[want], arr[cur]
    q["answer"] = [want]
pos_after = Counter(q["answer"][0] for q in questions if q["select"] == 1)
longest_correct = sum(1 for q in singles if max(range(4), key=lambda i: len(q["options"][i])) == q["answer"][0])

# --- sealed mocks: 4 scenarios x 15 questions, scenario usage spread evenly, domains pulled toward exam weights
qmap = {q["id"]: q for q in questions}
dom = lambda qid: qmap[qid]["subskill"].split(".")[0]
by_sc = defaultdict(list)
for q in questions: by_sc[q["scenario"]].append(q["id"])
for k in by_sc: rng.shuffle(by_sc[k])
used = set()

def pick_block(scn, k, counts, total):
    """Pick k unused questions from scenario scn, each time taking the domain furthest below its weight share."""
    avail = [x for x in by_sc[scn] if x not in used]
    spare = len(avail) - PRACTICE_RESERVE
    out = []
    while len(out) < min(k, max(0, spare)):
        n = total + len(out) + 1
        deficit = lambda x: DW[dom(x)] / 100 * n - counts[dom(x)]
        best = max((x for x in avail if x not in out), key=deficit)
        out.append(best); counts[dom(best)] += 1
    return out

usage = Counter()
sealed = []
for m in range(SEALED_MOCKS):
    # least-used scenarios first, ties broken by how many unused questions remain
    order = sorted(SC, key=lambda s: (usage[s], -len([x for x in by_sc[s] if x not in used]), rng.random()))
    chosen = order[:SCENARIOS_PER_MOCK]
    counts, ids, blocks = Counter(), [], []
    for s in chosen:
        block = pick_block(s, PER_SCENARIO, counts, len(ids))
        if len(block) < PER_SCENARIO: warnings.append(f"sealed mock {m+3}: scenario {s} short by {PER_SCENARIO-len(block)}")
        used.update(block); ids += block; usage[s] += 1
        blocks.append({"scenario": s, "ids": block})
    sealed.append(blocks)

practice = [q["id"] for q in questions if q["id"] not in used]
diag = []
for t, _, _ in TASKS:
    cand = [q["id"] for q in questions if q["subskill"] == t and q["id"] not in used]
    cand.sort(key=lambda x: (abs(qmap[x].get("difficulty", 2) - 2), x))
    if cand: diag.append(cand[0])
    else: warnings.append(f"diagnostic: no practice question for {t}")

bank = {
    "version": 2,
    "exam": {"code": "CCAR-F", "name": "Claude Certified Architect – Foundations", "items": MOCK_N, "minutes": 120,
             "scenariosPerExam": SCENARIOS_PER_MOCK, "perScenario": PER_SCENARIO},
    "domains": [{"code": c, "name": n, "weight": w} for c, n, w in DOMAINS],
    "subskills": [{"code": c, "name": n, "weight": w, "domain": c.split(".")[0]} for c, n, w in TASKS],
    "scenarios": [{"code": c, "name": n, "desc": d} for c, n, d in SCENARIOS],
    "lessons": [lessons[c] for c, _, _ in TASKS if c in lessons],
    "questions": questions,
    "diagnostic": diag,
    "sealedMocks": sealed,
    "practicePool": practice,
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(bank, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

by_t = Counter(q["subskill"] for q in questions)
by_d = Counter(q["subskill"].split(".")[0] for q in questions)
print(f"lessons {len(lessons)}/{len(TASKS)}  questions {len(questions)}  practice {len(practice)}  diag {len(diag)}")
print("per domain:", {d: f"{by_d[d]} ({by_d[d]*100//max(1,len(questions))}% vs {w}%)" for d, _, w in DOMAINS})
print("per task:", {t: by_t[t] for t, _, _ in TASKS})
print("per scenario:", {s: len(by_sc[s]) for s in SC})
for i, blocks in enumerate(sealed):
    ids = [x for b in blocks for x in b["ids"]]
    dc = Counter(dom(x) for x in ids)
    print(f"mock {i+3}: {[b['scenario'] for b in blocks]} n={len(ids)} domains={dict(sorted(dc.items()))}")
print("select mix:", Counter(q["select"] for q in questions), " difficulty:", Counter(q.get("difficulty") for q in questions))
print("single answer pos before", dict(pos_before), "after", dict(pos_after), f" correct-is-longest {longest_correct}/{len(singles)}")
missing = [c for c, _, _ in TASKS if c not in lessons]
if missing: print("MISSING LESSONS:", missing)
print(f"size {os.path.getsize(OUT)//1024} KB")
for e in errors: print("ERROR", e)
for w in warnings[:40]: print("WARN", w)
sys.exit(1 if errors else 0)
