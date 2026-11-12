# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/svm-training/. The authors are listed in prov/WT03MH.jsonl.

import math
import random

from svm_training import (dual_coordinate_descent, dual_objective, kkt_violation, pegasos,
                          pegasos_objective, primal_objective)


def blobs(seed, n, spread, bias=True):
    rng = random.Random(seed)
    xs, ys = [], []
    for i in range(n):
        y = 1 if i % 2 == 0 else -1
        x = [y + rng.gauss(0, spread), y + rng.gauss(0, spread)]
        if bias:
            x.append(1.0)  # constant feature: a regularized bias, as in LIBLINEAR
        xs.append(x)
        ys.append(y)
    return xs, ys


def test_page_example_by_hand() -> None:
    xs = [(1.0, 0.0), (0.0, 1.0), (-1.0, -1.0)]
    ys = [1, 1, -1]
    w, alpha, epochs = dual_coordinate_descent(xs, ys, 1.0, shuffle=False, shrinking=False)
    assert w == [1.0, 1.0] and alpha == [1.0, 1.0, 0.0] and epochs == 2
    assert primal_objective(w, xs, ys, 1.0) == dual_objective(alpha, xs, ys, 1.0) == 1.0
    w, alpha, _ = dual_coordinate_descent(xs, ys, 0.1, shuffle=False, shrinking=False)
    assert all(abs(a - b) < 1e-12 for a, b in zip(w + alpha, [0.2, 0.2, 0.1, 0.1, 0.1]))
    assert abs(primal_objective(w, xs, ys, 0.1) - 0.26) < 1e-12
    assert abs(dual_objective(alpha, xs, ys, 0.1) - 0.26) < 1e-12


def test_dual_cd_meets_kkt_and_closes_the_gap() -> None:
    for seed in range(4):
        for spread in (0.5, 1.5):
            xs, ys = blobs(seed, 80, spread)
            for c in (0.01, 0.1, 1.0):
                for loss in ("l1", "l2"):
                    w, alpha, _ = dual_coordinate_descent(xs, ys, c, loss=loss, tol=1e-9)
                    if loss == "l1":
                        assert all(0.0 <= a <= c for a in alpha)
                    else:
                        assert all(a >= 0.0 for a in alpha)
                    # w is kept equal to sum_i a_i y_i x_i.
                    for k in range(3):
                        assert abs(w[k] - sum(a * y * x[k] for a, x, y in zip(alpha, xs, ys))) < 1e-8
                    assert kkt_violation(w, alpha, xs, ys, c, loss) < 1e-8
                    p = primal_objective(w, xs, ys, c, loss)
                    d = dual_objective(alpha, xs, ys, c, loss)
                    assert -1e-9 <= p - d <= 1e-6 * (1 + abs(p))


def test_large_c_needs_many_more_epochs() -> None:
    # Dual coordinate descent is fast for small and moderate C. On overlapping
    # classes with a large C it needs far more passes, and here it does not
    # reach the tolerance in 10000 passes.
    xs, ys = blobs(3, 80, 1.5)
    _, _, e_small = dual_coordinate_descent(xs, ys, 1.0, tol=1e-9)
    w, alpha, e_large = dual_coordinate_descent(xs, ys, 100.0, tol=1e-9, max_epochs=10000)
    assert e_small < 200 and e_large == 10000
    assert kkt_violation(w, alpha, xs, ys, 100.0) > 1e-3


def test_shrinking_gives_the_same_solution() -> None:
    xs, ys = blobs(11, 150, 1.2)
    w1, _, _ = dual_coordinate_descent(xs, ys, 1.0, shrinking=False, tol=1e-10)
    w2, a2, _ = dual_coordinate_descent(xs, ys, 1.0, shrinking=True, tol=1e-10)
    assert max(abs(a - b) for a, b in zip(w1, w2)) < 1e-7
    assert kkt_violation(w2, a2, xs, ys, 1.0) < 1e-9


def test_against_an_exact_one_dimensional_optimum() -> None:
    # In one dimension P(w) is convex, so ternary search finds the optimum.
    rng = random.Random(5)
    for _ in range(20):
        xs = [[rng.uniform(-3, 3)] for _ in range(12)]
        ys = [1 if x[0] + rng.gauss(0, 1) > 0 else -1 for x in xs]
        c = rng.choice([0.05, 0.5, 5.0])
        lo, hi = -100.0, 100.0
        for _ in range(300):
            m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
            if primal_objective([m1], xs, ys, c) <= primal_objective([m2], xs, ys, c):
                hi = m2
            else:
                lo = m1
        w, _, _ = dual_coordinate_descent(xs, ys, c, tol=1e-12)
        assert abs(w[0] - (lo + hi) / 2) < 1e-6


def test_pegasos_approaches_the_optimum() -> None:
    xs, ys = blobs(1, 200, 1.5)
    lam = 1.0 / len(xs)  # the same problem as C = 1/(lam n) = 1
    w, _, _ = dual_coordinate_descent(xs, ys, 1.0, tol=1e-10)
    best = pegasos_objective(w, xs, ys, lam)
    assert abs(best - primal_objective(w, xs, ys, 1.0) / len(xs)) < 1e-12
    gaps = []
    for t in (100, 3000, 60000):
        wp = pegasos(xs, ys, lam, t, seed=2)
        assert math.sqrt(sum(v * v for v in wp)) <= 1 / math.sqrt(lam) + 1e-9
        gaps.append(pegasos_objective(wp, xs, ys, lam) - best)
    assert all(g >= -1e-12 for g in gaps)
    assert gaps[2] < gaps[0] and gaps[2] < 0.01 * best
    # Mini-batches of k points per step reach the same accuracy.
    wk = pegasos(xs, ys, lam, 6000, k=10, seed=3)
    assert pegasos_objective(wk, xs, ys, lam) - best < 0.01 * best
