#!/usr/bin/env python3
"""The validator must REJECT these. A spec that cannot fail a row is not a spec.

WHY THIS FILE EXISTS
--------------------
CI already proved `examples/iron-two-hosts.json` conforms. That is half a test. It
shows the validator says yes to something; it never showed the validator can say no,
and "can say no" is the entire value of a conformance spec. On 2026-08-29 the three
fixtures beside this file were all correctly rejected — by accident of construction,
with nothing asserting it would stay that way. This file is that assertion.

THE SYMMETRY MATTERS
--------------------
A suite that only checks rejections passes trivially if the validator breaks and
rejects everything. So the positive case is checked here too, in the same run. Both
directions or neither.

    python3 tests/test_rejections.py        # exits 1 if any case behaves wrongly
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
VALIDATOR = ROOT / "validator" / "validate_fdp.py"


def run(path: pathlib.Path) -> tuple[int, str]:
    p = subprocess.run([sys.executable, str(VALIDATOR), str(path)],
                       capture_output=True, text=True, timeout=60)
    return p.returncode, (p.stdout + p.stderr)


def main() -> int:
    failures: list[str] = []

    # --- must be REJECTED (exit 1) ---
    rejects = sorted((HERE / "non-conforming").glob("*.json"))
    if not rejects:
        print("no non-conforming fixtures found — the suite would pass vacuously")
        return 1
    for f in rejects:
        code, out = run(f)
        if code == 0:
            failures.append(f"{f.name}: ACCEPTED but must be rejected\n{out}")
        else:
            first = next((l.strip() for l in out.splitlines() if l.strip().startswith("-")), "")
            print(f"  rejected  {f.name:<44} {first[:72]}")

    # --- must be ACCEPTED (exit 0) — or a validator that rejects everything passes ---
    for f in sorted((ROOT / "examples").glob("*.json")):
        code, out = run(f)
        if code != 0:
            failures.append(f"{f.name}: REJECTED but must conform\n{out}")
        else:
            print(f"  conforms  {f.name}")

    if failures:
        print(f"\nFAIL — {len(failures)} case(s) behaved wrongly:\n")
        for x in failures:
            print(x)
        return 1
    print(f"\nOK — {len(rejects)} rejected, "
          f"{len(list((ROOT / 'examples').glob('*.json')))} conforming.")
    return 0


# pytest entry point. CI runs this file as a script, which is why it never noticed:
# in a fresh clone, `pytest tests/` printed "no tests collected". Every function here
# was named main()/run(), so a suite that LOOKS like pytest collected nothing, and the
# one thing a stranger is invited to do — clone it and watch a bad row get refused —
# silently did nothing at all. Both invocations have to work, because only one of them
# is the one a stranger will try.
def test_rejections() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
