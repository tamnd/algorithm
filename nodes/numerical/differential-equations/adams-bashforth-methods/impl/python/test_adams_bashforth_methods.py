# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adams-bashforth-methods/. The authors are listed in prov/4QMRZ8.jsonl.

import math
from fractions import Fraction as F

import pytest

from adams_bashforth_methods import ab_coefficients, adams_bashforth


def _rho_sigma(k):
    """alpha_i, beta_i (i = 0..k) of the k-step AB method written as sum alpha_i y_{n+i} = h sum beta_i f_{n+i}."""
    alpha = [F(0)] * (k + 1)
    alpha[k], alpha[k - 1] = F(1), F(-1)
    beta = [F(0)] * (k + 1)
    for j, b in enumerate(ab_coefficients(k)):
        beta[k - 1 - j] = b
    return alpha, beta


def _c(alpha, beta, q):
    s = sum(a * F(i) ** q for i, a in enumerate(alpha))
    if q > 0:
        s -= q * sum(b * F(i) ** (q - 1) for i, b in enumerate(beta))
    return s / math.factorial(q)


def test_known_coefficients() -> None:
    assert ab_coefficients(1) == [F(1)]
    assert ab_coefficients(2) == [F(3, 2), F(-1, 2)]
    assert ab_coefficients(3) == [F(23, 12), F(-16, 12), F(5, 12)]
    assert ab_coefficients(4) == [F(55, 24), F(-59, 24), F(37, 24), F(-9, 24)]
    assert ab_coefficients(5) == [F(1901, 720), F(-2774, 720), F(2616, 720), F(-1274, 720), F(251, 720)]


def test_order_conditions_and_error_constants_exact() -> None:
    expected = {1: F(1, 2), 2: F(5, 12), 3: F(3, 8), 4: F(251, 720), 5: F(95, 288), 6: F(19087, 60480)}
    for k in range(1, 7):
        alpha, beta = _rho_sigma(k)
        assert sum(ab_coefficients(k)) == 1
        for q in range(k + 1):
            assert _c(alpha, beta, q) == 0
        assert _c(alpha, beta, k + 1) == expected[k]


def test_observed_order() -> None:
    f = lambda t, y: -2 * t * y * y
    for k in range(1, 6):
        errs = []
        for N in (40, 80, 160, 320):
            ts, ys = adams_bashforth(f, 0.0, 1.0, 2.0, 2.0 / N, k)
            errs.append(max(abs(y - 1 / (1 + t * t)) for t, y in zip(ts, ys)))
        p = math.log2(errs[-2] / errs[-1])
        assert abs(p - k) < 0.25, (k, p)


def test_worked_example() -> None:
    ts, ys = adams_bashforth(lambda t, y: -2 * t * y * y, 0.0, 1.0, 0.2, 0.1, 2)
    assert ts == [0.0, 0.1, 0.2]
    assert abs(ys[1] - 0.990099) < 1e-6
    f1 = -2 * 0.1 * ys[1] ** 2
    assert abs(ys[2] - (ys[1] + 0.1 * 1.5 * f1)) < 1e-15
    assert abs(ys[2] - 0.960690) < 1e-6


def test_exact_for_polynomials() -> None:
    # AB4 with RK4 starting values is exact when y is a polynomial of degree at most 4.
    ts, ys = adams_bashforth(lambda t, y: t ** 3, 0.0, 1.0, 2.0, 0.1, 4)
    assert all(abs(y - (1 + t ** 4 / 4)) < 1e-12 for t, y in zip(ts, ys))


def test_vector_oscillator() -> None:
    f = lambda t, y: [y[1], -y[0]]
    ts, ys = adams_bashforth(f, 0.0, [1.0, 0.0], 2 * math.pi, 2 * math.pi / 400, 4)
    assert abs(ys[-1][0] - 1) < 1e-6 and abs(ys[-1][1]) < 1e-6
    # The energy is not conserved exactly, but its error is of the order of the global error.
    assert abs(ys[-1][0] ** 2 + ys[-1][1] ** 2 - 1) < 1e-6


def test_stability_interval_ab2() -> None:
    def growth(z, k=2, n=2000):
        ts, ys = adams_bashforth(lambda t, y: z * y, 0.0, 1.0, float(n), 1.0, k)
        return abs(ys[-1])
    assert growth(-0.9) < 1e-3
    assert growth(-1.1) > 1e3
    assert growth(-0.5, k=3) < 1e-3 and growth(-0.6, k=3) > 1e3
    assert growth(-0.28, k=4) < 1e-3 and growth(-0.32, k=4) > 1e3


def test_stiff_failure() -> None:
    f = lambda t, y: -1000.0 * (y - math.cos(t))
    _, ys = adams_bashforth(f, 0.0, 1.0, 1.0, 0.01, 2)
    assert not abs(ys[-1]) < 1e10
    _, ys = adams_bashforth(f, 0.0, 1.0, 1.0, 0.0005, 2)
    assert abs(ys[-1] - math.cos(1.0)) < 1e-3


def test_edges() -> None:
    assert adams_bashforth(lambda t, y: y, 0.0, 2.0, 0.0, 0.1) == ([0.0], [2.0])
    ts, ys = adams_bashforth(lambda t, y: y, 0.0, 1.0, 0.05, 1.0, 4)
    assert ts == [0.0, 0.05] and abs(ys[1] - math.exp(0.05)) < 1e-8
    ts, _ = adams_bashforth(lambda t, y: y, 0.0, 1.0, 1.0, 0.3, 3)
    assert len(ts) == 5 and ts[-1] == 1.0 and abs(ts[1] - 0.25) < 1e-15
    ts, ys = adams_bashforth(lambda t, y: y, 0.0, 1.0, 1.0, 0.1, 1)
    assert abs(ys[-1] - 1.1 ** 10) < 1e-12
    with pytest.raises(ValueError):
        adams_bashforth(lambda t, y: y, 0.0, 1.0, 1.0, 0.0)
    with pytest.raises(ValueError):
        adams_bashforth(lambda t, y: y, 1.0, 1.0, 0.0, 0.1)
    with pytest.raises(ValueError):
        ab_coefficients(0)
