# Changelog

All notable changes to **FDP-1 — Food Data Provenance Declaration** (the
specification, its reference validator and fixtures) are documented here. Format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The specification's
version is the git tag; `v0.1.0` is what `STUDY.md` pins, here and in
`murffious/biology_as_code`.

## [Unreleased]

On `main`, not yet tagged. Nothing below changes the normative text of the
specification; the pin `fdp-1@v0.1.0` still holds.

### Added
- **The spec is refusable** (2026-08-29): negative fixtures under
  `tests/non-conforming/`, including `reject-protein-mg.json` — a value written as a
  bare `protein_mg` column fails with `missing required §2 field(s): nutrient_ref,
  value, unit` and exit 1. `tests/test_rejections.py` keeps that true.
- **Rule E guard** — `tools/check_no_human_rows.py` with `tests/test_no_human_rows.py`:
  no person in a public repository. A study-level check, deliberately *not* an FDP-1
  rule: FDP-1 asks whether a value is provenanced; this asks whether the repository
  contains a person. A synced copy runs in `biology_as_code`.
- **`STUDY.md`** — the participation pin for study `NUTR-PUBLIC-001`: a row that does
  not validate is not study data. The `schema_ref` block is identical here and in
  `biology_as_code` and is compared whole; it grew from one schema to a three-part
  contract on 2026-08-30. Cut to the contract rather than a protocol paper; the split
  line reads food public, person in the body store, export only with DUO. The status
  of the MI-Nutrition schema and validator pinning is stated.

### Fixed
- **A stranger running `pytest` saw no tests at all** — the suite was not collected
  from a fresh clone (2026-08-29).
- `LICENSE`: Apache-2.0 appendix copyright line filled (2026-09-01).

## [0.1.0] — 2026-07-26

First public release. Concept DOI `10.5281/zenodo.21613721`; this version
`10.5281/zenodo.21613722`. Status: Draft / RFC — a specification leaves draft when
three independent implementations exist, and `biology_as_code` is the first.

### Added
- `FDP-1-food-data-provenance.md` — the specification: shared properties, per-value
  provenance fields, `OPEN` ≠ `NONE` ≠ 0, weakest-link grading, conformance tiers.
- `validator/validate_fdp.py` — dependency-free reference validator, exit 1 on
  non-conformance, documented to drop into CI.
- `examples/` — the worked example. `iron-two-hosts.json` is ungraded on purpose: its
  `OPEN` input is the point.
- **CDNO adopted as the canonical `nutrient_ref` vocabulary** after a commissioned
  investigation; `resolver/` resolves references against it.
- CI workflow and badge; `CITATION.cff`; `PATENTS.md` covenant; `NOTICE`,
  `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`.

### Changed
- Review round 1: the iron term corrected to *dietary iron*; repository furniture.
- Review round 2: the five blockers and the majors fixed; local prefix renamed to
  `foodprov`; `PATENTS.md` covenant scope corrected; Zenodo blurb states CDNO as
  canonical.
- README leads with the why (Yuka, Nutri-Score) and puts claims before fields; the §2
  crosswalk is a proper link matching §9.
- Zenodo DOI badge and `CITATION.cff` DOI added the same day, after the tag.
