# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ackermann-formula/. The authors are listed in prov/DZTY4S.jsonl.

import random
from fractions import Fraction

import pytest

import ctlmat as cm
from ackermann_formula import (
    ackermann,
    ackermann_poles,
    controllability_matrix,
    poly_from_roots,
    poly_of_matrix,
)


def closed_loop(A, b, K):
    return [[A[i][j] - b[i] * K[j] for j in range(len(A))] for i in range(len(A))]


def rand_pair(rng, n, lo=-3, hi=3):
    while True:
        A = [[rng.randint(lo, hi) for _ in range(n)] for _ in range(n)]
        b = [rng.randint(lo, hi) for _ in range(n)]
        if cm.det(controllability_matrix(A, b)) != 0:
            return A, b


def brute_force_gain(A, b, p):
    """Solve the affine map from K to the closed-loop coefficients directly.

    The coefficients of charpoly(A - b K) are affine in K, because
    A - b K is a rank-one change of A. Evaluate the map at K = 0 and at the
    n unit vectors, then solve the n by n linear system.
    """
    n = len(A)
    c0 = cm.charpoly(A)[1:]
    cols = []
    for j in range(n):
        e = [0] * n
        e[j] = 1
        cj = cm.charpoly(closed_loop(A, b, e))[1:]
        cols.append([x - y for x, y in zip(cj, c0)])
    M = cm.transpose(cols)
    rhs = [Fraction(x) - y for x, y in zip(p[1:], c0)]
    return cm.solve(M, rhs)


def test_double_integrator():
    A = [[0, 1], [0, 0]]
    b = [0, 1]
    K = ackermann(A, b, [1, 2, 2])
    assert K == [2, 2]
    assert cm.charpoly(closed_loop(A, b, K)) == [1, 2, 2]


def test_companion_example():
    A = [[0, 1], [-2, -3]]
    b = [0, 1]
    K = ackermann_poles(A, b, [-4, -5])
    assert K == [18, 6]


def test_zoh_double_integrator_deadbeat():
    for h in (Fraction(1, 10), Fraction(1, 2), Fraction(3)):
        A = [[1, h], [0, 1]]
        b = [h * h / 2, h]
        K = ackermann(A, b, [1, 0, 0])
        assert K == [1 / h ** 2, Fraction(3, 2) / h]
        Acl = closed_loop(A, b, K)
        assert cm.mat_power(Acl, 2) == cm.zeros(2)


def test_random_exact():
    rng = random.Random(1)
    for n in range(1, 7):
        for _ in range(6):
            A, b = rand_pair(rng, n)
            p = [1] + [Fraction(rng.randint(-20, 20), rng.randint(1, 4)) for _ in range(n)]
            K = ackermann(A, b, p)
            assert cm.charpoly(closed_loop(A, b, K)) == p
            assert K == brute_force_gain(A, b, p)


def test_poly_of_matrix_matches_powers():
    rng = random.Random(2)
    A = [[rng.randint(-4, 4) for _ in range(4)] for _ in range(4)]
    p = [1, 3, -2, 5, 7]
    want = cm.zeros(4)
    for i, c in enumerate(p):
        want = cm.add(want, cm.scale(c, cm.mat_power(A, len(p) - 1 - i)))
    assert poly_of_matrix(p, A) == want


def test_matches_textbook_form():
    # K = e_n^T W^(-1) p(A), with the inverse and p(A) formed explicitly.
    rng = random.Random(4)
    for n in range(1, 6):
        A, b = rand_pair(rng, n)
        p = [1] + [rng.randint(-9, 9) for _ in range(n)]
        Winv = cm.inv(controllability_matrix(A, b))
        want = cm.mul([Winv[-1]], poly_of_matrix(p, A))[0]
        assert ackermann(A, b, p) == want


def test_cayley_hamilton_gives_zero_gain():
    rng = random.Random(3)
    A, b = rand_pair(rng, 4)
    assert ackermann(A, b, cm.charpoly(A)) == [0, 0, 0, 0]


def test_complex_poles_float():
    A = [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, -2.0, 0.5]]
    b = [0.0, 0.0, 1.0]
    poles = [-2.0, complex(-1.0, 2.0), complex(-1.0, -2.0)]
    K = ackermann_poles(A, b, poles)
    assert all(isinstance(k, float) for k in K)
    roots = cm.polyroots(cm.charpoly(closed_loop(A, b, K)))
    for r, w in zip(roots, sorted(poles, key=lambda v: (complex(v).real, complex(v).imag))):
        assert abs(r - w) < 1e-9


def test_unpaired_complex_pole_rejected():
    with pytest.raises(ValueError):
        ackermann_poles([[0, 1], [0, 0]], [0, 1], [complex(-1, 1), -2])


def test_uncontrollable_rejected():
    A = [[1, 0], [0, 2]]
    b = [1, 0]
    with pytest.raises(ValueError):
        ackermann(A, b, [1, 3, 2])


def test_wrong_polynomial_rejected():
    with pytest.raises(ValueError):
        ackermann([[0, 1], [0, 0]], [0, 1], [2, 2, 2])
    with pytest.raises(ValueError):
        ackermann([[0, 1], [0, 0]], [0, 1], [1, 2])


def test_poly_from_roots_exact():
    assert poly_from_roots([-1, -2]) == [1, 3, 2]
    assert poly_from_roots([Fraction(1, 2)]) == [1, Fraction(-1, 2)]
    p = poly_from_roots([complex(-1, 1), complex(-1, -1)])
    assert p == [1.0, 2.0, 2.0]


def test_float_error_grows_with_n():
    # A = diag(-1, ..., -n), b = ones, poles at -(n + 1), ..., -2n. The
    # coefficient error of the placed polynomial, relative to its size,
    # grows quickly with n. This shows the instability; the bound is loose.
    def rel_error(n):
        A = [[float(-(i + 1)) if i == j else 0.0 for j in range(n)] for i in range(n)]
        b = [1.0] * n
        p = poly_from_roots([float(-(n + 1 + i)) for i in range(n)])
        K = ackermann(A, b, p)
        Acl = [[Fraction(v) for v in row] for row in closed_loop(A, b, K)]
        got = cm.charpoly(Acl)
        return max(abs(float(g) - c) / abs(c) for g, c in zip(got, p))

    assert rel_error(4) < 1e-10
    assert rel_error(12) > 100 * rel_error(4)
