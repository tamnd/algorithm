# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backward-differentiation-formulas/. The authors are listed in prov/NRVHTE.jsonl.

import cmath
import math
from fractions import Fraction as F

import pytest

from backward_differentiation_formulas import bdf, bdf_coefficients, gauss3_step


def _roots(c):
    """All roots of the polynomial with coefficients c (highest degree first), Durand-Kerner."""
    n = len(c) - 1
    c = [complex(x) / complex(c[0]) for x in c]
    r = [(0.4 + 0.9j) ** i for i in range(n)]
    for _ in range(2000):
        new = []
        for i in range(n):
            p = sum(c[j] * r[i] ** (n - j) for j in range(n + 1))
            d = 1
            for m in range(n):
                if m != i:
                    d *= r[i] - r[m]
            new.append(r[i] - p / d)
        r = new
    return r


def test_coefficients_order_and_error_constant_exact() -> None:
    assert bdf_coefficients(2) == [F(3, 2), F(-2), F(1, 2)]
    assert bdf_coefficients(3) == [F(11, 6), F(-3), F(3, 2), F(-1, 3)]
    for k in range(1, 8):
        alpha = bdf_coefficients(k)
        a = [alpha[k - m] for m in range(k + 1)]  # coefficient of y_{n+1-k+m}
        b = [F(0)] * k + [F(1)]

        def c(q):
            s = sum(a[m] * F(m) ** q for m in range(k + 1))
            if q > 0:
                s -= q * sum(b[m] * F(m) ** (q - 1) for m in range(k + 1))
            return s / math.factorial(q)

        assert all(c(q) == 0 for q in range(k + 1))
        assert c(k + 1) == F(-1, k + 1)
        assert alpha[0] == sum(F(1, j) for j in range(1, k + 1))


def test_zero_stable_exactly_up_to_six() -> None:
    for k in range(2, 8):
        rs = _roots([float(v) for v in bdf_coefficients(k)])
        spurious = max(abs(r) for r in rs if abs(r - 1) > 1e-8)
        if k <= 6:
            assert spurious < 0.87
        else:
            assert spurious > 1.02
    with pytest.raises(ValueError):
        bdf(lambda t, y: y, 0.0, 1.0, 1.0, 0.1, 7)


def test_a_alpha_angles() -> None:
    expected = {3: 86.03, 4: 73.35, 5: 51.84, 6: 17.84}
    for k, deg in expected.items():
        amin = math.pi / 2
        for i in range(1, 4000):
            z = sum((1 - cmath.exp(-1j * math.pi * i / 4000)) ** j / j for j in range(1, k + 1))
            if z.real < 0:
                amin = min(amin, abs(cmath.phase(-z)))
        assert abs(math.degrees(amin) - deg) < 0.05, (k, math.degrees(amin))


def test_observed_order() -> None:
    f = lambda t, y: -2 * t * y * y
    jac = lambda t, y: -4 * t * y
    for k in range(1, 7):
        errs = []
        for N in (40, 80, 160, 320):
            ts, ys = bdf(f, 0.0, 1.0, 2.0, 2.0 / N, k, jac=jac)
            errs.append(max(abs(y - 1 / (1 + t * t)) for t, y in zip(ts, ys)))
        p = math.log2(errs[-2] / errs[-1])
        assert abs(p - k) < 0.3, (k, p)


def test_worked_example_bdf2() -> None:
    _, ys = bdf(lambda t, y: -2 * t * y * y, 0.0, 1.0, 0.2, 0.1, 2)
    y0, y1, y2 = ys
    assert abs(1.5 * y2 - 2 * y1 + 0.5 * y0 - 0.1 * (-0.4 * y2 * y2)) < 1e-14
    assert abs(y1 - 1 / 1.01) < 1e-9 and abs(y2 - 0.9621143) < 1e-7


def test_gauss3_order_six() -> None:
    errs = [abs(gauss3_step(lambda t, y: [y[0]], 0.0, [1.0], h, None)[0] - math.exp(h)) for h in (0.4, 0.2)]
    assert 100 < errs[0] / errs[1] < 160  # local error O(h^7): ratio near 128


def test_stiff_linear_large_steps() -> None:
    f = lambda t, y: -1000.0 * (y - math.cos(t)) - math.sin(t)
    for k in range(1, 7):
        _, ys = bdf(f, 0.0, 1.0, 1.0, 0.1, k, jac=lambda t, y: -1000.0)
        assert abs(ys[-1] - math.cos(1.0)) < 1e-4


def test_robertson_conserves_mass() -> None:
    def rob(t, y):
        return [-0.04 * y[0] + 1e4 * y[1] * y[2], 0.04 * y[0] - 1e4 * y[1] * y[2] - 3e7 * y[1] ** 2, 3e7 * y[1] ** 2]

    def jr(t, y):
        return [[-0.04, 1e4 * y[2], 1e4 * y[1]], [0.04, -1e4 * y[2] - 6e7 * y[1], -1e4 * y[1]], [0.0, 6e7 * y[1], 0.0]]

    ts, ys = bdf(rob, 0.0, [1.0, 0.0, 0.0], 40.0, 0.04, 2, jac=jr)
    assert all(abs(sum(y) - 1) < 1e-12 for y in ys)
    assert abs(ys[-1][0] - 0.7158270687) < 5e-6
    assert abs(ys[-1][1] - 9.185534764e-6) < 1e-10


def test_edges() -> None:
    assert bdf(lambda t, y: y, 0.0, 2.0, 0.0, 0.1) == ([0.0], [2.0])
    ts, ys = bdf(lambda t, y: -y, 0.0, 1.0, 0.05, 1.0, 3)
    assert ts == [0.0, 0.05] and abs(ys[1] - math.exp(-0.05)) < 1e-12
    ts, _ = bdf(lambda t, y: -y, 0.0, 1.0, 1.0, 0.3, 2)
    assert len(ts) == 5 and ts[-1] == 1.0
    _, ys = bdf(lambda t, y: [-y[0], -2 * y[1]], 0.0, [1.0, 1.0], 1.0, 0.01, 4)
    assert abs(ys[-1][0] - math.exp(-1)) < 1e-8 and abs(ys[-1][1] - math.exp(-2)) < 1e-8
    with pytest.raises(ValueError):
        bdf(lambda t, y: y, 0.0, 1.0, 1.0, 0.0)
