# Contributing to FDP-1

FDP-1 is a **Draft — Request for Comments**, and comment is the entire mechanism
by which it becomes a standard. The most useful thing you can do is **run the
reference validator over your own data and tell us what breaks**:

```bash
python validator/validate_fdp.py your-declaration.json
```

Twenty rows is enough. If it rejects something it shouldn't — or accepts
something it shouldn't — [open an issue](https://github.com/murffious/fdp-1/issues)
with the section number (`§2`, `§3.1`, …), what you tried, and what you expected.
A spec debugged against real data is worth more than one endorsed in the abstract.

Larger changes (a new field, a change to a grade or the weakest-link rule) go
through an issue first — the forward-compatibility promise in §5 means anything
that lands is permanent, so we discuss before we merge.

By contributing you agree your contribution is licensed under Apache-2.0, and you
agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
