# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knapsack-fptas/. The authors are listed in prov/8ZRYG2.jsonl.

import itertools
import random
from fractions import Fraction

from knapsack_fptas import knapsack_fptas, scale_profits


def brute_force(profits: list[int], weights: list[int], capacity: int) -> int:
    best = 0
    n = len(profits)
    for r in range(n + 1):
        for c in itertools.combinations(range(n), r):
            if sum(weights[i] for i in c) <= capacity:
                best = max(best, sum(profits[i] for i in c))
    return best


def test_example() -> None:
    p = [56, 22, 12, 45, 58, 53]
    w = [2, 7, 3, 8, 9, 6]
    kept, scaled, k = scale_profits(p, w, 15, Fraction(1, 2))
    assert kept == [0, 1, 2, 3, 4, 5]
    assert k == Fraction(29, 6)
    assert scaled == [11, 4, 2, 9, 12, 10]
    s = knapsack_fptas(p, w, 15, Fraction(1, 2))
    assert s == [0, 2, 4]
    assert sum(p[i] for i in s) == 126
    assert brute_force(p, w, 15) == 131


def test_edges() -> None:
    assert knapsack_fptas([], [], 10, Fraction(1, 2)) == []
    assert knapsack_fptas([5, 7], [11, 12], 10, Fraction(1, 2)) == []
    assert knapsack_fptas([5], [10], 10, Fraction(1, 2)) == [0]
    assert knapsack_fptas([3, 4, 5], [1, 1, 1], 3, Fraction(1, 3)) == [0, 1, 2]
    assert knapsack_fptas([9, 9, 9], [5, 5, 5], 10, 1) in ([0, 1], [0, 2], [1, 2])
    # an item that does not fit is never chosen, even with a large profit
    assert knapsack_fptas([1000, 1, 1], [20, 1, 1], 5, Fraction(1, 2)) == [1, 2]


def test_ratio_and_table_size() -> None:
    rng = random.Random(2024)
    for _ in range(600):
        n = rng.randint(1, 8)
        p = [rng.randint(1, 100) for _ in range(n)]
        w = [rng.randint(1, 30) for _ in range(n)]
        cap = rng.randint(0, 60)
        opt = brute_force(p, w, cap)
        for eps in (Fraction(1), Fraction(1, 2), Fraction(1, 5), Fraction(1, 20)):
            s = knapsack_fptas(p, w, cap, eps)
            assert len(set(s)) == len(s)
            assert sum(w[i] for i in s) <= cap
            alg = sum(p[i] for i in s)
            assert alg >= (1 - eps) * opt
            kept, scaled, k = scale_profits(p, w, cap, eps)
            if kept:
                m = len(kept)
                assert all(x <= m / eps for x in scaled)
                assert sum(scaled) <= m * int(m / eps)
                # the additive loss of the proof: OPT - ALG <= n K
                assert opt - alg <= m * k


def test_small_eps_is_exact() -> None:
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(1, 7)
        p = [rng.randint(1, 20) for _ in range(n)]
        w = [rng.randint(1, 10) for _ in range(n)]
        cap = rng.randint(1, 30)
        fits = [p[i] for i in range(n) if w[i] <= cap]
        if not fits:
            continue
        # eps < 1 / (n * max p) makes n K < 1, so the integer optimum is found
        eps = Fraction(1, n * max(fits) + 1)
        s = knapsack_fptas(p, w, cap, eps)
        assert sum(p[i] for i in s) == brute_force(p, w, cap)
