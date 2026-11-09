"""Merge agent output, validate, balance answer positions, allocate diagnostic + sealed mocks.
Usage: python3 -I build.py   (run from anywhere; paths are relative to this file)
Writes ../app/bank.json and prints a report.
"""
import json, glob, os, random, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "app", "bank.json")

DOMAINS = [
    ("AI", "Applications & Integration", 33.1, 18),
    ("MSO", "Model Selection & Optimization", 16.8, 9),
    ("AW", "Agents & Workflows", 14.7, 8),
    ("PCE", "Prompt & Context Engineering", 11.0, 6),
    ("TM", "Tools & MCPs", 10.6, 6),
    ("SS", "Security & Safety", 8.1, 4),
    ("CC", "Claude Code", 3.1, 1),
    ("ETD", "Eval, Testing & Debugging", 2.6, 1),
]
SUBSKILLS = [
    ("AI.1", "Claude Application Design", 8.6), ("AI.2", "Software Engineering Foundations", 7.4),
    ("AI.3", "Claude API Mechanics", 6.8), ("AI.4", "Configuration Management", 4.1),
    ("AI.5", "Understanding Requirements", 3.4), ("AI.6", "Systems Life Cycle", 2.8),
    ("MSO.1", "Technical Fundamentals", 6.1), ("MSO.2", "LLM Fundamentals", 5.2),
    ("MSO.3", "Cost & Token Management", 2.8), ("MSO.4", "Model Selection & Trade-offs", 2.7),
    ("AW.1", "Agent Construction with Claude", 5.3), ("AW.2", "Agent Patterns & Frameworks", 4.9),
    ("AW.3", "Agent Architecture", 4.5),
    ("PCE.1", "Prompt Engineering", 4.6), ("PCE.2", "Context Engineering", 3.8), ("PCE.3", "Output Handling", 2.6),
    ("TM.1", "Tool Implementation", 4.4), ("TM.2", "Agentic Customization", 4.1), ("TM.3", "MCP Server Development", 2.1),
    ("SS.1", "AI Application Security", 3.2), ("SS.2", "Guardrails & Safe Deployment", 2.3),
    ("SS.3", "Identity, Secrets & Key Management", 1.6), ("SS.4", "Claude Hooks", 1.0),
    ("CC.1", "Claude Code Operation", 3.1),
    ("ETD.1", "Debugging & Error Handling", 2.6),
]
SS_W = {c: w for c, _, w in SUBSKILLS}
SEALED_MOCKS = 4  # mocks 3-6; mocks 1-2 are drawn from the practice bank at start time

rng = random.Random(20261109)
errors, warnings = [], []
lessons, questions = {}, []
seen_ids = set()

for path in sorted(glob.glob(os.path.join(HERE, "part*.json"))):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        errors.append(f"{os.path.basename(path)}: unparseable ({e})"); continue
    for l in d.get("lessons", []):
        lessons[l["subskill"]] = l
    for q in d.get("questions", []):
        qid = q.get("id")
        p = f"{os.path.basename(path)}:{qid}"
        ok = True
        if q.get("subskill") not in SS_W: errors.append(f"{p} bad subskill {q.get('subskill')}"); ok = False
        opts, ans, ex, sel = q.get("options", []), q.get("answer", []), q.get("explanations", []), q.get("select", 1)
        if sel == 1 and len(opts) != 4: warnings.append(f"{p} single-select with {len(opts)} options")
        if sel == 2 and len(opts) != 5: warnings.append(f"{p} select-2 with {len(opts)} options")
        if sel == 3 and len(opts) != 6: warnings.append(f"{p} select-3 with {len(opts)} options")
        if len(ans) != sel or len(set(ans)) != sel: errors.append(f"{p} answer/select mismatch"); ok = False
        if any((not isinstance(a, int)) or a < 0 or a >= len(opts) for a in ans): errors.append(f"{p} answer index out of range"); ok = False
        if len(ex) != len(opts): errors.append(f"{p} explanations != options"); ok = False
        if not q.get("stem"): errors.append(f"{p} empty stem"); ok = False
        if qid in seen_ids: qid = qid + "b"; q["id"] = qid; warnings.append(f"{p} duplicate id renamed")
        if ok:
            seen_ids.add(qid); questions.append(q)

