# FDP-1 — Food Data Provenance Declaration

[![CI](https://github.com/murffious/fdp-1/actions/workflows/ci.yml/badge.svg)](https://github.com/murffious/fdp-1/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)
[![Status](https://img.shields.io/badge/status-Draft%20%C2%B7%20RFC-orange)](FDP-1-food-data-provenance.md)

**This repository is the canonical home of the FDP-1 specification.** FDP-1 is a
minimal, RFC-style specification for declaring *where a nutrient value came from*
and *how well a score built on it is validated*. It does **not** score food — it
wraps any existing system (Nutri-Score, Health Star Rating, Nutri-Grade, Food
Compass, or a proprietary score) without modifying it.

> **[Read the specification → `FDP-1-food-data-provenance.md`](FDP-1-food-data-provenance.md)**

## The whole idea

**Every food score tells you its answer. None tells you what it knew.**

Nutri-Score says B; Yuka says 40/100. There's no way to tell whether they disagree
about the food or about the algorithm, because neither declares which data it read.
FDP-1 is the receipt — attach it to a score and someone else can check the number
instead of trusting it.

- **A score is only as good as its worst input.** Seven fields on a value, five on
  a score, one rule — the **weakest-link rule** (§3.1): a score's grade is its
  lowest-graded input. 40 lab values + 1 label value = Grade C. No averaging,
  because averaging is how a system buries its weak inputs.

- **A value is readable on its own.** `nutrient_ref` names *which* nutrient —
  canonically a CDNO term, with FDC numbers, INFOODS tagnames and ChEBI accepted
  and resolved to CDNO (see [`resolver/`](resolver/)). `source_ref` names *where
  the number came from*. Neither is inferable from the other.

- **There are three ways to say nothing, and they differ** (§4). Omitting a field
  is silence. `OPEN` is *not known*. `NONE` is *nothing to know*. A score resting
  on an `OPEN` input comes out honestly ungraded instead of quietly confident.

- **Once FDP, always FDP** (§5). A conforming document stays valid under every
  future revision. That's why the spec is small — everything in it is permanent,
  so very little belongs in it.

## Check a declaration

The reference validator is dependency-free (Python ≥ 3.11, standard library only):

```bash
python validator/validate_fdp.py examples/iron-two-hosts.json
```

It recomputes the weakest-link grade rather than trusting the declared one, and
exits non-zero on any non-conformance. See
[`examples/iron-two-hosts.json`](examples/iron-two-hosts.json) — one food, full
provenance on every input, a ~6× absorbed-iron delta across two host states,
honestly ungraded (`—`) because one modifier is `OPEN`.

## Reference implementation

A fuller reference implementation — a Python package that ingests foods, runs
digestion, and emits FDP-1 declarations, plus the `MASTER_CROSSWALK.tsv`
nutrient→metabolite join — lives at
[github.com/murffious/biology_as_code](https://github.com/murffious/biology_as_code).
The spec and the implementation are deliberately separate artifacts.

## Status & comments

**Draft — Request for Comments.** Expected to change until three independent
implementations exist. **[Open an issue](https://github.com/murffious/fdp-1/issues)** —
that is the entire mechanism by which FDP-1 becomes a standard rather than a
document.

## License

Apache-2.0 (see [`LICENSE`](LICENSE)), with a patent
[non-assertion covenant](PATENTS.md) over the specification and its reference
validator.
