# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-legendre-runge-kutta/. The authors are listed in prov/XS4SMM.jsonl.

import math
import random
from fractions import Fraction as Fr

import pytest

from gauss_legendre_runge_kutta import gauss_legendre_rk, gauss_legendre_tableau


def pade_coeffs(s):
    """Numerator of the (s, s) Pade approximant of exp, as exact fractions."""
    return [Fr(math.factorial(2 * s - k) * math.factorial(s),
               math.factorial(2 * s) * math.factorial(k) * math.factorial(s - k)) for k in range(s + 1)]


def mat_mul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y))) for j in range(len(Y[0]))] for i in range(len(X))]


def mat_poly(coeffs, Z):
    n = len(Z)
    out = [[0.0] * n for _ in range(n)]
    P = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for a in coeffs:
        out = [[out[i][j] + float(a) * P[i][j] for j in range(n)] for i in range(n)]
        P = mat_mul(P, Z)
    return out


def inv2(M):
    (a, b), (c, d) = M
    det = a * d - b * c
    return [[d / det, -b / det], [-c / det, a / det]]


def test_tableaux_closed_forms():
    A, b, c = gauss_legendre_tableau(1)
    assert A == [[0.5]] and b == [1.0] and c == [0.5]
    A, b, c = gauss_legendre_tableau(2)
    r = math.sqrt(3) / 6
    assert c == pytest.approx([0.5 - r, 0.5 + r], abs=1e-15)
    assert b == pytest.approx([0.5, 0.5], abs=1e-15)
    assert A[0] == pytest.approx([0.25, 0.25 - r], abs=1e-15)
    assert A[1] == pytest.approx([0.25 + r, 0.25], abs=1e-15)


@pytest.mark.parametrize("s", [1, 2, 3, 4, 5])
def test_simplifying_assumptions_and_symplecticity(s):
    A, b, c = gauss_legendre_tableau(s)
    for k in range(1, 2 * s + 1):  # B(2s)
        assert sum(b[i] * c[i] ** (k - 1) for i in range(s)) == pytest.approx(1 / k, abs=1e-13)
    for k in range(1, s + 1):  # C(s) and D(s)
        for i in range(s):
            assert sum(A[i][j] * c[j] ** (k - 1) for j in range(s)) == pytest.approx(c[i] ** k / k, abs=1e-13)
        for j in range(s):
            lhs = sum(b[i] * c[i] ** (k - 1) * A[i][j] for i in range(s))
            assert lhs == pytest.approx(b[j] * (1 - c[j] ** k) / k, abs=1e-13)
    for i in range(s):
        for j in range(s):
            assert b[i] * A[i][j] + b[j] * A[j][i] - b[i] * b[j] == pytest.approx(0.0, abs=1e-13)


def test_stability_function_exact_for_implicit_midpoint():
    a, bb = Fr(1, 2), Fr(1)
    for z in (Fr(-1, 2), Fr(3), Fr(-7, 3), Fr(5, 11)):
        R = 1 + z * bb / (1 - z * a)
        P = pade_coeffs(1)
        assert R == sum(P[k] * z ** k for k in range(2)) / sum(P[k] * (-z) ** k for k in range(2))
    P2 = pade_coeffs(2)
    z = Fr(-1, 2)
    assert sum(P2[k] * z ** k for k in range(3)) / sum(P2[k] * (-z) ** k for k in range(3)) == Fr(37, 61)


def test_worked_example():
    r1 = gauss_legendre_rk(lambda t, y: -y, 0.0, 1.0, 0.5, 0.5, s=1, jac=lambda t, y: -1.0)
    r2 = gauss_legendre_rk(lambda t, y: -y, 0.0, 1.0, 0.5, 0.5, s=2, jac=lambda t, y: -1.0)
    assert r1.y == pytest.approx(0.6, abs=1e-14)
    assert r2.y == pytest.approx(37 / 61, abs=1e-14)
    assert abs(r2.y - math.exp(-0.5)) == pytest.approx(2.672e-5, rel=1e-3)


