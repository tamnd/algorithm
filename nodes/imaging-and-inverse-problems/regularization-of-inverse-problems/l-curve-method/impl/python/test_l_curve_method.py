# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/l-curve-method/. The authors are listed in prov/W03DNM.jsonl.

import math
import random

from imgla import matmul, matvec, norm2, rmatvec, solve, svd, transpose
from l_curve_method import (
    coefficients,
    curvature,
    l_curve_corner,
    l_curve_corner_matrix,
    l_curve_points,
    norms,
    tikhonov_svd,
)


def deriv2(n):
    """Discretized Green's function of -u'' on [0, 1] with zero boundary values."""
    h = 1.0 / n
    t = [(i + 0.5) * h for i in range(n)]
    return [[h * (t[i] * (t[j] - 1.0) if t[i] < t[j] else t[j] * (t[i] - 1.0)) for j in range(n)] for i in range(n)]


def integration_matrix(n):
    h = 1.0 / n
    return [[h if j <= i else 0.0 for j in range(n)] for i in range(n)]


def bumps(n):
    t = [(j + 0.5) / n for j in range(n)]
    return [math.exp(-80.0 * (x - 0.3) ** 2) + 0.6 * math.exp(-80.0 * (x - 0.7) ** 2) for x in t]


def noisy(a, xt, rel, seed):
    y0 = matvec(a, xt)
    rng = random.Random(seed)
    e = [rng.gauss(0.0, 1.0) for _ in y0]
    c = rel * norm2(y0) / norm2(e)
    return [p + c * q for p, q in zip(y0, e)], c * norm2(e)


def tikhonov_solve(a, y, alpha):
    ata = matmul(transpose(a), a)
    for i in range(len(ata)):
        ata[i][i] += alpha
    return solve(ata, rmatvec(a, y))


def best_on_grid(s, v, b, xt):
    return min(math.dist(tikhonov_svd(s, v, b, 10.0 ** (k / 40.0)), xt) for k in range(-400, 40))


def test_page_example():
    a, xt = deriv2(24), bumps(24)
    y, delta = noisy(a, xt, 0.1, 0)
    u, s, v = svd(a)
    alpha, x, kappa = l_curve_corner(u, s, v, y)
    assert abs(alpha / 8.5477e-5 - 1.0) < 1e-3
    assert abs(kappa - 4.4994) < 1e-3
    assert abs(math.dist(x, xt) - 0.8850) < 1e-3
    b, p2 = coefficients(u, s, y)
    assert abs(math.sqrt(norms(s, b, p2, alpha)[1]) - 0.01782) < 1e-5
    assert abs(delta - 0.01754) < 1e-5


def test_norms_match_direct_solves():
    a = deriv2(10)
    y, _ = noisy(a, bumps(10), 0.05, 3)
    u, s, v = svd(a)
    b, p2 = coefficients(u, s, y)
    for alpha in (1e-6, 1e-4, 1e-2):
        x = tikhonov_solve(a, y, alpha)
        r = [p - q for p, q in zip(matvec(a, x), y)]
        eta, rho, _ = norms(s, b, p2, alpha)
        assert abs(eta - norm2(x) ** 2) <= 1e-8 * eta
        assert abs(rho - norm2(r) ** 2) <= 1e-8 * rho
        assert math.dist(tikhonov_svd(s, v, b, alpha), x) <= 1e-8 * norm2(x)


