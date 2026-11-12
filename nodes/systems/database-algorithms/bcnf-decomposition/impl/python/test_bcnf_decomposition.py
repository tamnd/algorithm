# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bcnf-decomposition/. The authors are listed in prov/F3CVSY.jsonl.

import random
from itertools import combinations

from bcnf_decomposition import bcnf_decomposition, bcnf_decomposition_poly


def fds_of(text):
    out = []
    for part in text.split(","):
        lhs, rhs = part.strip().split("->")
        out.append((frozenset(lhs.strip()), frozenset(rhs.strip())))
    return out


def closed_sets(r, fds):
    """Agreement sets of two-tuple relations that satisfy fds."""
    s = sorted(r)
    for k in range(len(s) + 1):
        for c in combinations(s, k):
            w = frozenset(c)
            if all(not lhs <= w or rhs <= w for lhs, rhs in fds):
                yield w


def bcnf_oracle(part, r, fds):
    """BCNF of a part, from the definition with implication decided by two-tuple relations."""
    ws = list(closed_sets(r, fds))

    def holds(x, a):
        return all(not x <= w or a in w for w in ws)

    attrs = sorted(part)
    for k in range(len(attrs)):
        for c in combinations(attrs, k):
            x = frozenset(c)
            fixed = {a for a in part if holds(x, a)}
            if fixed - x and fixed != set(part):
                return False
    return True


def chase_lossless(r, parts, fds):
    """The tableau chase for FDs: True when some row becomes all distinguished."""
    cols = sorted(r)
    rows = [[("a", c) if c in p else ("b", i, c) for c in cols] for i, p in enumerate(parts)]
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            li = [cols.index(c) for c in lhs]
            for i in range(len(rows)):
                for j in range(i + 1, len(rows)):
                    if all(rows[i][k] == rows[j][k] for k in li):
                        for c in rhs:
                            k = cols.index(c)
                            u, v = rows[i][k], rows[j][k]
                            if u != v:
                                keep, drop = (u, v) if u[0] == "a" or (v[0] != "a" and u < v) else (v, u)
                                for row in rows:
                                    if row[k] == drop:
                                        row[k] = keep
                                changed = True
    return any(all(s[0] == "a" for s in row) for row in rows)


def random_fds(rng, attrs, m):
    out = []
    for _ in range(m):
        lhs = frozenset(rng.sample(attrs, rng.randint(1, min(2, len(attrs)))))
        rhs = frozenset(rng.sample(attrs, rng.randint(1, 2))) - lhs
        if rhs:
            out.append((lhs, rhs))
    return out


def check(r, fds, parts):
    assert frozenset().union(*parts) == r
    for p in parts:
        assert bcnf_oracle(p, r, fds)
    assert chase_lossless(r, parts, fds)


def test_street_city_zip() -> None:
    r = frozenset({"street", "city", "zip"})
    f = [(frozenset({"street", "city"}), frozenset({"zip"})), (frozenset({"zip"}), frozenset({"city"}))]
    parts = bcnf_decomposition(r, f)
    assert sorted(sorted(p) for p in parts) == [["city", "zip"], ["street", "zip"]]
    check(r, f, parts)


def test_worked_example() -> None:
    r = frozenset("ABCDE")
    f = fds_of("A->B, B->C, CD->E")
    parts = bcnf_decomposition(r, f)
    assert sorted("".join(sorted(p)) for p in parts) == ["AB", "ADE", "BC"]
    check(r, f, parts)
    check(r, f, bcnf_decomposition_poly(r, f))


def test_already_bcnf_and_edges() -> None:
    assert bcnf_decomposition(frozenset("ABC"), fds_of("A->BC")) == [frozenset("ABC")]
    assert bcnf_decomposition(frozenset("A"), []) == [frozenset("A")]
    assert bcnf_decomposition(frozenset("AB"), []) == [frozenset("AB")]
    # The pair test is only sufficient for BCNF, so the variant may split a BCNF schema.
    parts = bcnf_decomposition_poly(frozenset("ABC"), fds_of("A->BC"))
    assert sorted("".join(sorted(p)) for p in parts) == ["AB", "AC"]
    check(frozenset("ABC"), fds_of("A->BC"), parts)


def test_random_against_oracles() -> None:
    rng = random.Random(2024)
    for _ in range(500):
        n = rng.randint(2, 6)
        attrs = list("ABCDEF"[:n])
        r = frozenset(attrs)
        f = random_fds(rng, attrs, rng.randint(0, 5))
        check(r, f, bcnf_decomposition(r, f))
        check(r, f, bcnf_decomposition_poly(r, f))
