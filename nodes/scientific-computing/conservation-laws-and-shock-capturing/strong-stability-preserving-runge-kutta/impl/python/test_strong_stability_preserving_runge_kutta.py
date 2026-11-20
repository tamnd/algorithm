# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strong-stability-preserving-runge-kutta/. The authors are listed in prov/4YEW5E.jsonl.

import random
from fractions import Fraction as Fr

from strong_stability_preserving_runge_kutta import METHODS, integrate, shu_osher_step, ssp_coefficient

# Classical RK4 in Shu-Osher form. It has a negative alpha, so its SSP coefficient is 0.
RK4_ALPHA = [[Fr(1)], [Fr(1), Fr(0)], [Fr(1), Fr(0), Fr(0)], [Fr(-1, 3), Fr(1, 3), Fr(2, 3), Fr(1, 3)]]
RK4_BETA = [[Fr(1, 2)], [Fr(0), Fr(1, 2)], [Fr(0), Fr(0), Fr(1)], [Fr(0), Fr(0), Fr(0), Fr(1, 6)]]


def total_variation(u):
    return sum(abs(u[j] - u[j - 1]) for j in range(len(u)))


def test_ssp_coefficients() -> None:
    expected = {"forward-euler": 1, "ssprk22": 1, "ssprk33": 1, "ssprk104": 6}
    for name, (alpha, beta, _) in METHODS.items():
        assert ssp_coefficient(alpha, beta) == expected[name]
        assert all(sum(row) == 1 for row in alpha)  # each stage is consistent
    assert ssp_coefficient(RK4_ALPHA, RK4_BETA) == 0


def test_stability_polynomials_exactly() -> None:
    # On u' = z u one step multiplies u by R(z); for s = p <= 4 stages R is the Taylor polynomial of e^z.
    for name, p in (("forward-euler", 1), ("ssprk22", 2), ("ssprk33", 3)):
        alpha, beta, _ = METHODS[name]
        for z in (Fr(-3, 2), Fr(-1, 3), Fr(2, 7)):
            r = shu_osher_step([Fr(1)], lambda v: [z * v[0]], Fr(1), alpha, beta)[0]
            taylor, term = Fr(0), Fr(1)
            for k in range(p + 1):
                taylor += term
                term = term * z / (k + 1)
            assert r == taylor
    r4 = shu_osher_step([Fr(1)], lambda v: [Fr(-1, 2) * v[0]], Fr(1), RK4_ALPHA, RK4_BETA)[0]
    assert r4 == 1 - Fr(1, 2) + Fr(1, 8) - Fr(1, 48) + Fr(1, 384)


def test_observed_orders_on_a_nonlinear_ode() -> None:
    # u' = -u^2, u(0) = 1, exact u(1) = 1/2. Halving dt divides the error by about 2^p.
    for name, (_, _, p) in METHODS.items():
        errs = [abs(integrate([1.0], lambda v: [-v[0] * v[0]], 1.0 / n, n, name)[0] - 0.5) for n in (10, 20, 40)]
        for e0, e1 in zip(errs, errs[1:]):
            assert 0.85 * 2**p < e0 / e1 < 1.25 * 2**p


def upwind(u):
    # u_t + u_x = 0, periodic, dx = 1: forward Euler with this L is TVD for dt <= 1.
    return [-(u[j] - u[j - 1]) for j in range(len(u))]


def test_tvd_up_to_the_ssp_time_step() -> None:
    rng = random.Random(11)
    u0 = [rng.uniform(-1, 1) for _ in range(30)]
    for name, dt in (("ssprk22", 1.0), ("ssprk33", 1.0), ("ssprk104", 6.0)):
        u = list(u0)
        tv = total_variation(u)
        for _ in range(40):
            u = integrate(u, upwind, dt, 1, name)
            assert total_variation(u) <= tv + 1e-12
            tv = total_variation(u)


def minmod(a, b):
    return 0.0 if a * b <= 0 else (a if abs(a) < abs(b) else b)


def burgers_muscl(u):
    """Burgers' equation, MUSCL with minmod slopes and the Godunov flux, periodic, dx = 1."""
    f = lambda v: v * v / 2

    def godunov(a, b):
        if a <= b:
            return 0.0 if a < 0 < b else min(f(a), f(b))
        return max(f(a), f(b))

    m = len(u)
    s = [minmod(u[(j + 1) % m] - u[j], u[j] - u[j - 1]) for j in range(m)]
    flux = [godunov(u[j] + s[j] / 2, u[(j + 1) % m] - s[(j + 1) % m] / 2) for j in range(m)]
    return [-(flux[j] - flux[j - 1]) for j in range(m)]


def gottlieb_shu_rk2(u, rhs, dt):
    """A second-order RK method with a negative coefficient (Gottlieb and Shu 1998)."""
    l0 = rhs(u)
    u1 = [a - 20 * dt * b for a, b in zip(u, l0)]
    l1 = rhs(u1)
    return [a + dt * (41 / 40 * b - 1 / 40 * c) for a, b, c in zip(u, l0, l1)]


def test_non_ssp_rk2_creates_oscillations_and_ssprk22_does_not() -> None:
    u0 = [1.0 if j < 20 else -0.5 for j in range(40)]
    dt = 0.3
    bad, good = list(u0), list(u0)
    tv_bad, tv_good = [], []
    for _ in range(26):
        bad = gottlieb_shu_rk2(bad, burgers_muscl, dt)
        good = integrate(good, burgers_muscl, dt, 1, "ssprk22")
        tv_bad.append(total_variation(bad))
        tv_good.append(total_variation(good))
    assert max(tv_good) <= 3 + 1e-12 and max(good) <= 1 + 1e-12
    assert max(tv_bad) > 3.1 and max(bad) > 1.03
