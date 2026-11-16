# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/global-nearest-neighbor-association/. The authors are listed in prov/VW85MF.jsonl.

import itertools
import math
import random

from global_nearest_neighbor_association import (
    INF,
    GNNTracker,
    gnn_assign,
    greedy_nearest_neighbor,
    hungarian,
    mahalanobis2,
)

I2 = [[1.0, 0.0], [0.0, 1.0]]


def brute_partial(c, n, m, c_miss, c_new):
    """Least cost over all partial one-to-one matchings of tracks to measurements."""
    best = INF
    for k in range(0, min(n, m) + 1):
        for rows in itertools.combinations(range(n), k):
            for cols in itertools.permutations(range(m), k):
                s = sum(c[i][j] for i, j in zip(rows, cols))
                s += (n - k) * c_miss + (m - k) * c_new
                best = min(best, s)
    return best


def test_page_example():
    z_hats = [(0.0, 0.0), (2.0, 0.0)]
    zs = [(1.2, 0.0), (3.5, 0.0), (10.0, 5.0)]
    pairs, missed, new, total = gnn_assign(z_hats, [I2, I2], zs, 9.21)
    assert pairs == {0: 0, 1: 1}
    assert missed == [] and new == [2]
    assert abs(total - (1.44 + 2.25 + 4.605)) < 1e-9
    assert greedy_nearest_neighbor(z_hats, [I2, I2], zs, 9.21) == {1: 0}


def test_mahalanobis():
    s = [[4.0, 0.0], [0.0, 1.0]]
    assert abs(mahalanobis2((2.0, 1.0), (0.0, 0.0), s) - 2.0) < 1e-12
    s = [[2.0, 1.0], [1.0, 2.0]]
    # inverse is [[2, -1], [-1, 2]] / 3, so (1, 1) gives 2 / 3
    assert abs(mahalanobis2((1.0, 1.0), (0.0, 0.0), s) - 2.0 / 3.0) < 1e-12


def test_empty_inputs():
    assert gnn_assign([], [], [], 9.21)[:3] == ({}, [], [])
    pairs, missed, new, total = gnn_assign([(0.0, 0.0)], [I2], [], 9.21)
    assert pairs == {} and missed == [0] and new == [] and abs(total - 4.605) < 1e-12
    pairs, missed, new, total = gnn_assign([], [], [(1.0, 1.0)], 9.21)
    assert pairs == {} and missed == [] and new == [0]


def test_hungarian_against_brute_force():
    rng = random.Random(4417)
    for _ in range(300):
        r = rng.randint(1, 4)
        c = rng.randint(r, 5)
        a = [[rng.choice([INF] + [rng.randint(0, 20)] * 4) for _ in range(c)] for _ in range(r)]
        best = INF
        for cols in itertools.permutations(range(c), r):
            best = min(best, sum(a[i][j] for i, j in enumerate(cols)))
        res = hungarian(a)
        if best == INF:
            assert res is None
        else:
            row_to_col, total = res
            assert len(set(row_to_col)) == r
            assert total == best


def test_gnn_is_optimal_against_brute_force():
    rng = random.Random(9031)
    for _ in range(500):
        n, m = rng.randint(0, 4), rng.randint(0, 4)
        z_hats = [(rng.uniform(0, 8), rng.uniform(0, 8)) for _ in range(n)]
        zs = [(rng.uniform(0, 8), rng.uniform(0, 8)) for _ in range(m)]
        covs = []
        for _ in range(n):
            a, b, d = rng.uniform(0.5, 3), rng.uniform(-0.4, 0.4), rng.uniform(0.5, 3)
            covs.append([[a, b], [b, d]])
        gamma = rng.choice([5.991, 9.21])
        c_miss, c_new = rng.uniform(1, 5), rng.uniform(1, 5)
        pairs, missed, new, total = gnn_assign(z_hats, covs, zs, gamma, c_miss, c_new)
        c = [[INF] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                d2 = mahalanobis2(zs[j], z_hats[i], covs[i])
                c[i][j] = d2 if d2 <= gamma else INF
        assert abs(total - brute_partial(c, n, m, c_miss, c_new)) < 1e-9
        # the reported pairs are gated, one to one, and their cost is the total
        assert len(set(pairs.values())) == len(pairs)
        own = sum(c[i][j] for i, j in pairs.items()) + len(missed) * c_miss + len(new) * c_new
        assert abs(own - total) < 1e-9
        assert sorted(list(pairs) + missed) == list(range(n))
        assert sorted(list(pairs.values()) + new) == list(range(m))


def test_gnn_never_worse_than_greedy():
    rng = random.Random(77)
    for _ in range(300):
        n, m = rng.randint(1, 4), rng.randint(1, 4)
        z_hats = [(rng.uniform(0, 5), rng.uniform(0, 5)) for _ in range(n)]
        zs = [(rng.uniform(0, 5), rng.uniform(0, 5)) for _ in range(m)]
        covs = [I2] * n
        g = greedy_nearest_neighbor(z_hats, covs, zs, 9.21)
        cost_g = sum(mahalanobis2(zs[j], z_hats[i], I2) for i, j in g.items())
        cost_g += (n - len(g)) * 4.605 + (m - len(g)) * 4.605
        total = gnn_assign(z_hats, covs, zs, 9.21)[3]
        assert total <= cost_g + 1e-9


def test_tracker_follows_three_targets():
    rng = random.Random(2024)
    starts = [(0.0, 0.0, 1.0, 0.5), (0.0, 10.0, 1.0, -0.2), (20.0, 5.0, -0.8, 0.0)]
    tracker = GNNTracker()
    ids = None
    errors = []
    for t in range(30):
        truth = [(x + vx * t, y + vy * t) for x, y, vx, vy in starts]
        zs = [(a + rng.gauss(0, 0.5), b + rng.gauss(0, 0.5)) for a, b in truth]
        if t % 7 == 3:
            zs.append((rng.uniform(-5, 25), rng.uniform(-5, 15)))  # a clutter point
        rng.shuffle(zs)
        est = tracker.step(zs)
        if t < 5:
            continue
        if ids is None:  # the track nearest to each target in frame 5
            ids = [min(est, key=lambda k: math.hypot(est[k][0] - a, est[k][1] - b)) for a, b in truth]
            assert len(set(ids)) == 3
        for k, (a, b) in enumerate(truth):
            ex, ey = est[ids[k]]  # the same track must still exist
            errors.append(math.hypot(ex - a, ey - b))
    # each target keeps its track through the crossing of targets 0 and 1 near frame 14
    assert max(errors) < 2.0
    assert sum(errors) / len(errors) < 0.6
