# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karmarkar-karp-bin-packing/. The authors are listed in prov/P2QGMB.jsonl.

import random
from fractions import Fraction
from functools import lru_cache

from karmarkar_karp_bin_packing import config_lp, configurations, covering_lp, geometric_grouping, karmarkar_karp_bin_packing


def brute_opt(sizes):
    n = len(sizes)
    load = [sum((sizes[i] for i in range(n) if m >> i & 1), Fraction(0)) for m in range(2 ** n)]

    @lru_cache(maxsize=None)
    def best(mask):
        if mask == 0:
            return 0
        low = mask & -mask
        rest = mask ^ low
        out = n
        sub = rest
        while True:
            if load[sub | low] <= 1:
                out = min(out, 1 + best(rest ^ sub))
            if sub == 0:
                break
            sub = (sub - 1) & rest
        return out

    return best(2 ** n - 1)


def levels(g):
    lev = 0
    while Fraction(1, 2 ** (lev + 1)) >= g:
        lev += 1
    return lev + 1  # the classes (2^-(l+1), 2^-l] that can hold an item of size >= g


def check(sizes, k):
    sizes = [Fraction(s) for s in sizes]
    trace = []
    bins = karmarkar_karp_bin_packing(sizes, k, trace)
    assert sorted(i for b in bins for i in b) == list(range(len(sizes)))
    assert all(sum(sizes[i] for i in b) <= 1 for b in bins)
    total = sum(sizes, Fraction(0))
    g = min(Fraction(1, 2), 1 / total)
    large = [s for s in sizes if s >= g]
    lp_large = config_lp(large)[0] if large else 0
    opt = brute_opt(sizes) if len(sizes) <= 9 else None
    for t, (size_j, lp_j, lp_r, packed, dropped, lp_n) in enumerate(trace):
        assert lp_r <= lp_j  # rounding up within groups does not raise the LP
        assert packed <= lp_r - lp_n  # the fractional parts still cover the rest
        assert dropped <= k * levels(g)  # one group of size at most k per class
        nxt = trace[t + 1][0] if t + 1 < len(trace) else 0
        if k >= 4:
            assert nxt < size_j / 2 or nxt == 0
    big = len([b for b in bins if any(sizes[i] >= g for i in b)])
    size_d = sum((d for *_, d, _ in trace), Fraction(0))
    assert big <= lp_large + 2 * size_d + 1  # the LP rounds telescope; first fit packs the rest
    assert len(bins) <= max(lp_large + 2 * size_d + 1, total / (1 - g) + 1)
    if opt is not None:
        assert lp_large <= opt <= len(bins)
    return bins, trace, opt


def test_page_example():
    sizes = [Fraction(v, 10) for v in (6, 6, 5, 5, 4, 4, 3, 3, 2)]
    bins, trace, opt = check(sizes, 1)
    assert opt == 4 and len(bins) == 4
    assert bins == [[5, 7, 6], [1, 4], [0, 8], [2, 3]]
    assert trace == [(Fraction(18, 5), Fraction(11, 3), 2, 2, Fraction(8, 5), 0)]
    assert config_lp(sizes)[0] == Fraction(23, 6)


def test_covering_lp_small():
    assert covering_lp([(1, 0), (0, 1), (1, 1)], [2, 3]) == (3, [0, 1, 2])
    assert configurations([Fraction(1, 2), Fraction(1, 3)]) ==[(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (2, 0)]


def test_grouping_dominates():
    sizes = [Fraction(v, 100) for v in (90, 80, 70, 60, 45, 40, 35, 30, 28, 26)]
    rounded, discarded = geometric_grouping(sizes, range(len(sizes)), 1)
    assert discarded == [0, 4, 5]
    assert rounded == {1: Fraction(80, 100), 2: Fraction(70, 100), 3: Fraction(60, 100),
                       6: Fraction(35, 100), 7: Fraction(35, 100), 8: Fraction(28, 100), 9: Fraction(28, 100)}


def test_random_against_brute_force():
    rng = random.Random(1982)
    for it in range(600):
        n = rng.randint(1, 9)
        den = rng.choice([6, 10, 12, 20])
        sizes = [Fraction(rng.randint(1, den), den) for _ in range(n)]
        check(sizes, rng.choice([1, 1, 2, 4]))


def test_larger_without_brute_force():
    rng = random.Random(7)
    for _ in range(20):
        sizes = [Fraction(rng.randint(3, 10), 10) for _ in range(rng.randint(10, 16))]
        check(sizes, 4)
