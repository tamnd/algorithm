# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-integrators/. The authors are listed in prov/4R98K0.jsonl.

import cmath
import math
import random
from fractions import Fraction

import pytest

from exponential_integrators import (exponential_rk, expm, mat_mul, mat_vec,
                                     phi, phi_blocks)


def phi_series(kidx, z, terms=60):
    """phi_k(z) by an exact rational Taylor sum, for |z| <= 1."""
    zf = Fraction(z)
    total, term = Fraction(0), Fraction(1, math.factorial(kidx))
    for j in range(terms):
        total += term
        term = term * zf / (j + 1 + kidx)
    return float(total)


def putzer(M):
    """e^M, phi_1(M), phi_2(M) for an invertible 2 x 2 matrix, by Putzer's formula."""
    s = (M[0][0] + M[1][1]) / 2
    det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    q = cmath.sqrt(s * s - det)
    c = cmath.cosh(q)
    sq = cmath.sinh(q) / q if abs(q) > 1e-12 else 1
    es = cmath.exp(s)
    E = [[(es * (c * (i == j) + sq * (M[i][j] - s * (i == j)))).real for j in range(2)]
         for i in range(2)]
    inv = [[M[1][1] / det, -M[0][1] / det], [-M[1][0] / det, M[0][0] / det]]
    EmI = [[E[i][j] - (i == j) for j in range(2)] for i in range(2)]
    P1 = mat_mul(inv, EmI)
    P2 = mat_mul(inv, [[P1[i][j] - (i == j) for j in range(2)] for i in range(2)])
    return E, P1, P2


def test_worked_example():
    # y' = -4 y + t, y(0) = 1, one step h = 1/2: ETD2RK is exact for g affine in t.
    r = exponential_rk(-4.0, lambda t, y: t, 0.0, 1.0, 0.5, 0.5)
    exact = 17 / 16 * math.exp(-2) + 0.5 / 4 - 1 / 16
    assert r.y == pytest.approx(exact, abs=1e-15)
    assert r.y == pytest.approx(0.2062938, abs=1e-7)
    assert phi(1, -2.0) == pytest.approx(0.4323324, abs=1e-7)
    assert phi(2, -2.0) == pytest.approx(0.2838338, abs=1e-7)
    assert r.steps == 1 and r.g_evals == 2


def test_scalar_phi_functions():
    for z in (-0.999, -0.5, -1e-6, -1e-12, 0.0, 1e-9, 0.3, 0.999):
        for k in (0, 1, 2, 3):
            assert phi(k, z) == pytest.approx(phi_series(k, z), rel=1e-14)
    for z in (-1e6, -40.0, -3.0, -1.0, 1.0, 5.0):
        assert phi(1, z) == pytest.approx(math.expm1(z) / z, rel=1e-13)
        assert phi(2, z) == pytest.approx((math.expm1(z) - z) / (z * z), rel=1e-12)


def test_block_exponential_matches_scalar_phi():
    for z in (-1e6, -50.0, -2.0, -1e-8, 0.0, 0.5, 3.0):
        E, P1, P2, _ = phi_blocks([[z]], 1.0)
        assert E[0][0] == pytest.approx(math.exp(z), rel=1e-13, abs=1e-300)
        assert P1[0][0] == pytest.approx(phi(1, z), rel=1e-12)
        assert P2[0][0] == pytest.approx(phi(2, z), rel=1e-12)


def test_random_matrices_against_putzer():
    rng = random.Random(77)
    count = 0
    while count < 500:
        M = [[rng.uniform(-3, 3) for _ in range(2)] for _ in range(2)]
        if abs(M[0][0] * M[1][1] - M[0][1] * M[1][0]) < 0.2:
            continue
        count += 1
        E, P1, P2, _ = phi_blocks(M, 1.0)
        Eo, P1o, P2o = putzer(M)
        for X, Y in ((E, Eo), (P1, P1o), (P2, P2o)):
            for i in range(2):
                for j in range(2):
                    assert X[i][j] == pytest.approx(Y[i][j], rel=1e-9, abs=1e-9)
        # one ETD2RK step with g(t, y) = c + t d (affine): compare the formula
        c = [rng.uniform(-1, 1) for _ in range(2)]
        d = [rng.uniform(-1, 1) for _ in range(2)]
        y0 = [rng.uniform(-1, 1) for _ in range(2)]
        r = exponential_rk(M, lambda t, y: [ci + t * di for ci, di in zip(c, d)],
                           0.0, y0, 1.0, 1.0)
        want = [a + b + e for a, b, e in zip(mat_vec(Eo, y0), mat_vec(P1o, c), mat_vec(P2o, d))]
        assert r.y == pytest.approx(want, rel=1e-8, abs=1e-8)


def test_exact_fractions_nilpotent_and_heun():
    # y1' = y2, y2' = t: A nilpotent, g affine, so ETD2RK is exact: y(1) = (7/6, 1/2).
    A = [[Fraction(0), Fraction(1)], [Fraction(0), Fraction(0)]]
    E, P1, P2, _ = phi_blocks(A, Fraction(1, 2))
    assert E == [[1, Fraction(1, 2)], [0, 1]]
    assert P1 == [[1, Fraction(1, 4)], [0, 1]]
    assert P2 == [[Fraction(1, 2), Fraction(1, 12)], [0, Fraction(1, 2)]]
    r = exponential_rk(A, lambda t, y: [0, t], Fraction(0), [Fraction(1), Fraction(0)],
                       Fraction(1), Fraction(1, 2))
    assert r.y == [Fraction(7, 6), Fraction(1, 2)]
    # A = 0: ETD2RK is Heun's method and exponential Euler is Euler's method.
    r = exponential_rk(Fraction(0), lambda t, y: y * y, Fraction(0), Fraction(1),
                       Fraction(1, 4), Fraction(1, 4))
    assert r.y == Fraction(169, 128)
    r = exponential_rk(Fraction(0), lambda t, y: y * y, Fraction(0), Fraction(1),
                       Fraction(1, 4), Fraction(1, 4), method="euler")
    assert r.y == Fraction(5, 4)


