# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blendshape-direct-manipulation/. The authors are listed in prov/RFBXKQ.jsonl.
"""Tests of direct manipulation of blendshapes.

The free solution has a zero gradient and beats random perturbations. The
bounded solution equals a brute force over all active sets of the box and
meets the KKT conditions. A large alpha keeps the current weights, and with
a tiny alpha a reachable goal is met. The check value of the page holds.
"""

import itertools
import random

import anim
from blendshape_direct_manipulation import (
    box_qp,
    constraint_rows,
    energy,
    evaluate,
    manipulate,
    normal_system,
)


def make_rig(rng, n=8, k=4):
    b0 = [tuple(rng.uniform(-1, 1) for _ in range(3)) for _ in range(n)]
    deltas = []
    for _ in range(k):
        d = [(0.0, 0.0, 0.0)] * n
        for i in rng.sample(range(n), 4):
            d[i] = tuple(rng.uniform(-0.5, 0.5) for _ in range(3))
        deltas.append(d)
    return b0, deltas


def goals_for(rng, b0, n_goals=2):
    idx = rng.sample(range(len(b0)), n_goals)
    return {i: tuple(x + rng.uniform(-0.4, 0.4) for x in b0[i]) for i in idx}


def brute_box(a, c, lo, hi):
    """Exact minimizer by trying every split of the variables into free, low and high."""
    k = len(c)
    best, best_val = None, float("inf")
    for state in itertools.product((0, 1, 2), repeat=k):
        free = [i for i in range(k) if state[i] == 0]
        w = [lo if s == 1 else hi if s == 2 else 0.0 for s in state]
        if free:
            sub = [[a[i][j] for j in free] for i in free]
            rhs = [c[i] - sum(a[i][j] * w[j] for j in range(k) if state[j] != 0) for i in free]
            x = anim.solve(sub, rhs)
            if any(v < lo - 1e-12 or v > hi + 1e-12 for v in x):
                continue
            for i, v in zip(free, x):
                w[i] = v
        val = 0.5 * sum(w[i] * a[i][j] * w[j] for i in range(k) for j in range(k)) - sum(
            ci * wi for ci, wi in zip(c, w)
        )
        if val < best_val:
            best, best_val = w, val
    return best


def test_free_solution_has_zero_gradient():
    rng = random.Random(1)
    b0, deltas = make_rig(rng)
    goals = goals_for(rng, b0)
    w0 = [rng.uniform(0, 1) for _ in deltas]
    w = manipulate(deltas, b0, goals, w0)
    s, m = constraint_rows(deltas, b0, goals)
    g = anim.num_grad(lambda x: energy(s, m, x, w0, 0.1, 0.001), w)
    assert max(abs(x) for x in g) < 1e-7


def test_free_solution_beats_perturbations():
    rng = random.Random(2)
    b0, deltas = make_rig(rng)
    goals = goals_for(rng, b0, 3)
    w0 = [rng.uniform(0, 1) for _ in deltas]
    w = manipulate(deltas, b0, goals, w0)
    s, m = constraint_rows(deltas, b0, goals)
    e = energy(s, m, w, w0, 0.1, 0.001)
    for _ in range(200):
        wp = [x + rng.gauss(0, 0.05) for x in w]
        assert energy(s, m, wp, w0, 0.1, 0.001) >= e


def test_bounded_solution_equals_brute_force():
    rng = random.Random(3)
    for _ in range(15):
        b0, deltas = make_rig(rng)
        goals = {i: tuple(x + rng.uniform(-1.5, 1.5) for x in b0[i]) for i in rng.sample(range(8), 2)}
        w0 = [rng.uniform(0, 1) for _ in deltas]
        w = manipulate(deltas, b0, goals, w0, bound=1.0)
        s, m = constraint_rows(deltas, b0, goals)
        a, c = normal_system(s, m, w0, 0.1, 0.001)
        ref = brute_box(a, c, 0.0, 1.0)
        assert max(abs(x - y) for x, y in zip(w, ref)) < 1e-9


def test_bounded_solution_meets_kkt():
    rng = random.Random(4)
    b0, deltas = make_rig(rng, k=5)
    goals = {i: tuple(x + rng.uniform(-2, 2) for x in b0[i]) for i in range(3)}
    w0 = [0.5] * 5
    w = manipulate(deltas, b0, goals, w0, bound=1.0)
    s, m = constraint_rows(deltas, b0, goals)
    a, c = normal_system(s, m, w0, 0.1, 0.001)
    grad = [sum(a[k][l] * w[l] for l in range(5)) - c[k] for k in range(5)]
    for wk, gk in zip(w, grad):
        assert -1e-12 <= wk <= 1.0 + 1e-12
        if 1e-9 < wk < 1.0 - 1e-9:
            assert abs(gk) < 1e-9
        elif wk <= 1e-9:
            assert gk >= -1e-9
        else:
            assert gk <= 1e-9


def test_large_alpha_keeps_current_weights():
    rng = random.Random(5)
    b0, deltas = make_rig(rng)
    goals = goals_for(rng, b0)
    w0 = [0.2, 0.4, 0.6, 0.8]
    w = manipulate(deltas, b0, goals, w0, alpha=1e9, mu=0.0)
    assert max(abs(x - y) for x, y in zip(w, w0)) < 1e-6


def test_reachable_goal_is_met_with_tiny_alpha():
    rng = random.Random(6)
    b0, deltas = make_rig(rng, n=6, k=6)
    w_true = [rng.uniform(0, 1) for _ in deltas]
    v_true = evaluate(deltas, b0, w_true)
    goals = {1: v_true[1], 3: v_true[3]}
    w = manipulate(deltas, b0, goals, [0.0] * 6, alpha=1e-10, mu=0.0)
    v = evaluate(deltas, b0, w)
    for i, p in goals.items():
        assert max(abs(x - y) for x, y in zip(v[i], p)) < 1e-6


def test_projected_gauss_seidel_on_a_known_box_qp():
    a = [[2.0, 0.0], [0.0, 2.0]]
    c = [4.0, -2.0]
    assert box_qp(a, c, 0.0, 1.0, [0.5, 0.5]) == [1.0, 0.0]


def test_check_value_of_the_page():
    b0 = [(0.0, 0.0, 0.0)]
    deltas = [[(1.0, 0.0, 0.0)], [(1.0, 1.0, 0.0)]]
    w = manipulate(deltas, b0, {0: (1.0, 0.5, 0.0)}, [0.0, 0.0], alpha=0.1, mu=0.0)
    assert abs(w[0] - 0.6 / 1.31) < 1e-12
    assert abs(w[1] - 0.65 / 1.31) < 1e-12
    wf = manipulate(deltas, b0, {0: (2.0, 1.5, 0.0)}, [0.0, 0.0], alpha=0.1, mu=0.0)
    assert abs(wf[1] - 1.85 / 1.31) < 1e-12
    wb = manipulate(deltas, b0, {0: (2.0, 1.5, 0.0)}, [0.0, 0.0], alpha=0.1, mu=0.0, bound=1.0)
    assert abs(wb[0] - 1.0 / 1.1) < 1e-12
    assert abs(wb[1] - 1.0) < 1e-12
