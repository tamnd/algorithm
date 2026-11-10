# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mcnaughton-wrap-around/. The authors are listed in prov/FQ9V3K.jsonl.

import itertools
import random
from fractions import Fraction

from mcnaughton_wrap_around import mcnaughton_wrap_around


def check_feasible(p, m, c, pieces) -> None:
    """Each machine runs one piece at a time, no job runs on two machines at once,
    every piece lies in [0, c], and each job gets exactly p_j units."""
    got = [Fraction(0)] * len(p)
    for j, i, s, e in pieces:
        assert 0 <= i < m and 0 <= s < e <= c
        got[j] += e - s
    assert got == [Fraction(x) for x in p]
    for a, b in itertools.combinations(pieces, 2):
        overlap = a[2] < b[3] and b[2] < a[3]
        if a[1] == b[1] or a[0] == b[0]:
            assert not overlap


def nonpreemptive_opt(p, m) -> int:
    if not p:
        return 0
    best = None
    for rest in itertools.product(range(m), repeat=len(p) - 1):
        load = [0] * m
        for x, i in zip(p, (0,) + rest):
            load[i] += x
        best = max(load) if best is None else min(best, max(load))
    return best


def test_example() -> None:
    p = [4, 3, 5, 2, 4, 3]
    c, pieces = mcnaughton_wrap_around(p, 3)
    assert c == 7
    assert pieces == [
        (0, 0, 0, 4), (1, 0, 4, 7), (2, 1, 0, 5), (3, 1, 5, 7),
        (4, 2, 0, 4), (5, 2, 4, 7),
    ]
    p = [5, 4, 4, 3, 2, 2]
    c, pieces = mcnaughton_wrap_around(p, 3)
    assert c == Fraction(20, 3)
    check_feasible(p, 3, c, pieces)
    assert nonpreemptive_opt(p, 3) == 7


def test_edges() -> None:
    assert mcnaughton_wrap_around([], 2) == (0, [])
    assert mcnaughton_wrap_around([5], 3) == (5, [(0, 0, 0, 5)])
    assert mcnaughton_wrap_around([0, 2], 1) == (2, [(1, 0, 0, 2)])
    c, pieces = mcnaughton_wrap_around([9, 1, 1], 2)
    assert c == 9 and pieces[0] == (0, 0, 0, 9)


def test_random() -> None:
    rng = random.Random(51)
    for _ in range(600):
        m = rng.randrange(1, 5)
        p = [rng.randrange(0, 12) for _ in range(rng.randrange(1, 9))]
        c, pieces = mcnaughton_wrap_around(p, m)
        check_feasible(p, m, c, pieces)
        assert c == max(max(p), Fraction(sum(p), m))
        split = {j for j, *_ in pieces if sum(1 for q in pieces if q[0] == j) > 1}
        assert len(split) <= m - 1
        assert all(sum(1 for q in pieces if q[0] == j) <= 2 for j in range(len(p)))
        if len(p) <= 6 and m <= 3:
            assert c <= nonpreemptive_opt(p, m) < 2 * c or c == 0


def test_fractions() -> None:
    p = [Fraction(1, 3), Fraction(1, 2), Fraction(5, 6), Fraction(1, 1)]
    c, pieces = mcnaughton_wrap_around(p, 2)
    assert c == Fraction(4, 3)
    check_feasible(p, 2, c, pieces)