def riccati(t):
    return 1 / (1 + math.exp(t))      # y' = -y + y^2, y(0) = 1/2


def test_observed_orders():
    for method, p in (("etd2rk", 2), ("euler", 1)):
        errs = []
        for j in range(3, 9):
            r = exponential_rk(-1.0, lambda t, y: y * y, 0.0, 0.5, 2.0, 2.0 ** -j, method)
            errs.append(abs(r.y - riccati(2.0)))
        orders = [math.log2(errs[i] / errs[i + 1]) for i in range(len(errs) - 1)]
        assert all(abs(q - p) < 0.15 for q in orders[2:]), (method, orders)


def test_stiff_uniform_error_constant():
    # y' = lam (y - sin t) + cos t; the error constant does not grow with |lam|.
    for lam in (-1e2, -1e4, -1e6):
        for j in range(3, 9):
            h = 2.0 ** -j
            r = exponential_rk(lam, lambda t, y: -lam * math.sin(t) + math.cos(t),
                               0.0, 1.0, 2.0, h)
            exact = math.sin(2.0) + math.exp(lam * 2.0)
            assert abs(r.y - exact) <= 0.1 * h * h


def test_chafee_infante_stiff_system():
    m, dx, mu = 15, 1 / 16, 20.0
    A = [[(-2 if i == j else (1 if abs(i - j) == 1 else 0)) / dx ** 2 for j in range(m)]
         for i in range(m)]
    g = lambda t, u: [mu * (x - x ** 3) for x in u]
    u0 = [0.1 * math.sin(math.pi * (i + 1) * dx) for i in range(m)]

    def rk4(T, h):
        u = u0[:]
        F = lambda v: [a + b for a, b in zip(mat_vec(A, v), g(0, v))]
        for _ in range(round(T / h)):
            k1 = F(u)
            k2 = F([x + h / 2 * k for x, k in zip(u, k1)])
            k3 = F([x + h / 2 * k for x, k in zip(u, k2)])
            k4 = F([x + h * k for x, k in zip(u, k3)])
            u = [x + h / 6 * (a + 2 * b + 2 * c + d) for x, a, b, c, d in zip(u, k1, k2, k3, k4)]
        return u

    ref = rk4(0.25, 1 / 2000)
    errs = []
    for h in (0.0125, 0.00625, 0.003125):
        r = exponential_rk(A, g, 0.0, u0, 0.25, h)
        errs.append(max(abs(a - b) for a, b in zip(r.y, ref)))
    assert errs[0] == pytest.approx(3.607e-3, rel=1e-3)
    assert all(1.8 < math.log2(errs[i] / errs[i + 1]) < 2.1 for i in range(2))


def test_equilibrium_preserved_exactly():
    # y' = -3 y + y^3 + 1 has an equilibrium y*; both methods keep it to rounding.
    y = 0.3
    for _ in range(50):
        y -= (-3 * y + y ** 3 + 1) / (-3 + 3 * y * y)
    for method in ("etd2rk", "euler"):
        r = exponential_rk(-3.0, lambda t, v: v ** 3 + 1, 0.0, y, 10.0, 0.7, method)
        assert abs(r.y - y) < 1e-14


def test_rotation_norm_conserved():
    r = exponential_rk([[0.0, 1.0], [-1.0, 0.0]], lambda t, y: [0.0, 0.0], 0.0, [1.0, 0.0],
                       100.0, 0.1)
    assert math.hypot(*r.y) == pytest.approx(1.0, abs=1e-12)
    assert r.y == pytest.approx([math.cos(100.0), -math.sin(100.0)], abs=1e-11)


def test_edge_cases():
    r = exponential_rk(-1.0, lambda t, y: 0.0, 1.0, 2.0, 1.0, 0.1)
    assert r.y == 2.0 and r.steps == 0 and r.g_evals == 0
    r = exponential_rk(-1.0, lambda t, y: 0.0, 0.0, 2.0, 1.0, 5.0)      # h > interval
    assert r.steps == 1 and r.y == pytest.approx(2 * math.exp(-1), rel=1e-14)
    r = exponential_rk(-1.0, lambda t, y: 1.0, 0.0, 0.0, 0.95, 0.3)      # off-grid T
    assert r.t == 0.95 and r.steps == 4
    assert r.y == pytest.approx(1 - math.exp(-0.95), rel=1e-13)
    with pytest.raises(ValueError):
        exponential_rk(-1.0, lambda t, y: 0.0, 0.0, 1.0, 1.0, 0.0)
    with pytest.raises(ValueError):
        exponential_rk(-1.0, lambda t, y: 0.0, 1.0, 1.0, 0.0, 0.1)
    with pytest.raises(ValueError):
        exponential_rk(-1.0, lambda t, y: 0.0, 0.0, 1.0, 1.0, 0.1, method="rk4")


def test_expm_identity_and_squarings():
    X, s = expm([[0.0, 0.0], [0.0, 0.0]])
    assert X == [[1.0, 0.0], [0.0, 1.0]] and s == 0
    X, s = expm([[-1e6]])
    assert X[0][0] == 0.0 and s == 21
