# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-relaxation-time-lattice-boltzmann/. The authors are listed in prov/JZ1BG8.jsonl.

import math
import random
from fractions import Fraction as Fr

from multiple_relaxation_time_lattice_boltzmann import (
    C, M, NORM2, W_EXACT, collide, equilibrium, equilibrium_moments, from_moments,
    guo_force, magic_q_rate, mrt_d2q9, nu_of_rate, rates, to_moments)


def rand_fr(rng, lo=-50, hi=50, den=100):
    return Fr(rng.randint(lo, hi), den)


def rand_pops(rng):
    return [w * (1 + rand_fr(rng, -20, 20)) for w in W_EXACT]


# ---------------------------------------------------------------- the moment basis


def test_rows_of_m_are_orthogonal():
    for a in range(9):
        for b in range(9):
            d = sum(M[a][i] * M[b][i] for i in range(9))
            assert d == (NORM2[a] if a == b else 0)


def test_transform_matches_matrix_and_inverts_exactly():
    rng = random.Random(1)
    for _ in range(500):
        f = [rand_fr(rng) for _ in range(9)]
        m = to_moments(f)
        assert m == [sum(M[k][i] * f[i] for i in range(9)) for k in range(9)]
        assert from_moments(m) == f


def test_equilibrium_moments_closed_form():
    rng = random.Random(2)
    for _ in range(500):
        rho = 1 + rand_fr(rng, -30, 30)
        ux, uy = rand_fr(rng, -20, 20), rand_fr(rng, -20, 20)
        assert to_moments(equilibrium(rho, ux, uy, True)) == equilibrium_moments(rho, ux, uy)


def test_hand_example_equilibrium_moments():
    # rho = 1, u = (1/10, 0): e = -2 + 3/100, epsilon = 1 - 3/100, p_xx = 1/100
    m = equilibrium_moments(Fr(1), Fr(1, 10), Fr(0))
    assert m == [1, Fr(-197, 100), Fr(97, 100), Fr(1, 10), Fr(-1, 10), 0, 0, Fr(1, 100), 0]


# ---------------------------------------------------------------- collision


def bgk_collide(f, tau, gx, gy):
    """Independent oracle: BGK with Guo forcing in population space."""
    rho = sum(f)
    ux = (sum(C[i][0] * f[i] for i in range(9)) + gx / 2) / rho
    uy = (sum(C[i][1] * f[i] for i in range(9)) + gy / 2) / rho
    feq = equilibrium(rho, ux, uy, True)
    out = []
    for i in range(9):
        cx, cy = C[i]
        cu = cx * ux + cy * uy
        force = W_EXACT[i] * ((3 * (cx - ux) + 9 * cu * cx) * gx + (3 * (cy - uy) + 9 * cu * cy) * gy)
        out.append(f[i] - (f[i] - feq[i]) / tau + (1 - 1 / (2 * tau)) * force)
    return out


def test_equal_rates_give_bgk_exactly():
    rng = random.Random(3)
    for _ in range(500):
        f = rand_pops(rng)
        tau = Fr(rng.randint(51, 300), 100)
        gx, gy = rand_fr(rng, -10, 10, 1000), rand_fr(rng, -10, 10, 1000)
        s = [1 / tau] * 9
        assert collide(f, s, gx, gy, exact=True) == bgk_collide(f, tau, gx, gy)


def test_conserved_rates_do_not_matter():
    rng = random.Random(4)
    for _ in range(200):
        f = rand_pops(rng)
        gx, gy = rand_fr(rng, -10, 10, 1000), rand_fr(rng, -10, 10, 1000)
        s = rates(Fr(rng.randint(10, 190), 100), Fr(rng.randint(10, 190), 100),
                  Fr(rng.randint(10, 190), 100), Fr(rng.randint(10, 190), 100))
        s2 = list(s)
        for k in (0, 3, 5):
            s2[k] = Fr(rng.randint(10, 190), 100)
        assert collide(f, s, gx, gy, True) == collide(f, s2, gx, gy, True)


def test_collision_moments():
    # density kept, momentum gains exactly g
    rng = random.Random(5)
    for _ in range(200):
        f = rand_pops(rng)
        gx, gy = rand_fr(rng, -10, 10, 1000), rand_fr(rng, -10, 10, 1000)
        s = rates(Fr(rng.randint(10, 190), 100), Fr(rng.randint(10, 190), 100))
        a, b = to_moments(f), to_moments(collide(f, s, gx, gy, True))
        assert b[0] == a[0] and b[3] == a[3] + gx and b[5] == a[5] + gy


