"""Merge question sources, validate, balance answer positions, allocate diagnostic + sealed mocks (CCAR-P).
Usage: python3 -I build.py   (run from anywhere; paths are relative to this file)
Sources: pro/retag/*.json (questions carried over from the Foundations and Developer banks) and
pro/new/*.json (lessons + new questions). Writes ../app/bank.json and prints a report.
"""
import json, glob, os, random, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "app", "bank.json")
SOURCES = sorted(glob.glob(os.path.join(HERE, "pro", "retag", "*.json"))) + sorted(glob.glob(os.path.join(HERE, "pro", "new", "*.json")))

MOCK_N = 63
SEALED_MOCKS = 4      # mocks 3-6; mocks 1-2 are drawn from the practice bank at start time
PRACTICE_KEEP = 2     # per objective, never sealed

DOMAINS = [  # code, name, weight %, questions per mock
    ("P1", "Solution Design & Architecture", 17, 11),
    ("P2", "Claude Models, Prompting & Context Engineering", 13, 8),
    ("P3", "Integration", 19, 12),
    ("P4", "Evaluation, Testing & Optimisation", 16, 10),
    ("P5", "Governance, Safety & Risk Management", 14, 9),
    ("P6", "Stakeholder Communication & Lifecycle Management", 14, 9),
    ("P7", "Developer Productivity & Operational Enablement", 7, 4),
]
assert sum(d[3] for d in DOMAINS) == MOCK_N
TASK_NAMES = {
    "P1": ["Translate business problems into Claude solutions", "Design end-to-end architectures",
           "Select architectural patterns", "Design multi-agent systems and orchestration",
           "Apply decomposition techniques", "Align solutions to business value pillars"],
    "P2": ["Select Claude models based on trade-offs", "Design system prompts, templates and guardrails",
           "Apply prompt engineering techniques", "Optimise context windows and token usage",
           "Implement prompt reuse strategies"],
    "P3": ["Evaluate configuration for capability bloat", "Analyse authn/authz for security gaps",
           "Evaluate accuracy-latency trade-offs", "Analyse observability and monitoring at scale",
           "Design a RAG pipeline (chunking, indexing)", "Match retrieval strategy to data and queries",
           "Select the integration mechanism (MCP, API/CLI, A2A)", "Progressive discovery vs monolithic context"],
    "P4": ["Define evaluation metrics", "Design evaluation datasets and test frameworks",
           "Conduct A/B testing and iteration", "Diagnose system issues",
           "Optimise token, latency and cost trade-offs", "Monitor performance with logging and observability"],
    "P5": ["Implement guardrails and safety controls", "Identify risks, limitations and failure modes",
           "Apply human-in-the-loop validation", "Ensure regulatory compliance", "Address ethical AI considerations"],
    "P6": ["Conduct discovery and requirement gathering", "Communicate decisions and trade-offs",
           "Manage feedback loops and expectations (SLAs)", "Document architectures and guidance",
           "Support lifecycle phases"],
    "P7": ["Configure Claude tools for teams", "Improve developer workflows with AI tooling",
           "Support debugging and operational issues"],
}
DW = {c: w for c, _, w, _ in DOMAINS}
TASKS = [(f"{d}.{i+1}", n, round(DW[d] / len(ns), 2)) for d, ns in TASK_NAMES.items() for i, n in enumerate(ns)]
TW = {c: w for c, _, w in TASKS}
# Foundations scenarios: kept only as context for carried-over questions that reference them.
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
SC = {c for c, _, _ in SCENARIOS}

rng = random.Random(20261117)
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
        else: warnings.append(f"{name}: lesson for unknown objective {l.get('subskill')}")
    for q in d.get("questions", []):
        if q.get("retired"): continue
        qid = q.get("id"); p = f"{name}:{qid}"; ok = True
        if q.get("subskill") not in TW: errors.append(f"{p} bad objective code {q.get('subskill')}"); ok = False
        if "scenario" in q and q["scenario"] not in SC: errors.append(f"{p} bad scenario {q.get('scenario')}"); ok = False
        opts, ans, ex, sel = q.get("options", []), q.get("answer", []), q.get("explanations", []), q.get("select", 1)
        if len(opts) != {1: 4, 2: 5, 3: 6}.get(sel, -1): warnings.append(f"{p} select-{sel} with {len(opts)} options")
        if len(ans) != sel or len(set(ans)) != sel: errors.append(f"{p} answer/select mismatch"); ok = False
        if any((not isinstance(a, int)) or a < 0 or a >= len(opts) for a in ans): errors.append(f"{p} answer index out of range"); ok = False
        if len(ex) != len(opts): errors.append(f"{p} explanations != options"); ok = False
        if not q.get("stem"): errors.append(f"{p} empty stem"); ok = False
        if qid in seen_ids: errors.append(f"{p} duplicate id"); ok = False
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

# --- sealed mocks: per domain, take its per-mock count, spread across objectives round-robin
by_t = defaultdict(list)
for q in questions: by_t[q["subskill"]].append(q["id"])
for k in by_t: rng.shuffle(by_t[k])
used = set()
sealed = []
for m in range(SEALED_MOCKS):
    ids = []
    for dcode, _, _, n in DOMAINS:
        tasks = [t for t, _, _ in TASKS if t.startswith(dcode + ".")]
        taken, i, stalls = [], m, 0
        while len(taken) < n and stalls < len(tasks):
            t = tasks[i % len(tasks)]; i += 1
            avail = [x for x in by_t[t] if x not in used]
            if len(avail) > PRACTICE_KEEP:
                taken.append(avail[0]); used.add(avail[0]); stalls = 0
            else:
                stalls += 1
        if len(taken) < n: warnings.append(f"sealed mock {m+3}: {dcode} short by {n-len(taken)}")
        ids += taken
    sealed.append(ids)

qmap = {q["id"]: q for q in questions}
practice = [q["id"] for q in questions if q["id"] not in used]
diag = []
for t, _, _ in TASKS:
    cand = sorted((x for x in by_t[t] if x not in used), key=lambda x: (abs(qmap[x].get("difficulty", 2) - 2), x))
    if cand: diag.append(cand[0])
    else: warnings.append(f"diagnostic: no practice question for {t}")

bank = {
    "version": 3,
    "exam": {"code": "CCAR-P", "name": "Claude Certified Architect – Professional", "items": MOCK_N, "minutes": 120},
    "domains": [{"code": c, "name": n, "weight": w, "perMock": k} for c, n, w, k in DOMAINS],
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

by_d = Counter(q["subskill"].split(".")[0] for q in questions)
print(f"lessons {len(lessons)}/{len(TASKS)}  questions {len(questions)}  practice {len(practice)}  sealed {[len(s) for s in sealed]}  diag {len(diag)}")
print("per domain:", {d: f"{by_d[d]} ({by_d[d]*100//max(1,len(questions))}% vs {w}%)" for d, _, w, _ in DOMAINS})
print("per objective:", {t: len(by_t[t]) for t, _, _ in TASKS})
print("select mix:", Counter(q["select"] for q in questions), " difficulty:", Counter(q.get("difficulty") for q in questions))
print("single answer pos before", dict(pos_before), "after", dict(pos_after), f" correct-is-longest {longest_correct}/{len(singles)}")
missing = [c for c, _, _ in TASKS if c not in lessons]
if missing: print("MISSING LESSONS:", missing)
print(f"size {os.path.getsize(OUT)//1024} KB")
for e in errors: print("ERROR", e)
for w in warnings[:40]: print("WARN", w)
sys.exit(1 if errors else 0)
