# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adams-moulton-methods/. The authors are listed in prov/S41K1C.jsonl.

import math
from fractions import Fraction as F

import pytest

from adams_moulton_methods import adams_moulton, am_coefficients


def _alpha_beta(k):
    """Coefficients of sum alpha_i y_{n+i} = h sum beta_i f_{n+i}, i = 0..max(k, 1)."""
    m = max(k, 1)
    alpha = [F(0)] * (m + 1)
    alpha[m], alpha[m - 1] = F(1), F(-1)
    beta = [F(0)] * (m + 1)
    for j, b in enumerate(am_coefficients(k)):
        beta[m - j] = b
    return alpha, beta


def _c(alpha, beta, q):
    s = sum(a * F(i) ** q for i, a in enumerate(alpha))
    if q > 0:
        s -= q * sum(b * F(i) ** (q - 1) for i, b in enumerate(beta))
    return s / math.factorial(q)


def test_known_coefficients() -> None:
    assert am_coefficients(0) == [F(1)]
    assert am_coefficients(1) == [F(1, 2), F(1, 2)]
    assert am_coefficients(2) == [F(5, 12), F(8, 12), F(-1, 12)]
    assert am_coefficients(3) == [F(9, 24), F(19, 24), F(-5, 24), F(1, 24)]
    assert am_coefficients(4) == [F(251, 720), F(646, 720), F(-264, 720), F(106, 720), F(-19, 720)]


def test_order_conditions_and_error_constants_exact() -> None:
    expected = [F(-1, 2), F(-1, 12), F(-1, 24), F(-19, 720), F(-3, 160), F(-863, 60480)]
    for k in range(6):
        alpha, beta = _alpha_beta(k)
        for q in range(k + 2):
            assert _c(alpha, beta, q) == 0
        assert _c(alpha, beta, k + 2) == expected[k]


def test_observed_order() -> None:
    f = lambda t, y: -2 * t * y * y
    jac = lambda t, y: -4 * t * y
    for k in range(5):
        errs = []
        for N in (40, 80, 160, 320):
            ts, ys = adams_moulton(f, 0.0, 1.0, 2.0, 2.0 / N, k, jac=jac)
            errs.append(max(abs(y - 1 / (1 + t * t)) for t, y in zip(ts, ys)))
        p = math.log2(errs[-2] / errs[-1])
        assert abs(p - (k + 1)) < 0.3, (k, p)


def test_worked_example() -> None:
    _, ys = adams_moulton(lambda t, y: -2 * t * y * y, 0.0, 1.0, 0.2, 0.1, 2)
    y1, y2 = ys[1], ys[2]
    # y2 must satisfy the implicit equation of AM2.
    rhs = y1 + 0.1 * (5 / 12 * (-0.4 * y2 * y2) + 8 / 12 * (-0.2 * y1 * y1) - 1 / 12 * 0.0)
    assert abs(y2 - rhs) < 1e-14
    assert abs(y2 - 0.9616165) < 1e-7


def test_exact_for_polynomials() -> None:
    ts, ys = adams_moulton(lambda t, y: t ** 3, 0.0, 1.0, 2.0, 0.1, 3)
    assert all(abs(y - (1 + t ** 4 / 4)) < 1e-12 for t, y in zip(ts, ys))


def test_trapezoidal_conserves_oscillator_energy() -> None:
    f = lambda t, y: [y[1], -y[0]]
    jac = lambda t, y: [[0.0, 1.0], [-1.0, 0.0]]
    _, ys = adams_moulton(f, 0.0, [1.0, 0.0], 100.0, 0.5, 1, jac=jac)
    assert all(abs(u * u + v * v - 1) < 1e-12 for u, v in ys)


def test_stability_and_stiffness() -> None:
    def last(z, k, n=400):
        _, ys = adams_moulton(lambda t, y: z * y, 0.0, 1.0, float(n), 1.0, k, jac=lambda t, y: z)
        return abs(ys[-1])
    assert last(-5.5, 2) < 1e-3 and last(-6.5, 2) > 1e3
    assert last(-2.8, 3) < 1e-3 and last(-3.2, 3) > 1e3
    # Backward Euler and the trapezoidal rule are A-stable.
    assert last(-1000.0, 0) < 1e-100 and last(-1000.0, 1) <= 1.0
    f = lambda t, y: -1000.0 * (y - math.cos(t))
    jac = lambda t, y: -1000.0
    _, ys = adams_moulton(f, 0.0, 1.0, 1.0, 0.05, 0, jac=jac)
    assert abs(ys[-1] - math.cos(1.0)) < 1e-3


def test_edges() -> None:
    assert adams_moulton(lambda t, y: y, 0.0, 2.0, 0.0, 0.1) == ([0.0], [2.0])
    ts, ys = adams_moulton(lambda t, y: y, 0.0, 1.0, 0.05, 1.0, 1)
    assert ts == [0.0, 0.05] and abs(ys[1] - (1 + 0.025) / (1 - 0.025)) < 1e-12
    ts, _ = adams_moulton(lambda t, y: y, 0.0, 1.0, 1.0, 0.3, 3)
    assert len(ts) == 5 and ts[-1] == 1.0
    ts, ys = adams_moulton(lambda t, y: [y[0], 2 * y[1]], 0.0, [1.0, 1.0], 1.0, 0.01, 3)
    assert abs(ys[-1][0] - math.e) < 1e-8 and abs(ys[-1][1] - math.e ** 2) < 1e-7
    with pytest.raises(ValueError):
        adams_moulton(lambda t, y: y, 0.0, 1.0, 1.0, -0.1)
    with pytest.raises(ValueError):
        am_coefficients(-1)
