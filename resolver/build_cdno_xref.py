#!/usr/bin/env python3
"""Extract the FDP-1 nutrient_ref resolver table from the CDNO ontology.

FDP-1 §2 makes `cdno` the canonical nutrient_ref namespace and accepts
`fdc.nutrient` / `fdc.nbr` / `infoods` / `chebi` as alternate keys that a
consumer MUST resolve to a CDNO term. CDNO publishes those mappings as
`xref:` annotations in its OBO release; this script extracts them into a small
TSV so the resolution can be done offline, pinned to a CDNO release.

Usage:
    python build_cdno_xref.py cdno.obo cdno-xref.tsv
Download cdno.obo from http://purl.obolibrary.org/obo/cdno.obo (CC BY 3.0).
"""
import re, sys

obo = open(sys.argv[1], encoding="utf-8").read()
version = (re.search(r"^data-version:\s*(\S+)", obo, re.M) or [None, "OPEN"])[1]

def cell(vals):
    return ";".join(sorted(set(vals))) if vals else "OPEN"

rows = []
for block in obo.split("\n[Term]"):
    m = re.search(r"^id:\s*(CDNO:\d+)", block, re.M)
    if not m:
        continue
    xrefs = re.findall(r"^xref:\s*(\S+)", block, re.M)
    fdc = [x.split(":", 1)[1] for x in xrefs if x.startswith("USDA_fdc_id:")]
    nbr = [x.split(":", 1)[1] for x in xrefs if x.startswith("USDA_nutrient_nbr:")]
    inf = [x.split(":", 1)[1] for x in xrefs if x.startswith("INFOODs:")]
    che = [x.split(":", 1)[1] for x in xrefs if x.upper().startswith("CHEBI:")]
    che += [x.split(":", 1)[1] for x in re.findall(r"^is_a:\s*(CHEBI:\d+)", block, re.M)]
    if not (fdc or nbr or inf):
        continue  # only rows that resolve an accepted alternate key
    rows.append((m.group(1).lower(), cell(fdc), cell(nbr), cell(inf),
                 cell(che)))
rows.sort()
with open(sys.argv[2], "w", encoding="utf-8") as fh:
    fh.write("cdno_id\tfdc.nutrient\tfdc.nbr\tinfoods\tchebi\n")
    for r in rows:
        fh.write("\t".join(r) + "\n")
print(f"cdno_version={version}  rows={len(rows)}")