def test_hand_example_collision():
    f = list(W_EXACT)
    f[1] += Fr(1, 100)
    f[3] += Fr(1, 100)
    s = rates(Fr(5, 4), Fr(8, 9), Fr(1), Fr(1))
    out = collide(f, s, exact=True)
    assert out == [Fr(34, 75), Fr(269, 2400), Fr(11, 96), Fr(269, 2400), Fr(11, 96)] + [Fr(17, 600)] * 4
    assert to_moments(out) == [Fr(51, 50), Fr(-51, 25), Fr(51, 50), 0, 0, 0, 0, Fr(-1, 200), 0]
    bgk = collide(f, [Fr(5, 4)] * 9, exact=True)
    assert bgk == [Fr(41, 90), Fr(401, 3600), Fr(41, 360), Fr(401, 3600), Fr(41, 360)] + [Fr(41, 1440)] * 4


def test_guo_force_moments():
    u, v, gx, gy = Fr(1, 10), Fr(1, 20), Fr(1, 1000), Fr(0)
    mf = to_moments(guo_force(u, v, gx, gy, True))
    assert mf == [0, Fr(3, 5000), Fr(-3, 5000), Fr(1, 1000), Fr(-1, 1000), 0, 0, Fr(1, 5000), Fr(1, 20000)]


# ---------------------------------------------------------------- whole runs


def test_exact_conservation_on_a_small_lattice():
    rng = random.Random(6)
    nx, ny = 3, 4
    f0 = [rand_pops(rng) for _ in range(nx * ny)]
    s = rates(Fr(6, 5), Fr(11, 10), Fr(13, 10), Fr(7, 5))
    gx, gy = Fr(1, 500), Fr(-1, 700)
    mass0 = sum(sum(p) for p in f0)
    jx0 = sum(sum(C[i][0] * p[i] for i in range(9)) for p in f0)
    jy0 = sum(sum(C[i][1] * p[i] for i in range(9)) for p in f0)
    for steps in (1, 2, 3):
        res = mrt_d2q9(nx, ny, s, steps, None, gx, gy, walls=False, exact=True, f0=f0)
        assert sum(sum(p) for p in res.f) == mass0
        assert sum(sum(C[i][0] * p[i] for i in range(9)) for p in res.f) == jx0 + steps * nx * ny * gx
        assert sum(sum(C[i][1] * p[i] for i in range(9)) for p in res.f) == jy0 + steps * nx * ny * gy
        walled = mrt_d2q9(nx, ny, s, steps, None, gx, 0, walls=True, exact=True, f0=f0)
        assert sum(sum(p) for p in walled.f) == mass0


def poiseuille(s_nu, s_q, ny, g=1e-6):
    nu = nu_of_rate(s_nu)
    steps = int(30 * ny * ny / (math.pi ** 2 * nu)) + 100
    res = mrt_d2q9(1, ny, rates(s_nu, s_q), steps, lambda x, y: (1.0, 0.0, 0.0), gx=g, walls=True)
    return [(res.ux[y][0] - g / (2 * nu) * (y + 0.5) * (ny - 0.5 - y)) / g for y in range(ny)]


def test_poiseuille_magic_rate_is_exact():
    for s_nu in (1.0, 1 / 0.8):
        err = poiseuille(s_nu, magic_q_rate(s_nu), 6)
        assert max(abs(e) for e in err) < 1e-7


def test_poiseuille_bgk_rates_slip():
    for tau in (1.0, 0.8):
        lam = tau - 0.5
        slip = 2 * lam - 3 / (8 * lam)
        err = poiseuille(1 / tau, 1 / tau, 6)
        assert max(abs(e - slip) for e in err) < 1e-6


def test_magic_rate_value():
    assert magic_q_rate(Fr(1)) == Fr(8, 7)
    assert (1 / Fr(5, 4) - Fr(1, 2)) * (1 / magic_q_rate(Fr(5, 4)) - Fr(1, 2)) == Fr(3, 16)


def taylor_green_error(n, s_nu, s_q):
    nu = nu_of_rate(s_nu)
    k = 2 * math.pi / n
    u0 = 0.16 / n
    steps = n * n // 8

    def init(x, y):
        rho = 1.0 - 0.75 * u0 * u0 * (math.cos(2 * k * x) + math.cos(2 * k * y))
        return rho, -u0 * math.cos(k * x) * math.sin(k * y), u0 * math.sin(k * x) * math.cos(k * y)

    res = mrt_d2q9(n, n, rates(s_nu, s_q), steps, init)
    dec = math.exp(-2 * nu * k * k * steps)
    err = max(abs(res.ux[y][x] + u0 * math.cos(k * x) * math.sin(k * y) * dec)
              for y in range(n) for x in range(n))
    return err / (u0 * dec)


def test_taylor_green_second_order():
    e8 = taylor_green_error(8, 1.25, 1.1)
    e16 = taylor_green_error(16, 1.25, 1.1)
    assert abs(e8 - 0.0796) < 5e-4
    assert abs(math.log2(e8 / e16) - 2) < 0.2
