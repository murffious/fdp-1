#!/usr/bin/env python3
"""Resolve an FDP-1 nutrient_ref alternate key to its canonical CDNO term(s).

FDP-1 §2 makes `cdno` canonical and accepts `fdc.nutrient` / `fdc.nbr` /
`infoods` / `chebi` as alternate keys that a consumer resolves to CDNO. This does
that lookup offline against cdno-xref.tsv (pinned to a CDNO release).

    python resolve.py infoods:FE        ->  cdno:0200157
    python resolve.py fdc.nutrient:1089 ->  cdno:0200157 cdno:0200651   (ambiguous)

~11% of FDC keys map to more than one CDNO term (a specific analyte and a broader
dietary total), which is exactly why a conforming producer SHOULD declare the
`cdno:` term directly. This resolver returns every candidate; it does not choose.
"""
import csv, os, sys

TABLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cdno-xref.tsv")

def load():
    idx = {}
    with open(TABLE, encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            for prefix in ("fdc.nutrient", "fdc.nbr", "infoods", "chebi"):
                for v in row[prefix].split(";"):
                    if v and v != "OPEN":
                        idx.setdefault((prefix, v), set()).add(row["cdno_id"])
    return idx

def resolve(curie, idx):
    if curie.startswith("cdno:"):
        return [curie]
    prefix, _, value = curie.partition(":")
    return sorted(idx.get((prefix, value), [])) if value else []

def main(argv):
    if len(argv) != 2:
        print(__doc__); return 2
    hits = resolve(argv[1], load())
    if hits:
        print(" ".join(hits)); return 0
    print(f"unresolved: {argv[1]}", file=sys.stderr); return 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
