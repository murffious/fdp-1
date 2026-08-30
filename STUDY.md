# STUDY.md — NUTR-PUBLIC-001

**This repository is the spec.** It defines the shared properties and provenance fields every participant emits, and ships the reference validator. It holds no study data.

```text
study_id:     NUTR-PUBLIC-001
schema_ref:
  food:       fdp-1@v0.1.0
  packet:     biology_as_code/schemas@v0.1.0
  study:      MI-Nutrition@v0.1
rule:         a row OR a study record that does not validate is not study data
split:        food deposits are public; person-level rows stay in body;
              research export only via ResearchRelease + DUO
paper:        producer keeps first analysis
```

- `study_id` names the pin, so the adoption tracker has something to count.
- `schema_ref` names **three** contracts, because a study is three things: the number
  on a food, the packet that carries it, and the study record itself. The pin used to
  name the first two and behave as though that covered the third. **The same block is in
  `biology_as_code/STUDY.md`.** If they diverge, the pin is broken.
  **Honest status of the third:** `food:` and `packet:` resolve to public repositories
  you can clone and watch refuse a bad row. `study:` names a version and nothing else,
  because MI-Nutrition has no neutral public home yet — its schema is served, but from a
  product-branded host this repository is not permitted to name, and its validator is not
  published at all. **The pin therefore names a contract a stranger cannot yet fetch or
  run.** That is stated rather than papered over, and closing it is the next task.
- `rule` is refusal. Enforced today: `tests/test_rejections.py` — a welded `protein_mg` column, an empty field where §4 requires the literal `OPEN`, and a bare `"iron"` where §2 requires a CURIE are all rejected.
- `split` is what stops a `human_id` landing in a public remote. Enforced today:
  `tools/check_no_human_rows.py`, which runs **first** in CI — every other failure here
  is recoverable, that one is not.
- `paper` is Fort Lauderdale 2003. Deposit the draft assay now, keep first publication
  on the analysis. It is the clause that makes this signable by a working lab.

Not in this file: nutrients, digestion machines, the ontology. `CONTRIBUTING.md`, the
specification and the book stay where they are.
