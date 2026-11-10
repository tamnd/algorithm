# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/first-fit-bin-packing/. The authors are listed in prov/2VPCK0.jsonl.

import math
import random
from fractions import Fraction as F

from first_fit_bin_packing import first_fit_bin_packing


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


def weight(a):
    """The weight function of the 17/10 proof."""
    if a <= F(1, 6):
        bonus = F(0)
    elif a <= F(1, 3):
        bonus = F(3, 5) * (a - F(1, 6))
    elif a <= F(1, 2):
        bonus = F(1, 10)
    else:
        bonus = F(2, 5)
    return F(6, 5) * a + bonus


def check_feasible(s, bins, capacity=1):
    assert sorted(i for b in bins for i in b) == list(range(len(s)))
    for b in bins:
        assert b and sum(s[i] for i in b) <= capacity


def test_example():
    s = [F(x, 10) for x in (2, 5, 4, 7, 1, 3, 8)]
    assert first_fit_bin_packing(s) == [[0, 1, 4], [2, 5], [3], [6]]
    assert brute_opt(s) == 3


def test_edges():
    assert first_fit_bin_packing([]) == []
    assert first_fit_bin_packing([1, 1]) == [[0], [1]]
    assert first_fit_bin_packing([3, 8, 7, 2], capacity=10) == [[0, 2], [1, 3]]
    try:
        first_fit_bin_packing([0])
    except ValueError:
        pass
    else:
        raise AssertionError("an item of size 0 must be rejected")


def test_against_brute_force():
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randrange(1, 10)
        s = [F(rng.randrange(1, 21), 20) for _ in range(n)]
        bins = first_fit_bin_packing(s)
        check_feasible(s, bins)
        assert bins == naive_first_fit(s)
        opt = brute_opt(s)
        assert len(bins) <= math.floor(F(17, 10) * opt)
        assert len(bins) <= 2 * math.ceil(sum(s)) - 1
        loads = [sum(s[i] for i in b) for b in bins]
        assert sum(1 for x in loads if x <= F(1, 2)) <= 1
        # each item does not fit into the free space of any earlier bin
        for j, b in enumerate(bins):
            for i in b:
                assert all(s[i] > 1 - loads[e] for e in range(j))


def test_weight_argument():
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randrange(1, 40)
        s = [F(rng.randrange(1, 61), 60) for _ in range(n)]
        bins = first_fit_bin_packing(s)
        total_weight = sum(weight(x) for x in s)
        # the proof shows W > FF - 2.9 and W <= 1.7 OPT
        assert total_weight > len(bins) - F(29, 10)


def test_five_thirds_family():
    # 6m items of 1/7 + e, then 6m of 1/3 + e, then 6m of 1/2 + e: FF = 10m, OPT = 6m.
    e = F(1, 1000)
    for m in range(1, 6):
        s = [F(1, 7) + e] * (6 * m) + [F(1, 3) + e] * (6 * m) + [F(1, 2) + e] * (6 * m)
        assert len(first_fit_bin_packing(s)) == 10 * m
        # one item of each kind per bin gives 6m bins, and the 6m items above 1/2 need 6m bins
        assert F(1, 7) + F(1, 3) + F(1, 2) + 3 * e <= 1
        assert sum(1 for x in s if x > F(1, 2)) == 6 * m


def test_lemma_a_on_feasible_sets():
    # any set of total size at most 1 has weight at most 17/10
    rng = random.Random(3)
    for _ in range(2000):
        s, load = [], F(0)
        while True:
            x = F(rng.randrange(1, 61), 60)
            if load + x > 1:
                break
            s.append(x)
            load += x
        assert sum(weight(x) for x in s) <= F(17, 10)
    near = [F(1, 2) + F(1, 100), F(1, 3) + F(1, 200), F(1, 6) - F(1, 50)]
    assert sum(near) <= 1
    assert F(16, 10) < sum(weight(x) for x in near) <= F(17, 10)
