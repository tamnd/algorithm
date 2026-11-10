# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-fit-bin-packing/. The authors are listed in prov/Z0DHY7.jsonl.

import math
import random
from fractions import Fraction as F

from best_fit_bin_packing import best_fit_bin_packing


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


def naive_best_fit(s):
    bins, loads = [], []
    for i, x in enumerate(s):
        j = -1
        for e, load in enumerate(loads):
            if load + x <= 1 and (j < 0 or load > loads[j]):
                j = e
        if j < 0:
            bins.append([i])
            loads.append(x)
        else:
            bins[j].append(i)
            loads[j] += x
    return bins


def naive_first_fit(s):
    bins, loads = [], []
    for i, x in enumerate(s):
        for j, load in enumerate(loads):
            if load + x <= 1:
                bins[j].append(i)
                loads[j] += x
                break
        else:
            bins.append([i])
            loads.append(x)
    return bins


def check_feasible(s, bins, capacity=1):
    assert sorted(i for b in bins for i in b) == list(range(len(s)))
    for b in bins:
        assert b and sum(s[i] for i in b) <= capacity


def tenths(*xs):
    return [F(x, 10) for x in xs]


def test_example():
    s = tenths(2, 5, 4, 7, 1, 3, 8)
    assert best_fit_bin_packing(s) == [[0, 1, 4], [2], [3, 5], [6]]
    assert brute_opt(s) == 3


def test_edges():
    assert best_fit_bin_packing([]) == []
    assert best_fit_bin_packing([1]) == [[0]]
    # the item 2 goes to the fuller bin (load 8), not to the first bin (load 3)
    assert best_fit_bin_packing([3, 8, 2], capacity=10) == [[0], [1, 2]]
    try:
        best_fit_bin_packing([F(-1, 2)])
    except ValueError:
        pass
    else:
        raise AssertionError("a negative size must be rejected")


def test_against_brute_force():
    rng = random.Random(13)
    for _ in range(300):
        n = rng.randrange(1, 10)
        s = [F(rng.randrange(1, 21), 20) for _ in range(n)]
        bins = best_fit_bin_packing(s)
        check_feasible(s, bins)
        assert bins == naive_best_fit(s)
        opt = brute_opt(s)
        assert len(bins) <= math.floor(F(17, 10) * opt)
        assert len(bins) <= 2 * math.ceil(sum(s)) - 1
        loads = [sum(s[i] for i in b) for b in bins]
        assert sum(1 for x in loads if x <= F(1, 2)) <= 1


def test_first_fit_and_best_fit_differ():
    s = tenths(5, 6, 9, 2, 3, 6, 4, 4)
    assert (len(naive_first_fit(s)), len(best_fit_bin_packing(s)), brute_opt(s)) == (4, 5, 4)
    s = tenths(3, 8, 9, 3, 8, 8, 2, 4)
    assert (len(naive_first_fit(s)), len(best_fit_bin_packing(s)), brute_opt(s)) == (6, 5, 5)


def test_five_thirds_family():
    e = F(1, 1000)
    for m in range(1, 6):
        s = [F(1, 7) + e] * (6 * m) + [F(1, 3) + e] * (6 * m) + [F(1, 2) + e] * (6 * m)
        assert len(best_fit_bin_packing(s)) == 10 * m
        assert F(1, 7) + F(1, 3) + F(1, 2) + 3 * e <= 1
        assert sum(1 for x in s if x > F(1, 2)) == 6 * m


def test_large_random_matches_naive():
    rng = random.Random(17)
    for _ in range(20):
        s = [F(rng.randrange(1, 101), 100) for _ in range(200)]
        assert best_fit_bin_packing(s) == naive_best_fit(s)
