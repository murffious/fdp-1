# FDP-1 `nutrient_ref` resolver

FDP-1 §2 makes **`cdno`** the canonical `nutrient_ref` namespace and accepts
`fdc.nutrient` / `fdc.nbr` / `infoods` / `chebi` as **alternate keys a consumer
resolves to CDNO**. This directory is the offline resolution layer — spec
infrastructure, small and pinned, distinct from the metabolite crosswalk in the
reference implementation.

## Files

- **`cdno-xref.tsv`** — the resolution table (364 rows), columns
  `cdno_id | fdc.nutrient | fdc.nbr | infoods | chebi`. Missing values are the
  literal `OPEN` (FDP-1 §4), so every row is self-validating and no cell is
  silent. Derived from CDNO release **`2026-06-10`** — pin declarations to the
  same `cdno_version`.
- **`build_cdno_xref.py`** — regenerates the table from CDNO's own `xref:`
  annotations: `python build_cdno_xref.py cdno.obo cdno-xref.tsv`
  (download `cdno.obo` from `http://purl.obolibrary.org/obo/cdno.obo`).
- **`resolve.py`** — `python resolve.py fdc.nutrient:1089` → the CDNO term(s).

## The 1:many caveat (why `cdno:` is canonical)

An alternate key is **not** guaranteed to resolve to a single CDNO term: **85 of
781 keys (~11%)** map to more than one, because CDNO distinguishes a specific
analyte from a broader dietary total. Iron is the worked case:

| key | resolves to |
|---|---|
| `infoods:FE` | `cdno:0200157` (iron(2+)) |
| `fdc.nutrient:1089` / `fdc.nbr:303` | `cdno:0200157` **and** `cdno:0200651` (dietary iron) |

A food-composition value for "iron" is *dietary iron* — **`cdno:0200651`**, not
the Fe²⁺ ion. The resolver returns every candidate and does **not** choose; that
ambiguity is the reason a conforming producer SHOULD declare the `cdno:` term
directly and treat alternate keys as a convenience.

## Attribution

`cdno-xref.tsv` is derived from the Compositional Dietary Nutrition Ontology
(CDNO), © its authors, licensed **CC BY 3.0**. See `../NOTICE`.
