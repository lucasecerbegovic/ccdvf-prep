# Answer-key review brief (CCAR-P)

Follow `content/review/BRIEF.md` (the method, classes and fix rules are the same), with these differences:
- The spec is `content/SPEC.md` (CCAR-P objectives P1.1–P7.3). New questions have no `scenario`; they must be
  self-contained.
- Also flag as `bad_fact` any claim about Anthropic certifications, contracts, SLAs, prices or limits that an
  official page doesn't state, and any arithmetic in a stem/explanation that doesn't check out.
- Write your report to `content/pro/review/<your label>.json` (not `content/review/`).
- Validate with `python3 -I content/build.py` (must exit 0; ignore errors in files that aren't yours).
