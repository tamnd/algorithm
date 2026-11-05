# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dinkelbach-algorithm/. The authors are listed in prov/VSSWCG.jsonl.

import itertools
import math
import random
from fractions import Fraction

from dinkelbach_algorithm import best_ratio_subset, dinkelbach, dinkelbach_trace

EXAMPLE = [(8, 1), (4, 2), (9, 4), (2, 2), (9, 5)]


def subset_oracle(items, k):
    def num(s):
        return sum(items[i][0] for i in s)

    def den(s):
        return sum(items[i][1] for i in s)

    def min_param(lam):
        order = sorted(range(len(items)), key=lambda i: (items[i][0] - lam * items[i][1], i))
        return tuple(sorted(order[:k]))

    return min_param, num, den


def brute(items, k):
    return min(
        Fraction(sum(items[i][0] for i in s), sum(items[i][1] for i in s))
        for s in itertools.combinations(range(len(items)), k)
    )


def test_example() -> None:
    s, lam = best_ratio_subset(EXAMPLE, 2)
    assert s == (1, 3)
    assert lam == Fraction(3, 2)


def test_example_trace() -> None:
    tr = dinkelbach_trace(*subset_oracle(EXAMPLE, 2), (0, 1))
    assert [t[0] for t in tr] == [(0, 1), (2, 4), (3, 4), (1, 3)]
    assert [t[1] for t in tr] == [Fraction(4), Fraction(2), Fraction(11, 7), Fraction(3, 2)]
    assert [t[2] for t in tr] == [Fraction(-18), Fraction(-3), Fraction(-2, 7), Fraction(0)]


def test_random_against_brute_force_and_invariants() -> None:
    rng = random.Random(5)
    for _ in range(1500):
        n = rng.randrange(1, 8)
        k = rng.randrange(1, n + 1)
        items = [(rng.randrange(-20, 21), rng.randrange(1, 10)) for _ in range(n)]
        s, lam = best_ratio_subset(items, k)
        assert lam == brute(items, k)
        tr = dinkelbach_trace(*subset_oracle(items, k), tuple(range(k)))
        lams = [t[1] for t in tr]
        fs = [t[2] for t in tr]
        dens = [sum(items[i][1] for i in t[0]) for t in tr]
        # the ratios strictly decrease, and F is negative until the last step
        assert all(a > b for a, b in zip(lams, lams[1:]))
        assert all(f < 0 for f in fs[:-1]) and fs[-1] == 0
        # from the first Newton step on, the denominators do not increase
        assert all(a >= b for a, b in zip(dens[1:], dens[2:]))
        # |F_k| / |F_{k-1}| + D_{k+1} / D_k <= 1
        for j in range(1, len(tr) - 1):
            assert abs(fs[j]) / abs(fs[j - 1]) + Fraction(dens[j + 1], dens[j]) <= 1
        # the O(log U) bound with U the largest |sum c| or sum t
        u = max(sum(abs(c) for c, _ in items), sum(t for _, t in items), 2)
        assert len(tr) <= 4 * math.log2(u) + 4


def test_generic_oracle_on_explicit_set() -> None:
    sols = [(3, 2), (5, 4), (7, 6), (1, 1), (9, 10)]
    best = min(sols, key=lambda p: Fraction(p[0], p[1]))

    def min_param(lam):
        return min(sols, key=lambda p: p[0] - lam * p[1])

    x, lam = dinkelbach(min_param, lambda p: p[0], lambda p: p[1], sols[0])
    assert lam == Fraction(best[0], best[1])
    assert Fraction(x[0], x[1]) == lam
