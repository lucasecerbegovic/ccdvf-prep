# CCAR-P Prep

Personal study program for the **Claude Certified Architect – Professional (CCAR-P)** exam
(guide v1.0, July 2026): a 19-step plan, 38 condensed lessons (one per exam objective), practice questions,
a diagnostic, and 6 timed mock exams scored on the 100–1000 scale (720 to pass).

Mocks mirror the real format: 63 standalone questions in 120 minutes, spread across the domains by the
official weights:

| Domain | Weight | Per mock |
|---|---|---|
| P1 Solution Design & Architecture | 17% | 11 |
| P2 Claude Models, Prompting & Context Engineering | 13% | 8 |
| P3 Integration | 19% | 12 |
| P4 Evaluation, Testing & Optimisation | 16% | 10 |
| P5 Governance, Safety & Risk Management | 14% | 9 |
| P6 Stakeholder Communication & Lifecycle Management | 14% | 9 |
| P7 Developer Productivity & Operational Enablement | 7% | 4 |

Live app (private): https://claude.ai/artifact/Ct1C8uYFdzYQdCrMYge6fL

All questions are original practice items, not real exam content. The domain list and objectives come from
third-party summaries of the official exam guide; check them against Anthropic's guide.

A second set of reviewers re-solved all 169 questions written for CCAR-P and checked them against the official
docs. They found no wrong answer keys and fixed six explanations or stems (reports in `content/pro/review/`).

## History

The bank was first built for the Developer exam (CCDV-F), then for Architect – Foundations (CCAR-F, commit
`5a40995`), and now targets Professional. Questions carried over from those banks keep their original ids;
some still name one of the Foundations scenarios, which the app shows as context above the question.

## Layout

| Path | What it is |
|---|---|
| `app/index.html` | The study app: one page, plain HTML/CSS/JS, no build step |
| `app/bank.json` | Generated question bank the app loads (don't edit by hand) |
| `content/SPEC.md` | Content spec: domains, objectives, question rules, JSON format |
| `content/pro/retag/*.json` | Questions carried over from the Foundations and Developer banks, re-tagged to CCAR-P objectives (with the dropped ids and reasons) |
| `content/pro/new/*.json` | Lessons and new questions written for CCAR-P, by domain |
| `content/pro/review/` | Independent answer-key review reports for the new questions |
| `content/build.py` | Merges `content/pro/`, validates, balances answer positions, builds the diagnostic and the sealed mocks |
| `content/new/`, `content/retag/`, `content/review/` | The Foundations (CCAR-F) sources; not built |
| `content/archive_ccdvf/` | The original Developer bank; not built |

## Editing questions

1. Edit the relevant file in `content/pro/retag/` or `content/pro/new/`. Each question needs an objective code in
   `subskill` (e.g. `P3.5`). `answer` uses 0-based option indexes, and `explanations` must line up with `options`.
   To drop a question without deleting it, add `"retired": true`; the build skips it.
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
syncs to your account. Professional progress is kept separate from the earlier Foundations progress.
