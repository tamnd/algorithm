# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lattice-boltzmann-method/. The authors are listed in prov/ANY3EP.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from lattice_boltzmann_method import (C, equilibrium, lbm_d1q3_diffusion, lbm_d2q9, moments)


def _rand_init(rng):
    vals = {}

    def init(x, y):
        if (x, y) not in vals:
            vals[(x, y)] = (1 + F(rng.randint(-5, 5), 100), F(rng.randint(-5, 5), 100),
                            F(rng.randint(-5, 5), 100))
        return vals[(x, y)]
    return init


def test_equilibrium_has_the_given_moments_exactly():
    rng = random.Random(7)
    for _ in range(20):
        rho = F(rng.randint(50, 150), 100)
        ux, uy = F(rng.randint(-20, 20), 100), F(rng.randint(-20, 20), 100)
        eq = equilibrium(rho, ux, uy, exact=True)
        assert sum(eq) == rho
        assert sum(C[i][0] * eq[i] for i in range(9)) == rho * ux
        assert sum(C[i][1] * eq[i] for i in range(9)) == rho * uy


def test_mass_and_momentum_are_conserved_exactly():
    init = _rand_init(random.Random(11))
    r0 = lbm_d2q9(3, 3, F(4, 5), 0, init=init)
    r = lbm_d2q9(3, 3, F(4, 5), 3, init=init)
    for a, b in ((r0, r),):
        assert sum(map(sum, a.f)) == sum(map(sum, b.f))
        for d in (0, 1):
            ja = sum(C[i][d] * sum(a.f[i]) for i in range(9))
            jb = sum(C[i][d] * sum(b.f[i]) for i in range(9))
            assert ja == jb


def test_force_adds_exactly_g_per_node_and_step():
    g = (F(1, 1000), F(-1, 2000))
    init = _rand_init(random.Random(3))
    r0 = lbm_d2q9(2, 3, F(3, 4), 0, init=init, force=g)
    r = lbm_d2q9(2, 3, F(3, 4), 4, init=init, force=g)
    for d in (0, 1):
        ja = sum(C[i][d] * sum(r0.f[i]) for i in range(9))
        jb = sum(C[i][d] * sum(r.f[i]) for i in range(9))
        assert jb - ja == 4 * 6 * g[d]


def test_bounce_back_conserves_mass_exactly():
    init = _rand_init(random.Random(5))
    r0 = lbm_d2q9(2, 3, F(9, 10), 0, init=init, walls=True)
    r = lbm_d2q9(2, 3, F(9, 10), 3, init=init, force=(F(1, 100), 0), walls=True)
    assert sum(map(sum, r0.f)) == sum(map(sum, r.f))


def _poiseuille(tau, ny=8, g=1e-6):
    nu = (tau - 0.5) / 3
    r = lbm_d2q9(1, ny, tau, int(6 * ny * ny / nu), force=(g, 0), walls=True)
    ex = [g / (2 * nu) * (y + 0.5) * (ny - 0.5 - y) for y in range(ny)]
    return [(r.ux[y][0] - ex[y]) / g for y in range(ny)], max(ex) / g


def test_poiseuille_profile_and_wall_slip():
    dev, peak = _poiseuille(0.5 + math.sqrt(3) / 4)
    assert max(abs(d) for d in dev) < 1e-6 * peak
    dev, _ = _poiseuille(1.0)
    assert all(abs(d - 0.25) < 1e-3 for d in dev)          # constant slip g/4


def _taylor_green(n, tau=0.8):
    k = 2 * math.pi / n
    u0 = 0.16 / n
    init = lambda x, y: (1.0, -u0 * math.cos(k * x) * math.sin(k * y), u0 * math.sin(k * x) * math.cos(k * y))
    steps = n * n // 8
    r = lbm_d2q9(n, n, tau, steps, init=init)
    dec = math.exp(-2 * (tau - 0.5) / 3 * k * k * steps)
    return max(abs(r.ux[y][x] + u0 * dec * math.cos(k * x) * math.sin(k * y))
               for y in range(n) for x in range(n)) / (u0 * dec)


def test_taylor_green_second_order_in_diffusive_scaling():
    e8, e16 = _taylor_green(8), _taylor_green(16)
    assert abs(e8 - 0.0865) < 1e-3
    assert 3.6 < e8 / e16 < 4.4


def test_d1q3_with_tau_one_is_ftcs_with_mu_one_sixth():
    rng = random.Random(1)
    rho = [F(rng.randint(0, 9)) for _ in range(7)]
    r = lbm_d1q3_diffusion(rho, F(1), 3)
    u = list(rho)
    for _ in range(3):
        u = [u[j] + F(1, 6) * (u[j - 1] - 2 * u[j] + u[(j + 1) % 7]) for j in range(7)]
    assert r == u
    assert lbm_d1q3_diffusion([F(0), F(0), F(1), F(0), F(0)], F(1), 2) == \
        [F(1, 36), F(2, 9), F(1, 2), F(2, 9), F(1, 36)]


def test_d1q3_orders():
    def err(tau, n):
        D = (tau - 0.5) / 3
        k = 2 * math.pi / n
        s = n * n // 16
        r = lbm_d1q3_diffusion([1 + 0.5 * math.sin(k * j) for j in range(n)], tau, s)
        return max(abs(r[j] - 1 - 0.5 * math.exp(-D * k * k * s) * math.sin(k * j)) for j in range(n))
    assert abs(math.log2(err(0.8, 16) / err(0.8, 32)) - 2) < 0.05
    assert abs(math.log2(err(1.0, 16) / err(1.0, 32)) - 4) < 0.1


def _shear(tau, u0, n=16, steps=300):
    k = 2 * math.pi / n

    def init(x, y):
        s = math.tanh(30 * (y / n - 0.25)) if y < n / 2 else math.tanh(30 * (0.75 - y / n))
        return (1.0, u0 * s, 0.05 * u0 * math.sin(k * x))
    try:
        r = lbm_d2q9(n, n, tau, steps, init=init)
    except (OverflowError, ZeroDivisionError):
        return math.inf
    return max(abs(r.ux[y][x]) for y in range(n) for x in range(n))


def test_low_viscosity_and_high_speed_go_unstable():
    assert _shear(0.6, 0.2) < 0.2
    assert _shear(0.501, 0.2) > 1


def test_edge_cases():
    r = lbm_d2q9(2, 2, 0.7, 0, init=lambda x, y: (1.0, 0.1, 0.0))
    assert r.steps == 0 and abs(r.ux[1][1] - 0.1) < 1e-15 and abs(r.rho[0][0] - 1) < 1e-15
    r = lbm_d2q9(1, 1, F(2, 3), 2)
    assert r.rho == [[1]] and r.ux == [[0]]
    with pytest.raises(ValueError):
        lbm_d2q9(2, 2, 0.5, 1)
    with pytest.raises(ValueError):
        lbm_d2q9(0, 2, 0.7, 1)
    with pytest.raises(ValueError):
        lbm_d2q9(2, 1, 0.7, 1, walls=True)
    with pytest.raises(ValueError):
        lbm_d2q9(2, 2, 0.7, -1)
    assert lbm_d1q3_diffusion([], 0.8, 5) == []
    with pytest.raises(ValueError):
        lbm_d1q3_diffusion([1.0], 0.5, 1)
    assert moments(equilibrium(1.0, 0.0, 0.0)) == (1.0, 0.0, 0.0)
