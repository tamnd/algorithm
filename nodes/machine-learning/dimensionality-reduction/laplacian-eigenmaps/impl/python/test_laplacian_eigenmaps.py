# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplacian-eigenmaps/. The authors are listed in prov/N1D05V.jsonl.

import math
import random

import pytest

from laplacian_eigenmaps import heat_kernel_graph, laplacian_eigenmaps, laplacian_eigenmaps_from_weights


def test_path_graph_closed_form():
    # Unit weights on a path of n vertices: lambda_k = 1 - cos(pi k / (n - 1)),
    # y_k(j) proportional to cos(pi k j / (n - 1)).
    n = 9
    pts = [(float(j),) for j in range(n)]
    y, lam = laplacian_eigenmaps(pts, 3, eps=1.0)
    for kk in range(1, 4):
        assert abs(lam[kk - 1] - (1 - math.cos(math.pi * kk / (n - 1)))) < 1e-12
        col = [r[kk - 1] for r in y]
        ref = [math.cos(math.pi * kk * j / (n - 1)) for j in range(n)]
        ratio = col[0] / ref[0]
        assert max(abs(a - ratio * b) for a, b in zip(col, ref)) < 1e-9


def test_generalized_eigen_equation_and_d_orthonormality():
    rng = random.Random(3)
    pts = [(rng.uniform(0, 3), rng.uniform(0, 1)) for _ in range(25)]
    w = heat_kernel_graph(pts, k=5, t=0.5)
    deg = [sum(row) for row in w]
    y, lam = laplacian_eigenmaps_from_weights(w, 3)
    n = len(pts)
    for l in range(3):
        f = [r[l] for r in y]
        lf = [deg[i] * f[i] - sum(w[i][j] * f[j] for j in range(n)) for i in range(n)]
        assert max(abs(lf[i] - lam[l] * deg[i] * f[i]) for i in range(n)) < 1e-9
        assert abs(sum(deg[i] * f[i] for i in range(n))) < 1e-9
        for l2 in range(3):
            g = [r[l2] for r in y]
            dot = sum(deg[i] * f[i] * g[i] for i in range(n))
            assert abs(dot - (1.0 if l == l2 else 0.0)) < 1e-9
    assert 0 < lam[0] <= lam[1] <= lam[2]


def test_curve_is_ordered():
    # Points on a spiral arc: the first coordinate is monotone along the arc.
    rng = random.Random(8)
    ts = [0.15 * i + rng.uniform(-0.03, 0.03) for i in range(30)]
    pts = [((1 + 0.3 * t) * math.cos(t), (1 + 0.3 * t) * math.sin(t)) for t in ts]
    y, _ = laplacian_eigenmaps(pts, 1, k=3, t=1.0)
    c = [v for (v,) in y]
    assert all(a < b for a, b in zip(c, c[1:])) or all(a > b for a, b in zip(c, c[1:]))


def test_disconnected_graph_is_rejected():
    pts = [(0.0,), (1.0,), (2.0,), (10.0,), (11.0,)]
    with pytest.raises(ValueError):
        laplacian_eigenmaps(pts, 1, eps=1.0)
