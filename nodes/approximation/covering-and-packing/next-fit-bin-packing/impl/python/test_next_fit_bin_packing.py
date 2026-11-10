# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/next-fit-bin-packing/. The authors are listed in prov/G0STDP.jsonl.

import math
import random
from fractions import Fraction as F

from next_fit_bin_packing import next_fit_bin_packing


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


def test_example():
    s = [F(x, 10) for x in (2, 5, 4, 7, 1, 3, 8)]
    bins = next_fit_bin_packing(s)
    assert bins == [[0, 1], [2], [3, 4], [5], [6]]
    assert brute_opt(s) == 3


def test_edges():
    assert next_fit_bin_packing([]) == []
    assert next_fit_bin_packing([1]) == [[0]]
    assert next_fit_bin_packing([F(1, 2), F(1, 2)]) == [[0, 1]]
    assert next_fit_bin_packing([3, 5, 2, 7], capacity=10) == [[0, 1, 2], [3]]
    try:
        next_fit_bin_packing([F(3, 2)])
    except ValueError:
        pass
    else:
        raise AssertionError("an item larger than the capacity must be rejected")


def test_against_brute_force():
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randrange(1, 10)
        s = [F(rng.randrange(1, 13), 12) for _ in range(n)]
        bins = next_fit_bin_packing(s)
        check_feasible(s, bins)
        opt = brute_opt(s)
        size_bound = math.ceil(sum(s))
        assert size_bound <= opt
        assert len(bins) <= 2 * size_bound - 1 <= 2 * opt - 1
        # each pair of consecutive bins holds more than one unit
        loads = [sum(s[i] for i in b) for b in bins]
        assert all(loads[j] + loads[j + 1] > 1 for j in range(len(loads) - 1))


def test_tight_family():
    # f, B, f, B, ..., f with f = 1/(2k) and B = 1 - 1/(4k): NF = 2k - 1 and OPT = k.
    for k in range(1, 9):
        f, big = F(1, 2 * k), 1 - F(1, 4 * k)
        s = [f] + [big, f] * (k - 1)
        assert len(next_fit_bin_packing(s)) == 2 * k - 1
        # k - 1 bins hold one big item each, one bin holds all the small items
        assert k * f <= 1 and sum(s) > k - 1
        if len(s) <= 11:
            assert brute_opt(s) == k


def test_ratio_tends_to_two():
    # (1/2, eps) repeated 2m times with eps = 1/(2m): NF = 2m and OPT = m + 1.
    for m in range(1, 6):
        s = [F(1, 2), F(1, 2 * m)] * (2 * m)
        assert len(next_fit_bin_packing(s)) == 2 * m
        assert math.ceil(sum(s)) == m + 1
        if len(s) <= 12:
            assert brute_opt(s) == m + 1
