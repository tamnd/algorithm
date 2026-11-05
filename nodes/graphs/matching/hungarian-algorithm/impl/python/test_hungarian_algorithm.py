# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hungarian-algorithm/. The authors are listed in prov/N33C44.jsonl.

import math
import random
from fractions import Fraction
from itertools import permutations

from hungarian_algorithm import hungarian_algorithm


def brute(cost):
    """Oracle: the least total over all injective maps of rows to columns, or None."""
    n = len(cost)
    if n == 0:
        return 0
    m = len(cost[0])
    best = None
    for cols in permutations(range(m), n):
        t = sum(cost[i][cols[i]] for i in range(n))
        if t != math.inf and (best is None or t < best):
            best = t
    return best


def check(cost, res):
    exp = brute(cost)
    if exp is None:
        assert res is None
        return
    total, assign = res
    assert len(set(assign)) == len(assign)
    assert sum(cost[i][assign[i]] for i in range(len(cost))) == total
    assert total == exp


EXAMPLE = [[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]]


def test_example():
    assert hungarian_algorithm(EXAMPLE) == (13, [1, 0, 2, 3])


def test_empty_and_single():
    assert hungarian_algorithm([]) == (0, [])
    assert hungarian_algorithm([[5]]) == (5, [0])
    assert hungarian_algorithm([[math.inf]]) is None


def test_no_perfect_matching():
    inf = math.inf
    # rows 0 and 1 can only use column 0
    cost = [[3, inf, inf], [4, inf, inf], [1, 2, 3]]
    assert hungarian_algorithm(cost) is None
    cost = [[inf, inf], [inf, inf]]
    assert hungarian_algorithm(cost) is None


def test_missing_edges_avoided():
    inf = math.inf
    cost = [[1, inf, 100], [inf, 1, inf], [1, inf, inf]]
    assert hungarian_algorithm(cost) == (102, [2, 1, 0])


def test_rectangular_negative_equal_and_fractions():
    check([[4, -1, 3], [-2, 0, 5]], hungarian_algorithm([[4, -1, 3], [-2, 0, 5]]))
    assert hungarian_algorithm([[7] * 4 for _ in range(4)])[0] == 28
    f = [[Fraction(1, 3), Fraction(1, 2)], [Fraction(1, 5), Fraction(1, 7)]]
    assert hungarian_algorithm(f)[0] == Fraction(1, 3) + Fraction(1, 7)
    big = 2**62
    assert hungarian_algorithm([[big, big - 1], [big - 1, big]])[0] == 2 * big - 2


def test_float_costs():
    rng = random.Random(77)
    for _ in range(100):
        n = rng.randint(1, 5)
        cost = [[rng.uniform(-10, 10) for _ in range(n)] for _ in range(n)]
        total, _ = hungarian_algorithm(cost)
        assert math.isclose(total, brute(cost), abs_tol=1e-9)


def test_random_against_brute_force():
    rng = random.Random(9031)
    for _ in range(700):
        n = rng.randint(0, 5)
        m = rng.randint(n, 6) if n else 0
        cost = [[rng.choice([math.inf] + list(range(-5, 10))) if rng.random() < 0.2 else rng.randint(-5, 9)
                 for _ in range(m)] for _ in range(n)]
        check(cost, hungarian_algorithm(cost))
