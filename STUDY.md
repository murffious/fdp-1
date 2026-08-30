# STUDY.md — NUTR-PUBLIC-001

**This repository is the spec.** It defines the shared properties and provenance fields every participant emits, and ships the reference validator. It holds no study data.

```text
study_id:     NUTR-PUBLIC-001
schema_ref:   fdp-1@v0.1.0 + biology_as_code/schemas@v0.1.0
rule:         a row that does not validate is not study data
split:        food deposits are public; person-level rows stay in body;
              research export only via ResearchRelease + DUO
paper:        producer keeps first analysis
```

- `study_id` names the pin, so the adoption tracker has something to count.
- `schema_ref` is the tag CI actually checks. **The same string is in
  `biology_as_code/STUDY.md`.** If they diverge, the pin is broken.
- `rule` is refusal. Enforced today: `tests/test_rejections.py` — a welded `protein_mg` column, an empty field where §4 requires the literal `OPEN`, and a bare `"iron"` where §2 requires a CURIE are all rejected.
- `split` is what stops a `human_id` landing in a public remote. Enforced today:
  `tools/check_no_human_rows.py`, which runs **first** in CI — every other failure here
  is recoverable, that one is not.
- `paper` is Fort Lauderdale 2003. Deposit the draft assay now, keep first publication
  on the analysis. It is the clause that makes this signable by a working lab.

Not in this file: nutrients, digestion machines, the ontology. `CONTRIBUTING.md`, the
specification and the book stay where they are.
