# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/first-fit-decreasing/. The authors are listed in prov/Q1QQRH.jsonl.

import math
import random
from fractions import Fraction as F

from first_fit_decreasing import first_fit_decreasing


def brute_opt(s):
    """Least number of unit bins, by a DP over subsets (min bins, then min last load)."""
    n = len(s)
    best = [(n + 1, F(0))] * (1 << n)
    best[0] = (0, F(1))
    for m in range(1 << n):
        b, load = best[m]
        if b > n:
            continue
        for i in range(n):
            if m >> i & 1:
                continue
            c = (b, load + s[i]) if load + s[i] <= 1 else (b + 1, s[i])
            if c < best[m | 1 << i]:
                best[m | 1 << i] = c
    return best[-1][0]


def check_feasible(s, bins, capacity=1):
    assert sorted(i for b in bins for i in b) == list(range(len(s)))
    for b in bins:
        assert b and sum(s[i] for i in b) <= capacity


def four_types(na, nb, nc, nd, e=F(1, 100)):
    q = F(1, 4)
    return [F(1, 2) + e] * na + [q + 2 * e] * nb + [q + e] * nc + [q - 2 * e] * nd


def test_example():
    s = [F(x, 10) for x in (2, 5, 4, 7, 1, 3, 8)]
    assert first_fit_decreasing(s) == [[6, 0], [3, 5], [1, 2, 4]]
    assert brute_opt(s) == 3


def test_edges():
    assert first_fit_decreasing([]) == []
    assert first_fit_decreasing([F(1, 3)] * 3) == [[0, 1, 2]]
    try:
        first_fit_decreasing([2])
    except ValueError:
        pass
    else:
        raise AssertionError("an item larger than the capacity must be rejected")


def test_partition_instance():
    # OPT = 2 with {4, 2, 2} and {3, 3, 2}, but FFD packs [4 3] [3 2 2] [2]
    s = [4, 3, 3, 2, 2, 2]
    bins = first_fit_decreasing(s, capacity=8)
    assert [[s[i] for i in b] for b in bins] == [[4, 3], [3, 2, 2], [2]]
    assert len(bins) == F(3, 2) * 2


def test_against_brute_force():
    rng = random.Random(19)
    for _ in range(300):
        n = rng.randrange(1, 11)
        s = [F(rng.randrange(1, 25), 24) for _ in range(n)]
        bins = first_fit_decreasing(s)
        check_feasible(s, bins)
        opt = brute_opt(s)
        assert len(bins) <= F(11, 9) * opt + F(6, 9)
        assert len(bins) <= F(3, 2) * opt


def test_asymptotic_family():
    # 6m, 6m, 6m, 12m items of the four types: FFD = 11m and OPT = 9m
    for m in range(1, 5):
        s = four_types(6 * m, 6 * m, 6 * m, 12 * m)
        assert len(first_fit_decreasing(s)) == 11 * m
        assert sum(s) == 9 * m  # the size bound gives OPT >= 9m
        # bins {a, c, d} and {b, b, d, d} give 6m + 3m bins
        a, b, c, d = sorted(set(s), reverse=True)
        assert a + c + d <= 1 and 2 * b + 2 * d <= 1


def test_additive_tight_family():
    # N = 6m + 4 items of each of the first three types and 2N of the last:
    # OPT = 9m + 6 and FFD = 11m + 8 = 11/9 OPT + 6/9
    for m in range(0, 4):
        n_ = 6 * m + 4
        s = four_types(n_, n_, n_, 2 * n_)
        opt = 9 * m + 6
        assert sum(s) == opt
        assert len(first_fit_decreasing(s)) == 11 * m + 8 == F(11, 9) * opt + F(6, 9)
