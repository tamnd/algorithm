# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/classical-runge-kutta-4/. The authors are listed in prov/349F36.jsonl.

import math
from fractions import Fraction as F

import pytest

from classical_runge_kutta_4 import A, B, C, rk4, rk4_step, stability_function


def test_order_conditions_exact() -> None:
    s = 4
    assert all(C[i] == sum(A[i]) for i in range(s))
    Ac = [sum(A[i][j] * C[j] for j in range(s)) for i in range(s)]
    Acc = [sum(A[i][j] * C[j] ** 2 for j in range(s)) for i in range(s)]
    AAc = [sum(A[i][j] * Ac[j] for j in range(s)) for i in range(s)]
    conds = [
        (sum(B), F(1)),
        (sum(B[i] * C[i] for i in range(s)), F(1, 2)),
        (sum(B[i] * C[i] ** 2 for i in range(s)), F(1, 3)),
        (sum(B[i] * Ac[i] for i in range(s)), F(1, 6)),
        (sum(B[i] * C[i] ** 3 for i in range(s)), F(1, 4)),
        (sum(B[i] * C[i] * Ac[i] for i in range(s)), F(1, 8)),
        (sum(B[i] * Acc[i] for i in range(s)), F(1, 12)),
        (sum(B[i] * AAc[i] for i in range(s)), F(1, 24)),
    ]
    for got, want in conds:
        assert got == want
    # order 5 fails: the condition sum b_i c_i^4 = 1/5 is violated
    assert sum(B[i] * C[i] ** 4 for i in range(s)) == F(5, 24) != F(1, 5)


def test_worked_examples() -> None:
    y = rk4_step(lambda t, y: y, 0.0, [1.0], 0.1)
    assert y[0] == pytest.approx(1.1051708333333333, abs=1e-15)
    ts, ys = rk4(lambda t, y: -2.0 * t * y * y, 0.0, 1.0, 1.0, 0.5)
    assert ys[1] == pytest.approx(0.7983792622884115, abs=1e-15)
    assert ys[2] == pytest.approx(0.4997015228649558, abs=1e-15)


def test_observed_order_four() -> None:
    f = lambda t, y: -2.0 * t * y * y
    errs = [abs(rk4(f, 0.0, 1.0, 2.0, 0.1 / 2**k)[1][-1] - 0.2) for k in range(4)]
    for a, b in zip(errs, errs[1:]):
        assert math.log2(a / b) == pytest.approx(4.0, abs=0.1)


def test_linear_system_matrix_exponential() -> None:
    f = lambda t, y: [-2 * y[0] + y[1], y[0] - 2 * y[1]]
    exact = [math.exp(-1) + math.exp(-3), math.exp(-1) - math.exp(-3)]
    errs = []
    for h in (0.05, 0.025):
        _, ys = rk4(f, 0.0, [2.0, 0.0], 1.0, h)
        errs.append(max(abs(a - b) for a, b in zip(ys[-1], exact)))
    assert errs[0] < 1e-6 and 15 < errs[0] / errs[1] < 18


def test_logistic() -> None:
    _, ys = rk4(lambda t, y: y * (1 - y), 0.0, 0.1, 5.0, 0.05)
    assert abs(ys[-1] - 1 / (1 + 9 * math.exp(-5.0))) < 1e-8


def test_stability_function() -> None:
    for z in (-1.0, -2.5, 0.3 + 0.7j, 2j):
        h, lam = 0.5, z / 0.5
        y = rk4_step(lambda t, y: [lam * y[0]], 0.0, [1.0 + 0j], h)
        assert abs(y[0] - stability_function(z)) < 1e-12
    assert abs(stability_function(-2.78)) < 1 < abs(stability_function(-2.79))
    assert abs(stability_function(2.8j)) <= 1 < abs(stability_function(2.9j))


def test_harmonic_oscillator_energy_loss() -> None:
    # |R(ih)|^2 = 1 - h^6/72 + h^8/576, so the energy shrinks by this factor per step
    h = 0.5
    _, ys = rk4(lambda t, y: [y[1], -y[0]], 0.0, [1.0, 0.0], 20 * h, h)
    q = 1 - h**6 / 72 + h**8 / 576
    for n, y in enumerate(ys):
        assert y[0] ** 2 + y[1] ** 2 == pytest.approx(q**n, rel=1e-12)


def test_stiff_problem_fails_explicit() -> None:
    _, ys = rk4(lambda t, y: -1000.0 * y, 0.0, 1.0, 1.0, 0.01)  # z = -10, outside the region
    assert abs(ys[-1]) > 1e100
    _, ys = rk4(lambda t, y: -1000.0 * y, 0.0, 1.0, 1.0, 0.002)  # z = -2, inside
    assert abs(ys[-1]) < 1e-10


def test_edges() -> None:
    f = lambda t, y: -y
    assert rk4(f, 0.0, 1.0, 0.0, 0.1) == ([0.0], [1.0])
    ts, _ = rk4(f, 0.0, 1.0, 1.0, 0.3)
    assert ts[-1] == 1.0 and len(ts) == 5
    ts, ys = rk4(f, 0.0, 1.0, 0.5, 4.0)
    assert ts == [0.0, 0.5] and ys[1] == pytest.approx(float(stability_function(-0.5)))
    ts, _ = rk4(f, 0.0, 1.0, 1.0, 0.1)
    assert len(ts) == 11 and ts[-1] == 1.0
    with pytest.raises(ValueError):
        rk4(f, 0.0, 1.0, -1.0, 0.1)
