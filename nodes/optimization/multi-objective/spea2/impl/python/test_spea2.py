# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spea2/. The authors are listed in prov/3QZDDW.jsonl.

import itertools
import math
import random

from spea2 import blend_gauss, dominates, environmental_selection, fitness, spea2, truncate

U = [(1, 5), (2, 2), (5, 1), (3, 3), (4, 4), (6, 6)]


def test_example() -> None:
    s, r, d, f = fitness(U, 2)
    assert s == [1, 3, 1, 2, 1, 0]
    assert r == [0, 0, 0, 3, 5, 8]
    sig = [math.sqrt(10), math.sqrt(8), math.sqrt(10), math.sqrt(2), math.sqrt(8), math.sqrt(18)]
    assert all(math.isclose(d[i], 1 / (sig[i] + 2)) for i in range(6))
    assert sorted(environmental_selection(U, f, 2)) == [0, 2]
    assert sorted(environmental_selection(U, f, 4)) == [0, 1, 2, 3]


def test_truncation_can_drop_an_extreme() -> None:
    pts = [(0, 2, 3), (1, 0, 5), (1, 3, 2), (4, 0, 4), (6, 1, 3)]
    kept = truncate(pts, range(5), 4)
    assert 0 not in kept
    assert min(pts[i][0] for i in kept) == 1


def naive_truncate(pts, members, m):
    left = list(members)
    while len(left) > m:
        vec = {i: sorted(math.dist(pts[i], pts[j]) for j in left if j != i) for i in left}
        left.remove(min(left, key=lambda i: (vec[i], i)))
    return left


def test_truncation_matches_naive() -> None:
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 10)
        p = rng.choice((2, 3))
        pts = [tuple(rng.randint(0, 5) for _ in range(p)) for _ in range(n)]
        m = rng.randint(1, n)
        assert truncate(pts, range(n), m) == naive_truncate(pts, range(n), m)


def test_fitness_below_one_iff_nondominated() -> None:
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(1, 12)
        p = rng.choice((2, 3))
        pts = [tuple(rng.randint(0, 5) for _ in range(p)) for _ in range(n)]
        _, r, d, f = fitness(pts, max(1, math.isqrt(n)))
        for i in range(n):
            nd = not any(dominates(pts[j], pts[i]) for j in range(n))
            assert (f[i] < 1) == nd
            assert 0 < d[i] <= 0.5
            assert r[i] == 0 or r[i] >= 1


def test_archive_size_and_content() -> None:
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(1, 12)
        pts = [tuple(rng.randint(0, 6) for _ in range(2)) for _ in range(n)]
        m = rng.randint(1, n)
        _, _, _, f = fitness(pts, max(1, math.isqrt(n)))
        keep = environmental_selection(pts, f, m)
        assert len(keep) == m == len(set(keep))
        nd = {i for i in range(n) if not any(dominates(pts[j], pts[i]) for j in range(n))}
        if len(nd) >= m:
            assert set(keep) <= nd
        else:
            assert nd <= set(keep)
            worst_kept = max(f[i] for i in keep)
            assert all(f[i] >= worst_kept for i in range(n) if i not in keep)


def zdt1(x):
    g = 1 + 9 * sum(x[1:]) / (len(x) - 1)
    return (x[0], g * (1 - math.sqrt(x[0] / g)))


def test_run_invariants() -> None:
    for seed, n, m in [(1, 10, 6), (2, 8, 8), (3, 5, 1)]:
        rng = random.Random(seed)
        lo, hi = [0.0] * 3, [1.0] * 3

        def hook(pop, archive):
            assert len(pop) == n and len(archive) == m
            for x, y in pop + archive:
                assert all(0 <= v <= 1 for v in x) and y == zdt1(x)

        out = spea2(lambda r: tuple(r.random() for _ in range(3)), zdt1, blend_gauss(lo, hi), n, m, 15, rng, hook)
        assert out
        for (_, a), (_, b) in itertools.permutations(out, 2):
            assert not dominates(a, b)