def test_derivative_and_curvature_match_finite_differences():
    a = deriv2(12)
    y, _ = noisy(a, bumps(12), 0.05, 4)
    u, s, v = svd(a)
    b, p2 = coefficients(u, s, y)
    for t in (-14.0, -11.0, -9.0, -6.0):
        h = 1e-4
        ep = norms(s, b, p2, math.exp(t + h))[0]
        em = norms(s, b, p2, math.exp(t - h))[0]
        deta = norms(s, b, p2, math.exp(t))[2]
        assert abs((ep - em) / (math.exp(t + h) - math.exp(t - h)) - deta) <= 1e-6 * abs(deta)
        # curvature of the parametric curve (log rho / 2, log eta / 2) in t = log alpha
        (x0, y0), (x1, y1), (x2, y2) = l_curve_points(s, b, p2, [math.exp(t - h), math.exp(t), math.exp(t + h)])
        dx, dy = (x2 - x0) / (2 * h), (y2 - y0) / (2 * h)
        ddx, ddy = (x2 - 2 * x1 + x0) / h ** 2, (y2 - 2 * y1 + y0) / h ** 2
        k_fd = (dx * ddy - ddx * dy) / (dx * dx + dy * dy) ** 1.5
        k = curvature(s, b, p2, math.exp(t))
        assert abs(k_fd - k) <= 1e-4 * max(1.0, abs(k))


def test_curve_is_monotone():
    a = deriv2(10)
    y, _ = noisy(a, bumps(10), 0.02, 5)
    u, s, v = svd(a)
    b, p2 = coefficients(u, s, y)
    pts = l_curve_points(s, b, p2, [10.0 ** (k / 4.0) for k in range(-40, 0)])
    assert all(pts[i][0] < pts[i + 1][0] for i in range(len(pts) - 1))
    assert all(pts[i][1] > pts[i + 1][1] for i in range(len(pts) - 1))


def test_corner_is_a_local_maximum_above_the_grid():
    a = deriv2(16)
    u, s, v = svd(a)
    for seed in range(3):
        y, _ = noisy(a, bumps(16), 0.05, 10 + seed)
        b, p2 = coefficients(u, s, y)
        alpha, _, kappa = l_curve_corner(u, s, v, y)
        assert abs(curvature(s, b, p2, alpha) - kappa) <= 1e-12 * abs(kappa)
        lo, hi = math.log(s[-1] ** 2), math.log(s[0] ** 2)
        grid = [curvature(s, b, p2, math.exp(lo + (hi - lo) * j / 59)) for j in range(60)]
        assert kappa >= max(grid)
        for f in (0.999, 1.001):
            assert curvature(s, b, p2, alpha * f) <= kappa + 1e-9


def test_error_close_to_best_on_a_favourable_problem():
    a, xt = deriv2(24), bumps(24)
    u, s, v = svd(a)
    for rel, factor in ((0.1, 1.6), (0.01, 2.0)):
        for seed in range(3):
            y, _ = noisy(a, xt, rel, seed)
            b, _ = coefficients(u, s, y)
            _, x, _ = l_curve_corner(u, s, v, y)
            assert math.dist(x, xt) <= factor * best_on_grid(s, v, b, xt)


def test_scaling_moves_alpha_by_c_squared():
    a = deriv2(12)
    y, _ = noisy(a, bumps(12), 0.05, 6)
    alpha, x, kappa = l_curve_corner_matrix(a, y)
    c = 7.0
    ac = [[c * t for t in row] for row in a]
    alpha_c, x_c, kappa_c = l_curve_corner_matrix(ac, [c * t for t in y])
    assert abs(alpha_c / (c * c * alpha) - 1.0) < 1e-4
    assert math.dist(x, x_c) <= 1e-4 * norm2(x)
    assert abs(kappa - kappa_c) <= 1e-6 * abs(kappa)


def test_no_corner_on_a_mildly_ill_posed_problem():
    n = 16
    a = integration_matrix(n)
    xt = [math.sin(math.pi * (j + 0.5) / n) for j in range(n)]
    y, _ = noisy(a, xt, 0.01, 1)
    u, s, v = svd(a)
    b, p2 = coefficients(u, s, y)
    _, _, kappa = l_curve_corner(u, s, v, y)
    assert kappa < 0.0
    lo, hi = math.log(s[-1] ** 2), math.log(s[0] ** 2)
    assert all(curvature(s, b, p2, math.exp(lo + (hi - lo) * j / 99)) < 0.0 for j in range(100))
