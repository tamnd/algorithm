# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/locality-preserving-projections/. The authors are listed in prov/3ZFNH0.jsonl.

import math
import random

import pytest

from locality_preserving_projections import (
    heat_kernel_graph,
    locality_preserving_projections,
    lpp_from_weights,
    project,
)


def generalized_residual(x, w, a, lam):
    n, p = len(x), len(x[0])
    deg = [sum(row) for row in w]
    f = [sum(a[b] * x[i][b] for b in range(p)) for i in range(n)]
    lf = [deg[i] * f[i] - sum(w[i][j] * f[j] for j in range(n)) for i in range(n)]
    left = [sum(x[i][b] * lf[i] for i in range(n)) for b in range(p)]
    right = [lam * sum(x[i][b] * deg[i] * f[i] for i in range(n)) for b in range(p)]
    return max(abs(u - v) for u, v in zip(left, right))


def test_identity_features_give_laplacian_eigenmaps_on_a_path():
    # With X = I, P = L and Q = D, so LPP solves L y = lambda D y, the problem of
    # Laplacian eigenmaps. On a path the solutions are cos(pi k j / (n - 1)).
    n = 8
    w = [[1.0 if abs(i - j) == 1 else 0.0 for j in range(n)] for i in range(n)]
    ident = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    a, lam = lpp_from_weights(ident, w, 4)
    assert abs(lam[0]) < 1e-12
    assert max(abs(v - a[0][0]) for v in a[0]) < 1e-12  # the constant, lambda_0 = 0
    for kk in range(1, 4):
        assert abs(lam[kk] - (1 - math.cos(math.pi * kk / (n - 1)))) < 1e-12
        ref = [math.cos(math.pi * kk * j / (n - 1)) for j in range(n)]
        ratio = a[kk][0] / ref[0]
        assert max(abs(u - ratio * v) for u, v in zip(a[kk], ref)) < 1e-9


def test_identity_features_solve_the_eigenmap_equation_on_a_heat_kernel_graph():
    rng = random.Random(4)
    pts = [(rng.uniform(0, 3), rng.uniform(0, 1)) for _ in range(15)]
    w = heat_kernel_graph(pts, k=4, t=0.5)
    n = len(pts)
    deg = [sum(row) for row in w]
    ident = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    a, lam = lpp_from_weights(ident, w, 4)
    assert abs(lam[0]) < 1e-10
    for l in range(1, 4):
        y = a[l]
        ly = [deg[i] * y[i] - sum(w[i][j] * y[j] for j in range(n)) for i in range(n)]
        assert max(abs(ly[i] - lam[l] * deg[i] * y[i]) for i in range(n)) < 1e-9
        assert abs(sum(deg[i] * y[i] for i in range(n))) < 1e-9


def test_two_rows_example():
    # Two rows y = 0.75 and y = -0.75, x = 0, 1, 2, unit weights within a row.
    pts = [(float(x), 0.75) for x in range(3)] + [(float(x), -0.75) for x in range(3)]
    a, y, lam = locality_preserving_projections(pts, 2, eps=1.0)
    assert abs(lam[0]) < 1e-12 and abs(lam[1] - 1 / 3) < 1e-12
    assert abs(a[0][0]) < 1e-12 and abs(abs(a[0][1]) - 1 / math.sqrt(4.5)) < 1e-12
    assert abs(abs(a[1][0]) - 1 / math.sqrt(12)) < 1e-12 and abs(a[1][1]) < 1e-12
    first = [abs(v[0]) for v in y]
    assert all(abs(v - 1 / (2 * math.sqrt(2))) < 1e-12 for v in first)


def test_equation_and_q_orthonormality_in_three_dimensions():
    rng = random.Random(5)
    pts = []
    for _ in range(30):
        u = rng.uniform(0, 4)
        pts.append((u, math.sin(u) + rng.gauss(0, 0.05), rng.gauss(0, 0.3)))
    w = heat_kernel_graph(pts, k=5, t=1.0)
    a, lam = lpp_from_weights(pts, w, 3)
    deg = [sum(row) for row in w]
    for l in range(3):
        assert generalized_residual(pts, w, a[l], lam[l]) < 1e-9
        for l2 in range(3):
            fa = project([a[l]], pts)
            fb = project([a[l2]], pts)
            dot = sum(deg[i] * fa[i][0] * fb[i][0] for i in range(len(pts)))
            assert abs(dot - (1.0 if l == l2 else 0.0)) < 1e-9
    assert lam[0] <= lam[1] <= lam[2]


def test_new_points_use_the_same_linear_map():
    pts = [(float(x), 0.75) for x in range(3)] + [(float(x), -0.75) for x in range(3)]
    a, _, _ = locality_preserving_projections(pts, 1, eps=1.0)
    (y_new,) = project(a, [(10.0, 0.75)])
    assert abs(abs(y_new[0]) - 1 / (2 * math.sqrt(2))) < 1e-12


def test_rank_deficient_data_is_rejected():
    pts = [(float(i), 2.0 * i, 0.0) for i in range(5)]
    with pytest.raises(ValueError):
        locality_preserving_projections(pts, 1, k=2)
