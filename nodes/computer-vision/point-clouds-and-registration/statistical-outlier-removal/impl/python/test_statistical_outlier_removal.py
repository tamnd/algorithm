# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/statistical-outlier-removal/. The authors are listed in prov/RBGT7A.jsonl.

import math
import random
import statistics

import pytest

from statistical_outlier_removal import mean_knn_distances, statistical_outlier_removal

GRID = [(x, y, 0) for y in range(3) for x in range(3)] + [(4, 4, 0)]


def oracle(points, k, alpha):
    """Sort all distances of each point, then use the statistics module."""
    d = []
    for i, p in enumerate(points):
        ds = sorted(math.dist(p, q) for j, q in enumerate(points) if j != i)
        d.append(sum(ds[:k]) / k)
    t = statistics.mean(d) + alpha * statistics.stdev(d)
    return [i for i in range(len(points)) if d[i] <= t + 1e-12], d


def test_example() -> None:
    d = mean_knn_distances(GRID, 2)
    assert all(abs(x - 1.0) < 1e-12 for x in d[:9])
    assert abs(d[9] - (math.sqrt(8) + math.sqrt(13)) / 2) < 1e-12
    kept, t = statistical_outlier_removal(GRID, 2, 1.0)
    assert kept == list(range(9))
    assert abs(t - 1.92277246) < 1e-7
    kept3, t3 = statistical_outlier_removal(GRID, 2, 3.0)
    assert kept3 == list(range(10))  # one outlier inflates sigma and hides itself


def test_matches_oracle() -> None:
    rng = random.Random(5)
    for _ in range(30):
        n = rng.randint(3, 40)
        pts = [tuple(rng.uniform(-2, 2) for _ in range(3)) for _ in range(n)]
        k = rng.randint(1, n - 1)
        alpha = rng.choice([0.0, 0.5, 1.0, 2.0])
        kept, _ = statistical_outlier_removal(pts, k, alpha)
        want, _ = oracle(pts, k, alpha)
        assert kept == want


def test_planted_outliers_are_removed() -> None:
    rng = random.Random(6)
    surface = [(0.1 * i + rng.gauss(0, 0.005), 0.1 * j + rng.gauss(0, 0.005), rng.gauss(0, 0.005))
               for i in range(10) for j in range(8)]
    outliers = [(rng.uniform(-2, 3), rng.uniform(-2, 3), rng.uniform(0.6, 2.0)) for _ in range(6)]
    pts = surface + outliers
    kept, _ = statistical_outlier_removal(pts, 6, 1.0)
    assert kept == list(range(len(surface)))


def test_cantelli_bound_on_removed_fraction() -> None:
    rng = random.Random(7)
    for _ in range(20):
        n = rng.randint(5, 50)
        pts = [tuple(rng.expovariate(1.0) ** 3 for _ in range(3)) for _ in range(n)]
        for alpha in (0.5, 1.0, 2.0):
            kept, _ = statistical_outlier_removal(pts, 3, alpha)
            removed = n - len(kept)
            assert removed <= n / (1 + alpha * alpha)


def test_invariance_under_order_and_rigid_motion() -> None:
    rng = random.Random(8)
    pts = [tuple(rng.gauss(0, 1) for _ in range(3)) for _ in range(30)] + [(9.0, 9.0, 9.0)]
    kept, _ = statistical_outlier_removal(pts, 4, 1.0)
    perm = list(range(len(pts)))
    rng.shuffle(perm)
    kept_p, _ = statistical_outlier_removal([pts[i] for i in perm], 4, 1.0)
    assert sorted(perm[i] for i in kept_p) == kept
    c, s = math.cos(0.7), math.sin(0.7)
    moved = [(c * x - s * y + 5.0, s * x + c * y - 2.0, z + 1.0) for x, y, z in pts]
    kept_m, _ = statistical_outlier_removal(moved, 4, 1.0)
    assert kept_m == kept
    assert len(pts) - 1 not in kept


def test_edges() -> None:
    same = [(1.0, 1.0, 1.0)] * 5
    kept, t = statistical_outlier_removal(same, 2, 1.0)
    assert kept == [0, 1, 2, 3, 4] and t == 0.0
    with pytest.raises(ValueError):
        statistical_outlier_removal([(0.0, 0.0, 0.0)], 1, 1.0)
    with pytest.raises(ValueError):
        statistical_outlier_removal(GRID, 10, 1.0)
