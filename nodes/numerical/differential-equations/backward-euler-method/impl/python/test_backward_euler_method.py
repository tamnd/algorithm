# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backward-euler-method/. The authors are listed in prov/8ARQ7F.jsonl.

import math
import random

import pytest

from backward_euler_method import backward_euler, backward_euler_step, solve_linear


def test_worked_example_linear() -> None:
    ts, ys = backward_euler(lambda t, y: -10.0 * y, 0.0, 1.0, 1.0, 0.25, jac=lambda t, y: -10.0)
    assert ts == [0.0, 0.25, 0.5, 0.75, 1.0]
    for n, y in enumerate(ys):
        assert y == pytest.approx((1.0 / 3.5) ** n, rel=1e-12)


def test_worked_example_nonlinear() -> None:
    ts, ys = backward_euler(lambda t, y: -2.0 * t * y * y, 0.0, 1.0, 1.0, 0.5)
    y1 = -1.0 + math.sqrt(3.0)
    assert ys[1] == pytest.approx(y1, rel=1e-10)
    assert ys[2] == pytest.approx((-1.0 + math.sqrt(1.0 + 4.0 * y1)) / 2.0, rel=1e-10)


def _err(h: float) -> float:
    ts, ys = backward_euler(lambda t, y: -2.0 * t * y * y, 0.0, 1.0, 2.0, h)
    return abs(ys[-1] - 1.0 / (1.0 + 4.0))


def test_observed_order_one() -> None:
    errs = [_err(0.1 / 2**k) for k in range(4)]
    for a, b in zip(errs, errs[1:]):
        assert math.log2(a / b) == pytest.approx(1.0, abs=0.08)


def test_linear_system_against_matrix_exponential() -> None:
    # y' = A y with A = [[-2, 1], [1, -2]]: eigenvalues -1 and -3.
    f = lambda t, y: [-2 * y[0] + y[1], y[0] - 2 * y[1]]
    jac = lambda t, y: [[-2.0, 1.0], [1.0, -2.0]]
    exact = lambda t: [math.exp(-t) + math.exp(-3 * t), math.exp(-t) - math.exp(-3 * t)]  # y0 = (2, 0)
    errs = []
    for h in (0.02, 0.01, 0.005):
        _, ys = backward_euler(f, 0.0, [2.0, 0.0], 1.0, h, jac=jac)
        errs.append(max(abs(a - b) for a, b in zip(ys[-1], exact(1.0))))
    assert 1.9 < errs[0] / errs[1] < 2.1 and 1.9 < errs[1] / errs[2] < 2.1


def test_logistic() -> None:
    _, ys = backward_euler(lambda t, y: y * (1 - y), 0.0, 0.1, 3.0, 0.001)
    exact = 1.0 / (1.0 + 9.0 * math.exp(-3.0))
    assert abs(ys[-1] - exact) < 2e-4


def test_harmonic_oscillator_damps_exactly() -> None:
    # y' = (y2, -y1); each step multiplies the Euclidean norm by 1 / sqrt(1 + h^2).
    f = lambda t, y: [y[1], -y[0]]
    h = 0.1
    _, ys = backward_euler(f, 0.0, [1.0, 0.0], 5.0, h)
    for n, y in enumerate(ys):
        assert math.hypot(*y) == pytest.approx((1 + h * h) ** (-n / 2), rel=1e-9)


def test_stiff_problem_stays_bounded() -> None:
    lam = -1.0e6
    _, ys = backward_euler(lambda t, y: lam * (y - math.cos(t)), 0.0, 0.0, 1.0, 0.1, jac=lambda t, y: lam)
    assert abs(ys[-1] - math.cos(1.0)) < 1e-6
    # forward Euler with the same h has |1 + h lam| = 99999 and blows up
    y = 0.0
    for n in range(10):
        y = y + 0.1 * lam * (y - math.cos(n * 0.1))
    assert abs(y) > 1e40


def test_contractive_for_dissipative_f() -> None:
    # f(y) = -y^3 has one-sided Lipschitz constant 0, so distances never grow for any h.
    rng = random.Random(7)
    for _ in range(50):
        a, b = rng.uniform(-3, 3), rng.uniform(-3, 3)
        h = rng.uniform(0.01, 5.0)
        ya, _ = backward_euler_step(lambda t, y: [-y[0] ** 3], 0.0, [a], h)
        yb, _ = backward_euler_step(lambda t, y: [-y[0] ** 3], 0.0, [b], h)
        assert abs(ya[0] - yb[0]) <= abs(a - b) + 1e-12


def test_grid_edges() -> None:
    f = lambda t, y: -y
    assert backward_euler(f, 0.0, 1.0, 0.0, 0.1) == ([0.0], [1.0])
    ts, ys = backward_euler(f, 0.0, 1.0, 1.0, 0.3)
    assert ts[-1] == 1.0 and len(ts) == 5
    assert ts[-2] == pytest.approx(0.9)
    ts, ys = backward_euler(f, 0.0, 1.0, 0.5, 2.0)  # h larger than the interval
    assert ts == [0.0, 0.5] and ys[1] == pytest.approx(1 / 1.5)
    with pytest.raises(ValueError):
        backward_euler(f, 0.0, 1.0, 1.0, 0.0)


def test_solve_linear() -> None:
    x = solve_linear([[0.0, 2.0], [3.0, 1.0]], [4.0, 5.0])
    assert x == pytest.approx([1.0, 2.0])
