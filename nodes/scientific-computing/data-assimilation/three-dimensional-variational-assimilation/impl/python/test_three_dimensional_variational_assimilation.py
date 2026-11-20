# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-dimensional-variational-assimilation/. The authors are listed in prov/BZ95E9.jsonl.

import math
import random

import scimat
from three_dimensional_variational_assimilation import (
    conjugate_gradient,
    cost,
    gradient,
    linear_operator,
    var3d,
)


def random_spd(rng, n):
    L = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    S = scimat.matmul(L, scimat.transpose(L))
    for i in range(n):
        S[i][i] += 0.5
    return S


def kalman_analysis(xb, B, yo, H, R):
    """Oracle: x^b + B H^T (H B H^T + R)^-1 (y^o - H x^b), by Gaussian elimination."""
    A = scimat.add(scimat.matmul(scimat.matmul(H, B), scimat.transpose(H)), R)
    d = scimat.sub(yo, scimat.matvec(H, xb))
    z = scimat.solve(A, d)
    return scimat.add(xb, scimat.matvec(scimat.matmul(B, scimat.transpose(H)), z))


def speed():
    h = lambda x: [math.hypot(x[0], x[1])]
    jac = lambda x: [[x[0] / math.hypot(x[0], x[1]), x[1] / math.hypot(x[0], x[1])]]
    return h, jac


def test_scalar_check_value():
    h, jac = linear_operator([[1.0]])
    xa, _ = var3d([0.0], [[1.0]], [1.0], h, jac, [[1.0]])
    assert abs(xa[0] - 0.5) < 1e-15


def test_linear_equals_kalman_and_oi_formula():
    rng = random.Random(21)
    for _ in range(200):
        n, p = rng.randint(1, 6), rng.randint(1, 5)
        B, R = random_spd(rng, n), random_spd(rng, p)
        H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)]
        xb = [rng.uniform(-3, 3) for _ in range(n)]
        yo = [rng.uniform(-3, 3) for _ in range(p)]
        h, jac = linear_operator(H)
        xa, its = var3d(xb, B, yo, h, jac, R)
        xk = kalman_analysis(xb, B, yo, H, R)
        for a, b in zip(xa, xk):
            assert abs(a - b) <= 1e-10 * (1 + abs(b))
        # one outer loop is exact for a linear h
        for a, b in zip(its[1], xk):
            assert abs(a - b) <= 1e-10 * (1 + abs(b))
        assert len(its) <= 3


def test_gradient_matches_finite_differences():
    rng = random.Random(22)
    n, p = 4, 3

    def h(x):
        return [x[0] * x[1], math.sin(x[2]) + x[3], x[0] ** 2 - x[3]]

    def jac(x):
        return [[x[1], x[0], 0.0, 0.0], [0.0, 0.0, math.cos(x[2]), 1.0], [2 * x[0], 0.0, 0.0, -1.0]]

    B, R = random_spd(rng, n), random_spd(rng, p)
    xb = [rng.uniform(-1, 1) for _ in range(n)]
    yo = [rng.uniform(-1, 1) for _ in range(p)]
    for _ in range(5):
        x = [rng.uniform(-1, 1) for _ in range(n)]
        g = gradient(x, xb, B, yo, h, jac, R)
        eps = 1e-6
        for j in range(n):
            xp, xm = list(x), list(x)
            xp[j] += eps
            xm[j] -= eps
            fd = (cost(xp, xb, B, yo, h, R) - cost(xm, xb, B, yo, h, R)) / (2 * eps)
            assert abs(fd - g[j]) < 1e-6 * (1 + abs(g[j]))


def test_wind_speed_isotropic_exact():
    # B = I: the minimum lies on the ray through x^b with speed (5 + 6) / 2.
    h, jac = speed()
    xa, its = var3d([3.0, 4.0], [[1.0, 0.0], [0.0, 1.0]], [6.0], h, jac, [[1.0]])
    assert abs(xa[0] - 3.3) < 1e-12 and abs(xa[1] - 4.4) < 1e-12


def test_wind_speed_anisotropic_converges_to_stationary_point():
    h, jac = speed()
    B = [[1.0, 0.0], [0.0, 4.0]]
    xa, its = var3d([3.0, 4.0], B, [6.0], h, jac, [[1.0]])
    g = gradient(xa, [3.0, 4.0], B, [6.0], h, jac, [[1.0]])
    assert max(abs(v) for v in g) < 1e-10
    assert abs(xa[0] - 3.134034646) < 1e-8 and abs(xa[1] - 4.825496589) < 1e-8
    costs = [cost(x, [3.0, 4.0], B, [6.0], h, [[1.0]]) for x in its]
    assert all(costs[k + 1] <= costs[k] + 1e-15 for k in range(len(costs) - 1))
    # Gauss-Newton converges linearly here: the residual is not zero and h is curved.
    e = [scimat.norm2(scimat.sub(x, xa)) for x in its[1:5]]
    for k in range(len(e) - 1):
        assert 0.01 < e[k + 1] / e[k] < 0.1
    # The minimum is a global one: compare with a fine grid search.
    best = min(
        cost([3.0 + i * 0.01 - 1.0, 4.0 + j * 0.01 - 1.0], [3.0, 4.0], B, [6.0], h, [[1.0]])
        for i in range(201)
        for j in range(201)
    )
    assert cost(xa, [3.0, 4.0], B, [6.0], h, [[1.0]]) <= best + 1e-12


def test_conjugate_gradient_against_elimination():
    rng = random.Random(23)
    for _ in range(100):
        n = rng.randint(1, 8)
        A = random_spd(rng, n)
        b = [rng.uniform(-1, 1) for _ in range(n)]
        z = conjugate_gradient(lambda v: scimat.matvec(A, v), b)
        zo = scimat.solve(A, b)
        for a, c in zip(z, zo):
            assert abs(a - c) <= 1e-9 * (1 + abs(c))


def test_no_information_in_observations():
    # Huge R: the analysis stays at the background.
    h, jac = linear_operator([[1.0, 1.0]])
    xa, _ = var3d([1.0, 2.0], [[1.0, 0.3], [0.3, 2.0]], [100.0], h, jac, [[1e12]])
    assert abs(xa[0] - 1.0) < 1e-8 and abs(xa[1] - 2.0) < 1e-8
