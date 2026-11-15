# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-matrix-control/. The authors are listed in prov/078WY3.jsonl.

import random

import pytest

from dynamic_matrix_control import DMC, dmc_gain, dynamic_matrix, step_response


def make_plant(a=0.8, b=0.2):
    """y(k+1) = a y(k) + b u(k-1): a first order lag with one extra sample of delay."""
    st = {"y": 0.0, "u1": 0.0}

    def plant(u):
        st["y"], st["u1"] = a * st["y"] + b * st["u1"], u
        return st["y"]
    return plant


S30 = step_response(make_plant(), 30)


def run(ctrl, plant, refs, dist=lambda k: 0.0):
    y, ys, us = 0.0, [], []
    for k, r in enumerate(refs):
        u = ctrl.step(y + dist(k), r)
        y = plant(u)
        ys.append(y + dist(k + 1))
        us.append(u)
    return ys, us


def test_step_response_of_the_example_plant():
    for i, si in enumerate(S30, start=1):
        assert abs(si - (1 - 0.8 ** (i - 1))) < 1e-12


def test_dynamic_matrix_is_lower_triangular_toeplitz():
    s = [0.1 * i for i in range(1, 8)]
    S = dynamic_matrix(s, 5, 3)
    for i in range(5):
        for j in range(3):
            assert S[i][j] == (s[i - j] if i >= j else 0.0)


def test_gain_solves_the_least_squares_problem():
    rng = random.Random(31)
    P, M, lam = 10, 3, 0.4
    S = dynamic_matrix(S30, P, M)
    Kall = dmc_gain(S30, P, M, lam)
    for _ in range(20):
        e = [rng.uniform(-1, 1) for _ in range(P)]
        du = [sum(Kall[a][i] * e[i] for i in range(P)) for a in range(M)]
        res = [sum(S[i][j] * du[j] for j in range(M)) - e[i] for i in range(P)]
        grad = [sum(S[i][a] * res[i] for i in range(P)) + lam * du[a] for a in range(M)]
        assert max(abs(g) for g in grad) < 1e-12
        cost = sum(v * v for v in res) + lam * sum(v * v for v in du)
        for _ in range(10):  # any other move sequence costs more
            other = [v + rng.uniform(-0.1, 0.1) for v in du]
            r2 = [sum(S[i][j] * other[j] for j in range(M)) - e[i] for i in range(P)]
            assert sum(v * v for v in r2) + lam * sum(v * v for v in other) >= cost - 1e-12


def test_prediction_is_exact_for_a_step_model_plant():
    rng = random.Random(32)
    s = S30[:12]
    Ns = len(s)

    def fir_output(moves, k):  # y(k) = sum_(j>=1) s_min(j, Ns) du(k - j)
        return sum(s[min(k - i, Ns) - 1] * moves[i] for i in range(k)) + 0.4  # constant output offset

    ctrl = DMC(s, 8, 3, 0.2)
    moves = []
    for k in range(15):  # closed loop for a while with random setpoints
        u_before = ctrl.u
        ctrl.step(fir_output(moves, k), rng.uniform(-1, 1))
        moves.append(ctrl.u - u_before)
    k = len(moves)
    future = [rng.uniform(-1, 1) for _ in range(3)]
    pred = ctrl.predict(fir_output(moves, k), future)
    allm = moves + future + [0.0] * 8
    for i in range(1, 9):
        assert abs(pred[i - 1] - fir_output(allm, k + i)) < 1e-12


def test_example_closed_loop():
    ctrl = DMC(S30, 10, 2, 0.1)
    assert ctrl.K[0] == 0.0  # s_1 = 0: the first output cannot move
    assert abs(sum(ctrl.K) - 1.8422) < 5e-5
    ys, us = run(ctrl, make_plant(), [1.0] * 40)
    assert abs(us[0] - sum(ctrl.K)) < 1e-12
    assert ys[0] == 0.0 and abs(ys[1] - 0.2 * us[0]) < 1e-12
    assert abs(ys[-1] - 1.0) < 1e-4


def test_no_offset_with_model_error_and_output_disturbance():
    for b in (0.14, 0.2, 0.26):  # plant gain 0.7, 1 and 1.3 against a model gain of 1
        ctrl = DMC(S30, 10, 2, 0.1)
        ys, us = run(ctrl, make_plant(0.8, b), [1.0] * 120, dist=lambda k: 0.5 if k >= 40 else 0.0)
        assert abs(ys[-1] - 1.0) < 1e-6
        assert abs(us[-1] - 0.5 * 0.2 / b) < 1e-5  # u = (r - d) / plant gain


def test_unconstrained_dmc_is_linear():
    rng = random.Random(33)
    r1 = [rng.uniform(-1, 1) for _ in range(30)]
    r2 = [rng.uniform(-1, 1) for _ in range(30)]
    y1, _ = run(DMC(S30, 10, 2, 0.1), make_plant(), r1)
    y2, _ = run(DMC(S30, 10, 2, 0.1), make_plant(), r2)
    y3, _ = run(DMC(S30, 10, 2, 0.1), make_plant(), [2 * a - 3 * b for a, b in zip(r1, r2)])
    assert max(abs(c - (2 * a - 3 * b)) for a, b, c in zip(y1, y2, y3)) < 1e-12


def test_larger_move_weight_gives_smaller_first_move():
    first = [sum(DMC(S30, 10, 2, lam).K) for lam in (0.0, 0.1, 1.0, 10.0)]
    assert all(a > b for a, b in zip(first, first[1:]))


def test_model_shorter_than_horizon_is_rejected():
    with pytest.raises(ValueError):
        DMC(S30[:5], 10, 2, 0.1)
