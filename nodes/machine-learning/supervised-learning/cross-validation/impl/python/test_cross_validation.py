# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cross-validation/. The authors are listed in prov/1RKJ3F.jsonl.

import random
from fractions import Fraction as F

from cross_validation import (cv_estimate, fit_ridge, kfold, leave_one_out, leverages,
                              loo_residuals_refit, loo_residuals_shortcut, nested_cv,
                              predict_linear, stratified_kfold)


def assert_partition(folds: list[list[int]], n: int) -> None:
    seen = [i for f in folds for i in f]
    assert sorted(seen) == list(range(n))  # every index once: disjoint and covering
    sizes = [len(f) for f in folds]
    assert max(sizes) - min(sizes) <= 1


def test_folds_partition_the_data() -> None:
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(2, 40)
        k = rng.randint(2, n)
        assert_partition(kfold(n, k, rng), n)
        labels = [rng.randrange(3) for _ in range(n)]
        folds = stratified_kfold(labels, k, rng)
        assert_partition(folds, n)
        for c in set(labels):
            per = [sum(1 for i in f if labels[i] == c) for f in folds]
            assert max(per) - min(per) <= 1
        assert_partition(leave_one_out(n), n)


def test_loo_shortcut_equals_refits_exactly() -> None:
    rng = random.Random(2)
    checked = 0
    for _ in range(200):
        n, d = rng.randint(4, 8), rng.randint(1, 3)
        X = [[F(1)] + [F(rng.randint(-5, 5)) for _ in range(d - 1)] for _ in range(n)]
        y = [F(rng.randint(-9, 9)) for _ in range(n)]
        for lam in (F(0), F(1, 2), F(3)):
            try:
                refit = loo_residuals_refit(X, y, lam)
                h = leverages(X, lam)
            except ZeroDivisionError:
                continue  # a design that loses rank without one row
            assert all(hi < 1 for hi in h)
            assert loo_residuals_shortcut(X, y, lam) == refit
            checked += 1
    assert checked > 300


def test_trace_of_hat_matrix_is_the_rank() -> None:
    X = [[F(1), F(t)] for t in (0, 1, 2, 4)]
    assert sum(leverages(X)) == 2


def test_cv_estimate_mean_predictor_loo() -> None:
    y = [F(v) for v in (1, 2, 3, 10)]
    X = [[F(1)] for _ in y]
    est = cv_estimate(fit_ridge, predict_linear, lambda t, p: (t - p) ** 2, X, y, leave_one_out(4))
    # LOO residual of the mean is (y_i - mean) * n / (n - 1); mean 4, deviations -3, -2, -1, 6
    assert est == sum((F(4, 3) * e) ** 2 for e in (-3, -2, -1, 6)) / 4


def nearest_label(train_x: list, train_y: list, x: list) -> int:
    best = min(range(len(train_x)), key=lambda i: sum((a - b) ** 2 for a, b in zip(train_x[i], x)))
    return train_y[best]


def top_features(X: list, y: list, m: int) -> list[int]:
    n = len(y)
    my = sum(y) / n
    scores = []
    for j in range(len(X[0])):
        col = [row[j] for row in X]
        mc = sum(col) / n
        scores.append((abs(sum((c - mc) * (t - my) for c, t in zip(col, y))), j))
    return [j for _, j in sorted(scores, reverse=True)[:m]]


def test_selection_outside_the_folds_leaks() -> None:
    rng = random.Random(3)
    n, p, m = 40, 1000, 20
    X = [[rng.gauss(0, 1) for _ in range(p)] for _ in range(n)]
    y = [i % 2 for i in range(n)]  # labels independent of X: the true error is 1/2
    folds = kfold(n, 10, rng)

    def run(select_inside: bool) -> float:
        keep_all = top_features(X, y, m)
        wrong = 0
        for test in folds:
            tr = [i for i in range(n) if i not in set(test)]
            keep = top_features([X[i] for i in tr], [y[i] for i in tr], m) if select_inside else keep_all
            proj = [[X[i][j] for j in keep] for i in range(n)]
            for i in test:
                wrong += nearest_label([proj[t] for t in tr], [y[t] for t in tr], proj[i]) != y[i]
        return wrong / n

    assert run(select_inside=False) < 0.25
    assert run(select_inside=True) > 0.3


def test_nested_cv_on_noise_is_honest() -> None:
    rng = random.Random(4)
    n = 60
    X = [[rng.gauss(0, 1) for _ in range(5)] for _ in range(n)]
    y = [rng.randint(0, 1) for _ in range(n)]

    def make_fit(kind: str):
        def fit(Xt, yt):
            if kind == "majority":
                return ("majority", int(2 * sum(yt) >= len(yt)))
            return ("1nn", Xt, yt)
        return fit

    def predict(model, x):
        return model[1] if model[0] == "majority" else nearest_label(model[1], model[2], x)

    est, chosen = nested_cv(make_fit, predict, lambda t, p: float(t != p), ["majority", "1nn"],
                            X, y, 5, 4, rng)
    assert set(chosen) <= {"majority", "1nn"} and len(chosen) == 5
    assert 0.3 < est < 0.75
