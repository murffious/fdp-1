#!/usr/bin/env python3
"""The Rule E guard must catch a person, and must NOT catch prose about one.

Both directions are asserted here. A guard that only proves it stays quiet is
indistinguishable from a guard that does nothing, and a guard that fires on the
sentence "do not store human_id" gets switched off within a week.

The violating fixtures are CREATED AT TEST TIME and deleted in a finally block.
They are deliberately not committed: a file shaped like a person does not belong in
a public repository even as a fixture, and an allowlist entry to permit one would be
a hole in the only gate whose failure cannot be undone.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GUARD = ROOT / "tools" / "check_no_human_rows.py"


def run() -> int:
    return subprocess.run([sys.executable, str(GUARD)],
                          capture_output=True, text=True, timeout=120).returncode


def main() -> int:
    fails = []

    if run() != 0:
        fails.append("baseline: the repository ALREADY contains a human-row field")
    else:
        print("  clean      repository has no human-row fields")

    tmp = {
        ROOT / "_t_violation.json": json.dumps(
            {"fdp": "1.0", "human_id": "SYNTHETIC", "values": {}}),
        ROOT / "_t_cols.csv": "food,nutrient_ref,amount,patient_id\nx,cdno:1,1,p\n",
        # Prose. Says the forbidden words on purpose. MUST NOT trip the guard.
        ROOT / "_t_prose.md": "Never store a human_id or date_of_birth here.\n",
    }
    try:
        (ROOT / "_t_prose.md").write_text(tmp[ROOT / "_t_prose.md"])
        if run() != 0:
            fails.append("prose mentioning human_id tripped the guard (mention vs use)")
        else:
            print("  mention    prose naming human_id did NOT trip it")

        for p, body in tmp.items():
            p.write_text(body)
        if run() == 0:
            fails.append("a JSON human_id key and a CSV patient_id column were NOT caught")
        else:
            print("  use        JSON key and CSV column were caught")
    finally:
        for p in tmp:
            if p.exists():
                p.unlink()

    if run() != 0:
        fails.append("guard still failing after cleanup — fixtures leaked")

    if fails:
        print("\nFAIL:")
        for f in fails:
            print("  -", f)
        return 1
    print("\nOK — guard fires on use, stays silent on mention.")
    return 0


# pytest entry point. CI runs this file as a script, which is why it never noticed:
# in a fresh clone, `pytest tests/` printed "no tests collected". Every function here
# was named main()/run(), so a suite that LOOKS like pytest collected nothing, and the
# one thing a stranger is invited to do — clone it and watch a bad row get refused —
# silently did nothing at all. Both invocations have to work, because only one of them
# is the one a stranger will try.
def test_no_human_rows() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
