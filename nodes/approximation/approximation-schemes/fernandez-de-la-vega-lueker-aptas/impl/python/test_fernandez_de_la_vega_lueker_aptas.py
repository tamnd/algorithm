# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fernandez-de-la-vega-lueker-aptas/. The authors are listed in prov/SZNNHA.jsonl.

import random
from fractions import Fraction
from math import ceil, floor

from fernandez_de_la_vega_lueker_aptas import configuration_lp, exact_pack, fernandez_de_la_vega_lueker_aptas


def brute_opt(sizes):
    """The least number of bins, by a subset DP that keeps (bins, load of the last bin) as small as possible."""
    n = len(sizes)
    if n == 0:
        return 0
    best = [None] * (1 << n)
    best[0] = (1, Fraction(0))
    for mask in range(1 << n):
        b, load = best[mask]
        for i in range(n):
            if mask >> i & 1:
                continue
            nxt = (b, load + sizes[i]) if load + sizes[i] <= 1 else (b + 1, sizes[i])
            t = mask | 1 << i
            if best[t] is None or nxt < best[t]:
                best[t] = nxt
    return best[-1][0]


def check_packing(sizes, bins):
    flat = sorted(j for b in bins for j in b)
    assert flat == list(range(len(sizes)))
    assert all(b and sum(Fraction(sizes[j]) for j in b) <= 1 for b in bins)


def check_small_items(s, bins, delta):
    """If first fit opened a bin for a small item, every bin but the last one has load above 1 - delta."""
    opened = [b for b in bins if all(s[j] < delta for j in b)]
    if opened:
        loads = [sum(s[j] for j in b) for b in bins]
        assert sum(1 for v in loads if v <= 1 - delta) <= 1


def pair_opt(sizes):
    """OPT for items of size at least 1/2: at most two per bin, and a two-pointer greedy finds the most pairs."""
    s = sorted(sizes)
    i, j, bins = 0, len(s) - 1, 0
    while i <= j:
        if i < j and s[i] + s[j] <= 1:
            i += 1
        j -= 1
        bins += 1
    return bins


def test_example() -> None:
    sizes = ["0.9", "0.85", "0.8", "0.75", "0.7", "0.65", "0.6", "0.6", "0.55", "0.5", "0.5", "0.5",
             "0.3", "0.2", "0.2", "0.1", "0.1"]
    st = {}
    bins = fernandez_de_la_vega_lueker_aptas(sizes, 1, exact_limit=12, stats=st)
    check_packing(sizes, bins)
    assert st["K"] == 3 and st["d"] == 3 and st["lp"] == Fraction(15, 2) and st["lp_bins"] == 8
    assert len(bins) == 11 and brute_opt([Fraction(v) for v in sizes[:12]]) == 11
    configs, x, z = configuration_lp([Fraction("0.75"), Fraction("0.6"), Fraction("0.5")], [3, 3, 3])
    assert dict(zip(configs, x)) == {(0, 0, 1): 0, (0, 0, 2): Fraction(3, 2), (0, 1, 0): 3, (1, 0, 0): 3}


def test_exact_pack_is_optimal() -> None:
    rng = random.Random(1981)
    for _ in range(200):
        n = rng.randint(0, 9)
        s = [Fraction(rng.randint(1, 12), 12) for _ in range(n)]
        bins = exact_pack(s)
        check_packing(s, bins)
        assert len(bins) == brute_opt(s)


def test_bound_for_several_eps() -> None:
    rng = random.Random(1349)
    for eps in (Fraction(1), Fraction(1, 2), Fraction(1, 4)):
        for _ in range(60):
            n = rng.randint(1, 10)
            s = [Fraction(rng.randint(1, 20), 20) for _ in range(n)]
            bins = fernandez_de_la_vega_lueker_aptas(s, eps)
            check_packing(s, bins)
            check_small_items(s, bins, eps / 2)
            assert len(bins) <= (1 + eps) * brute_opt(s) + 1


def test_lp_path_and_grouping() -> None:
    rng = random.Random(355)
    for eps in (Fraction(1), Fraction(2, 3), Fraction(1, 2)):
        delta = eps / 2
        grid = [Fraction(a, 12) for a in range(ceil(delta * 12), 13)]
        for _ in range(25):
            n1 = rng.randint(1, 11)
            large = [rng.choice(grid) for _ in range(n1)]
            small = [Fraction(rng.randint(1, 5), 24) for _ in range(rng.randint(0, 4))]
            s = large + small
            st = {}
            bins = fernandez_de_la_vega_lueker_aptas(s, eps, exact_limit=1, stats=st)
            check_packing(s, bins)
            check_small_items(s, bins, delta)
            k, d = st["K"], st["d"]
            assert k == max(1, floor(delta * delta * n1))
            # linear grouping: the rounded size of group i + 1 is at most the smallest item of group i
            order = sorted(large, reverse=True)
            groups = [order[a:a + k] for a in range(0, n1, k)]
            for g, h in zip(groups, groups[1:]):
                assert h[0] <= g[-1]
            assert d <= len(groups) - 1
            rounded = [h[0] for h in groups[1:] for _ in h]
            opt_l, opt_j = brute_opt(large), brute_opt(rounded)
            assert opt_j <= opt_l
            if d:
                assert st["support"] <= d
                assert sum(rounded) <= st["lp"] <= opt_j
                assert st["lp_bins"] <= st["lp"] + d
            large_bins = sum(1 for b in bins if any(s[j] >= delta for j in b))
            assert large_bins <= opt_l + k + d


def test_guaranteed_regime() -> None:
    # eps = 1 gives delta = 1/2, so the LP path runs once there are 2 / delta^4 = 32 large items
    rng = random.Random(4)
    for _ in range(25):
        n1 = rng.randint(32, 44)
        large = [Fraction(rng.randint(10, 20), 20) for _ in range(n1)]
        small = [Fraction(rng.randint(1, 9), 20) for _ in range(rng.randint(0, 30))]
        s = large + small
        st = {}
        bins = fernandez_de_la_vega_lueker_aptas(s, 1, stats=st)
        check_packing(s, bins)
        check_small_items(s, bins, Fraction(1, 2))
        opt_l = pair_opt(large)
        assert st["lp"] is not None and st["K"] == n1 // 4
        large_bins = sum(1 for b in bins if any(s[j] >= Fraction(1, 2) for j in b))
        assert large_bins <= opt_l + st["K"] + st["d"] <= 2 * opt_l
        assert len(bins) <= 2 * max(opt_l, ceil(sum(s))) + 1
