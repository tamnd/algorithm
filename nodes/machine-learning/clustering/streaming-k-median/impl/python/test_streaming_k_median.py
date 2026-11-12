# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/streaming-k-median/. The authors are listed in prov/NTSNHM.jsonl.

import random
from itertools import combinations

from streaming_k_median import (
    StreamingKMedian,
    exact_solver,
    local_search_solver,
    stream_k_median,
    weighted_cost,
)


def manhattan(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def opt_discrete(points, k):
    return min(sum(min(manhattan(p, c) for c in cs) for p in points)
               for cs in combinations(points, min(k, len(points))))


def random_points(rng, n):
    return [(rng.randint(0, 20), rng.randint(0, 20)) for _ in range(n)]


def run(points, k, m, solver):
    s = StreamingKMedian(k, m, manhattan, solver)
    peak = 0
    for p in points:
        s.insert(p)
        peak = max(peak, max(len(b) for b in s.levels))
    centers = s.finish()
    return s, centers, peak


def test_exact_solver_bound_and_level_inequalities():
    rng = random.Random(1)
    for _ in range(40):
        n = rng.randint(6, 16)
        k = rng.randint(1, 2)
        m = rng.randint(k + 1, 5)
        pts = random_points(rng, n)
        s, centers, peak = run(pts, k, m, exact_solver)
        opt = opt_discrete(pts, k)
        L = len(s.levels) - 1
        # each level i: A_i <= 2 b (OPT + S_i) with b = 1
        prefix = 0
        for a in s.level_cost:
            assert a <= 2 * (opt + prefix)
            prefix += a
        cost = sum(min(manhattan(p, c) for c in centers) for p in pts)
        assert len(centers) <= k
        assert cost <= (3 ** (L + 1) - 1) * opt
        assert peak < m


def test_local_search_bound():
    rng = random.Random(2)
    for _ in range(30):
        n = rng.randint(6, 20)
        k = rng.randint(1, 3)
        m = rng.randint(k + 1, 7)
        pts = random_points(rng, n)
        s, centers, _ = run(pts, k, m, local_search_solver)
        L = len(s.levels) - 1
        cost = sum(min(manhattan(p, c) for c in centers) for p in pts)
        assert cost <= (11 ** (L + 1) - 1) * opt_discrete(pts, k)


def test_weight_is_conserved_and_memory_is_small():
    rng = random.Random(3)
    pts = random_points(rng, 500)
    k, m = 3, 10
    s = StreamingKMedian(k, m, manhattan)
    for p in pts:
        s.insert(p)
        assert all(len(b) < m for b in s.levels)
    assert sum(w for b in s.levels for _, w in b) == 500
    # level i receives about 500 (k/m)^i points
    assert len(s.levels) <= 5
    assert s.memory() < m * len(s.levels)
    assert len(s.finish()) == k


def test_short_stream_is_solved_directly():
    rng = random.Random(4)
    for _ in range(20):
        pts = random_points(rng, 7)
        centers = stream_k_median(pts, 2, 8, manhattan, exact_solver)
        cost = weighted_cost([(p, 1) for p in pts], centers, manhattan)
        assert cost == opt_discrete(pts, 2)


def test_local_search_is_single_swap_local_optimum():
    rng = random.Random(5)
    for _ in range(30):
        n = rng.randint(3, 9)
        items = [(p, rng.randint(1, 4)) for p in random_points(rng, n)]
        k = rng.randint(1, n - 1)
        idx = local_search_solver(items, k, manhattan)
        cost = weighted_cost(items, [items[i][0] for i in idx], manhattan)
        for a in range(k):
            for h in range(n):
                if h not in idx:
                    trial = idx[:a] + [h] + idx[a + 1:]
                    assert weighted_cost(items, [items[i][0] for i in trial], manhattan) >= cost
        best = min(weighted_cost(items, [items[i][0] for i in c], manhattan)
                   for c in combinations(range(n), k))
        assert cost <= 5 * best
