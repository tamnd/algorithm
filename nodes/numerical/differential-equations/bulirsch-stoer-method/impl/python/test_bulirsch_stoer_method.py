# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bulirsch-stoer-method/. The authors are listed in prov/FA09JN.jsonl.

import math
from fractions import Fraction as Fr

import pytest

from bulirsch_stoer_method import bs_step, bulirsch_stoer, extrapolate, modified_midpoint

f_ex = lambda t, y: [-2 * t * y[0] ** 2]
y_ex = lambda t: 1 / (1 + t * t)


def test_extrapolation_is_exact_on_polynomials_in_h2() -> None:
    # T(h) = 3 + 5 h^2 - 7 h^4 + 2 h^6 sampled at h = 1/n_j is extrapolated to T(0) = 3 exactly.
    ns = [2, 4, 6, 8]
    rows = []
    for n in ns:
        h = Fr(1, n)
        rows.append([[3 + 5 * h ** 2 - 7 * h ** 4 + 2 * h ** 6]])
        extrapolate(rows, [Fr(m) for m in ns])
    assert rows[3][3][0] == 3 and rows[2][2][0] != 3


def test_hand_example() -> None:
    assert modified_midpoint(lambda t, y: [y[0]], 0.0, [1.0], [1.0], 1.0, 2) == [2.5]
    assert modified_midpoint(lambda t, y: [y[0]], 0.0, [1.0], [1.0], 1.0, 4) == [2.65625]
    y, e = bs_step(lambda t, y: [y[0]], 0.0, [1.0], 1.0, 2)
    assert abs(y[0] - 65 / 24) < 1e-15 and abs(e[0] - 5 / 96) < 1e-15


@pytest.mark.parametrize("k", [2, 3, 4])
def test_stability_function_is_taylor_polynomial(k) -> None:
    for z in (-1.0, -2.5, 0.5 + 1.5j):
        y, _ = bs_step(lambda t, y: [z * y[0]], 0.0, [1.0], 1.0, k)
        taylor = sum(z ** q / math.factorial(q) for q in range(2 * k + 1))
        assert abs(y[0] - taylor) < 1e-13


@pytest.mark.parametrize("k,p", [(1, 2), (2, 4), (3, 6)])
def test_fixed_step_order_2k(k, p) -> None:
    def run(n):
        big_h, y = 2.0 / n, [1.0]
        for i in range(n):
            y, _ = bs_step(f_ex, i * big_h, y, big_h, k)
        return abs(y[0] - y_ex(2.0))

    e = [run(n) for n in (8, 16, 32)]
    assert abs(math.log2(e[1] / e[2]) - p) < 0.25


def test_adaptive_tolerance_and_cost() -> None:
    errs = []
    for tol in (1e-6, 1e-10):
        ts, ys, st = bulirsch_stoer(lambda t, y: -2 * t * y * y, 0.0, 1.0, 2.0, rtol=tol, atol=tol)
        assert ts[-1] == 2.0
        errs.append(max(abs(y - y_ex(t)) for t, y in zip(ts, ys)))
        assert st["evaluations"] == 17 * (st["accepted"] + st["rejected"])  # k^2 + 1 with k = 4
    assert errs[0] < 1e-5 and errs[1] < 1e-9


def test_vector_oscillator_and_invariant() -> None:
    ts, ys, _ = bulirsch_stoer(lambda t, y: [y[1], -y[0]], 0.0, [1.0, 0.0], 2 * math.pi, rtol=1e-11, atol=1e-12)
    assert abs(ys[-1][0] - 1) < 1e-9 and abs(ys[-1][1]) < 1e-9
    f = lambda t, y: [-y[0] * y[1], y[0] * y[1] - 0.5 * y[1], 0.5 * y[1]]
    _, ys, _ = bulirsch_stoer(f, 0.0, [0.99, 0.01, 0.0], 30.0, rtol=1e-8)
    assert all(abs(sum(y) - 1.0) < 1e-13 for y in ys)


def test_stiff_problem_needs_many_steps() -> None:
    g = lambda t, y: -1000.0 * (y - math.cos(t)) - math.sin(t)
    ts, ys, st = bulirsch_stoer(g, 0.0, 1.0, 1.0, rtol=1e-3, atol=1e-6)
    assert abs(ys[-1] - math.cos(1.0)) < 1e-2
    assert st["accepted"] > 200 and st["evaluations"] > 3000


def test_edges() -> None:
    assert bulirsch_stoer(lambda t, y: y, 1.0, 2.0, 1.0)[:2] == ([1.0], [2.0])
    ts, ys, _ = bulirsch_stoer(lambda t, y: 3 * t * t, 0.0, 0.0, 0.5, h0=10.0)  # H larger than the interval
    assert ts == [0.0, 0.5] and abs(ys[-1] - 0.125) < 1e-15
    ts, ys, _ = bulirsch_stoer(lambda t, y: math.cos(t), 0.0, 0.0, 1.0, h0=0.3)  # last step off the grid
    assert ts[-1] == 1.0 and abs(ys[-1] - math.sin(1.0)) < 1e-9
    with pytest.raises(ValueError):
        bulirsch_stoer(lambda t, y: y, 0.0, 1.0, 1.0, k=1)
    with pytest.raises(ArithmeticError):
        bulirsch_stoer(lambda t, y: -1e6 * y, 0.0, 1.0, 1.0, max_steps=20)
