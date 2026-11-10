# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/total-tardiness-minimization/. The authors are listed in prov/0G2W28.jsonl.

import itertools
import random
from fractions import Fraction

from total_tardiness_minimization import fptas, lawler_decomposition, total_tardiness


def brute_force(p, d):
    return min(total_tardiness(p, d, o) for o in itertools.permutations(range(len(p))))


def test_page_example() -> None:
    p = [7, 8, 3, 1, 6]
    d = [4, 7, 11, 14, 20]
    order, value = lawler_decomposition(p, d)
    assert order == [0, 2, 3, 1, 4] and value == 20 == brute_force(p, d)
    assert total_tardiness(p, d, [0, 1, 2, 3, 4]) == 28  # EDD
    assert total_tardiness(p, d, [3, 2, 4, 0, 1]) == 31  # SPT
    big_p, big_d = [10 * x for x in p], [10 * x for x in d]
    for eps in (Fraction(1), Fraction(1, 2), Fraction(1, 4)):
        assert fptas(big_p, big_d, eps) == ([0, 2, 3, 1, 4], 200)


def test_decomposition_against_brute_force() -> None:
    rng = random.Random(71)
    for _ in range(400):
        n = rng.randint(1, 7)
        p = [rng.randint(0, 5) for _ in range(n)]
        d = [rng.randint(-2, 16) for _ in range(n)]
        order, value = lawler_decomposition(p, d)
        assert sorted(order) == list(range(n))
        assert value == total_tardiness(p, d, order) == brute_force(p, d)


def test_fptas_ratio() -> None:
    rng = random.Random(72)
    for eps in (Fraction(1), Fraction(1, 2), Fraction(1, 4), Fraction(1, 10)):
        for _ in range(60):
            n = rng.randint(1, 6)
            p = [rng.randint(1, 400) for _ in range(n)]
            d = [rng.randint(0, 200 * n) for _ in range(n)]
            order, value = fptas(p, d, eps)
            assert sorted(order) == list(range(n))
            assert value == total_tardiness(p, d, order)
            opt = brute_force(p, d)
            assert opt <= value <= (1 + eps) * opt


def test_bounds_from_edd() -> None:
    rng = random.Random(73)
    for _ in range(300):
        n = rng.randint(1, 7)
        p = [rng.randint(0, 6) for _ in range(n)]
        d = [rng.randint(0, 20) for _ in range(n)]
        edd = sorted(range(n), key=lambda j: d[j])
        t, tmax = 0, 0
        for j in edd:
            t += p[j]
            tmax = max(tmax, t - d[j])
        opt = brute_force(p, d)
        assert tmax <= opt <= n * tmax


def test_edges() -> None:
    assert lawler_decomposition([], []) == ([], 0)
    assert fptas([], [], 1) == ([], 0)
    assert fptas([2, 3], [10, 10], Fraction(1, 2)) == ([0, 1], 0)