# --- balance answer positions (single-select only; skip items whose text references option letters)
letter_ref = re.compile(r"\b(option|answer|choice)\s+[A-F]\b|\([A-F]\)", re.I)
pos_before = Counter(q["answer"][0] for q in questions if q["select"] == 1)
singles = [q for q in questions if q["select"] == 1]
rng.shuffle(singles)
target = 0
for q in singles:
    blob = q["stem"] + " ".join(q["options"]) + " ".join(q["explanations"])
    if letter_ref.search(blob): continue
    want = target % 4; target += 1
    cur = q["answer"][0]
    if cur == want: continue
    for arr in (q["options"], q["explanations"]):
        arr[cur], arr[want] = arr[want], arr[cur]
    q["answer"] = [want]
pos_after = Counter(q["answer"][0] for q in questions if q["select"] == 1)
longest_correct = sum(1 for q in questions if q["select"] == 1 and max(range(4), key=lambda i: len(q["options"][i])) == q["answer"][0])

# --- allocation
by_ss = defaultdict(list)
for q in questions: by_ss[q["subskill"]].append(q["id"])
for k in by_ss: rng.shuffle(by_ss[k])
qmap = {q["id"]: q for q in questions}

def split_domain(dcode, n, offset):
    subs = [c for c, _, _ in SUBSKILLS if c.split(".")[0] == dcode]
    tot = sum(SS_W[s] for s in subs)
    raw = [(s, n * SS_W[s] / tot) for s in subs]
    base = {s: int(x) for s, x in raw}
    rem = n - sum(base.values())
    order = sorted(raw, key=lambda t: -(t[1] - int(t[1])))
    for i in range(rem): base[order[(i + offset) % len(order)][0]] += 1
    return base

# diagnostic: one per subskill, taken from the practice side (allocated after sealed mocks)
sealed = []
used = set()
for m in range(SEALED_MOCKS):
    ids = []
    for dcode, _, _, n in DOMAINS:
        alloc = split_domain(dcode, n, m)
        for s, k in alloc.items():
            avail = [x for x in by_ss[s] if x not in used]
            # keep >= 2 per subskill for the practice side
            take = avail[: max(0, min(k, len(avail) - 2))]
            ids += take; used.update(take)
            short = k - len(take)
            if short:
                sibs = [c for c, _, _ in SUBSKILLS if c.split(".")[0] == dcode and c != s]
                for sib in sorted(sibs, key=lambda c: -len([x for x in by_ss[c] if x not in used])):
                    av2 = [x for x in by_ss[sib] if x not in used]
                    extra = av2[: max(0, min(short, len(av2) - 2))]
                    ids += extra; used.update(extra); short -= len(extra)
                    if not short: break
                if short: warnings.append(f"sealed mock {m+3}: short {short} in {dcode}")
    sealed.append(ids)

practice = [q["id"] for q in questions if q["id"] not in used]
diag = []
for s, _, _ in SUBSKILLS:
    cand = [x for x in by_ss[s] if x not in used]
    cand.sort(key=lambda x: abs(qmap[x].get("difficulty", 2) - 2))
    if cand: diag.append(cand[0])
    else: warnings.append(f"diagnostic: no question for {s}")

bank = {
    "version": 1,
    "domains": [{"code": c, "name": n, "weight": w, "perMock": k} for c, n, w, k in DOMAINS],
    "subskills": [{"code": c, "name": n, "weight": w, "domain": c.split(".")[0]} for c, n, w in SUBSKILLS],
    "lessons": [lessons[c] for c, _, _ in SUBSKILLS if c in lessons],
    "questions": questions,
    "diagnostic": diag,
    "sealedMocks": sealed,
    "practicePool": practice,
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(bank, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

print(f"lessons {len(lessons)}/25  questions {len(questions)}  practice {len(practice)}  sealed {[len(m) for m in sealed]}  diag {len(diag)}")
print("per subskill:", {s: len(by_ss[s]) for s, _, _ in SUBSKILLS})
print("select mix:", Counter(q["select"] for q in questions), " difficulty:", Counter(q.get("difficulty") for q in questions))
print("single answer pos before", dict(pos_before), "after", dict(pos_after), f" correct-is-longest {longest_correct}/{len(singles)}")
code_langs = Counter((q.get("code") or {}).get("lang") for q in questions if q.get("code"))
print("code langs:", dict(code_langs))
missing_lessons = [c for c, _, _ in SUBSKILLS if c not in lessons]
if missing_lessons: print("MISSING LESSONS:", missing_lessons)
print(f"size {os.path.getsize(OUT)//1024} KB")
for e in errors: print("ERROR", e)
for w in warnings[:40]: print("WARN", w)
sys.exit(1 if errors else 0)
