# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/savitzky-golay-filter/. The authors are listed in prov/WPM8SW.jsonl.

import random
from fractions import Fraction
from math import factorial

from savitzky_golay_filter import gram_polynomials, savitzky_golay, sg_coefficients


def solve(a, b):
    """Gaussian elimination in Fraction."""
    n = len(a)
    m = [list(row) + [v] for row, v in zip(a, b)]
    for col in range(n):
        piv = next(r for r in range(col, n) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col] / m[col][col]
                m[r] = [u - f * v for u, v in zip(m[r], m[col])]
    return [m[i][n] / m[i][i] for i in range(n)]


def direct_fit(y, m, p):
    """Least squares coefficients a_0 .. a_p of the fit sum a_k i^k on i = -m .. m, by the normal equations."""
    pts = range(-m, m + 1)
    ata = [[Fraction(sum(i ** (j + k) for i in pts)) for k in range(p + 1)] for j in range(p + 1)]
    aty = [sum(Fraction(v) * i ** j for i, v in zip(pts, y)) for j in range(p + 1)]
    return solve(ata, aty)


def fit_value(a, t, d):
    return sum(a[k] * (factorial(k) // factorial(k - d)) * Fraction(t) ** (k - d) for k in range(d, len(a)))


def test_coefficients_equal_direct_least_squares() -> None:
    for m in range(0, 5):
        for p in range(0, 2 * m + 1):
            for d in range(0, min(p, 2) + 1):
                for t in (0, -m, m):
                    c = sg_coefficients(m, p, t, d)
                    for idx in range(2 * m + 1):
                        unit = [0] * (2 * m + 1)
                        unit[idx] = 1
                        assert c[idx] == fit_value(direct_fit(unit, m, p), t, d)


def test_known_tables() -> None:
    assert sg_coefficients(2, 2) == [Fraction(v, 35) for v in (-3, 12, 17, 12, -3)]
    assert sg_coefficients(3, 2) == [Fraction(v, 21) for v in (-2, 3, 6, 7, 6, 3, -2)]
    assert sg_coefficients(2, 2, 0, 1) == [Fraction(v, 10) for v in (-2, -1, 0, 1, 2)]
    assert sg_coefficients(1, 0) == [Fraction(1, 3)] * 3  # degree 0 is the moving average


def test_even_degree_equals_next_odd() -> None:
    for m in range(1, 7):
        for p in range(0, 2 * m, 2):
            assert sg_coefficients(m, p) == sg_coefficients(m, p + 1)


def test_noise_gain() -> None:
    """sum c_i^2 = c_0 because the weights are a row of a projection; for m = 2, p = 2 it is 17/35."""
    for m in range(1, 6):
        for p in range(0, 2 * m + 1):
            c = sg_coefficients(m, p)
            assert sum(v * v for v in c) == c[m]
    assert sum(v * v for v in sg_coefficients(2, 2)) == Fraction(17, 35)


def test_reproduces_polynomials() -> None:
    rng = random.Random(9101)
    for _ in range(40):
        m = rng.randint(1, 5)
        p = rng.randint(0, 2 * m)
        q = [Fraction(rng.randint(-9, 9)) for _ in range(p + 1)]
        x = [sum(a * k ** j for j, a in enumerate(q)) for k in range(3 * m + 4)]
        assert savitzky_golay(x, m, p) == x
        dq = [j * q[j] for j in range(1, len(q))]
        if p >= 1:
            assert savitzky_golay(x, m, p, 1) == [sum(a * k ** j for j, a in enumerate(dq)) for k in range(len(x))]


def test_filter_equals_window_fits() -> None:
    rng = random.Random(9102)
    for _ in range(30):
        m = rng.randint(1, 4)
        p = rng.randint(0, 2 * m)
        x = [rng.randint(-50, 50) for _ in range(rng.randint(2 * m + 1, 4 * m + 6))]
        y = savitzky_golay(x, m, p)
        n = len(x)
        for k in range(n):
            base = min(max(k - m, 0), n - 2 * m - 1)
            a = direct_fit(x[base:base + 2 * m + 1], m, p)
            assert y[k] == fit_value(a, k - base - m, 0)


def test_gram_polynomials_orthogonal() -> None:
    for m in range(1, 6):
        polys = gram_polynomials(m, 2 * m)
        for a in range(len(polys)):
            for b in range(a):
                s = sum(sum(c * i ** j for j, c in enumerate(polys[a])) * sum(c * i ** j for j, c in enumerate(polys[b]))
                        for i in range(-m, m + 1))
                assert s == 0
