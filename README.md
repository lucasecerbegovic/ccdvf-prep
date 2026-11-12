# CCAR-F Prep

Personal study program for the **Claude Certified Architect – Foundations (CCAR-F)** exam
(guide v1.0, effective July 2026): a 19-step plan, 30 condensed lessons (one per task statement),
scenario-based practice questions, a diagnostic, and 6 timed mock exams scored on the 100–1000 scale (720 to pass).

Mocks mirror the real format: 60 questions in 120 minutes, grouped under 4 of the 6 exam scenarios
(15 questions each), with domains close to the official weights:

| Domain | Weight |
|---|---|
| D1 Agentic Architecture & Orchestration | 27% |
| D2 Tool Design & MCP Integration | 18% |
| D3 Claude Code Configuration & Workflows | 20% |
| D4 Prompt Engineering & Structured Output | 20% |
| D5 Context Management & Reliability | 15% |

Live app (private): https://claude.ai/artifact/Ct1C8uYFdzYQdCrMYge6fL

All questions are original practice items, not real exam content. In November 2026 a second set of reviewers
re-solved every new question and the flagged carried-over ones, and checked them against the official docs.
That found no wrong answer keys. It fixed wording in nine questions (reports in `content/review/`).

## Layout

| Path | What it is |
|---|---|
| `app/index.html` | The study app: one page, plain HTML/CSS/JS, no build step |
| `app/bank.json` | Generated question bank the app loads (don't edit by hand) |
| `content/SPEC.md` | Content spec: domains, task statements, scenarios, question rules, JSON format |
| `content/retag/part*.json` | Questions carried over from the earlier Developer (CCDV-F) bank, re-tagged to CCAR-F |
| `content/new/d*.json` | Lessons and new questions, one file per domain |
| `content/review/` | Independent answer-key review: the reviewer brief and one findings report per domain |
| `content/archive_ccdvf/` | The original Developer bank, kept for reference; not built |
| `content/build.py` | Merges the sources, validates them, balances answer positions, builds the diagnostic and the sealed scenario mocks |

## Editing questions

1. Edit the relevant file in `content/retag/` or `content/new/`. Each question needs a task code in `subskill`
   (e.g. `D3.6`) and a `scenario` (`S1`–`S6`). `answer` uses 0-based option indexes, and `explanations` must
   line up with `options`. To drop a question without deleting it, add `"retired": true`; the build skips it.
2. Rebuild the bank:

   ```bash
   python3 -I content/build.py
   ```

   The script exits non-zero and prints `ERROR` lines if any question is malformed.
3. Republish `app/index.html` with `app/bank.json` as a supporting file, to the same artifact URL.

Rebuilding is deterministic (fixed seed), so the sealed mocks (Mocks 3–6) keep the same questions
unless you add or remove questions.

## Running locally

```bash
cd app && python3 -m http.server 8765
```

Then open http://127.0.0.1:8765. Progress is saved in the browser here; on claude.ai it also
syncs to your account.
