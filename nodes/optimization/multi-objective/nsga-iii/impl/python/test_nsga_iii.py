# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nsga-iii/. The authors are listed in prov/YWZJB7.jsonl.

import itertools
import math
import random
from fractions import Fraction as Fr

from nsga_iii import (
    das_dennis,
    dominates,
    dtlz2,
    fast_non_dominated_sort,
    normalize,
    nsga_iii,
    perpendicular_sq,
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


EXAMPLE = [(0, 10), (1, 1), (10, 0), (2, 8), (3, 6), (4, 4), (7, 2), (5, 9), (9, 5), (8, 8)]


def test_das_dennis_count() -> None:
    for p in range(1, 5):
        for h in range(1, 7):
            pts = das_dennis(p, h)
            brute = [c for c in itertools.product(range(h + 1), repeat=p) if sum(c) == h]
            assert sorted(pts) == sorted(tuple(Fr(v, h) for v in c) for c in brute)
            assert len(pts) == math.comb(h + p - 1, p - 1)
            assert len(set(pts)) == len(pts)
    assert len(das_dennis(3, 12)) == 91


def test_example() -> None:
    ex = [tuple(Fr(v) for v in y) for y in EXAMPLE]
    assert peel(ex) == [[0, 1, 2], [3, 4, 5, 6], [7, 8, 9]]
    refs = das_dennis(2, 4)
    for seed in range(20):
        trace = {}
        keep = survival(ex, 5, refs, random.Random(seed), trace)
        assert trace["cuts"] == [10, 10]
        assert trace["norm"][3] == (Fr(1, 5), Fr(4, 5))
        idx = {w: j for j, w in enumerate(refs)}
        q, h3, half = Fr(1, 4), Fr(3, 4), Fr(1, 2)
        assert trace["line"][3] == trace["line"][4] == idx[(q, h3)]
        assert trace["line"][5] == idx[(half, half)] and trace["dist"][5] == 0
        assert trace["line"][6] == idx[(h3, q)]
        assert trace["dist"][3] == Fr(1, 250) and trace["dist"][4] == Fr(9, 1000) and trace["dist"][6] == Fr(1, 1000)
        assert trace["rho"] == [1, 0, 1, 0, 1]
        assert sorted(keep) == [0, 1, 2, 3, 6]


def random_case(rng):
    m = rng.randint(3, 16)
    p = rng.randint(2, 3)
    pts = [tuple(Fr(rng.randint(0, 9)) for _ in range(p)) for _ in range(m)]
    return pts, p, rng.randint(1, m)


def test_survival_keeps_whole_fronts() -> None:
    rng = random.Random(1)
    for _ in range(300):
        pts, p, n = random_case(rng)
        keep = survival(pts, n, das_dennis(p, rng.randint(1, 5)), rng)
        assert len(keep) == n == len(set(keep))
        total = 0
        for fr in peel(pts):
            if total + len(fr) <= n:
                assert set(fr) <= set(keep)
                total += len(fr)
            else:
                assert len([i for i in fr if i in keep]) == n - total
                break


def test_empty_niches_are_served_first() -> None:
    rng = random.Random(2)
    checked = 0
    for _ in range(400):
        pts, p, n = random_case(rng)
        trace = {}
        survival(pts, n, das_dennis(p, rng.randint(1, 5)), rng, trace)
        if "added" not in trace:
            continue
        checked += 1
        line, dist, rho, last = trace["line"], trace["dist"], trace["rho"], trace["last"]
        empty = {line[i] for i in last if rho[line[i]] == 0}
        first = trace["added"][: len(empty)]
        assert len({line[i] for i in first}) == len(first)
        assert all(line[i] in empty for i in first)
        for i in first:
            assert dist[i] == min(dist[k] for k in last if line[k] == line[i])
    assert checked > 50


def test_normalization() -> None:
    rng = random.Random(3)
    for _ in range(300):
        pts, p, _ = random_case(rng)
        members = list(range(len(pts)))
        norm, cuts = normalize(pts, members)
        assert all(c > 0 for c in cuts)
        assert all(v >= 0 for s in norm.values() for v in s)
        for m in range(p):
            assert min(s[m] for s in norm.values()) == 0


def test_perpendicular_distance() -> None:
    assert perpendicular_sq((Fr(3), Fr(4)), (Fr(1), Fr(0))) == 16
    assert perpendicular_sq((Fr(2), Fr(2)), (Fr(1), Fr(1))) == 0
    assert perpendicular_sq((Fr(1), Fr(0)), (Fr(1), Fr(1))) == Fr(1, 2)


def test_run_invariants() -> None:
    for seed, n in [(1, 16), (2, 10)]:
        rng = random.Random(seed)
        lo, hi = [0.0] * 5, [1.0] * 5

        def hook(pop, union):
            assert len(pop) == n
            assert all(all(0 <= v <= 1 for v in x) and y == dtlz2(x) for x, y in pop)
            first = [union[i][1] for i in fast_non_dominated_sort([y for _, y in union])[0]]
            if len(first) <= n:
                kept = [y for _, y in pop]
                assert all(y in kept for y in first)

        out = nsga_iii(dtlz2, n, 3, 4, lo, hi, 15, rng, on_generation=hook)
        assert out
        for (_, a), (_, b) in itertools.permutations(out, 2):
            assert not dominates(a, b)
