# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nsga-ii/. The authors are listed in prov/736BVW.jsonl.

import itertools
import math
import random
from fractions import Fraction as Fr

from nsga_ii import (
    crowding_distance,
    dominates,
    fast_non_dominated_sort,
    nsga_ii,
    nsga_ii_loop,
    polynomial_mutation,
    sbx,
    survival,
)


def peel(images):
    """Reference: peel the non-dominated points one front at a time."""
    left = list(range(len(images)))
    fronts = []
    while left:
        front = [i for i in left if not any(dominates(images[j], images[i]) for j in left)]
        fronts.append(sorted(front))
        left = [i for i in left if i not in front]
    return fronts


def zdt1(x):
    g = 1 + 9 * sum(x[1:]) / (len(x) - 1)
    return (x[0], g * (1 - math.sqrt(x[0] / g)))


EXAMPLE = [(1, 1), (1, 9), (2, 6), (4, 5), (6, 2), (9, 1), (5, 7), (7, 6)]


def test_example() -> None:
    assert peel(EXAMPLE) == [[0], [1, 2, 3, 4, 5], [6, 7]]
    ex = [tuple(Fr(v) for v in p) for p in EXAMPLE]
    cd = crowding_distance(ex, [1, 2, 3, 4, 5])
    assert cd[2] == Fr(7, 8) and cd[3] == 1 and cd[4] == Fr(9, 8)
    assert cd[1] == cd[5] == math.inf
    assert sorted(survival(ex, 4)) == [0, 1, 4, 5]
    assert sorted(survival(ex, 6)) == [0, 1, 2, 3, 4, 5]


def test_sort_matches_peeling() -> None:
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(0, 14)
        p = rng.randint(1, 4)
        pts = [tuple(rng.randint(0, 4) for _ in range(p)) for _ in range(n)]
        assert [sorted(fr) for fr in fast_non_dominated_sort(pts)] == peel(pts)


def test_survival_rules() -> None:
    rng = random.Random(2)
    for _ in range(300):
        m = rng.randint(2, 16)
        n = rng.randint(1, m)
        pts = [tuple(Fr(rng.randint(0, 9)) for _ in range(2)) for _ in range(m)]
        keep = survival(pts, n)
        assert len(keep) == n == len(set(keep))
        fronts = peel(pts)
        # if the first front fits, all of it survives; so do all fronts that fit whole
        total = 0
        for fr in fronts:
            if total + len(fr) <= n:
                assert set(fr) <= set(keep)
                total += len(fr)
            else:
                part = [i for i in fr if i in keep]
                assert len(part) == n - total
                cd = crowding_distance(pts, fr)
                dropped = [i for i in fr if i not in keep]
                if part and dropped:
                    assert min(cd[i] for i in part) >= max(cd[i] for i in dropped)
                break


def test_operators_stay_in_bounds() -> None:
    rng = random.Random(3)
    lo, hi = [0.0, -1.0, 2.0], [1.0, 1.0, 5.0]
    for _ in range(500):
        a = tuple(rng.uniform(l, h) for l, h in zip(lo, hi))
        b = tuple(rng.uniform(l, h) for l, h in zip(lo, hi))
        c1, c2 = sbx(a, b, 15, lo, hi, rng)
        for c in (c1, c2, polynomial_mutation(a, 20, 1.0, lo, hi, rng)):
            assert all(l <= v <= h for v, l, h in zip(c, lo, hi))


def test_real_coded_invariants() -> None:
    for seed, n in [(1, 12), (2, 9)]:
        rng = random.Random(seed)
        lo, hi = [0.0] * 4, [1.0] * 4

        def hook(pop, union):
            assert len(pop) == n
            assert all(all(0 <= v <= 1 for v in x) and y == zdt1(x) for x, y in pop)
            first = [union[i][1] for i in fast_non_dominated_sort([y for _, y in union])[0]]
            if len(first) <= n:
                kept = [y for _, y in pop]
                for y in first:
                    assert y in kept

        out = nsga_ii(zdt1, n, lo, hi, 20, rng, on_generation=hook)
        for (_, a), (_, b) in itertools.permutations(out, 2):
            assert not dominates(a, b)


def one_min_max(x):
    s = sum(x)
    return (s, len(x) - s)


def test_one_min_max_keeps_front_values() -> None:
    """With N >= 4(n + 1), each objective value present stays present (Zheng, Liu and Doerr, 2022)."""
    for seed, nb in [(1, 4), (2, 6)]:
        rng = random.Random(seed)
        n = 4 * (nb + 1)
        pop = []
        for _ in range(n):
            x = tuple(rng.randint(0, 1) for _ in range(nb))
            pop.append((x, one_min_max(x)))
        seen = {y for _, y in pop}

        def flip(parents, r):
            return [tuple(b ^ 1 if r.random() < 1 / nb else b for b in x) for x in parents]

        def hook(new_pop, union):
            nonlocal seen
            now = {y for _, y in new_pop}
            assert seen <= now
            seen = now

        nsga_ii_loop(pop, one_min_max, flip, n, 30, rng, hook)
