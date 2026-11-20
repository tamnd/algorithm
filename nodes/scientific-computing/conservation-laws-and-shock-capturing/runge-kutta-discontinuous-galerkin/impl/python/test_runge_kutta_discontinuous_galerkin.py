# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/runge-kutta-discontinuous-galerkin/. The authors are listed in prov/FE63NV.jsonl.

import math
import random

import pytest

from runge_kutta_discontinuous_galerkin import (
    gauss_legendre, godunov_flux_burgers, legendre, limit, means, minmod, project,
    rkdg_solve, total_variation, tvb_minmod,
)

fb = lambda u: u * u / 2
u0 = lambda x: 0.5 + 0.25 * math.sin(2 * math.pi * x)
square = lambda x: 1.0 if 0.25 <= x < 0.75 else 0.0


def burgers_exact_smooth(x, t):
    """Solution of u = u0(x - u t) by Newton's method (valid before the shock time 2/pi)."""
    u = u0(x)
    for _ in range(60):
        g = u - u0(x - u * t)
        dg = 1 + t * 0.5 * math.pi * math.cos(2 * math.pi * (x - u * t))
        u -= g / dg
    return u


def square_exact(x, t):
    """Rarefaction from 0.25 and shock from 0.75 at speed 1/2 (valid for t < 1)."""
    if 0.25 <= x < 0.25 + t:
        return (x - 0.25) / t
    if 0.25 + t <= x < 0.75 + t / 2:
        return 1.0
    return 0.0


def l2_error(U, ex, q=6):
    M = len(U)
    dx = 1.0 / M
    xs, ws = gauss_legendre(q)
    s = 0.0
    for j in range(M):
        for xi, w in zip(xs, ws):
            uh = sum(c * legendre(l, xi) for l, c in enumerate(U[j]))
            s += w * (uh - ex((j + 0.5) * dx + xi * dx / 2)) ** 2 * dx / 2
    return math.sqrt(s)


def godunov_fv_ssprk3(v, dx, dt, T):
    """Independent first-order finite volume Godunov scheme with SSP-RK3 in time."""
    def L(w):
        n = len(w)
        F = [godunov_flux_burgers(w[j], w[(j + 1) % n]) for j in range(n)]
        return [-(F[j] - F[j - 1]) / dx for j in range(n)]
    t = 0.0
    while t < T - 1e-14:
        h = min(dt, T - t)
        a = [x + h * y for x, y in zip(v, L(v))]
        b = [0.75 * x + 0.25 * (y + h * z) for x, y, z in zip(v, a, L(a))]
        v = [x / 3 + 2 / 3 * (y + h * z) for x, y, z in zip(v, b, L(b))]
        t += h
    return v


def test_minmod_and_tvb_minmod():
    assert minmod(1.0, 2.0, 0.5) == 0.5
    assert minmod(-1.0, -2.0, -0.5) == -0.5
    assert minmod(1.0, -2.0, 0.5) == 0.0
    assert tvb_minmod(0.01, -1.0, 1.0, 0.02) == 0.01
    assert tvb_minmod(0.03, -1.0, 1.0, 0.02) == 0.0


def test_limiter_keeps_a_linear_function():
    M, dx = 10, 0.1
    U = [[0.3 + (j + 0.5) * dx, dx / 2, 0.0] for j in range(M)]
    V = limit(U, dx, 0.0)
    for j in range(1, M - 1):                 # the periodic wrap makes a jump at the ends
        assert V[j] == U[j]


def test_limiter_flattens_a_local_extremum_of_the_means():
    U = [[0.0, 0.0], [1.0, 0.4], [0.0, 0.0], [0.0, 0.0]]
    V = limit(U, 0.25, 0.0)
    assert V[1] == [1.0, 0.0]
    V = limit(U, 0.25, 1e3)                   # a large TVB constant leaves it alone
    assert V[1] == [1.0, 0.4]


