# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/land-doig-algorithm/. The authors are listed in prov/XVSXFR.jsonl.

import itertools
import random
from fractions import Fraction

from land_doig_algorithm import land_doig, solve_lp


def brute(c, a, b, box):
    best = None
    for x in itertools.product(*(range(u + 1) for u in box)):
        if all(sum(r[j] * x[j] for j in range(len(x))) <= bi for r, bi in zip(a, b)):
            v = sum(cj * xj for cj, xj in zip(c, x))
            if best is None or v > best:
                best = v
    return best


def test_example_of_the_page() -> None:
    stats: dict[str, int] = {}
    trace: list = []
    z, x = land_doig([5, 4], [[6, 4], [1, 2]], [24, 6], stats=stats, trace=trace)
    assert z == 20 and x == [4, 0]
    assert stats == {"lps": 7, "expanded": 2}
    assert [v for _, v in trace] == [21, Fraction(62, 3), 20]


def test_lp_solver() -> None:
    assert solve_lp([5, 4], [[6, 4], [1, 2]], [24, 6]) == ("optimal", [3, Fraction(3, 2)], 21)
    assert solve_lp([1], [[1], [-1]], [1, -2])[0] == "infeasible"
    assert solve_lp([1, 1], [[1, -1]], [1])[0] == "unbounded"
    assert solve_lp([-1], [[-1]], [-2]) == ("optimal", [2], -2)


def test_edges() -> None:
    # integer LP optimum: the root is solved by its LP
    assert land_doig([1, 1], [[1, 0], [0, 1]], [2, 3]) == (5, [2, 3])
    # no integer point: 0.2 <= x <= 0.8
    assert land_doig([1], [[1], [-1]], [Fraction(4, 5), Fraction(-1, 5)]) == (None, None)
    # infeasible LP
    assert land_doig([1], [[1], [-1]], [1, -2]) == (None, None)
    # mixed: only x0 integer
    z, x = land_doig([1, 1], [[2, 0], [0, 2], [1, 1]], [3, 3, 5], integer=[0])
    assert z == Fraction(5, 2) and x == [1, Fraction(3, 2)]


def test_random_against_brute_force() -> None:
    rng = random.Random(1910129)
    for _ in range(500):
        n = rng.randint(1, 3)
        box = [rng.randint(0, 4) for _ in range(n)]
        a = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        b = list(box)
        for _ in range(rng.randint(1, 3)):
            a.append([rng.randint(-3, 6) for _ in range(n)])
            b.append(rng.randint(-2, 12))
        c = [rng.randint(-5, 9) for _ in range(n)]
        z, x = land_doig(c, a, b)
        expect = brute(c, a, b, box)
        assert z == expect
        if x is not None:
            assert all(v.denominator == 1 for v in x)
            assert all(sum(r[j] * x[j] for j in range(n)) <= bi for r, bi in zip(a, b))
            assert sum(cj * xj for cj, xj in zip(c, x)) == z
