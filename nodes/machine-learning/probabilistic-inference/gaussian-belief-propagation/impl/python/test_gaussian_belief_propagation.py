# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-belief-propagation/. The authors are listed in prov/63EWRZ.jsonl.

import math
import random

from gaussian_belief_propagation import exact, gabp, grid_edges, grid_precision, walk_summability_radius

GRID = grid_edges(3, 3)


def max_diff(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


def test_exact_means_and_variances_on_a_tree():
    rng = random.Random(1)
    tree = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5), (5, 6)]
    for _ in range(5):
        n = 7
        J = [[0.0] * n for _ in range(n)]
        for i in range(n):
            J[i][i] = rng.uniform(1.0, 2.0)
        for i, j in tree:
            J[i][j] = J[j][i] = rng.uniform(-0.33, 0.33)  # degree at most 3: diagonally dominant
        h = [rng.uniform(-1, 1) for _ in range(n)]
        m, s, it, ok = gabp(J, h)
        em, es = exact(J, h)
        assert ok and max_diff(m, em) < 1e-12 and max_diff(s, es) < 1e-12


def test_exact_means_inexact_variances_on_a_loopy_walk_summable_model():
    rng = random.Random(2)
    for _ in range(5):
        J = grid_precision(3, 3, {e: rng.uniform(-0.24, 0.24) for e in GRID})
        h = [rng.uniform(-1, 1) for _ in range(9)]
        assert walk_summability_radius(J) < 1  # at most 4 neighbors of weight 0.24
        m, s, _, ok = gabp(J, h)
        em, es = exact(J, h)
        assert ok
        assert max_diff(m, em) < 1e-10
        assert max_diff(s, es) > 1e-5


def test_attractive_model_variances_are_too_small():
    J = grid_precision(3, 3, {e: -0.2 for e in GRID})
    h = [0.5, -0.2, 0.3, 0.0, 1.0, -0.4, 0.2, 0.1, -0.3]
    assert abs(walk_summability_radius(J) - 0.4 * math.sqrt(2)) < 1e-9
    m, s, it, ok = gabp(J, h)
    em, es = exact(J, h)
    assert ok and it == 28
    assert max_diff(m, em) < 1e-10
    assert all(a < b for a, b in zip(s, es))
    assert [round(x, 4) for x in s[:5]] == [1.0961, 1.149, 1.0961, 1.149, 1.2115]
    assert [round(x, 4) for x in es[:5]] == [1.1023, 1.1611, 1.1023, 1.1611, 1.2353]


def k4(r):
    return [[1.0 if i == j else r for j in range(4)] for i in range(4)]


def test_positive_definite_but_not_walk_summable():
    h = [1.0, 0.0, 0.0, 0.0]
    # Eigenvalues of k4(r) are 1 + 3r and 1 - r: positive definite for r < 1.
    m, s, _, ok = gabp(k4(0.3), h)  # rho(|R|) = 0.9, walk-summable
    em, _ = exact(k4(0.3), h)
    assert abs(walk_summability_radius(k4(0.3)) - 0.9) < 1e-9
    assert ok and max_diff(m, em) < 1e-9
    for r in (0.35, 0.4, 0.5):  # rho(|R|) = 3r > 1
        assert walk_summability_radius(k4(r)) > 1
        assert not gabp(k4(r), h, max_iter=5000)[3]


def test_variance_recursion_has_no_fixed_point_past_one_eighth():
    # By symmetry every precision message on k4(r) is the same P, with P = -r^2 / (1 + 2P),
    # that is 2P^2 + P + r^2 = 0, which has a real root only when r^2 <= 1/8.
    for r, has_root in ((0.35, True), (0.36, False)):
        P = 0.0
        for _ in range(4000):
            if 1 + 2 * P <= 0:
                break
            P = -r * r / (1 + 2 * P)
        assert (1 + 2 * P > 0 and abs(2 * P * P + P + r * r) < 1e-9) == has_root
