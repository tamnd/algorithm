# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lie-algebraic-rotation-averaging/. The authors are listed in prov/XFRXH0.jsonl.

import math
import random

import pytest

from cvla import mul, transpose
from lie_algebraic_rotation_averaging import (angle, cost, laplacian_system,
                                              lie_algebraic_rotation_averaging, residual,
                                              robust_rotation_averaging, so3_exp, so3_log,
                                              tree_init)


def random_rot(rng):
    w = [rng.gauss(0, 1) for _ in range(3)]
    n = math.sqrt(sum(x * x for x in w))
    return so3_exp([x / n * rng.uniform(0, math.pi) for x in w])


def make_problem(seed, n=12, p=0.5, noise=0.0, outliers=0.0):
    rng = random.Random(seed)
    rots = [random_rot(rng) for _ in range(n)]
    edges = [(k, k + 1) for k in range(n - 1)]
    edges += [(i, j) for i in range(n) for j in range(i + 2, n) if rng.random() < p]
    out = []
    for i, j in edges:
        rij = mul(rots[j], transpose(rots[i]))
        if rng.random() < outliers:
            rij = random_rot(rng)
        elif noise > 0:
            rij = mul(so3_exp([rng.gauss(0, noise) for _ in range(3)]), rij)
        out.append((i, j, rij))
    return rots, out


def relative_error(est, true):
    """The largest angle between R_j R_i^T of the estimate and of the truth."""
    worst = 0.0
    for i in range(len(true)):
        for j in range(i + 1, len(true)):
            a = mul(est[j], transpose(est[i]))
            b = mul(true[j], transpose(true[i]))
            worst = max(worst, angle(a, b))
    return worst


def test_exp_and_log_are_inverse():
    rng = random.Random(1)
    for _ in range(50):
        w = [rng.gauss(0, 1) for _ in range(3)]
        n = math.sqrt(sum(x * x for x in w))
        th = rng.uniform(0, math.pi - 1e-3)
        w = [x / n * th for x in w]
        assert max(abs(a - b) for a, b in zip(so3_log(so3_exp(w)), w)) < 1e-8
    w = [0.0, math.pi - 1e-6, 0.0]
    assert max(abs(a - b) for a, b in zip(so3_log(so3_exp(w)), w)) < 1e-5


def test_exact_data_is_recovered_up_to_the_gauge():
    true, edges = make_problem(2)
    est, it = lie_algebraic_rotation_averaging(len(true), edges)
    # acos near 1 limits the angle to about 1e-8
    assert relative_error(est, true) < 1e-7
    assert it <= 2


def test_gradient_is_minus_two_b():
    true, edges = make_problem(3, n=6, noise=0.2)
    rots = tree_init(6, edges)
    res = [residual(rots, e) for e in edges]
    _, b = laplacian_system(6, edges, res, [1.0] * len(edges))
    h = 1e-6
    for k in range(1, 6):
        for a in range(3):
            d = [0.0, 0.0, 0.0]
            d[a] = h
            plus = [mul(r, so3_exp(d)) if m == k else r for m, r in enumerate(rots)]
            d[a] = -h
            minus = [mul(r, so3_exp(d)) if m == k else r for m, r in enumerate(rots)]
            fd = (cost(plus, edges) - cost(minus, edges)) / (2 * h)
            assert abs(fd + 2 * b[k - 1][a]) < 1e-5


def test_l2_reaches_a_stationary_point_below_the_tree_start():
    true, edges = make_problem(4, n=15, noise=0.05)
    start = tree_init(15, edges)
    est, it = lie_algebraic_rotation_averaging(15, edges, max_iter=50, eps=1e-11)
    assert it < 50
    assert cost(est, edges) < cost(start, edges)
    res = [residual(est, e) for e in edges]
    _, b = laplacian_system(15, edges, res, [1.0] * len(edges))
    assert max(abs(x) for row in b for x in row) < 1e-9
    assert relative_error(est, true) < 0.15


def test_robust_cost_handles_outliers():
    true, edges = make_problem(5, n=15, p=0.6, noise=0.01, outliers=0.15)
    l2, _ = lie_algebraic_rotation_averaging(15, edges, max_iter=50)
    robust = robust_rotation_averaging(15, edges, sigma=0.05)
    assert relative_error(robust, true) < 0.1
    assert relative_error(l2, true) > 3 * relative_error(robust, true)


def test_disconnected_graph_is_rejected():
    _, edges = make_problem(6, n=5)
    with pytest.raises(ValueError):
        tree_init(7, edges)
