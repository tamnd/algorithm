# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maccormack-method/. The authors are listed in prov/6EZVM9.jsonl.

import cmath
import math
import random
from fractions import Fraction as Fr

from maccormack_method import maccormack, maccormack_step, numerical_flux

G = 1.4


def lax_wendroff_advection(u, nu):
    """Independent oracle: the Lax-Wendroff scheme for u_t + a u_x = 0 with nu = a dt / dx, periodic."""
    m = len(u)
    return [
        u[j] - nu / 2 * (u[(j + 1) % m] - u[j - 1]) + nu * nu / 2 * (u[(j + 1) % m] - 2 * u[j] + u[j - 1])
        for j in range(m)
    ]


def total_variation(u):
    return sum(abs(u[j] - u[j - 1]) for j in range(len(u)))


def euler_flux(w):
    rho, mom, e = w
    u = mom / rho
    p = (G - 1) * (e - mom * u / 2)
    return (mom, mom * u + p, u * (e + p))


def test_equals_lax_wendroff_on_linear_advection() -> None:
    rng = random.Random(3)
    for a, lam in ((Fr(1), Fr(1, 2)), (Fr(-1, 2), Fr(3, 4)), (Fr(2), Fr(2, 5))):
        u = [Fr(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(11)]
        v = list(u)
        for _ in range(5):
            v = lax_wendroff_advection(v, a * lam)
        assert maccormack(u, lambda x: a * x, Fr(1), lam, 5) == v


def test_hand_example_overshoots() -> None:
    u = [Fr(1)] * 3 + [Fr(0)] * 3
    v = maccormack(u, lambda x: x, Fr(1), Fr(1, 2), 1)
    assert v == [Fr(5, 8), Fr(1), Fr(9, 8), Fr(3, 8), Fr(0), Fr(-1, 8)]
    assert total_variation(u) == 2 and total_variation(v) == Fr(5, 2)


def test_courant_number_one_is_an_exact_shift() -> None:
    u = [Fr(k * k % 7) for k in range(9)]
    assert maccormack(u, lambda x: x, Fr(1), Fr(1), 1) == [u[j - 1] for j in range(9)]


def test_amplification_factor() -> None:
    m, k = 16, 3
    theta = 2 * math.pi * k / m
    for nu in (0.3, 0.8, 1.0, 1.1):
        u = [cmath.exp(1j * j * theta) for j in range(m)]
        v = maccormack(u, lambda x: nu * x, 1.0, 1.0, 1)
        g = 1 - 1j * nu * math.sin(theta) - nu * nu * (1 - math.cos(theta))
        assert all(abs(v[j] - g * u[j]) < 1e-12 for j in range(m))
        assert (abs(g) <= 1 + 1e-12) == (nu <= 1)


def test_conservation_form_is_exact() -> None:
    rng = random.Random(5)
    lam = Fr(1, 3)
    for bc in ("periodic", "transmissive"):
        u = [(Fr(rng.randint(-6, 6), 4),) for _ in range(9)]
        flux = lambda v: (v[0] * v[0] / 2,)
        new = maccormack_step(u, flux, lam, bc)
        h = numerical_flux(u, flux, lam, bc)
        assert all(new[j][0] == u[j][0] - lam * (h[j + 1][0] - h[j][0]) for j in range(9))
        if bc == "periodic":
            assert sum(v[0] for v in new) == sum(v[0] for v in u)


def burgers_exact(x, t):
    u0 = lambda y: 0.5 + 0.25 * math.sin(2 * math.pi * y)
    du0 = lambda y: 0.5 * math.pi * math.cos(2 * math.pi * y)
    u = u0(x)
    for _ in range(30):
        u -= (u - u0(x - u * t)) / (1 + du0(x - u * t) * t)
    return u


def test_second_order_on_smooth_burgers() -> None:
    t, errs = 0.3, []
    for m in (40, 80, 160):
        dx = 1 / m
        n = round(t / (0.4 * dx))
        u = maccormack([0.5 + 0.25 * math.sin(2 * math.pi * j * dx) for j in range(m)], lambda v: v * v / 2, dx, t / n, n)
        errs.append(dx * sum(abs(u[j] - burgers_exact(j * dx, t)) for j in range(m)))
    assert errs[0] / errs[1] > 3.7 and errs[1] / errs[2] > 3.8


def test_second_order_on_an_euler_density_wave() -> None:
    t, errs = 0.25, []
    for m in (40, 80, 160):
        dx = 1 / m
        n = round(t / (0.4 * dx / 2.2))
        w = []
        for j in range(m):
            rho = 1 + 0.2 * math.sin(2 * math.pi * j * dx)
            w.append((rho, rho, 1 / (G - 1) + rho / 2))
        w = maccormack(w, euler_flux, dx, t / n, n)
        errs.append(dx * sum(abs(w[j][0] - 1 - 0.2 * math.sin(2 * math.pi * (j * dx - t))) for j in range(m)))
    assert errs[0] / errs[1] > 3.8 and errs[1] / errs[2] > 3.9


def sod(m):
    w = []
    for j in range(m):
        rho, p = (1.0, 1.0) if (j + 0.5) / m < 0.5 else (0.125, 0.1)
        w.append((rho, 0.0, p / (G - 1)))
    return w


def pressures(w):
    return [(G - 1) * (e - mom * mom / (2 * rho)) for rho, mom, e in w]


def test_sod_without_viscosity_loses_positivity() -> None:
    m = 100
    w = sod(m)
    for _ in range(10):
        w = maccormack(w, euler_flux, 1 / m, 0.2 / m, 1, bc="transmissive")
    assert min(pressures(w)) < 0


def test_sod_with_viscosity_puts_the_shock_in_the_right_place() -> None:
    m, lam, t = 100, 0.4, 0.2
    n = round(t / (lam / m))
    w = maccormack(sod(m), euler_flux, 1 / m, t / n, n, bc="transmissive", visc=0.05)
    assert min(pressures(w)) > 0
    # The exact shock is at 0.5 + 1.75216 t, between rho = 0.26557 and rho = 0.125.
    mid = (0.26557 + 0.125) / 2
    cross = next((j + 0.5) / m for j in range(m - 1, 0, -1) if w[j][0] > mid)
    assert abs(cross - (0.5 + 1.75216 * t)) < 3 / m
