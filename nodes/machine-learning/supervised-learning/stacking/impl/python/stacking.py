# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stacking/. The authors are listed in prov/2W5J8D.jsonl.
"""Stacked generalization (Wolpert 1992) for regression, with Breiman's (1996) level-1
learner: non-negative least squares (NNLS) on the out-of-fold level-0 predictions.

Data model: xs is a list of n real inputs, ys a list of n real targets. A level-0 learner is
a function fit(xs, ys) that returns a predictor, a function from an input to a real number.
"""

import itertools
import random
from typing import Callable, Optional, Sequence

Learner = Callable[[Sequence[float], Sequence[float]], Callable[[float], float]]


def fit_mean(xs: Sequence[float], ys: Sequence[float]) -> Callable[[float], float]:
    m = sum(ys) / len(ys)
    return lambda x: m


def fit_one_nn(xs: Sequence[float], ys: Sequence[float]) -> Callable[[float], float]:
    pts = list(zip(xs, ys))
    return lambda x: min(pts, key=lambda p: abs(p[0] - x))[1]


def make_ridge(lam: float) -> Learner:
    """Ridge regression of y on (1, x), with the penalty lam on the slope only."""
    def fit(xs: Sequence[float], ys: Sequence[float]) -> Callable[[float], float]:
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        sxx = sum((x - mx) ** 2 for x in xs)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        slope = sxy / (sxx + lam) if sxx + lam > 0 else 0.0
        return lambda x: my + slope * (x - mx)
    return fit


def k_folds(n: int, k: int, rng: random.Random) -> list[list[int]]:
    """A random partition of range(n) into k folds whose sizes differ by at most 1."""
    perm = list(range(n))
    rng.shuffle(perm)
    return [sorted(perm[j::k]) for j in range(k)]


def out_of_fold(xs: Sequence[float], ys: Sequence[float], learners: Sequence[Learner],
                folds: Sequence[Sequence[int]]) -> list[list[float]]:
    """z[i][l] = the prediction for x_i of learner l fitted without the fold that holds i."""
    n = len(xs)
    z = [[0.0] * len(learners) for _ in range(n)]
    for fold in folds:  # @line L2
        held = set(fold)
        train = [i for i in range(n) if i not in held]
        for l, fit in enumerate(learners):  # @line L3
            g = fit([xs[i] for i in train], [ys[i] for i in train])
            for i in fold:
                z[i][l] = g(xs[i])
    return z


def in_sample(xs: Sequence[float], ys: Sequence[float], learners: Sequence[Learner]) -> list[list[float]]:
    """The leaky alternative: each learner fitted on all of the data predicts its own training inputs."""
    fs = [fit(xs, ys) for fit in learners]
    return [[f(x) for f in fs] for x in xs]


def solve(a: list[list[float]], b: list[float]) -> Optional[list[float]]:
    """Gaussian elimination with partial pivoting; None if the matrix is singular."""
    m = len(b)
    rows = [row[:] + [bb] for row, bb in zip(a, b)]
    for c in range(m):
        p = max(range(c, m), key=lambda r: abs(rows[r][c]))
        if abs(rows[p][c]) < 1e-12:
            return None
        rows[c], rows[p] = rows[p], rows[c]
        for r in range(m):
            if r != c:
                f = rows[r][c] / rows[c][c]
                rows[r] = [u - f * v for u, v in zip(rows[r], rows[c])]
    return [rows[c][m] / rows[c][c] for c in range(m)]


def sse(z: Sequence[Sequence[float]], y: Sequence[float], w: Sequence[float]) -> float:
    return sum((sum(wl * zl for wl, zl in zip(w, row)) - yy) ** 2 for row, yy in zip(z, y))


def nnls(z: Sequence[Sequence[float]], y: Sequence[float]) -> list[float]:
    """min ||Z w - y||^2 subject to w >= 0, by trying every support (for a few columns).

    The problem is convex. Its solution w* solves the unconstrained least squares problem on
    its support P, so the best non-negative such solution over all supports is optimal.
    """
    cols = len(z[0])
    best_w, best_v = [0.0] * cols, sse(z, y, [0.0] * cols)
    for size in range(1, cols + 1):
        for support in itertools.combinations(range(cols), size):
            gram = [[sum(row[a] * row[b] for row in z) for b in support] for a in support]
            rhs = [sum(row[a] * yy for row, yy in zip(z, y)) for a in support]
            sol = solve(gram, rhs)
            if sol is None or min(sol) < 0:
                continue
            w = [0.0] * cols
            for a, v in zip(support, sol):
                w[a] = v
            v = sse(z, y, w)
            if v < best_v - 1e-12:
                best_w, best_v = w, v
    return best_w


def stack(xs: Sequence[float], ys: Sequence[float], learners: Sequence[Learner], k: int,
          rng: random.Random) -> tuple[list[float], Callable[[float], float]]:
    """Return the level-1 weights and the stacked predictor."""
    folds = k_folds(len(xs), k, rng)  # @line L1
    z = out_of_fold(xs, ys, learners, folds)
    w = nnls(z, ys)  # @line L4
    fs = [fit(xs, ys) for fit in learners]  # @line L5
    return w, lambda x: sum(wl * f(x) for wl, f in zip(w, fs))  # @line L6
