# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-polynomial-regression/. The authors are listed in prov/C1XC0A.jsonl.

import random
from fractions import Fraction

from local_polynomial_regression import (
    epanechnikov, local_linear_closed_form, local_poly, local_poly_coefficients,
    lowess, tricube,
)

LOWESS_X = list(range(1, 11))
LOWESS_Y = [3.1, 4.9, 7.2, 8.8, 11.1, 13.0, 30.0, 16.9, 19.2, 21.0]


def F(v):
    return [Fraction(t) for t in v]


def test_page_example() -> None:
    xs = list(range(7))
    sq = [x * x for x in xs]
    ll = [local_poly(Fraction(x), xs, sq, Fraction(3)) for x in xs]
    lc = [local_poly(Fraction(x), xs, sq, Fraction(3), 0) for x in xs]
    assert ll == [Fraction(-20, 73), Fraction(67, 35), Fraction(28, 5), Fraction(53, 5),
                  Fraction(88, 5), Fraction(907, 35), Fraction(2608, 73)]
    assert lc == [Fraction(14, 11), Fraction(43, 15), Fraction(28, 5), Fraction(53, 5),
                  Fraction(88, 5), Fraction(343, 15), Fraction(302, 11)]
    line = [2 * x for x in xs]
    assert [local_poly(Fraction(x), xs, line, Fraction(2)) for x in xs] == line
    plain = lowess(LOWESS_X, LOWESS_Y, 2 / 3, 0)
    robust = lowess(LOWESS_X, LOWESS_Y, 2 / 3, 2)
    assert abs(plain[6] - 19.31) < 0.01
    assert all(abs(f - (2 * x + 1)) < 0.1 for x, f in zip(LOWESS_X, robust))


def test_reproduces_polynomials_of_its_degree_exactly() -> None:
    rng = random.Random(81)
    checked = 0
    for _ in range(150):
        p = rng.choice((1, 1, 2, 3))
        n = rng.randint(p + 1, 12)
        xs = [Fraction(rng.randint(-30, 30), rng.randint(1, 4)) for _ in range(n)]
        coef = [Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(p + 1)]
        q = lambda t: sum(c * t ** k for k, c in enumerate(coef))
        ys = [q(t) for t in xs]
        h = Fraction(rng.randint(2, 40), rng.randint(1, 3))
        # Any x, including points at the edge of the data and outside it.
        x = Fraction(rng.randint(-40, 40), rng.randint(1, 4))
        beta = local_poly_coefficients(x, xs, ys, h, p)
        if beta is None:  # fewer than p + 1 distinct points with weight
            continue
        checked += 1
        assert beta[0] == q(x)
        if p >= 1:  # beta_1 is the slope q'(x)
            assert beta[1] == sum(k * c * x ** (k - 1) for k, c in enumerate(coef) if k)
    assert checked > 50


def test_local_linear_matches_closed_form() -> None:
    rng = random.Random(82)
    for _ in range(200):
        n = rng.randint(1, 10)
        xs = [Fraction(rng.randint(-20, 20), rng.randint(1, 3)) for _ in range(n)]
        ys = [Fraction(rng.randint(-20, 20)) for _ in range(n)]
        h = Fraction(rng.randint(1, 30), rng.randint(1, 3))
        x = Fraction(rng.randint(-25, 25), rng.randint(1, 3))
        assert local_poly(x, xs, ys, h, 1) == local_linear_closed_form(x, xs, ys, h)


def test_degree_zero_is_nadaraya_watson() -> None:
    rng = random.Random(83)
    for _ in range(200):
        n = rng.randint(1, 10)
        xs = [Fraction(rng.randint(-20, 20), rng.randint(1, 3)) for _ in range(n)]
        ys = [Fraction(rng.randint(-20, 20)) for _ in range(n)]
        h = Fraction(rng.randint(1, 30), rng.randint(1, 3))
        x = Fraction(rng.randint(-25, 25), rng.randint(1, 3))
        w = [epanechnikov((x - xi) / h) for xi in xs]
        nw = sum(a * b for a, b in zip(w, ys)) / sum(w) if sum(w) else None
        assert local_poly(x, xs, ys, h, 0) == nw


def test_boundary_bias_is_of_order_h_squared() -> None:
    # Uniform design i/N on [0, 1]. A line has no bias at the end point 0,
    # and for m(x) = x^2 the bias over h^2 tends to
    # (mu2^2 - mu1 mu3) / (mu0 mu2 - mu1^2) = -11/95 (Epanechnikov, one-sided moments).
    for N, h in ((1000, Fraction(1, 10)), (4000, Fraction(1, 20))):
        xs = [Fraction(i, N) for i in range(N + 1)]
        assert local_poly(Fraction(0), xs, [3 - 2 * x for x in xs], h) == 3
        ratio = local_poly(Fraction(0), xs, [x * x for x in xs], h) / (h * h)
        assert abs(ratio + Fraction(11, 95)) < Fraction(1, 2) / (N * h)


def test_lowess_on_a_line_and_with_outliers() -> None:
    xs = F(range(12))
    line = [Fraction(5) - Fraction(1, 3) * x for x in xs]
    assert lowess(xs, line, 2 / 3, 2) == line
    rng = random.Random(84)
    xs = sorted(rng.uniform(0, 10) for _ in range(40))
    ys = [1 + 0.5 * x + rng.gauss(0, 0.2) for x in xs]
    for i in rng.sample(range(5, 35), 4):
        ys[i] += 15
    truth = [1 + 0.5 * x for x in xs]
    err = lambda fit: max(abs(f - t) for f, t in zip(fit, truth))
    # Measured on this seed: robustness weights remove the pull of the outliers.
    assert err(lowess(xs, ys, 2 / 3, 0)) > 1.0
    assert err(lowess(xs, ys, 2 / 3, 2)) < 0.4
    assert tricube(Fraction(1, 2)) == Fraction(343, 512)
