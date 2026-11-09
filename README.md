# CCDV-F Prep

Personal study program for the **Claude Certified Developer – Foundations (CCDV-F)** exam:
an 18-day plan, 25 condensed lessons, 399 original scenario questions, a diagnostic,
and 6 timed mock exams scored on the 100–1000 scale (720 to pass).

Live app (private): https://claude.ai/artifact/Ct1C8uYFdzYQdCrMYge6fL

All questions are original practice items, not real exam content.

## Layout

| Path | What it is |
|---|---|
| `app/index.html` | The study app: one page, plain HTML/CSS/JS, no build step |
| `app/bank.json` | Generated question bank the app loads (don't edit by hand) |
| `content/part*.json` | Source lessons and questions, one file per domain group |
| `content/SPEC.md` | Content spec: blueprint, sub-skill codes, question rules, JSON format |
| `content/build.py` | Merges the parts, validates them, balances answer positions, builds the diagnostic and the sealed mocks |

## Editing questions

1. Edit the relevant `content/part*.json` file. `answer` uses 0-based option indexes, and
   `explanations` must line up with `options`.
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
