# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bin-packing-aptas/. The authors are listed in prov/SC1BGZ.jsonl.

import random
from fractions import Fraction as F

from bin_packing_aptas import bin_packing_aptas, exact_by_counts


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


def full_bins(rng, k, parts=(2, 3, 4), denom=60):
    """A shuffled list made of k bins of load exactly 1, so OPT = k."""
    s = []
    for _ in range(k):
        m = rng.choice(parts)
        cuts = sorted(rng.sample(range(1, denom), m - 1))
        s += [F(b - a, denom) for a, b in zip([0] + cuts, cuts + [denom])]
    rng.shuffle(s)
    return s


def test_exact_by_counts():
    # sizes 1/2, 1/3, 1/6, two of each: total 2, two bins suffice
    plan = exact_by_counts([F(1, 2), F(1, 3), F(1, 6)], [2, 2, 2])
    assert len(plan) == 2
    assert sorted(t for b in plan for t in b) == [0, 0, 1, 1, 2, 2]
    # with three items 1/3 and one 1/6 the total is 13/6, so three bins are needed
    assert len(exact_by_counts([F(1, 2), F(1, 3), F(1, 6)], [2, 3, 1])) == 3


def test_edges():
    assert bin_packing_aptas([], 1) == []
    assert bin_packing_aptas([F(1, 10)] * 5, 1) == [[0, 1, 2, 3, 4]]
    assert len(bin_packing_aptas([6, 4, 5, 5], 1, capacity=10)) == 2
    for bad in (0, F(3, 2)):
        try:
            bin_packing_aptas([F(1, 2)], bad)
        except ValueError:
            pass
        else:
            raise AssertionError("eps outside (0, 1] must be rejected")


def test_against_brute_force():
    rng = random.Random(23)
    for _ in range(150):
        n = rng.randrange(1, 11)
        s = [F(rng.randrange(1, 25), 24) for _ in range(n)]
        opt = brute_opt(s)
        for eps in (F(1, 2), F(2, 3), F(1)):
            bins = bin_packing_aptas(s, eps)
            check_feasible(s, bins)
            assert len(bins) <= (1 + eps) * opt + 1


def test_grouping_with_known_opt():
    # lists with OPT = k known by construction; large enough to use the grouping step
    rng = random.Random(29)
    for _ in range(12):
        k = rng.randrange(6, 11)
        s = full_bins(rng, k)
        bins = bin_packing_aptas(s, 1)
        check_feasible(s, bins)
        assert len(bins) <= 2 * k + 1
        bins = bin_packing_aptas(s, F(2, 3))
        check_feasible(s, bins)
        assert len(bins) <= F(5, 3) * k + 1


def test_rounded_instance_is_dominated():
    # OPT(J) <= OPT(large items): checked by solving both exactly
    rng = random.Random(31)
    delta = F(1, 3)
    for _ in range(20):
        large = sorted((F(rng.randrange(20, 61), 60) for _ in range(rng.randrange(9, 13))), reverse=True)
        k = int(delta * delta * len(large))
        groups = [large[a:a + k] for a in range(0, len(large), k)]
        rounded = [g[0] for g in groups[1:] for _ in g]
        assert brute_opt(rounded) <= brute_opt(large)
        assert k <= delta * brute_opt(large)
