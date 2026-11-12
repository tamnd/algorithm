# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/one-vs-one/. The authors are listed in prov/W9KQF9.jsonl.
"""One-vs-one: one binary classifier for each pair of classes i < j, trained only on the
examples of those two classes (class i as +1, class j as -1). Prediction by voting, with a
tie going to the smallest class index as in LIBSVM, or broken by the summed confidences.
Also the decision DAG (DDAG) evaluation with k - 1 classifiers.
The default binary learner is regularized least squares on the targets +1 and -1."""

from itertools import combinations
from typing import Callable

Score = Callable[[list[float]], float]
BinaryLearner = Callable[[list[list[float]], list[int]], Score]


def _solve(a: list[list[float]], b: list[float]) -> list[float]:
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
    def fit(X: list[list[float]], t: list[int]) -> Score:
        Z = [x + [1.0] for x in X]
        d = len(Z[0])
        a = [[sum(z[i] * z[j] for z in Z) + (lam if i == j else 0.0) for j in range(d)] for i in range(d)]
        w = _solve(a, [sum(z[j] * ti for z, ti in zip(Z, t)) for j in range(d)])
        return lambda x: sum(wj * v for wj, v in zip(w, x + [1.0]))
    return fit


def train(X: list[list[float]], y: list[int], k: int,
          binary: BinaryLearner) -> dict[tuple[int, int], Score]:
    """Classes are 0..k-1. Returns {(i, j): f_ij} for i < j; f_ij > 0 means class i."""
    models = {}
    for i, j in combinations(range(k), 2):  # @line L1
        idx = [t for t, c in enumerate(y) if c == i or c == j]  # @line L2
        models[(i, j)] = binary([X[t] for t in idx], [1 if y[t] == i else -1 for t in idx])  # @line L3
    return models  # @line L4


def votes(models: dict[tuple[int, int], Score], k: int, x: list[float]) -> list[int]:
    v = [0] * k  # @line L5
    for (i, j), f in models.items():  # @line L6
        if f(x) > 0:  # @line L7
            v[i] += 1
        else:
            v[j] += 1
    return v


def predict(models: dict[tuple[int, int], Score], k: int, x: list[float]) -> int:
    """Most votes; a tie goes to the smallest class index (the LIBSVM rule)."""
    v = votes(models, k, x)
    return v.index(max(v))  # @line L8


def predict_confidence_tiebreak(models: dict[tuple[int, int], Score], k: int, x: list[float]) -> int:
    """Most votes; among tied classes, the largest sum of scores in its favor."""
    v = votes(models, k, x)
    conf = [0.0] * k
    for (i, j), f in models.items():
        s = f(x)
        conf[i] += s
        conf[j] -= s
    best = max(v)
    tied = [c for c in range(k) if v[c] == best]
    return max(tied, key=lambda c: (conf[c], -c))


def predict_ddag(models: dict[tuple[int, int], Score], k: int, x: list[float]) -> int:
    """Decision DAG: keep a list of candidates, test the first against the last, drop the loser."""
    cand = list(range(k))
    while len(cand) > 1:
        i, j = cand[0], cand[-1]
        if models[(i, j)](x) > 0:
            cand.pop()
        else:
            cand.pop(0)
    return cand[0]
