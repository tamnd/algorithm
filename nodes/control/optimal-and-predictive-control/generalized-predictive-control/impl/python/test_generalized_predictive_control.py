# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-predictive-control/. The authors are listed in prov/J9ZFD5.jsonl.

import random
from fractions import Fraction as Fr

import pytest

from generalized_predictive_control import GPC, diophantine, poly_mul

A_EX = [1, -0.8]
B_EX = [0, 0.2]  # y(t) = 0.8 y(t-1) + 0.2 u(t-2)


class Plant:
    """A(q^-1) y(t) = B(q^-1) u(t-1) + load(t), simulated directly."""

    def __init__(self, A, B):
        self.A, self.B = A, B
        self.y = [0.0] * len(A)  # y(t), y(t-1), ...
        self.u = [0.0] * (len(B) + 1)  # u(t), u(t-1), ...

    def output(self):
        return self.y[0]

    def advance(self, u, load=0.0):
        """Apply u(t) and return y(t+1)."""
        self.u = [u] + self.u[:-1]
        y = load - sum(a * yy for a, yy in zip(self.A[1:], self.y))
        y += sum(b * uu for b, uu in zip(self.B, self.u))  # B u(t) for y(t+1)
        self.y = [y] + self.y[:-1]
        return y


def run_gpc(ctrl, plant, ws, load=lambda t: 0.0):
    ys, us = [], []
    for t, w in enumerate(ws):
        u = ctrl.step(plant.output(), w)
        plant.advance(u, load(t + 1))
        ys.append(plant.output())
        us.append(u)
    return ys, us


def test_diophantine_identity_exact():
    rng = random.Random(41)
    for _ in range(10):
        A = [1] + [Fr(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(rng.randint(1, 3))]
        At = poly_mul(A, [1, -1])
        for j in range(1, 10):
            E, F = diophantine(At, j)
            assert len(E) == j and len(F) == len(A)
            lhs = poly_mul(E, At)
            for i, c in enumerate(F):
                lhs[j + i] += c
            assert lhs[0] == 1 and all(c == 0 for c in lhs[1:])
            assert sum(F) == 1  # F_j(1) = 1, because At(1) = 0


def test_example_diophantine_polynomials():
    At = poly_mul([1, Fr(-4, 5)], [1, -1])
    assert diophantine(At, 1) == ([1], [Fr(9, 5), Fr(-4, 5)])
    assert diophantine(At, 2) == ([1, Fr(9, 5)], [Fr(61, 25), Fr(-36, 25)])


def test_step_coefficients_of_the_example():
    ctrl = GPC(A_EX, B_EX, 1, 10, 2, 0.1)
    assert ctrl.g[0] == 0
    for i in range(1, 10):
        assert abs(ctrl.g[i] - (1 - 0.8 ** i)) < 1e-12


def test_prediction_is_exact_for_a_carima_plant():
    rng = random.Random(42)
    for _ in range(10):
        A = [1, rng.uniform(-1.2, 1.2), rng.uniform(-0.4, 0.4)]
        B = [0.0] * rng.randint(0, 2) + [rng.uniform(0.1, 1.0), rng.uniform(-0.5, 0.5)]
        N1, N2, Nu = 1, 8, 3
        ctrl2 = GPC(A, B, N1, N2, Nu, 0.5)
        plant2 = Plant(A, B)
        for t in range(12):  # random setpoints; a load step is an integrated disturbance
            ctrl2.step(plant2.output(), rng.uniform(-1, 1))
            plant2.advance(ctrl2.u, 0.7 if t >= 3 else 0.0)
        ctrl2.step(plant2.output(), 0.0)
        du0 = ctrl2.dus[0]
        future = [du0] + [rng.uniform(-1, 1) for _ in range(Nu - 1)]
        pred = ctrl2.predict(future)
        u = ctrl2.u
        ys = []
        for i in range(N2):
            if 0 < i < Nu:
                u += future[i]
            ys.append(plant2.advance(u, 0.7))
        for j in range(N1, N2 + 1):
            assert abs(pred[j - N1] - ys[j - 1]) < 1e-9


def test_rst_form_gives_the_same_inputs():
    rng = random.Random(43)
    ctrl = GPC(A_EX, B_EX, 1, 10, 2, 0.1)
    R, S, T = ctrl.rst()
    assert abs(sum(S) - T) < 1e-12  # S(1) = T: unit steady-state gain
    ws = [rng.uniform(-1, 1) for _ in range(30)]
    loads = [rng.uniform(-0.2, 0.2) for _ in range(31)]
    _, u_gpc = run_gpc(ctrl, Plant(A_EX, B_EX), ws, lambda t: loads[t])
    plant = Plant(A_EX, B_EX)
    ys, dus, u = [0.0] * len(S), [0.0] * (len(R) - 1), 0.0
    for t, w in enumerate(ws):
        ys = [plant.output()] + ys[:-1]
        du = T * w - sum(s * y for s, y in zip(S, ys)) - sum(r * d for r, d in zip(R[1:], dus))
        dus = [du] + dus[:-1]
        u += du
        assert abs(u - u_gpc[t]) < 1e-9
        plant.advance(u, loads[t + 1])


def test_closed_loop_polynomial_of_the_example():
    ctrl = GPC(A_EX, B_EX, 1, 10, 2, 0.1)
    pc = ctrl.closed_loop_polynomial()
    assert len(pc) == 4 and abs(pc[3]) < 1e-12
    # z^3 Pc = z (z^2 + p1 z + p2): a complex pair of modulus sqrt(p2)
    assert pc[1] ** 2 - 4 * pc[2] < 0
    assert abs(pc[2] ** 0.5 - 0.5218) < 5e-5
    # the simulated output satisfies Pc(q^-1) y(t) = q^-1 B T w for a constant w
    _, _, T = ctrl.rst()
    ys, _ = run_gpc(ctrl, Plant(A_EX, B_EX), [1.0] * 30)
    for t in range(5, 30):
        lhs = sum(p * ys[t - i] for i, p in enumerate(pc))
        assert abs(lhs - sum(B_EX) * T) < 1e-9


def test_example_closed_loop_and_offset():
    ctrl = GPC(A_EX, B_EX, 1, 10, 2, 0.1)
    assert abs(sum(ctrl.K) - 1.8422) < 5e-5
    ys, _ = run_gpc(ctrl, Plant(A_EX, B_EX), [1.0] * 60, lambda t: 0.3 if t >= 25 else 0.0)
    assert ys[0] == 0.0 and abs(ys[1] - 0.3684) < 5e-5 and abs(ys[2] - 0.7015) < 5e-5
    assert abs(ys[-1] - 1.0) < 1e-6


def test_no_offset_with_model_error():
    for b in (0.12, 0.3):
        ctrl = GPC(A_EX, B_EX, 1, 10, 2, 0.1)
        ys, _ = run_gpc(ctrl, Plant([1, -0.85], [0, b]), [1.0] * 150, lambda t: 0.2 if t >= 50 else 0.0)
        assert abs(ys[-1] - 1.0) < 1e-6


def test_one_step_horizon_after_the_delay_puts_all_poles_at_zero():
    ctrl = GPC([1, Fr(-4, 5)], [0, Fr(1, 5)], 2, 2, 1, 0)
    assert ctrl.closed_loop_polynomial() == [1, 0, 0, 0]


def test_input_checks():
    with pytest.raises(ValueError):
        GPC([2, -0.8], B_EX, 1, 5, 1, 0.1)
