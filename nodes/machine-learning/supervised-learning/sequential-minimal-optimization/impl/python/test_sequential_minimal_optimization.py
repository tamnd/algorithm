# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-minimal-optimization/. The authors are listed in prov/9XT69N.jsonl.

import math
import random

from sequential_minimal_optimization import (
    SMO,
    decision_values,
    dual_objective,
    exact_svm_dual,
    kkt_violation,
    smo,
)


def linear_gram(xs):
    return [[sum(a * b for a, b in zip(p, q)) for q in xs] for p in xs]


def gauss_gram(xs, s=1.0):
    return [[math.exp(-sum((a - b) ** 2 for a, b in zip(p, q)) / (2 * s * s)) for q in xs] for p in xs]


def blobs(seed, n, spread):
    rng = random.Random(seed)
    xs, ys = [], []
    for i in range(n):
        y = 1 if i % 2 == 0 else -1
        xs.append((y + rng.gauss(0, spread), y + rng.gauss(0, spread)))
        ys.append(y)
    return xs, ys


def test_kkt_conditions_hold_within_tolerance() -> None:
    for seed in range(6):
        for spread in (0.5, 1.5):
            xs, ys = blobs(seed, 30, spread)
            for gram in (linear_gram(xs), gauss_gram(xs)):
                for c in (0.1, 1.0, 10.0):
                    alpha, b = smo(gram, ys, c, tol=1e-3, rng=random.Random(seed))
                    assert all(0 <= a <= c for a in alpha)
                    assert abs(sum(a * y for a, y in zip(alpha, ys))) < 1e-9
                    assert kkt_violation(gram, ys, alpha, b, c) <= 1e-3 + 1e-9


def test_a_coarse_step_threshold_can_stop_early() -> None:
    xs, ys = blobs(3, 30, 1.5)
    gram = linear_gram(xs)
    coarse = SMO(gram, ys, 10.0, tol=1e-3, eps=1e-3, rng=random.Random(3))
    a, b = coarse.run()
    assert kkt_violation(gram, ys, a, b, 10.0) > 0.05
    fine = SMO(gram, ys, 10.0, tol=1e-3, eps=1e-8, rng=random.Random(3))
    a, b = fine.run()
    assert kkt_violation(gram, ys, a, b, 10.0) <= 1e-3 + 1e-9


def test_matches_the_exact_qp_on_a_tiny_problem() -> None:
    xs = [(2, 2), (1, 3), (3, 1), (0, 0), (1, 0), (2, 3)]
    ys = [1, 1, 1, -1, -1, -1]  # (2, 3) is a negative point inside the positive group
    gram = linear_gram(xs)
    for c in (1, 2):
        exact = exact_svm_dual(gram, ys, c)
        assert exact is not None
        ea, eb = exact
        alpha, b = smo(gram, ys, float(c), tol=1e-7, eps=1e-10, rng=random.Random(1))
        assert abs(dual_objective(gram, ys, alpha) - float(dual_objective(gram, ys, ea))) < 1e-6
        f_exact = decision_values(gram, ys, ea, eb)
        f_smo = decision_values(gram, ys, alpha, b)
        assert all(abs(float(u) - v) < 1e-5 for u, v in zip(f_exact, f_smo))
        w_exact = [sum(ea[i] * ys[i] * xs[i][t] for i in range(6)) for t in range(2)]
        w_smo = [sum(alpha[i] * ys[i] * xs[i][t] for i in range(6)) for t in range(2)]
        assert all(abs(float(u) - v) < 1e-5 for u, v in zip(w_exact, w_smo))


def test_exact_solver_satisfies_kkt_exactly() -> None:
    xs = [(2, 2), (1, 3), (3, 1), (0, 0), (1, 0), (2, 3)]
    ys = [1, 1, 1, -1, -1, -1]
    gram = linear_gram(xs)
    alpha, b = exact_svm_dual(gram, ys, 1)
    assert kkt_violation(gram, ys, alpha, b, 1) == 0


def test_separable_data_with_large_c_gives_the_maximum_margin() -> None:
    xs = [(2, 0), (0, 2), (3, 3), (-1, 0), (0, -1), (-2, -2)]
    ys = [1, 1, 1, -1, -1, -1]
    gram = linear_gram(xs)
    alpha, b = smo(gram, ys, 1e6, tol=1e-8, eps=1e-12)
    w = [sum(alpha[i] * ys[i] * xs[i][t] for i in range(6)) for t in range(2)]
    # The closest pairs are (2,0)/(0,2) against (-1,0)/(0,-1): w = (2/3, 2/3), b = -1/3.
    assert abs(w[0] - 2 / 3) < 1e-6 and abs(w[1] - 2 / 3) < 1e-6 and abs(b + 1 / 3) < 1e-6
    margin = 2 / math.hypot(*w)
    assert abs(margin - 3 / math.sqrt(2)) < 1e-6


def test_negative_eta_branch_with_an_indefinite_matrix() -> None:
    # Two identical points with opposite labels give eta = 0; the step must not divide by 0.
    gram = linear_gram([(1, 1), (1, 1), (2, 0), (-2, 0)])
    ys = [1, -1, 1, -1]
    s = SMO(gram, ys, 1.0, tol=1e-6)
    alpha, b = s.run()
    assert all(0 <= a <= 1 for a in alpha)
    assert kkt_violation(gram, ys, alpha, b, 1.0) < 1e-5


def test_heuristics_take_fewer_steps_than_n_squared() -> None:
    xs, ys = blobs(42, 60, 1.0)
    s = SMO(gauss_gram(xs), ys, 1.0, rng=random.Random(42))
    s.run()
    assert 0 < s.steps < 60 * 60
