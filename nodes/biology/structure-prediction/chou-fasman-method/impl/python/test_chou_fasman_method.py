# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chou-fasman-method/. The authors are listed in prov/Q8MXAA.jsonl.

import random
from fractions import Fraction

from chou_fasman_method import HELIX, PROPENSITY, STRAND, chou_fasman, extend, nuclei


def mean(xs):
    return Fraction(sum(xs), len(xs))


def reference(seq, table):
    """The same rules, written from their definitions with exact means."""
    pa = [table[c][0] for c in seq]
    pb = [table[c][1] for c in seq]
    n = len(seq)

    def accepted(p, q, rule):
        window, need, former, accept = rule
        segs = []
        for s0 in range(n - window + 1):
            if len([v for v in p[s0:s0 + window] if v > former]) < need:
                continue
            e0 = s0 + window
            # The extended segment is the widest [s, e) whose new end windows all have mean >= 100.
            s = min(t for t in range(s0 + 1) if all(mean(p[u:u + 4]) >= 100 for u in range(t, s0)))
            e = max(t for t in range(e0, n + 1) if all(mean(p[u - 3:u + 1]) >= 100 for u in range(e0, t)))
            if mean(p[s:e]) > accept and mean(p[s:e]) > mean(q[s:e]):
                segs.append((s, e))
        return segs

    h = {r for s, e in accepted(pa, pb, HELIX) for r in range(s, e)}
    b = {r for s, e in accepted(pb, pa, STRAND) for r in range(s, e)}
    out = []
    for r in range(n):
        if r in h and r in b:
            lo = r
            while lo - 1 in h and lo - 1 in b:
                lo -= 1
            hi = r
            while hi + 1 in h and hi + 1 in b:
                hi += 1
            out.append("H" if sum(pa[lo:hi + 1]) > sum(pb[lo:hi + 1]) else "E")
        else:
            out.append("H" if r in h else "E" if r in b else "C")
    return "".join(out)


def test_example() -> None:
    s = "ENSESAVNEYVT"
    pa = [PROPENSITY[c][0] for c in s]
    pb = [PROPENSITY[c][1] for c in s]
    assert nuclei(pa, 6, 4, 103) == [3, 5]
    assert nuclei(pb, 5, 3, 100) == [6, 7]
    assert extend(pa, 3, 9) == (2, 9)
    assert extend(pa, 5, 11) == (5, 12)
    assert extend(pb, 6, 11) == (6, 12)
    assert chou_fasman(s) == "CCHHHHHHHEEE"


def test_edges() -> None:
    assert chou_fasman("") == ""
    assert chou_fasman("AEL") == "CCC"
    assert chou_fasman("GGGGGGGGGG") == "C" * 10
    assert chou_fasman("AAAAAA") == "HHHHHH"
    assert chou_fasman("VVVVV") == "EEEEE"


def test_against_reference() -> None:
    rng = random.Random(1974)
    letters = sorted(PROPENSITY)
    for _ in range(400):
        s = "".join(rng.choice(letters) for _ in range(rng.randint(0, 25)))
        assert chou_fasman(s) == reference(s, PROPENSITY), s
    for _ in range(200):
        table = {c: (rng.randint(50, 160), rng.randint(40, 170)) for c in "ABCD"}
        s = "".join(rng.choice("ABCD") for _ in range(rng.randint(0, 20)))
        assert chou_fasman(s, table) == reference(s, table), s
