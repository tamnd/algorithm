# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hessian-eigenmaps/. The authors are listed in prov/MMQJ8B.jsonl.

import math
import random

import pytest

from hessian_eigenmaps import hessian_eigenmaps, hessian_matrix


def l_domain(seed, curved=False):
    """A jittered grid on the L-shaped region [0,3]^2 minus (1.5,3]^2, which is not convex.
    The flat version lies in a tilted plane in R^3. The curved version rolls the sheet
    onto a cylinder of radius 2, which keeps all lengths on the sheet."""
    rng = random.Random(seed)
    uv = []
    for a in range(7):
        for b in range(7):
            u, v = 0.5 * a, 0.5 * b
            if u > 1.5 and v > 1.5:
                continue
            uv.append((u + rng.uniform(-0.1, 0.1), v + rng.uniform(-0.1, 0.1)))
    if curved:
        pts = [(2 * math.cos(u / 2), 2 * math.sin(u / 2), v) for u, v in uv]
    else:
        pts = [((3 * u + 4 * v) / 5, (12 * u - 9 * v) / 25, (16 * u - 12 * v) / 25 + 1) for u, v in uv]
    return pts, uv


def residual_of_fit(y, z):
    """Least squares residual of z on the columns [1, y], relative to the spread of z."""
    n, m = len(y), len(y[0])
    q = []
    for col in [[1.0] * n] + [[r[l] for r in y] for l in range(m)]:
        v = col[:]
        for u in q:
            d = sum(a * b for a, b in zip(u, v))
            v = [a - d * b for a, b in zip(v, u)]
        nv = math.sqrt(sum(a * a for a in v))
        if nv > 1e-12:
            q.append([a / nv for a in v])
    r = list(z)
    for u in q:
        d = sum(a * b for a, b in zip(u, r))
        r = [a - d * b for a, b in zip(r, u)]
    mean = sum(z) / n
    return math.sqrt(sum(a * a for a in r) / sum((a - mean) ** 2 for a in z))


def test_flat_map_is_an_isometry():
    pts, uv = l_domain(0)
    for i in range(0, len(uv), 7):
        for j in range(len(uv)):
            assert abs(math.dist(pts[i], pts[j]) - math.dist(uv[i], uv[j])) < 1e-12


def test_constant_and_linear_functions_are_in_the_null_space():
    pts, uv = l_domain(1)
    h = hessian_matrix(pts, k=8, m=2)
    n = len(pts)
    for f in ([1.0] * n, [p[0] for p in uv], [p[1] for p in uv]):
        hf = [sum(h[i][j] * f[j] for j in range(n)) for i in range(n)]
        assert max(abs(x) for x in hf) < 1e-9


def test_quadratic_function_is_not_in_the_null_space():
    pts, uv = l_domain(1)
    h = hessian_matrix(pts, k=8, m=2)
    n = len(pts)
    f = [p[0] * p[1] for p in uv]
    assert sum(f[i] * h[i][j] * f[j] for i in range(n) for j in range(n)) > 1e-2


def test_recovers_nonconvex_flat_sheet():
    pts, uv = l_domain(2)
    y, lam = hessian_eigenmaps(pts, k=8, m=2)
    assert abs(lam[0]) < 1e-9 and abs(lam[1]) < 1e-9 and lam[2] > 1e-4
    for c in range(2):
        assert residual_of_fit(y, [p[c] for p in uv]) < 1e-6


def test_recovers_rolled_sheet_approximately():
    pts, uv = l_domain(3, curved=True)
    y, _ = hessian_eigenmaps(pts, k=8, m=2)
    for c in range(2):
        assert residual_of_fit(y, [p[c] for p in uv]) < 0.05


def test_too_few_neighbors():
    pts, _ = l_domain(0)
    with pytest.raises(ValueError):
        hessian_eigenmaps(pts, k=4, m=2)
