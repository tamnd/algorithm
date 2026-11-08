# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/romberg-integration/. The authors are listed in prov/M6H41M.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from romberg_integration import romberg


def counted(f):
    calls = [0]

    def g(x):
        calls[0] += 1
        return f(x)

    return g, calls


def full_table(f, a, b, K):
    """The whole table to level K: min_level > K disables the early stop."""
    return romberg(f, a, b, tol=0, max_level=K, min_level=K + 1)[2]


def trap(f, a, b, m):
    h = (b - a) / m
    return h * (sum(f(a + j * h) for j in range(1, m)) + (f(a) + f(b)) / 2)


def simpson(f, a, b, m):
    h = (b - a) / m
    return h / 3 * (f(a) + f(b) + sum((4 if j % 2 else 2) * f(a + j * h) for j in range(1, m)))


def test_first_columns_are_trapezoid_simpson_boole() -> None:
    f = lambda x: 1 / (1 + x * x)
    a, b = F(0), F(1)
    t = full_table(f, a, b, 5)
    for i in range(6):
        assert t[i][0] == trap(f, a, b, 2**i)
    for i in range(1, 6):
        assert t[i][1] == simpson(f, a, b, 2**i)
    # Boole on 4 subintervals: weights 7, 32, 12, 32, 7 over 90
    h = (b - a) / 4
    boole = (b - a) / 90 * sum(w * f(a + j * h) for j, w in enumerate((7, 32, 12, 32, 7)))
    assert t[2][2] == boole


def test_degree_of_exactness_of_each_column() -> None:
    # R[i][k] is exact for x^m, m <= 2k + 1, and fails for m = 2k + 2.
    for a, b in ((F(0), F(1)), (F(-2, 3), F(5, 4))):
        for k in range(0, 5):
            for m in range(0, 2 * k + 3):
                exact = (b ** (m + 1) - a ** (m + 1)) / (m + 1)
                t = full_table(lambda x, m=m: x**m, a, b, k)
                if m <= 2 * k + 1:
                    assert t[k][k] == exact, (k, m)
                else:
                    assert t[k][k] != exact, (k, m)


def test_random_polynomials_exact() -> None:
    rng = random.Random(1955)
    for _ in range(500):
        k = rng.randint(0, 4)
        c = [F(rng.randint(-9, 9), rng.randint(1, 7)) for _ in range(2 * k + 2)]
        a = F(rng.randint(-8, 8), rng.randint(1, 3))
        b = a + F(rng.randint(-8, 8), rng.randint(1, 3))
        p = lambda x: sum(ci * x**i for i, ci in enumerate(c))
        exact = sum(ci * (b ** (i + 1) - a ** (i + 1)) / (i + 1) for i, ci in enumerate(c))
        t = full_table(p, a, b, k)
        assert t[k][k] == exact


def test_weights_are_positive() -> None:
    # The rule R[K][k] is a linear rule on the 2^K + 1 nodes; recover its
    # weights from unit vectors in exact arithmetic (Bauer, Rutishauser, Stiefel).
    for K in range(0, 6):
        n = 2**K
        for k in range(0, K + 1):
            weights = []
            for j in range(n + 1):
                e = lambda x, j=j: F(1) if x == F(j, n) else F(0)
                t = full_table(e, F(0), F(1), K)
                weights.append(t[K][k])
            assert all(w > 0 for w in weights) and sum(weights) == 1


def test_convergence_and_evaluations_on_exp() -> None:
    g, calls = counted(math.exp)
    v, est, t = romberg(g, 0.0, 1.0, tol=1e-13)
    K = len(t) - 1
    assert calls[0] == 2**K + 1
    assert abs(v - (math.e - 1)) < 1e-14 and K <= 6
    # diagonal errors fall superlinearly: each is far below the last
    errs = [abs(t[i][i] - (math.e - 1)) for i in range(4)]
    assert errs[1] < 1e-2 * errs[0] and errs[2] < 1e-2 * errs[1] and errs[3] < 1e-2 * errs[2]
    # column k converges like h^(2k + 2): ratios near 4^(k + 1)
    for k in range(0, 3):
        r = (t[4][k] - (math.e - 1)) / (t[5][k] - (math.e - 1))
        assert abs(r / 4 ** (k + 1) - 1) < 0.05


def test_pi() -> None:
    v, est, _ = romberg(lambda x: 4 / (1 + x * x), 0.0, 1.0, tol=1e-12)
    assert abs(v - math.pi) < 1e-12 and est <= 1e-12


def test_singular_and_nonsmooth_integrands_converge_slowly() -> None:
    # sqrt(x): the expansion has an h^(3/2) term, so extrapolation gains little
    t = full_table(math.sqrt, 0.0, 1.0, 10)
    v = t[10][10]
    err_trap = abs(t[10][0] - 2 / 3)
    err_diag = abs(v - 2 / 3)
    assert 1e-6 < err_diag < err_trap < 1e-3
    # kink at the irrational point 1/sqrt(2): the errors are O(h^2) and
    # irregular, and extrapolation does not improve them
    c = 1 / math.sqrt(2)
    exact = c * c / 2 + (1 - c) ** 2 / 2
    t = full_table(lambda x: abs(x - c), 0.0, 1.0, 12)
    assert 1e-10 < abs(t[12][12] - exact) < 1e-6
    assert abs(t[12][12] - exact) > 0.1 * abs(t[12][0] - exact)
    # a kink at 1/3 is a curiosity: the trapezoidal errors are exactly
    # (2/9) 4^(-i) because 1/3 has a periodic binary expansion, and column 1
    # is exact
    t = full_table(lambda x: abs(x - F(1, 3)), F(0), F(1), 6)
    assert all(t[i][0] - F(5, 18) == F(2, 9) / 4**i for i in range(7))
    assert all(t[i][1] == F(5, 18) for i in range(1, 7))


def test_periodic_integrand_is_already_converged_in_column_zero() -> None:
    exact = 2 * math.pi * 1.2660658777520083  # 2 pi I_0(1)
    t = full_table(lambda x: math.exp(math.cos(x)), 0.0, 2 * math.pi, 4)
    assert abs(t[4][0] - exact) < 1e-13
    # extrapolation mixes in the coarse rows and makes it worse
    assert abs(t[4][4] - exact) > 1e-6


def test_edge_cases() -> None:
    v, est, t = romberg(math.exp, 2.0, 2.0)
    assert v == 0.0 and est == 0.0
    v1, _, _ = romberg(math.exp, 0.0, 1.0)
    v2, _, _ = romberg(math.exp, 1.0, 0.0)
    assert abs(v1 + v2) < 1e-15
    v, est, t = romberg(math.exp, 0.0, 1.0, max_level=0)
    assert len(t) == 1 and v == (1 + math.e) / 2 and est == 0.0
    # min_level guards against early stops on functions that vanish at the
    # first nodes: sin(2 pi x)^2 is 0 at 0, 1/2, 1 but has integral 1/2
    v, _, _ = romberg(lambda x: math.sin(2 * math.pi * x) ** 2, 0.0, 1.0, tol=1e-10)
    assert abs(v - 0.5) < 1e-10
    with pytest.raises(ValueError):
        romberg(math.exp, 0.0, 1.0, max_level=-1)
