# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/one-vs-rest/. The authors are listed in prov/56YRRQ.jsonl.
"""One-vs-rest: k binary score functions, the j-th trained on all n examples with class j as
+1 and every other class as -1, and prediction by the largest score (smallest index on a tie).
The default binary learner is regularized least squares on the targets +1 and -1."""

from typing import Callable

Score = Callable[[list[float]], float]
BinaryLearner = Callable[[list[list[float]], list[int]], Score]


def _solve(a: list[list[float]], b: list[float]) -> list[float]:
    """Gaussian elimination with partial pivoting."""
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [u - f * v for u, v in zip(m[r], m[c])]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))) / m[i][i]
    return x


def least_squares_learner(lam: float = 1e-6) -> BinaryLearner:
    """Fit w, b minimizing sum (t_i - w.x_i - b)^2 + lam ||(w, b)||^2; score(x) = w.x + b."""
    def fit(X: list[list[float]], t: list[int]) -> Score:
        Z = [x + [1.0] for x in X]
        d = len(Z[0])
        a = [[sum(z[i] * z[j] for z in Z) + (lam if i == j else 0.0) for j in range(d)] for i in range(d)]
        w = _solve(a, [sum(z[j] * ti for z, ti in zip(Z, t)) for j in range(d)])
        return lambda x: sum(wj * v for wj, v in zip(w, x + [1.0]))
    return fit


def train(X: list[list[float]], y: list[int], k: int, binary: BinaryLearner) -> list[Score]:
    """Classes are 0..k-1. Returns the k score functions."""
    scores = []
    for j in range(k):  # @line L1
        t = [1 if yi == j else -1 for yi in y]  # @line L2
        scores.append(binary(X, t))  # @line L3
    return scores  # @line L4


def predict(scores: list[Score], x: list[float]) -> int:
    """The class with the largest score; the smallest index wins a tie."""
    v = [f(x) for f in scores]
    return v.index(max(v))  # @line L5


def predict_hard_votes(scores: list[Score], x: list[float]) -> list[int]:
    """The classes whose binary classifier says +1. It can be empty or have several members."""
    return [j for j, f in enumerate(scores) if f(x) > 0]
