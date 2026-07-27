# FDP-1: Food Data Provenance Declaration

**Status:** Draft — Request for Comments
**Version:** 0.1.0
**Author:** Paul Murff
**Date:** 2026-07-26
**License:** Apache-2.0. Patent non-assertion covenant applies (see PATENTS.md).
**Normative form:** This Markdown document is normative. Any rendered PDF is provided for convenience only; if the two differ, the Markdown governs.

---

## Conventions

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when, and only when, they appear in all capitals, as shown here.

---

## Abstract

Food-quality scores are computed from data that regulation permits to be inaccurate, and no current scoring system declares which data it used. This document specifies a minimal format for declaring the provenance of a nutrient value and the validation status of a score computed from such values. It does not specify how to score food. It is intended to wrap any existing system — Nutri-Score, Health Star Rating, Nutri-Grade, Food Compass, or proprietary scores — without modification to that system.

---

## 1. Motivation

Under 21 CFR 101.9(g), a declared nutrient value in the United States is compliant if Class I nutrients meet at least 100% of the declared amount, Class II at least 80%, and calories, sugars, sodium, fat, and cholesterol do not exceed 120%. In the European Union, Regulation (EU) No 1169/2011 Article 31(4) permits declared values to derive from manufacturer analysis, calculation from ingredients, *or* calculation from generally accepted data, with Commission tolerance ranges applied on top.

A label value is therefore a legally bounded estimate, not a measurement. Databases that ingest label values — including USDA FoodData Central's Branded Foods — inherit those bounds. Every score computed downstream inherits them silently, with no error bar and no indication of source.

The gap this addresses is not "which food is healthy." It is that no scoring system currently states what it knew, how well it knew it, or how much of its answer rests on a legally permitted approximation.

---

## 2. Value declaration

Every nutrient value SHALL declare seven fields.

| Field | Type | Notes |
|---|---|---|
| `nutrient_ref` | CURIE | Food-component identity, `prefix:id`. Canonical `cdno` (e.g. `cdno:0200651` = dietary iron); `chebi` / `fdc.nutrient` / `fdc.nbr` / `infoods` also accepted. See below. |
| `value` | number \| `OPEN` \| `NONE` | See §4 |
| `unit` | UCUM string | e.g. `mg`, `g`, `kcal` |
| `source` | enum | `analytical` \| `label` \| `calculated` \| `imputed` \| `literature` \| `OPEN` |
| `source_ref` | string \| `OPEN` | Identifier of the *source record* the value was taken from: `usda.fdc:169097`, `foodb:FDB012345` |
| `method` | string \| `OPEN` \| `NONE` | Analytical method where applicable: `aoac:2011.25`, `aoac:991.43`. `NONE` when the value was not measured (see §4) |
| `retrieved` | ISO 8601 date \| `OPEN` | When the value was obtained from `source_ref` |

**`nutrient_ref` names the nutrient; `source_ref` names the source** — *which* nutrient versus *where* the number came from; a value is unreadable in isolation without the first. `nutrient_ref` is a CURIE (`prefix:id`). Its **canonical** namespace is **`cdno`**, the OBO Compositional Dietary Nutrition Ontology — a food-composition (analyte) vocabulary grounded in ChEBI, resolvable at `purl.obolibrary.org/obo/CDNO_{id}`, and already carrying cross-references to the systems real data is keyed on. A producer SHOULD give the CDNO analyte term (e.g. `cdno:0200651`, dietary iron) and MAY additionally give an accepted alternate key — `fdc.nutrient` (USDA FDC internal nutrient id, e.g. `1089`), `fdc.nbr` (USDA legacy nutrient number, e.g. `303`), or `infoods` (FAO/INFOODS tagname, e.g. `FE`) — which a consumer resolves to CDNO through CDNO's published `hasDbXref` mappings (a pinned resolution table ships in `resolver/`). An alternate key is not guaranteed to resolve 1:1 — an FDC number may map to several CDNO terms (a specific analyte and a broader dietary total) — so the canonical `cdno:` form is unambiguous and preferred: a conforming producer MUST declare the `cdno:` term directly when an alternate key resolves to more than one CDNO term, and a consumer MUST NOT silently pick one. **Distinguish `fdc.nutrient` from `fdc.nbr`:** FoodData Central carries two nutrient identifier systems (internal id `1089` and legacy number `303` both denote iron), and a bare `fdc:` is ambiguous.

