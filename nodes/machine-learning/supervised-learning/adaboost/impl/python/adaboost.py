# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaboost/. The authors are listed in prov/F7R3H9.jsonl.
"""AdaBoost (Freund and Schapire 1997) for labels in {-1, +1}, with decision stumps.

The weak learner is the stump of least weighted error. A stump (f, thr, s)
predicts s when x[f] > thr and -s otherwise. Both signs are tried, so the
weighted error of the chosen stump is at most 1/2.

Each round records eps_t, alpha_t, Z_t, the training error of the vote after
round t, the product of the Z_t and the bound exp(-2 sum gamma_t^2).
"""

import math
from typing import NamedTuple, Sequence

Point = Sequence[float]
Stump = tuple[int, float, int]


class Round(NamedTuple):
    stump: Stump
    eps: float
    alpha: float
    z: float
    train_error: float
    prod_z: float
    exp_bound: float


def stump_predict(s: Stump, x: Point) -> int:
    f, thr, sgn = s
    return sgn if x[f] > thr else -sgn


def thresholds(xs: Sequence[Point], f: int) -> list[float]:
    """One threshold below all values, then the midpoints between distinct sorted values."""
    vals = sorted(set(x[f] for x in xs))
    return [vals[0] - 1.0] + [(a + b) / 2 for a, b in zip(vals, vals[1:])]


def weighted_error(s: Stump, xs: Sequence[Point], ys: Sequence[int], w: Sequence[float]) -> float:
    return sum(wi for x, y, wi in zip(xs, ys, w) if stump_predict(s, x) != y)


def best_stump(xs: Sequence[Point], ys: Sequence[int], w: Sequence[float]) -> tuple[Stump, float]:
    """The stump of least weighted error. One sorted sweep per feature, O(d n log n)."""
    total = sum(w)
    best: tuple[Stump, float] = ((0, 0.0, 1), math.inf)
    for f in range(len(xs[0])):
        order = sorted(range(len(xs)), key=lambda i: xs[i][f])
        thr = xs[order[0]][f] - 1.0
        # Sign +1 with the threshold below all points predicts +1 everywhere.
        err = sum(w[i] for i in order if ys[i] != 1)
        for pos in range(len(order) + 1):
            if pos > 0:
                i = order[pos - 1]
                err += w[i] if ys[i] == 1 else -w[i]  # point i moves to the side that predicts -1
                if pos < len(order) and xs[order[pos]][f] == xs[i][f]:
                    continue  # no threshold between equal values
                if pos == len(order):
                    break  # all points on one side again: same as the first threshold
                thr = (xs[i][f] + xs[order[pos]][f]) / 2
            for sgn, e in ((1, err), (-1, total - err)):
                if e < best[1] - 1e-12:
                    best = ((f, thr, sgn), e)
    return best


def vote(model: Sequence[tuple[float, Stump]], x: Point) -> float:
    """The real-valued score F(x) = sum alpha_t h_t(x)."""
    return sum(a * stump_predict(s, x) for a, s in model)


def predict(model: Sequence[tuple[float, Stump]], x: Point) -> int:
    """sign(F(x)), with sign(0) = -1 so that a tie counts as an error in the bound."""
    return 1 if vote(model, x) > 0 else -1  # @line L10


def adaboost(xs: Sequence[Point], ys: Sequence[int], rounds: int) -> tuple[list[tuple[float, Stump]], list[Round], list[list[float]]]:
    """Run AdaBoost. Return the model [(alpha_t, h_t)], the round records and the weights D_1 .. D_{T+1}."""
    n = len(xs)
    d = [1.0 / n] * n  # @line L1
    dists = [d[:]]
    model: list[tuple[float, Stump]] = []
    hist: list[Round] = []
    prod_z, sum_g2 = 1.0, 0.0
    for _ in range(rounds):  # @line L2
        s, eps = best_stump(xs, ys, d)  # @line L3 L4
        if eps >= 0.5:  # @line L5
            break  # no edge: the weak learning assumption fails
        if eps <= 0.0:  # @line L6
            # A perfect stump: alpha would be infinite, so the vote is this stump alone.
            model = [(1.0, s)]
            hist.append(Round(s, 0.0, math.inf, 0.0, 0.0, 0.0, 0.0))
            break
        alpha = 0.5 * math.log((1 - eps) / eps)  # @line L7
        model.append((alpha, s))
        d = [di * math.exp(-alpha * y * stump_predict(s, x)) for di, x, y in zip(d, xs, ys)]  # @line L8
        z = sum(d)  # @line L9
        d = [di / z for di in d]
        dists.append(d[:])
        prod_z *= z
        sum_g2 += (0.5 - eps) ** 2
        err = sum(predict(model, x) != y for x, y in zip(xs, ys)) / n
        hist.append(Round(s, eps, alpha, z, err, prod_z, math.exp(-2 * sum_g2)))
    return model, hist, dists
