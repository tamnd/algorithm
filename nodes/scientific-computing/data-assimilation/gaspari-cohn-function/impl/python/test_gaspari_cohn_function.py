# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaspari-cohn-function/. The authors are listed in prov/4P6AFK.jsonl.

import math
import random
from fractions import Fraction as F

from gaspari_cohn_function import (
    _inner,
    _outer,
    chordal_ring_distance,
    gaspari_cohn,
    ring_distance,
    taper_matrix,
)


def test_check_values_exact():
    c = F(2)
    assert gaspari_cohn(F(0), c) == 1
    assert gaspari_cohn(F(1), c) == F(263, 384)
    assert gaspari_cohn(F(2), c) == F(5, 24)
    assert gaspari_cohn(F(3), c) == F(19, 1152)
    assert gaspari_cohn(F(4), c) == 0
    assert gaspari_cohn(F(9, 2), c) == 0
    assert gaspari_cohn(F(-3), c) == F(19, 1152)


def test_pieces_join_smoothly():
    one, two = F(1), F(2)
    assert _inner(one) == _outer(one) == F(5, 24)
    assert _outer(two) == 0
    h = 1e-3
    for z0, f, g in ((1.0, _inner, _outer), (2.0, _outer, lambda z: 0.0)):
        d1f = (f(z0 + h) - f(z0 - h)) / (2 * h)
        d1g = (g(z0 + h) - g(z0 - h)) / (2 * h)
        d2f = (f(z0 + h) - 2 * f(z0) + f(z0 - h)) / h ** 2
        d2g = (g(z0 + h) - 2 * g(z0) + g(z0 - h)) / h ** 2
        assert abs(d1f - d1g) < 1e-5 and abs(d2f - d2g) < 1e-4


def test_decreasing_between_zero_and_2c():
    vals = [gaspari_cohn(k / 100, 1.0) for k in range(201)]
    assert all(b < a for a, b in zip(vals, vals[1:]))
    assert all(0 <= v <= 1 for v in vals)


def circulant_eigenvalues(row):
    n = len(row)
    return [sum(row[k] * math.cos(2 * math.pi * j * k / n) for k in range(n)) for j in range(n)]


def test_ring_of_40_points():
    n = 40
    for c in (2, 4, 8, 10, 12, 15, 20, 40):
        lam = circulant_eigenvalues([gaspari_cohn(chordal_ring_distance(n)(0, k), c) for k in range(n)])
        assert min(lam) > 0
    for c in (2, 4, 8, 10):
        lam = circulant_eigenvalues([gaspari_cohn(ring_distance(n)(0, k), c) for k in range(n)])
        assert min(lam) > 0
    lam = circulant_eigenvalues([gaspari_cohn(ring_distance(n)(0, k), 15) for k in range(n)])
    assert min(lam) < -0.06


def cholesky_ok(a):
    n = len(a)
    low = [[0.0] * n for _ in range(n)]
    for j in range(n):
        s = a[j][j] - sum(low[j][k] ** 2 for k in range(j))
        if s <= 0:
            return False
        low[j][j] = math.sqrt(s)
        for i in range(j + 1, n):
            low[i][j] = (a[i][j] - sum(low[i][k] * low[j][k] for k in range(j))) / low[j][j]
    return True


def test_positive_definite_for_points_in_three_dimensions():
    rng = random.Random(7)
    pts = [tuple(rng.uniform(0, 3) for _ in range(3)) for _ in range(40)]
    A = taper_matrix(pts, 1.0, math.dist)
    assert all(A[i][i] == 1 for i in range(40))
    assert cholesky_ok(A)


def test_gaussian_with_the_same_curvature():
    L = math.sqrt(0.3)
    for z in (0.05, 0.1):
        assert abs(gaspari_cohn(z, 1.0) - math.exp(-z * z / (2 * L * L))) < 2 * z ** 3