def test_degree_zero_is_the_godunov_scheme():
    M = 30
    dx = 1.0 / M
    U = project(square, M, 0, 0.0, 1.0, q=20)
    v = godunov_fv_ssprk3(means(U), dx, 0.4 * dx, 0.2)
    W = means(rkdg_solve(U, dx, 0.4 * dx, 0.2, fb, godunov_flux_burgers))
    assert max(abs(a - b) for a, b in zip(v, W)) < 1e-13


@pytest.mark.parametrize("k,p_min", [(1, 1.85), (2, 2.8)])
def test_order_on_smooth_burgers_with_tvb_constant(k, p_min):
    T = 0.2
    errs = []
    for M in (10, 20, 40):
        dx = 1.0 / M
        U = rkdg_solve(project(u0, M, k, 0.0, 1.0), dx, 0.2 * dx, T, fb, godunov_flux_burgers, Mtvb=50.0)
        errs.append(l2_error(U, lambda x: burgers_exact_smooth(x, T)))
    assert math.log2(errs[1] / errs[2]) > p_min, errs


def test_minmod_limiter_clips_smooth_extrema():
    # With Mtvb = 0 the P2 method is limited at the extrema and loses its third order.
    T, errs = 0.2, []
    for M in (20, 40):
        dx = 1.0 / M
        U = rkdg_solve(project(u0, M, 2, 0.0, 1.0), dx, 0.2 * dx, T, fb, godunov_flux_burgers, Mtvb=0.0)
        errs.append(l2_error(U, lambda x: burgers_exact_smooth(x, T)))
    assert math.log2(errs[0] / errs[1]) < 2.2


@pytest.mark.parametrize("k", [1, 2])
def test_limited_means_stay_in_bounds_and_tv_does_not_grow(k):
    M = 50
    dx = 1.0 / M
    U = rkdg_solve(project(square, M, k, 0.0, 1.0, q=20), dx, 0.15 * dx, 0.0, fb, godunov_flux_burgers)
    tv = total_variation(means(U))
    for _ in range(40):
        U = rkdg_solve(U, dx, 0.15 * dx, 0.15 * dx, fb, godunov_flux_burgers)
        m = means(U)
        assert min(m) > -1e-12 and max(m) < 1 + 1e-12
        assert total_variation(m) <= tv + 1e-12
        tv = total_variation(m)


def test_unlimited_dg_overshoots_at_the_shock():
    M = 50
    dx = 1.0 / M
    U = rkdg_solve(project(square, M, 1, 0.0, 1.0, q=20), dx, 0.15 * dx, 0.3, fb,
                   godunov_flux_burgers, limiter=False)
    assert max(means(U)) > 1.005


def test_limited_p1_beats_first_order_godunov_after_the_shock():
    M, T = 100, 0.3
    dx = 1.0 / M
    exm = [sum(square_exact((j + (i + 0.5) / 100) * dx, T) for i in range(100)) / 100 for j in range(M)]
    e = {}
    for k in (0, 1):
        U = rkdg_solve(project(square, M, k, 0.0, 1.0, q=20), dx, 0.15 * dx, T, fb, godunov_flux_burgers)
        e[k] = sum(abs(a - b) for a, b in zip(means(U), exm)) * dx
    assert e[1] < 0.5 * e[0]
    assert e[1] < 1e-2


def test_mass_is_conserved_with_the_limiter():
    rng = random.Random(11)
    M = 24
    dx = 1.0 / M
    U = [[rng.uniform(0, 1), rng.uniform(-0.2, 0.2), rng.uniform(-0.05, 0.05)] for _ in range(M)]
    m0 = sum(means(U)) * dx
    V = rkdg_solve(U, dx, 0.1 * dx, 0.1, fb, godunov_flux_burgers)
    assert abs(sum(means(V)) * dx - m0) < 1e-13


def test_rejects_bad_steps():
    with pytest.raises(ValueError):
        rkdg_solve([[0.0, 0.0]] * 3, 0.1, -1.0, 1.0, fb, godunov_flux_burgers)