def test_random_linear_systems_match_pade():
    rng = random.Random(21)
    for case in range(500):
        s = rng.randint(1, 3)
        M = [[rng.uniform(-2, 2) for _ in range(2)] for _ in range(2)]
        h = rng.uniform(0.05, 1.0)
        y0 = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        r = gauss_legendre_rk(lambda t, y: [M[0][0] * y[0] + M[0][1] * y[1], M[1][0] * y[0] + M[1][1] * y[1]],
                              0.0, y0, h, h, s=s, jac=lambda t, y: M)
        Z = [[h * M[i][j] for j in range(2)] for i in range(2)]
        P = pade_coeffs(s)
        num = mat_poly(P, Z)
        den = mat_poly([p * (-1) ** k for k, p in enumerate(P)], Z)
        R = mat_mul(inv2(den), num)
        want = [R[0][0] * y0[0] + R[0][1] * y0[1], R[1][0] * y0[0] + R[1][1] * y0[1]]
        assert r.y == pytest.approx(want, rel=1e-11, abs=1e-11)


@pytest.mark.parametrize("s,hs", [(1, (0.2, 0.1, 0.05)), (2, (0.2, 0.1, 0.05)), (3, (0.5, 0.25, 0.125))])
def test_observed_order_2s(s, hs):
    errs = []
    for h in hs:
        r = gauss_legendre_rk(lambda t, y: math.cos(t) * y, 0.0, 1.0, 2.0, h, s=s,
                              jac=lambda t, y: math.cos(t))
        errs.append(abs(r.y - math.exp(math.sin(2.0))))
    for k in range(2):
        p = math.log2(errs[k] / errs[k + 1])
        assert abs(p - 2 * s) < 0.15


def test_quadratic_invariants_preserved():
    r = gauss_legendre_rk(lambda t, y: [y[1], -y[0]], 0.0, [1.0, 0.0], 1000.0, 0.5, s=2,
                          jac=lambda t, y: [[0.0, 1.0], [-1.0, 0.0]])
    assert abs(r.y[0] ** 2 + r.y[1] ** 2 - 1.0) < 1e-12 and r.steps == 2000
    I1, I2, I3 = 2.0, 1.0, 2.0 / 3.0  # free rigid body, |y|^2 is a quadratic invariant

    def rigid(t, y):
        return [(1 / I3 - 1 / I2) * y[1] * y[2], (1 / I1 - 1 / I3) * y[2] * y[0], (1 / I2 - 1 / I1) * y[0] * y[1]]
    y0 = [math.cos(1.1), 0.0, math.sin(1.1)]
    r = gauss_legendre_rk(rigid, 0.0, y0, 20.0, 0.1, s=2)  # finite-difference Jacobian
    assert abs(sum(v * v for v in r.y) - 1.0) < 1e-11


def test_stiff_a_stable_not_l_stable():
    for s in (1, 2, 3):
        r = gauss_legendre_rk(lambda t, y: -1e6 * y, 0.0, 1.0, 1.0, 0.1, s=s, jac=lambda t, y: -1e6)
        assert abs(r.y) <= 1.0 and abs(r.y) > 0.99  # |R(-10^5)| close to |R(-inf)| = 1


def test_edge_cases():
    r = gauss_legendre_rk(lambda t, y: -y, 0.0, 2.0, 0.0, 0.1)
    assert r.y == 2.0 and r.steps == 0 and r.f_evals == 0
    r = gauss_legendre_rk(lambda t, y: -y, 0.0, 1.0, 0.3, 5.0, s=2)  # h larger than the interval
    assert r.steps == 1 and r.t == 0.3
    r = gauss_legendre_rk(lambda t, y: 1.0, 0.0, 0.0, 1.0, 0.3, s=1)  # off-grid end, y = t exactly
    assert r.steps == 4 and r.y == pytest.approx(1.0, abs=1e-14)
    r = gauss_legendre_rk(lambda t, y: (y[0], 2 * y[1]), 0.0, (1.0, 1.0), 0.1, 0.1, s=2)
    assert isinstance(r.y, list) and r.y[1] == pytest.approx((1 + 0.1 + 0.04 / 12) / (1 - 0.1 + 0.04 / 12), rel=1e-12)
    with pytest.raises(ValueError):
        gauss_legendre_tableau(0)
    with pytest.raises(ValueError):
        gauss_legendre_rk(lambda t, y: y, 0.0, 1.0, 1.0, 0.0)
    with pytest.raises(ValueError):
        gauss_legendre_rk(lambda t, y: y, 1.0, 1.0, 0.0, 0.1)
