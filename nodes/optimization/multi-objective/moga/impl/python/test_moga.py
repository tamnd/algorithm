# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moga/. The authors are listed in prov/0EWQ9V.jsonl.

import itertools
import math
import random

from moga import (
    average_by_rank,
    dominates,
    ff_rank,
    moga,
    moga_fitness,
    niche_counts,
    raw_fitness,
    share_and_scale,
    sus,
)

POINTS = [(1, 8), (2, 5), (3, 6), (4, 2), (5, 4), (6, 7), (7, 1), (8, 3)]


def sch(x):
    return (x[0] ** 2, (x[0] - 2) ** 2)


def test_example() -> None:
    r = ff_rank(POINTS)
    assert r == [1, 1, 2, 1, 2, 5, 1, 3]
    base = average_by_rank(raw_fitness(r), r)
    assert base == [6.5, 6.5, 3.5, 6.5, 3.5, 1.0, 6.5, 2.0]
    m = niche_counts(POINTS, r, 4 / 7)
    assert math.isclose(m[0], 2 - math.sqrt(10) / 4)
    assert math.isclose(m[1], 1 + (1 - math.sqrt(10) / 4) + (1 - math.sqrt(13) / 4))
    phi = share_and_scale(base, m, r)
    assert math.isclose(phi[0] + phi[1] + phi[3] + phi[6], 26)
    assert phi[0] > base[0] > phi[1]
    assert phi[2] == phi[4] == 3.5


def test_rank_facts_random() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randint(1, 12)
        p = rng.choice([2, 3])
        pts = [tuple(rng.randint(0, 5) for _ in range(p)) for _ in range(n)]
        r = ff_rank(pts)
        for i in range(n):
            nondom = not any(dominates(z, pts[i]) for z in pts)
            assert (r[i] == 1) == nondom
        for i, j in itertools.permutations(range(n), 2):
            if dominates(pts[i], pts[j]):
                assert r[i] < r[j]
        raw = raw_fitness(r)
        assert sorted(raw) == list(range(1, n + 1))
        base = average_by_rank(raw, r)
        assert math.isclose(sum(base), n * (n + 1) / 2)
        # a better rank gets a strictly larger averaged fitness
        for i, j in itertools.permutations(range(n), 2):
            if r[i] < r[j]:
                assert base[i] > base[j]
            if r[i] == r[j]:
                assert base[i] == base[j]
        phi = moga_fitness(pts, 0.5)
        for rank in set(r):
            mem = [i for i in range(n) if r[i] == rank]
            assert math.isclose(sum(phi[i] for i in mem), sum(base[i] for i in mem))
        assert all(v > 0 for v in phi)


def test_sus() -> None:
    rng = random.Random(1)
    w = [3, 1, 0, 4]
    for _ in range(200):
        s = sus(w, 8, rng)
        assert len(s) == 8
        counts = [s.count(i) for i in range(4)]
        # SUS gives each index floor or ceil of its expected count
        assert counts == [3, 1, 0, 4]
    w = [1.5, 2.5]
    for _ in range(200):
        c = sus(w, 2, rng).count(0)
        assert c in (0, 1)


def test_run_invariants() -> None:
    for seed, n in [(1, 10), (2, 7), (5, 2)]:
        rng = random.Random(seed)

        def hook(pop):
            assert len(pop) == n
            assert all(-4 <= x[0] <= 4 and y == sch(x) for x, y in pop)

        out = moga(sch, n, [-4], [4], 0.3, 25, rng, on_generation=hook)
        assert out
        for (_, a), (_, b) in itertools.permutations(out, 2):
            assert not dominates(a, b)
