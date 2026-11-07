# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/back-substitution/. The authors are listed in prov/4HMP35.jsonl.

import random
from fractions import Fraction

import pytest

from back_substitution import back_substitution, forward_substitution

U_ROUND = Fraction(1, 2**53)


def gamma(k: int) -> Fraction:
    return k * U_ROUND / (1 - k * U_ROUND)


def exact_upper(u, b):
    n = len(b)
    x = [Fraction(0)] * n
    for i in range(n - 1, -1, -1):
        s = Fraction(b[i]) - sum(Fraction(u[i][j]) * x[j] for j in range(i + 1, n))
        x[i] = s / Fraction(u[i][i])
    return x


def check_backward(t, b, x, upper):
    """Check |b - T x| <= gamma_n |T| |x| row by row, in exact arithmetic.

    This is implied by (T + dT) x = b with |dT| <= gamma_n |T|.
    """
    n = len(b)
    g = gamma(n)
    for i in range(n):
        cols = range(i, n) if upper else range(i + 1)
        r = Fraction(b[i]) - sum(Fraction(t[i][j]) * Fraction(x[j]) for j in cols)
        bound = g * sum(abs(Fraction(t[i][j]) * Fraction(x[j])) for j in cols)
        assert abs(r) <= bound


def test_page_example():
    u = [[2.0, 1.0, -1.0, 3.0], [0.0, 1.0, 2.0, -1.0], [0.0, 0.0, 4.0, 2.0], [0.0, 0.0, 0.0, 5.0]]
    assert back_substitution(u, [0.0, 3.0, 14.0, 5.0]) == [1.0, -2.0, 3.0, 1.0]


def test_one_by_one_and_diagonal():
    assert back_substitution([[4.0]], [2.0]) == [0.5]
    d = [[2.0, 0.0, 0.0], [0.0, -4.0, 0.0], [0.0, 0.0, 0.5]]
    assert back_substitution(d, [1.0, 1.0, 1.0]) == [0.5, -0.25, 2.0]
    assert forward_substitution(d, [1.0, 1.0, 1.0]) == [0.5, -0.25, 2.0]


def test_singular_reported():
    with pytest.raises(ValueError):
        back_substitution([[1.0, 2.0], [0.0, 0.0]], [1.0, 1.0])
    with pytest.raises(ValueError):
        forward_substitution([[0.0, 0.0], [1.0, 1.0]], [1.0, 1.0])


def test_unit_diagonal_ignores_diagonal():
    l = [[99.0, 0.0], [3.0, 99.0]]
    assert forward_substitution(l, [1.0, 5.0], unit_diagonal=True) == [1.0, 2.0]


def test_m_matrix_accurate_despite_condition():
    # kappa_inf = 40 * 2^39, yet each component is accurate to a few units of roundoff.
    n = 40
    t = [[1.0 if i == j else (-1.0 if j > i else 0.0) for j in range(n)] for i in range(n)]
    b = [1.0 / (i + 1) for i in range(n)]
    x = back_substitution(t, b)
    xe = exact_upper(t, b)
    worst = max(abs(Fraction(a) - e) / e for a, e in zip(x, xe))
    assert worst <= 8 * U_ROUND
    check_backward(t, b, x, upper=True)


def test_random_against_exact():
    rng = random.Random(4171)
    for _ in range(600):
        n = rng.randint(1, 9)
        u = [[(rng.uniform(-3, 3) if j > i else 0.0) for j in range(n)] for i in range(n)]
        for i in range(n):
            u[i][i] = rng.choice([-1, 1]) * rng.uniform(0.05, 4)
        b = [rng.uniform(-5, 5) for _ in range(n)]
        x = back_substitution(u, b)
        check_backward(u, b, x, upper=True)
        lt = [[u[j][i] for j in range(n)] for i in range(n)]  # the transpose is lower triangular
        y = forward_substitution(lt, b)
        check_backward(lt, b, y, upper=False)
        # the normwise forward error bound gamma_n kappa / (1 - gamma_n kappa), in the infinity norm
        xe = exact_upper(u, b)
        cols = [exact_upper(u, [1.0 if k == j else 0.0 for k in range(n)]) for j in range(n)]
        inv_norm = max(sum(abs(cols[j][i]) for j in range(n)) for i in range(n))
        kappa = max(sum(abs(Fraction(v)) for v in row) for row in u) * inv_norm
        gk = gamma(n) * kappa
        if gk < 1 and any(xe):
            err = max(abs(Fraction(a) - e) for a, e in zip(x, xe)) / max(abs(e) for e in xe)
            assert err <= gk / (1 - gk)
