# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exact-riemann-solver/. The authors are listed in prov/P7B1QH.jsonl.

import random

import pytest

from exact_riemann_solver import (
    VacuumError,
    euler_flux,
    godunov_flux,
    pressure_function,
    sample,
    sound_speed,
    star_state,
)

G = 1.4
SOD = ((1.0, 0.0, 1.0), (0.125, 0.0, 0.1))

# The five standard tests of Toro 2009, Section 4.3.3, with p* and u* to the digits printed there.
TORO = [
    ((1.0, 0.0, 1.0), (0.125, 0.0, 0.1), 0.30313, 0.92745),
    ((1.0, -2.0, 0.4), (1.0, 2.0, 0.4), 0.00189, 0.0),
    ((1.0, 0.0, 1000.0), (1.0, 0.0, 0.01), 460.894, 19.5975),
    ((1.0, 0.0, 0.01), (1.0, 0.0, 100.0), 46.0950, -6.19633),
    ((5.99924, 19.5975, 460.894), (5.99242, -6.19633, 46.0950), 1691.64, 8.68975),
]


def conserved(w):
    rho, u, p = w
    return (rho, rho * u, p / (G - 1.0) + 0.5 * rho * u * u)


def test_sod_check_values() -> None:
    s = star_state(*SOD)
    assert abs(s["p"] - 0.30313) < 5e-6
    assert abs(s["u"] - 0.92745) < 5e-6
    assert abs(s["rho_L"] - 0.42632) < 5e-6
    assert abs(s["rho_R"] - 0.26557) < 5e-6
    assert abs(s["shock_R"] - 1.75216) < 5e-6
    assert s["iterations"] <= 5


def test_toro_table() -> None:
    for left, right, p, u in TORO:
        s = star_state(left, right)
        assert abs(s["p"] - p) <= 5e-5 * max(1.0, p) + 5e-6
        assert abs(s["u"] - u) <= 5e-5 * max(1.0, abs(u))


def test_root_against_bisection() -> None:
    rng = random.Random(7)
    for _ in range(200):
        left = (rng.uniform(0.1, 5), rng.uniform(-1, 1), rng.uniform(0.1, 5))
        right = (rng.uniform(0.1, 5), rng.uniform(-1, 1), rng.uniform(0.1, 5))
        p = star_state(left, right)["p"]
        lo, hi = 1e-12, 1e3
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if pressure_function(mid, left, right, G)[0] < 0:
                lo = mid
            else:
                hi = mid
        assert abs(p - lo) <= 1e-9 * max(1.0, p)


def test_shocks_satisfy_rankine_hugoniot() -> None:
    for left, right, _, _ in TORO:
        s = star_state(left, right)
        for side, data in (("L", left), ("R", right)):
            if "shock_" + side not in s:
                continue
            star = (s["rho_" + side], s["u"], s["p"])
            sp = s["shock_" + side]
            uq, ud = conserved(star), conserved(data)
            fq, fd = euler_flux(star), euler_flux(data)
            for k in range(3):
                jump = sp * (uq[k] - ud[k]) - (fq[k] - fd[k])
                assert abs(jump) <= 1e-9 * (1.0 + abs(fq[k]) + abs(fd[k]))


def test_rarefaction_invariants() -> None:
    left, right = SOD
    s = star_state(left, right)
    ent = left[2] / left[0] ** G
    inv = left[1] + 2.0 * sound_speed(left[0], left[2], G) / (G - 1.0)
    for k in range(11):
        xi = s["head_L"] + (s["tail_L"] - s["head_L"]) * k / 10
        rho, u, p = sample(xi, left, right, star=s)
        assert abs(p / rho**G - ent) < 1e-12
        assert abs(u + 2.0 * sound_speed(rho, p, G) / (G - 1.0) - inv) < 1e-12
        assert abs(u - sound_speed(rho, p, G) - xi) < 1e-12


def test_integral_form_of_the_conservation_law() -> None:
    # Over [-a, a] at t = 1: integral of U = a (U_L + U_R) - (F(U_R) - F(U_L)).
    for left, right, _, _ in TORO[:2]:
        a, n = 4.0, 20000
        s = star_state(left, right)
        total = [0.0, 0.0, 0.0]
        dx = 2 * a / n
        for i in range(n):
            q = conserved(sample(-a + (i + 0.5) * dx, left, right, star=s))
            for k in range(3):
                total[k] += q[k] * dx
        ul, ur = conserved(left), conserved(right)
        fl, fr = euler_flux(left), euler_flux(right)
        for k in range(3):
            assert abs(total[k] - (a * (ul[k] + ur[k]) - (fr[k] - fl[k]))) < 2e-3


def test_mirror_symmetry() -> None:
    left, right = (1.0, 0.3, 2.0), (0.5, -0.2, 0.4)
    s = star_state(left, right)
    m = star_state((right[0], -right[1], right[2]), (left[0], -left[1], left[2]))
    assert abs(s["p"] - m["p"]) < 1e-12
    assert abs(s["u"] + m["u"]) < 1e-12
    for xi in (-2.0, -0.7, 0.1, 0.9, 2.5):
        a = sample(xi, left, right)
        b = sample(-xi, (right[0], -right[1], right[2]), (left[0], -left[1], left[2]))
        assert abs(a[0] - b[0]) < 1e-12 and abs(a[1] + b[1]) < 1e-12 and abs(a[2] - b[2]) < 1e-12


def test_vacuum_is_detected() -> None:
    with pytest.raises(VacuumError):
        star_state((1.0, -5.0, 0.4), (1.0, 5.0, 0.4))


def test_godunov_flux_of_equal_states() -> None:
    w = (0.7, 0.4, 1.3)
    f = godunov_flux(w, w)
    e = euler_flux(w)
    assert all(abs(x - y) < 1e-12 for x, y in zip(f, e))
