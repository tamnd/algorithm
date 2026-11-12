# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/umap/. The authors are listed in prov/FBD238.jsonl.

import math
import random

from umap import (
    attract_coeff,
    distances,
    fit_ab,
    fuzzy_simplicial_set,
    fuzzy_union,
    nearest_neighbors,
    repel_coeff,
    smooth_knn,
    spectral_init,
    umap,
)


def blobs(rng, n_per=8, centers=((0.0, 0.0, 0.0, 0.0), (8.0, 0.0, 0.0, 0.0), (0.0, 8.0, 0.0, 0.0))):
    return [[c + rng.gauss(0.0, 1.0) for c in center] for center in centers for _ in range(n_per)]


def test_sigma_search_meets_log2_k():
    x = blobs(random.Random(3))
    d = distances(x)
    for k in (3, 5, 10):
        for i, nbrs in enumerate(nearest_neighbors(d, k)):
            ds = [d[i][j] for j in nbrs]
            rho, sigma = smooth_knn(ds, tol=1e-9)
            assert rho == min(ds)
            s = sum(math.exp(-max(0.0, v - rho) / sigma) for v in ds)
            assert abs(s - math.log2(k)) < 1e-8


def test_hand_example_memberships():
    a = fuzzy_simplicial_set([[0.0], [1.0], [3.0], [7.0]], 3)
    for i in range(4):
        assert max(a[i]) == 1.0  # the nearest neighbor always gets membership 1
    assert abs(a[0][2] - 0.4767) < 1e-4 and abs(a[3][0] - 0.2203) < 1e-4


def test_fuzzy_union():
    assert abs(fuzzy_union([[0.0, 0.5], [0.4, 0.0]])[0][1] - 0.7) < 1e-15
    a = fuzzy_simplicial_set(blobs(random.Random(7)), 5)
    w = fuzzy_union(a)
    n = len(w)
    for i in range(n):
        for j in range(n):
            assert w[i][j] == w[j][i]
            assert max(a[i][j], a[j][i]) - 1e-15 <= w[i][j] <= min(1.0, a[i][j] + a[j][i]) + 1e-15


def test_ab_fit_at_min_dist_0_1():
    a, b = fit_ab(0.1)
    # umap-learn's find_ab_params(spread=1, min_dist=0.1) gives a = 1.5769, b = 0.8951
    assert abs(a - 1.5769) < 1e-3 and abs(b - 0.8951) < 1e-3
    a0, b0 = fit_ab(0.5)
    assert a0 < a and b0 > b  # a larger min_dist gives a flatter top


def test_sgd_coefficients_are_cross_entropy_gradients():
    a, b = 1.5769, 0.8951
    h = 1e-6
    for yi in (0.3, 1.0, 2.5):
        def v(y):
            return 1.0 / (1.0 + a * (y * y) ** b)
        fd_attr = (-math.log(v(yi + h)) + math.log(v(yi - h))) / (2 * h)
        fd_rep = (-math.log(1 - v(yi + h)) + math.log(1 - v(yi - h))) / (2 * h)
        # the SGD step is minus the gradient: coeff * (y_i - y_j) with y_j = 0
        assert abs(attract_coeff(yi * yi, a, b) * yi + fd_attr) < 1e-6
        assert abs(repel_coeff(yi * yi, a, b, eps=0.0) * yi + fd_rep) < 1e-6


def test_spectral_init_orders_a_path():
    w = fuzzy_union(fuzzy_simplicial_set([[0.0], [1.0], [3.0], [7.0]], 3))
    y = [r[0] for r in spectral_init(w, 1)]
    assert y == sorted(y) or y == sorted(y, reverse=True)


def test_umap_keeps_blobs_apart():
    x = blobs(random.Random(5))
    y, _ = umap(x, random.Random(1), k=5, epochs=200)
    n = len(y)
    for i in range(n):
        j = min((k for k in range(n) if k != i), key=lambda k: sum((u - v) ** 2 for u, v in zip(y[i], y[k])))
        assert i // 8 == j // 8
