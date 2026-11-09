# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spea/. The authors are listed in prov/Y5WMKW.jsonl.

import itertools
import math
import random
from fractions import Fraction as Fr

from spea import blend_gauss, cluster_reduce, covers, dominates, population_fitness, spea, strengths, update_archive

ARCHIVE = [(1, 7), (3, 4), (6, 2)]
POP = [(2, 8), (4, 5), (4, 8), (7, 3), (7, 7), (8, 9)]


def front(images):
    return {y for y in images if not any(dominates(z, y) for z in images)}


def test_example() -> None:
    s = strengths(ARCHIVE, POP)
    assert s == [Fr(4, 7), Fr(4, 7), Fr(3, 7)]
    fit = population_fitness(ARCHIVE, s, POP)
    assert fit == [Fr(11, 7), Fr(11, 7), Fr(15, 7), Fr(10, 7), Fr(18, 7), Fr(18, 7)]
    # (7, 7) dominates (8, 9) but both get 18/7
    assert dominates(POP[4], POP[5]) and fit[4] == fit[5]


def test_cluster_example() -> None:
    pts = [(0, 10), (1, 9), (2, 8), (8, 2), (9, 1), (10, 0)]
    out = cluster_reduce([(p, p) for p in pts], 2)
    assert sorted(y for _, y in out) == [(1, 9), (9, 1)]


def naive_average_linkage(pts, m):
    clusters = [[i] for i in range(len(pts))]
    while len(clusters) > m:
        best = None
        for a, b in itertools.combinations(range(len(clusters)), 2):
            d = sum(math.dist(pts[i], pts[j]) for i in clusters[a] for j in clusters[b]) / (len(clusters[a]) * len(clusters[b]))
            if best is None or d < best[0]:
                best = (d, a, b)
        _, a, b = best
        clusters[a] = clusters[a] + clusters[b]
        del clusters[b]
    return sorted(sorted(c) for c in clusters)


def test_clustering_matches_naive() -> None:
    rng = random.Random(1)
    for _ in range(150):
        k = rng.randint(1, 10)
        m = rng.randint(1, 6)
        pts = [(rng.random(), rng.random()) for _ in range(k)]
        out = cluster_reduce([(i, p) for i, p in enumerate(pts)], m)
        assert len(out) == min(k, m)
        if k > m:
            groups = naive_average_linkage(pts, m)
            reps = sorted(i for i, _ in out)
            # one representative per cluster, the one with the least total distance to its cluster
            for g in groups:
                inside = [i for i in reps if i in g]
                assert len(inside) == 1
                tot = {i: sum(math.dist(pts[i], pts[j]) for j in g) for i in g}
                assert tot[inside[0]] == min(tot.values())


def test_fitness_properties() -> None:
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randint(1, 10)
        pop = [tuple(rng.randint(0, 6) for _ in range(2)) for _ in range(n)]
        arch = sorted(front(pop + [tuple(rng.randint(0, 6) for _ in range(2)) for _ in range(4)]))
        s = strengths(arch, pop)
        fit = population_fitness(arch, s, pop)
        assert all(0 <= v <= Fr(n, n + 1) for v in s)
        assert all(v >= 1 for v in fit)
        for i, j in itertools.permutations(range(n), 2):
            if covers(pop[i], pop[j]):
                assert fit[i] <= fit[j]


def bits(n):
    return lambda r: tuple(r.randint(0, 1) for _ in range(n))


def flip(parents, r):
    return [tuple(b ^ 1 if r.random() < 0.2 else b for b in x) for x in parents]


def two_knapsacks(x):
    w1 = [3, 1, 4, 1, 5, 9]
    w2 = [2, 7, 1, 8, 2, 8]
    return (-sum(a * b for a, b in zip(x, w1)), -sum((1 - a) * b for a, b in zip(x, w2)))


def test_unbounded_archive_is_front_of_seen() -> None:
    for seed in range(3):
        rng = random.Random(seed)
        seen = set()

        def hook(pop, archive):
            seen.update(y for _, y in pop)
            imgs = [y for _, y in archive]
            assert len(set(imgs)) == len(imgs)
            assert set(imgs) == front(seen)

        spea(bits(6), two_knapsacks, flip, 8, 1000, 12, rng, hook)


def zdt1(x):
    g = 1 + 9 * sum(x[1:]) / (len(x) - 1)
    return (x[0], g * (1 - math.sqrt(x[0] / g)))


def test_run_invariants() -> None:
    for seed, n, m in [(1, 10, 4), (2, 6, 6), (3, 5, 1)]:
        rng = random.Random(seed)
        lo, hi = [0.0] * 3, [1.0] * 3

        def hook(pop, archive):
            assert len(pop) == n
            assert 1 <= len(archive) <= m
            for x, y in pop + archive:
                assert all(0 <= v <= 1 for v in x) and y == zdt1(x)
            for (_, a), (_, b) in itertools.permutations(archive, 2):
                assert not covers(a, b)

        out = spea(lambda r: tuple(r.random() for _ in range(3)), zdt1, blend_gauss(lo, hi), n, m, 15, rng, hook)
        assert out


def test_update_keeps_one_copy() -> None:
    a = update_archive([("a", (1, 2))], [("b", (1, 2)), ("c", (2, 1)), ("d", (3, 3))])
    assert a == [("a", (1, 2)), ("c", (2, 1))]
