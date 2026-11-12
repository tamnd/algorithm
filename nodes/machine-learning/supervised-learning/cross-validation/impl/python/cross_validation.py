# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cross-validation/. The authors are listed in prov/1RKJ3F.jsonl.
"""K-fold, stratified K-fold and leave-one-out splits, the cross-validation estimate of the
risk of a learner, nested cross-validation for a hyperparameter, and the leave-one-out
shortcut (y_i - yhat_i) / (1 - h_ii) for least squares and ridge regression through the
hat matrix. The linear algebra is exact over Fractions when the inputs are Fractions."""

import random
from fractions import Fraction
from typing import Any, Callable

Fit = Callable[[list, list], Any]          # fit(X_train, y_train) -> model
Predict = Callable[[Any, Any], Any]         # predict(model, x) -> prediction
Loss = Callable[[Any, Any], float]          # loss(y, prediction) -> number


def kfold(n: int, k: int, rng: random.Random) -> list[list[int]]:
    """Shuffle 0..n-1 and cut it into k folds whose sizes differ by at most 1."""
    if not 2 <= k <= n:
        raise ValueError("need 2 <= k <= n")
    idx = list(range(n))
    rng.shuffle(idx)
    q, r = divmod(n, k)
    folds, start = [], 0
    for f in range(k):
        size = q + (1 if f < r else 0)
        folds.append(sorted(idx[start:start + size]))
        start += size
    return folds


def stratified_kfold(labels: list, k: int, rng: random.Random) -> list[list[int]]:
    """Shuffle within each class, list the classes one after another, and deal the list
    round-robin. Each class count, and each fold size, differs by at most 1 across folds."""
    by_class: dict = {}
    for i, y in enumerate(labels):
        by_class.setdefault(y, []).append(i)
    order = []
    for y in sorted(by_class, key=repr):
        members = by_class[y]
        rng.shuffle(members)
        order.extend(members)
    folds: list[list[int]] = [[] for _ in range(k)]
    for pos, i in enumerate(order):
        folds[pos % k].append(i)
    return [sorted(f) for f in folds]


def leave_one_out(n: int) -> list[list[int]]:
    return [[i] for i in range(n)]


def cv_estimate(fit: Fit, predict: Predict, loss: Loss, X: list, y: list,
                split: list[list[int]] | Callable[[int], list[list[int]]]) -> float:
    """Train on all folds but one, test on that one, and average the loss over all n examples.
    split is a list of folds or a function n -> folds."""
    n = len(X)
    folds = split(n) if callable(split) else split  # @line L1
    total = 0  # @line L2
    for test in folds:  # @line L3
        held = set(test)
        model = fit([X[i] for i in range(n) if i not in held],  # @line L4
                    [y[i] for i in range(n) if i not in held])
        for i in test:  # @line L5
            total += loss(y[i], predict(model, X[i]))  # @line L6
    return total / n  # @line L7


def nested_cv(make_fit: Callable[[Any], Fit], predict: Predict, loss: Loss, grid: list,
              X: list, y: list, k_outer: int, k_inner: int, rng: random.Random) -> tuple[float, list]:
    """Outer K-fold estimate of the whole procedure 'choose the hyperparameter by inner K-fold
    CV on the training part, then refit'. Returns the estimate and the chosen values."""
    n, total, chosen = len(X), 0, []
    for test in kfold(n, k_outer, rng):
        held = set(test)
        tr = [i for i in range(n) if i not in held]
        Xt, yt = [X[i] for i in tr], [y[i] for i in tr]
        inner = kfold(len(tr), k_inner, rng)
        best = min(grid, key=lambda h: cv_estimate(make_fit(h), predict, loss, Xt, yt, inner))
        chosen.append(best)
        model = make_fit(best)(Xt, yt)
        total += sum(loss(y[i], predict(model, X[i])) for i in test)
    return total / n, chosen


# Small exact linear algebra for least squares.

def solve(a: list[list], b: list) -> list:
    """Gauss-Jordan elimination with partial pivoting (exact for Fractions)."""
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ZeroDivisionError("singular matrix")
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [u - f * v for u, v in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def gram(X: list[list], lam=0) -> list[list]:
    d = len(X[0])
    return [[sum(x[i] * x[j] for x in X) + (lam if i == j else 0) for j in range(d)] for i in range(d)]


def fit_ridge(X: list[list], y: list, lam=0) -> list:
    """argmin ||y - X b||^2 + lam ||b||^2; lam = 0 is ordinary least squares."""
    d = len(X[0])
    return solve(gram(X, lam), [sum(x[j] * t for x, t in zip(X, y)) for j in range(d)])


def predict_linear(beta: list, x: list):
    return sum(b * v for b, v in zip(beta, x))


def leverages(X: list[list], lam=0) -> list:
    """h_ii = x_i^T (X^T X + lam I)^{-1} x_i, the diagonal of the hat matrix."""
    a = gram(X, lam)
    return [predict_linear(solve(a, x), x) for x in X]


def loo_residuals_shortcut(X: list[list], y: list, lam=0) -> list:
    """(y_i - yhat_i) / (1 - h_ii) from one fit on all the data."""
    beta = fit_ridge(X, y, lam)
    return [(t - predict_linear(beta, x)) / (1 - h) for x, t, h in zip(X, y, leverages(X, lam))]


def loo_residuals_refit(X: list[list], y: list, lam=0) -> list:
    """y_i minus the prediction of the model refitted without example i (n fits)."""
    out = []
    for i in range(len(X)):
        beta = fit_ridge(X[:i] + X[i + 1:], y[:i] + y[i + 1:], lam)
        out.append(y[i] - predict_linear(beta, X[i]))
    return out
