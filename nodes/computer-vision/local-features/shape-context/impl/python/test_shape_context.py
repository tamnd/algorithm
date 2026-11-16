# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shape-context/. The authors are listed in prov/A629T3.jsonl.

import itertools
import math
import random

from shape_context import assign_with_dummies, chi2_cost, hungarian, match_shapes, mean_distance, shape_contexts


def brute_assignment(cost):
    n = len(cost)
    best = None
    for perm in itertools.permutations(range(n)):
        s = sum(cost[i][perm[i]] for i in range(n))
        if best is None or s < best:
            best = s
    return best


def random_shape(rng, n):
    pts = set()
    while len(pts) < n:
        pts.add((rng.randint(-20, 20), rng.randint(-20, 20)))
    return sorted(pts)


def test_hungarian_matches_brute_force():
    rng = random.Random(1)
    for n in range(1, 8):
        for _ in range(12):
            cost = [[rng.randint(0, 30) for _ in range(n)] for _ in range(n)]
            a = hungarian(cost)
            assert sorted(a) == list(range(n))
            assert sum(cost[i][a[i]] for i in range(n)) == brute_assignment(cost)


def test_hungarian_with_float_costs():
    rng = random.Random(2)
    for n in (5, 6):
        cost = [[rng.random() for _ in range(n)] for _ in range(n)]
        a = hungarian(cost)
        assert abs(sum(cost[i][a[i]] for i in range(n)) - brute_assignment(cost)) < 1e-12


def test_mean_distance_by_hand():
    pts = [(0, 0), (3, 4)]
    # Ordered pairs: 0, 5, 5, 0, so the mean over n^2 = 4 pairs is 2.5.
    assert mean_distance(pts) == 2.5


def test_histograms_sum_to_one_and_count_by_hand():
    pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (-1.0, 0.0), (0.0, -1.0)]
    h = shape_contexts(pts)
    assert all(abs(sum(x) - 1.0) < 1e-12 for x in h)
    # The mean distance is (8 * 1 + 4 * (2 + 2 * sqrt(2))) / 25.
    alpha = (8 + 4 * (2 + 2 * math.sqrt(2))) / 25
    assert abs(mean_distance(pts) - alpha) < 1e-12
    # From the center, the four points are at r = 1 / alpha, angles 0, 90, 180 and 270 degrees.
    r = 1 / alpha
    kr = int(5 * (math.log(r) - math.log(0.125)) / math.log(16))
    expected = [0.0] * 60
    for kt in (0, 3, 6, 9):
        expected[kr * 12 + kt] = 0.25
    assert h[0] == expected


def test_chi2_cost_properties():
    a = [0.5, 0.5, 0.0]
    b = [0.0, 0.5, 0.5]
    assert chi2_cost(a, a) == 0.0
    assert abs(chi2_cost(a, b) - 0.5) < 1e-12
    assert abs(chi2_cost([1.0, 0.0], [0.0, 1.0]) - 1.0) < 1e-12


def test_translation_and_scale_do_not_change_the_descriptors():
    rng = random.Random(3)
    pts = random_shape(rng, 20)
    h = shape_contexts(pts)
    moved = [(4 * x + 17, 4 * y - 9) for x, y in pts]
    h2 = shape_contexts(moved)
    for a, b in zip(h, h2):
        assert max(abs(x - y) for x, y in zip(a, b)) < 1e-12


def test_permuted_scaled_copy_is_matched_exactly():
    rng = random.Random(4)
    pts = random_shape(rng, 18)
    perm = list(range(18))
    rng.shuffle(perm)
    q = [None] * 18
    for i, j in enumerate(perm):
        x, y = pts[i]
        q[j] = (0.5 * x + 3.0, 0.5 * y + 1.0)
    m, total = match_shapes(pts, q)
    assert m == perm
    assert total < 1e-12


def test_noisy_copy_is_mostly_matched():
    rng = random.Random(5)
    pts = [(10 * math.cos(2 * math.pi * k / 24), 6 * math.sin(2 * math.pi * k / 24)) for k in range(24)]
    pts += [(-3.0 + k, 0.0) for k in range(7)]
    q = [(x + rng.gauss(0, 0.15), y + rng.gauss(0, 0.15)) for x, y in pts]
    m, _ = match_shapes(pts, q)
    right = sum(1 for i, j in enumerate(m) if i == j)
    assert right >= 24


def brute_partial(cost, m, eps):
    """Best partial matching: each unmatched row or column costs eps."""
    n = len(cost)
    best = None
    for k in range(min(n, m) + 1):
        for rows in itertools.combinations(range(n), k):
            for cols in itertools.permutations(range(m), k):
                s = sum(cost[r][c] for r, c in zip(rows, cols)) + eps * (n - k + m - k)
                if best is None or s < best:
                    best = s
    return best


def test_dummies_match_brute_force_partial_matching():
    rng = random.Random(6)
    for n, m in ((3, 3), (4, 2), (2, 5), (4, 4)):
        for _ in range(6):
            cost = [[rng.random() for _ in range(m)] for _ in range(n)]
            eps = rng.choice([0.1, 0.3, 0.5])
            out, total = assign_with_dummies(cost, m, eps)
            assert abs(total - brute_partial(cost, m, eps)) < 1e-12
            used = [j for j in out if j >= 0]
            assert len(used) == len(set(used))


def test_outlier_row_goes_to_a_dummy():
    cost = [[0.05, 0.9, 0.9], [0.9, 0.1, 0.9], [0.95, 0.9, 0.97]]
    out, total = assign_with_dummies(cost, 3, eps_d=0.4)
    assert out == [0, 1, -1]
    assert abs(total - (0.05 + 0.1 + 0.4 + 0.4)) < 1e-12
    out2, _ = assign_with_dummies([[0.2, 0.5], [0.4, 0.1], [0.3, 0.3]], 2)
    assert out2 == [0, 1, -1]
