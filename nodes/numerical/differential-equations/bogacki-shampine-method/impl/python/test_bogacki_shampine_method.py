# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bogacki-shampine-method/. The authors are listed in prov/34RG05.jsonl.

import math
from fractions import Fraction as Fr

import pytest

from bogacki_shampine_method import A, B, BHAT, C, bogacki_shampine, bs23_step

f_ex = lambda t, y: -2 * t * y * y
y_ex = lambda t: 1 / (1 + t * t)


def _conds(b):
    s = 4
    Ac = [sum(A[i][j] * C[j] for j in range(s)) for i in range(s)]
    return [sum(b), sum(b[i] * C[i] for i in range(s)), sum(b[i] * C[i] ** 2 for i in range(s)),
            sum(b[i] * Ac[i] for i in range(s)), sum(b[i] * C[i] ** 3 for i in range(s))]


def test_order_conditions_exact() -> None:
    assert all(C[i] == sum(A[i]) for i in range(4))
    cb = _conds(B)
    assert cb[:4] == [1, Fr(1, 2), Fr(1, 3), Fr(1, 6)] and cb[4] != Fr(1, 4)
    ch = _conds(BHAT)
    assert ch[:2] == [1, Fr(1, 2)] and ch[2] != Fr(1, 3)
    assert A[3] == B  # FSAL: the last stage is f at the new solution


def test_stability_function_of_order3_solution() -> None:
    # Explicit 3 stages used by b with order 3, so R(z) = 1 + z + z^2/2 + z^3/6.
    for z in (-1.0, -2.5, 0.5 + 1.0j):
        y1, _, _ = bs23_step(lambda t, y: [z * y[0]], 0.0, [1.0], 1.0, [z])
        assert abs(y1[0] - (1 + z + z * z / 2 + z ** 3 / 6)) < 1e-14
    r = lambda x: 1 + x + x * x / 2 + x ** 3 / 6
    assert abs(r(-2.5127) + 1) < 1e-3 and abs(r(-2.4)) < 1 and abs(r(-2.6)) > 1


def test_fixed_step_order_three() -> None:
    fv = lambda t, y: [f_ex(t, y[0])]

    def run(n):
        h, y, k1 = 2.0 / n, [1.0], [0.0]
        for i in range(n):
            y, k1, _ = bs23_step(fv, i * h, y, h, k1)
        return abs(y[0] - y_ex(2.0))

    errs = [run(n) for n in (40, 80, 160)]
    assert all(abs(math.log2(errs[i] / errs[i + 1]) - 3) < 0.15 for i in range(2))


def test_error_estimate_is_order_three_locally() -> None:
    fv = lambda t, y: [f_ex(t, y[0])]
    est = [abs(bs23_step(fv, 0.5, [y_ex(0.5)], h, fv(0.5, [y_ex(0.5)]))[2][0]) for h in (0.04, 0.02)]
    assert abs(math.log2(est[0] / est[1]) - 3) < 0.2


def test_worked_example() -> None:
    y1, k4, e = bs23_step(lambda t, y: [f_ex(t, y[0])], 0.0, [1.0], 0.5, [0.0])
    assert y1[0] == 0.806640625
    assert abs(e[0] + 0.0076730) < 1e-7


def test_adaptive_tolerance_proportionality_and_fsal() -> None:
    errs, steps = [], []
    for tol in (1e-4, 1e-6):
        ts, ys, st = bogacki_shampine(f_ex, 0.0, 1.0, 2.0, rtol=tol, atol=tol)
        assert ts[-1] == 2.0
        errs.append(max(abs(y - y_ex(t)) for t, y in zip(ts, ys)))
        steps.append(st["accepted"])
        assert st["evaluations"] == 1 + 3 * (st["accepted"] + st["rejected"])
    assert 30 < errs[0] / errs[1] < 300  # global error roughly proportional to tol
    assert 3 < steps[1] / steps[0] < 6  # steps grow like tol^(-1/3)


def test_vector_oscillator() -> None:
    ts, ys, _ = bogacki_shampine(lambda t, y: [y[1], -y[0]], 0.0, [1.0, 0.0], 2 * math.pi, rtol=1e-8, atol=1e-10)
    assert abs(ys[-1][0] - 1) < 1e-6 and abs(ys[-1][1]) < 1e-6


def test_stiff_problem_needs_many_steps() -> None:
    f = lambda t, y: -1000.0 * (y - math.cos(t)) - math.sin(t)
    ts, ys, st = bogacki_shampine(f, 0.0, 1.0, 1.0, rtol=1e-3, atol=1e-6)
    assert abs(ys[-1] - math.cos(1.0)) < 1e-2
    assert st["accepted"] > 350  # stability bounds h by about 2.51/1000, so about 398 steps


def test_edges() -> None:
    assert bogacki_shampine(lambda t, y: y, 1.0, 2.0, 1.0)[:2] == ([1.0], [2.0])
    ts, ys, st = bogacki_shampine(lambda t, y: 1.0, 0.0, 0.0, 0.3, h0=10.0)
    assert ts == [0.0, 0.3] and abs(ys[-1] - 0.3) < 1e-15
    ts, _, _ = bogacki_shampine(lambda t, y: math.cos(t), 0.0, 0.0, 1.0, h_max=0.3)
    assert ts[-1] == 1.0 and all(b - a <= 0.3 + 1e-15 for a, b in zip(ts, ts[1:]))
    with pytest.raises(ValueError):
        bogacki_shampine(lambda t, y: y, 1.0, 1.0, 0.0)
    with pytest.raises(ArithmeticError):
        bogacki_shampine(lambda t, y: -1e6 * y, 0.0, 1.0, 1.0, max_steps=50)


def test_linear_invariant_is_conserved() -> None:
    f = lambda t, y: [-y[0] * y[1], y[0] * y[1] - 0.5 * y[1], 0.5 * y[1]]  # SIR model: the sum is constant
    _, ys, _ = bogacki_shampine(f, 0.0, [0.99, 0.01, 0.0], 30.0, rtol=1e-5, atol=1e-8)
    assert all(abs(sum(y) - 1.0) < 1e-13 for y in ys)
