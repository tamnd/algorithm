# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shared-resource-matrix/. The authors are listed in prov/3Z77T4.jsonl.

import random

from shared_resource_matrix import from_rows, shared_resource_matrix

PRIMS = ["WRITE FILE", "READ FILE", "LOCK FILE", "UNLOCK FILE", "OPEN FILE", "CLOSE FILE", "FILE LOCKED", "FILE OPENED"]
W, RD, LK, UL, OP, CL, FL, FO = PRIMS

# Table 1 of Kemmerer (ACSAC 2002), the file system example.
KEMMERER_ROWS = {
    "Process ID": {},
    "Access Rights": {LK: "R", OP: "R", FL: "R", FO: "R"},
    "Buffer": {W: "R", RD: "M"},
    "Security Classes": {LK: "R", OP: "R", FL: "R", FO: "R"},
    "File ID": {},
    "Locked By": {W: "R", LK: "M", UL: "R"},
    "Locked": {W: "R", LK: "R/M", UL: "R/M", OP: "R", FL: "R"},
    "In-use Set": {RD: "R", LK: "R", OP: "R/M", CL: "R/M", FO: "R"},
    "Value": {W: "M", RD: "R"},
    "Current Proc": {W: "R", RD: "R", LK: "R", UL: "R", OP: "R", CL: "R"},
}

# The spooler example of the page.
SPOOLER_ATTRS = ["Level", "Queue", "Count", "Owner"]
SPOOLER_ROWS = {
    "Level": {"SUBMIT": "R", "CANCEL": "R", "LIST": "R"},
    "Queue": {"SUBMIT": "M", "CANCEL": "M", "LIST": "R"},
    "Count": {"SUBMIT": "R/M", "CANCEL": "M", "STATUS": "R"},
    "Owner": {"SUBMIT": "M", "CANCEL": "R"},
}


def closed_and_candidates(attrs, rows):
    refs, mods = from_rows(rows)
    return shared_resource_matrix(attrs, refs, mods)


def naive_closure(attrs, prims, r_entries, m_entries):
    """Kemmerer's rule applied literally to the matrix until nothing changes."""
    r = set(r_entries)
    changed = True
    while changed:
        changed = False
        for a, p in sorted(r):
            for q in prims:
                if (a, q) in m_entries:
                    for b in attrs:
                        if (b, q) in r and (b, p) not in r:
                            r.add((b, p))
                            changed = True
    return r


def test_kemmerer_table_2() -> None:
    attrs = list(KEMMERER_ROWS)
    closed, cands = closed_and_candidates(attrs, KEMMERER_ROWS)
    full = {"Access Rights", "Security Classes", "Locked By", "Locked", "In-use Set", "Current Proc"}
    for p in PRIMS:
        want = set(full)
        if p in (W, RD):
            want |= {"Buffer", "Value"}
        assert closed[p] == want
    rows = [a for a, _, _ in cands]
    assert rows == ["Buffer", "Locked By", "Locked", "In-use Set", "Value"]
    cand = {a: (mods, sens) for a, mods, sens in cands}
    assert cand["In-use Set"][0] == [OP, CL]
    assert cand["Locked"][0] == [LK, UL]
    assert FO in cand["In-use Set"][1] and FL in cand["Locked"][1]
    assert "Process ID" not in rows and "File ID" not in rows


def test_spooler_example() -> None:
    closed, cands = closed_and_candidates(SPOOLER_ATTRS, SPOOLER_ROWS)
    assert closed["SUBMIT"] == {"Level", "Count", "Owner"}
    assert closed["CANCEL"] == {"Level", "Owner", "Count"}
    assert closed["STATUS"] == {"Count", "Level", "Owner"}
    assert closed["LIST"] == {"Level", "Queue", "Count", "Owner"}
    # from_rows meets the primitives in the order SUBMIT, CANCEL, LIST, STATUS.
    assert cands == [
        ("Queue", ["SUBMIT", "CANCEL"], ["LIST"]),
        ("Count", ["SUBMIT", "CANCEL"], ["SUBMIT", "CANCEL", "LIST", "STATUS"]),
        ("Owner", ["SUBMIT"], ["SUBMIT", "CANCEL", "LIST", "STATUS"]),
    ]


def test_edges() -> None:
    assert shared_resource_matrix([], {}, {}) == ({}, [])
    closed, cands = shared_resource_matrix(["a"], {"p": set()}, {"p": set()})
    assert closed == {"p": set()} and cands == []
    # A modified attribute that nobody references is not a candidate.
    closed, cands = shared_resource_matrix(["a"], {"p": set()}, {"p": {"a"}})
    assert cands == []
    # One primitive that references and modifies the same attribute.
    closed, cands = shared_resource_matrix(["a"], {"p": {"a"}}, {"p": {"a"}})
    assert closed == {"p": {"a"}} and cands == [("a", ["p"], ["p"])]
    # A chain needs more than one round: p reads a, q writes a from b, r writes b from c.
    refs = {"p": {"a"}, "q": {"b"}, "r": {"c"}}
    mods = {"p": set(), "q": {"a"}, "r": {"b"}}
    closed, _ = shared_resource_matrix(["a", "b", "c"], refs, mods)
    assert closed["p"] == {"a", "b", "c"}
    assert closed["q"] == {"b", "c"}
    assert closed["r"] == {"c"}


def test_not_standard_transitive_closure() -> None:
    # The flow goes against the edge a -> b of "q writes a after reading b": a reader
    # of b learns nothing about a.
    refs = {"p": {"b"}, "q": {"b"}}
    mods = {"p": set(), "q": {"a"}}
    closed, _ = shared_resource_matrix(["a", "b"], refs, mods)
    assert closed["p"] == {"b"}


def test_against_naive_rule() -> None:
    rng = random.Random(1983)
    for _ in range(600):
        n = rng.randint(1, 6)
        m = rng.randint(1, 6)
        attrs = [f"a{i}" for i in range(n)]
        prims = [f"p{j}" for j in range(m)]
        refs = {p: {a for a in attrs if rng.random() < 0.3} for p in prims}
        mods = {p: {a for a in attrs if rng.random() < 0.3} for p in prims}
        closed, cands = shared_resource_matrix(attrs, refs, mods)
        r0 = {(a, p) for p in prims for a in refs[p]}
        m0 = {(a, p) for p in prims for a in mods[p]}
        want = naive_closure(attrs, prims, r0, m0)
        got = {(a, p) for p in prims for a in closed[p]}
        assert got == want
        want_c = [a for a in attrs if any((a, p) in m0 for p in prims) and any((a, p) in want for p in prims)]
        assert [a for a, _, _ in cands] == want_c
        # The closure keeps the input and is idempotent.
        assert all(refs[p] <= closed[p] for p in prims)
        again, _ = shared_resource_matrix(attrs, closed, mods)
        assert again == closed