Every prefix MUST be one of the accepted set — `cdno`, `chebi`, `fdc.nutrient`, `fdc.nbr`, `infoods`, `foodprov` — or a prefix registered in the Bioregistry (`bioregistry.io`); ad-hoc, unregistered prefixes are non-conforming. The alternate-key prefixes are named here explicitly (and are being registered in the Bioregistry) so that the accepted set and the reference validator agree without depending on registration timing. A `chebi:` identity is **terminal** — it names the nutrient directly (used when no CDNO term exists) and is not resolved onward to CDNO. A component with no term in any accepted registry (e.g. total polyphenols) takes the nearest ChEBI class (e.g. `chebi:26195`, polyphenol), or — only if none applies — a `foodprov:` identifier carrying an optional `nutrient_ref_status: unregistered`. If an accepted alternate key has no CDNO term (the resolver returns nothing), a declaration MAY use the alternate key alone and MUST then flag `nutrient_ref_mapped: false`, so a consumer knows resolution to canonical CDNO was not possible. Because CDNO is revised on a release cadence, a declaration SHOULD record the CDNO release it resolved against (optional `cdno_version`); identifiers are never reassigned, and a superseded term carries `replaced_by`. `nutrient_ref` is **not** a metabolite identifier: mapping a nutrient onto a body metabolite (e.g. via the [`MASTER_CROSSWALK.tsv`](https://github.com/murffious/biology_as_code/blob/main/MASTER_CROSSWALK.tsv), joined on ChEBI) is a separate downstream layer.

**`method` is not optional decoration.** Dietary fibre determined by AOAC 985.29, 991.43, and 2011.25 yields systematically different results for the same food, because the later methods capture resistant starch and low-molecular-weight soluble fibre the earlier ones miss. A fibre value without a method is not comparable to another fibre value.

### Provenance grades

| Grade | `source` | Meaning |
|---|---|---|
| **A** | `analytical` | Laboratory-determined, method declared |
| **B** | `calculated` | Derived from analytical values of declared components |
| **C** | `label` | Manufacturer-declared; subject to regulatory tolerance |
| **D** | `imputed` \| `literature` | Borrowed from a similar food or the published record |
| **—** | `OPEN` | Not known. See §4 |

---

## 3. Score declaration

A score computed from declared values SHALL declare five fields.

| Field | Type | Notes |
|---|---|---|
| `score_id` | string | System and version: `nutri-score:2023`, `kibo:2.1` |
| `inputs` | array | Array of `{ nutrient_ref, source_ref }` pairs, each identifying one value declaration (§2) consumed |
| `provenance_grade` | enum | **Computed, not asserted.** See §3.1 |
| `weights_published` | URI \| `false` | Where the weights and their derivation can be read |
| `validation` | object | See §3.2 |

### 3.1 The weakest-link rule

> **A score's provenance grade is the grade of its lowest-graded input.**

A score is not more trustworthy than the worst thing it was computed from. A composite drawing 40 analytical values and one label-derived value is Grade C. This is the only normative computation in this specification, and it is deliberately unforgiving: averaging provenance would let a system bury its weak inputs under its strong ones, which is precisely the behaviour this document exists to prevent.

### 3.2 Validation status

| Level | Meaning |
|---|---|
| `none` | No published validation |
| `face` | Expert judgment that outputs appear sensible |
| `convergent` | Agrees with an already-validated instrument |
| `criterion-intermediate` | Associated with health outcomes in published cohorts |
| `criterion-substantial` | Consistently associated with hard outcomes across multiple independent cohorts |

`validation` SHALL carry `{ level, citation }`. A level above `none` without a citation is non-conforming.

The tiers follow the rubric used in the 2023 *AJCN* systematic review of nutrient profiling systems, which found substantial criterion validation for Nutri-Score and intermediate for most others. A WHO review has found that the large majority of nutrient profiling models carry no validation mechanism at all. Declaring `none` honestly is conforming; implying more than you have is not.

---

## 4. The OPEN and NONE conventions

Two tokens carry the difference between *not knowing* and *knowing there is nothing to know*. Both are first-class values, matched by exact spelling (`OPEN`, `NONE`, uppercase).

> **`OPEN` — not known.** A value or identifier we do not have, but which exists and could in principle be supplied. A value that is not known SHALL be declared `OPEN`. It SHALL NOT be imputed silently, defaulted to zero, or omitted.

> **`NONE` — not applicable / known absent.** A field that categorically does not apply, or a value or identifier known not to exist. A value obtained without measurement (`calculated`, `label`, `imputed`) declares `method: NONE` — no analytical method was used — which is a different statement from `method: OPEN`, which asserts a method exists but is unknown.

Omitting a field, declaring it `OPEN`, and declaring it `NONE` are three different statements — silence, a claim about the limit of what is known, and a claim about what does not exist. Consumers of a declaration MUST be able to distinguish them.

A nutrient with no term in an accepted registry SHALL be given the nearest ChEBI class (e.g. `chebi:26195`, polyphenol) or, failing that, a `foodprov:` identifier (§2) — never `OPEN` or `NONE` — so the value remains referenceable. That records the absence of a standard *term*, not the absence of a nutrient.

Coverage SHOULD be reported as the fraction of fields carrying a determinate (non-`OPEN`) value, per dataset. Honest partial coverage is conforming; invented completeness is not.

---

## 5. Forward compatibility

> **Once FDP, always FDP.**

Any document conforming to FDP-1 SHALL remain valid under all future revisions. Future versions may add optional fields; they may not remove fields, redefine grades, or alter the weakest-link rule. Archives written today must still parse in twenty years.

This is a promise, not a version policy. It is why the specification is small: everything in it is permanent, so very little belongs in it.

---

## 6. Conformance

An implementation conforms if:

1. Every nutrient value carries all seven fields of §2.
2. Every score carries all five fields of §3, and every `inputs` entry resolves to a declared value by its `{ nutrient_ref, source_ref }` pair.
3. `provenance_grade` is computed by the weakest-link rule, not asserted.
4. Unknown values are `OPEN`; values or fields known absent or not applicable are `NONE`. Neither is invented, defaulted to zero, or silently omitted.
5. `validation.level` above `none` carries a citation.

Conformance says nothing about whether a score is *correct*. It says only that a reader can determine what the score was computed from and what evidence supports it. That is the entire scope of this document.

---

## 7. Non-goals

This specification does not define healthy food, prescribe nutrients to include in a score, define weights, rank foods, or endorse any scoring system. Systems competing on scoring methodology can and should conform simultaneously.

---

## 8. Normative references

- **[RFC 2119]** / **[RFC 8174]** — key words for requirement levels (BCP 14). <https://www.rfc-editor.org/info/rfc2119>, <https://www.rfc-editor.org/info/rfc8174>
- **CDNO** — Compositional Dietary Nutrition Ontology, release **2026-06-10** (canonical `nutrient_ref` vocabulary). <http://purl.obolibrary.org/obo/cdno.owl>
- **ChEBI** — Chemical Entities of Biological Interest (terminal nutrient identity where no CDNO term exists). <https://www.ebi.ac.uk/chebi/>
- **Bioregistry** — prefix registry governing accepted `nutrient_ref` prefixes. <https://bioregistry.io>
- **FAO/INFOODS** food component tagnames (accepted alternate key). <https://www.fao.org/infoods/infoods/standards-guidelines/food-component-identifiers-tagnames/en/>
- **USDA FoodData Central** — nutrient numbers `fdc.nutrient` / `fdc.nbr` (accepted alternate keys). <https://fdc.nal.usda.gov>
- **UCUM** — Unified Code for Units of Measure (the `unit` field). <https://ucum.org>
- **ISO 8601** — date representation (the `retrieved` field).
- **AOAC** Official Methods of Analysis (the `method` field). <https://www.aoac.org>
- **21 CFR 101.9(g)** — US nutrient-declaration compliance tolerances.
- **Regulation (EU) No 1169/2011**, Article 31(4) — EU food-information tolerances.

---

## 9. Reference implementation

This repository — the reference `validator/`, the `resolver/` table mapping accepted alternate keys to canonical CDNO terms (pinned to a CDNO release), and a worked `examples/` declaration across a single meal under two host states. `github.com/murffious/biology_as_code` is a fuller reference implementation (a Python package) and hosts the [`MASTER_CROSSWALK.tsv`](https://github.com/murffious/biology_as_code/blob/main/MASTER_CROSSWALK.tsv) nutrient→metabolite join — a downstream layer, not the `nutrient_ref` vocabulary.

---

## Comments

Open an issue on the repository. This is a draft and expected to change until three independent implementations exist.
