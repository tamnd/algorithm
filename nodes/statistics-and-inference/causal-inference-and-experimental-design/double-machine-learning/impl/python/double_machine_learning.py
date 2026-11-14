# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-machine-learning/. The authors are listed in prov/AN6TYE.jsonl.

"""Double (debiased) machine learning with cross-fitting.

Two estimators are given:

* dml_ate: the average treatment effect with the AIPW (doubly robust) score
      psi_i = m1(X_i) - m0(X_i) + T_i (Y_i - m1(X_i)) / e(X_i) - (1 - T_i)(Y_i - m0(X_i)) / (1 - e(X_i)),
  where the nuisances e, m1, m0 for unit i are fitted on the folds that do not contain i.
* dml_plr: the coefficient theta of the partially linear model Y = theta T + g(X) + error,
  with the residual-on-residual (Robinson) score (Y - l(X) - theta (T - m(X))) (T - m(X)),
  l(X) = E[Y | X], m(X) = E[T | X].

A learner is a function learner(xs, ys) that returns a predictor x -> prediction.
With k = 1 there is no cross-fitting: the nuisances are fitted on the whole sample.
"""

import math
import random
from collections.abc import Callable, Sequence
from statistics import NormalDist
from typing import NamedTuple

Learner = Callable[[list, list], Callable]


class DMLResult(NamedTuple):
    estimate: object  # the point estimate
    se: float  # the standard error from the score variance
    lower: float  # lower end of the normal interval
    upper: float  # upper end of the normal interval
    scores: list  # the per-unit scores (for the ATE) or the per-unit products (for the PLR)


def make_folds(n: int, k: int, rng: random.Random | None) -> list[int]:
    """Fold label of each unit: a random permutation cut into k parts whose sizes differ by at most 1.
    With k = 1 every unit is in fold 0."""
    if not 1 <= k <= n:
        raise ValueError("need 1 <= k <= n")
    order = list(range(n))
    if rng is not None:
        rng.shuffle(order)
    label = [0] * n
    for pos, i in enumerate(order):
        label[i] = pos * k // n
    return label


def _train_test(label, fold, k):
    """With k = 1, train and test on everything (no cross-fitting)."""
    if k == 1:
        return range(len(label)), range(len(label))
    return [i for i, f in enumerate(label) if f != fold], [i for i, f in enumerate(label) if f == fold]


def _interval(est, var, alpha):
    se = math.sqrt(float(var))
    z = NormalDist().inv_cdf(1 - alpha / 2)
    return se, float(est) - z * se, float(est) + z * se


def dml_ate(x: Sequence, t: Sequence[int], y: Sequence, outcome_learner: Learner, propensity_learner: Learner, k: int = 5, rng: random.Random | None = None, trim: float = 0.0, alpha: float = 0.05) -> DMLResult:
    """Cross-fitted AIPW estimate of the ATE. The propensity predictions are clipped to [trim, 1 - trim].
    Cost: k fits of each learner plus Theta(n)."""
    n = len(t)
    if not (n == len(x) == len(y)):
        raise ValueError("x, t and y must have the same length")
    label = make_folds(n, k, rng)  # @line L1
    psi = [None] * n
    for fold in range(k):  # @line L2
        train, test = _train_test(label, fold, k)
        tr1 = [i for i in train if t[i] == 1]
        tr0 = [i for i in train if t[i] == 0]
        if not tr1 or not tr0:
            raise ValueError("a training set has no treated or no control units")
        e_hat = propensity_learner([x[i] for i in train], [t[i] for i in train])  # @line L3
        m1_hat = outcome_learner([x[i] for i in tr1], [y[i] for i in tr1])  # @line L4
        m0_hat = outcome_learner([x[i] for i in tr0], [y[i] for i in tr0])
        for i in test:  # @line L5
            e = e_hat(x[i])
            if trim:
                e = min(max(e, trim), 1 - trim)
            if not 0 < e < 1:
                raise ValueError("positivity fails: a predicted propensity is 0 or 1")
            a, b = m1_hat(x[i]), m0_hat(x[i])
            psi[i] = a - b + ((y[i] - a) / e if t[i] == 1 else -(y[i] - b) / (1 - e))  # @line L6
    est = sum(psi) / n  # @line L7
    var = sum((p - est) ** 2 for p in psi) / (n - 1) / n
    se, lo, hi = _interval(est, var, alpha)
    return DMLResult(est, se, lo, hi, psi)  # @line L8


def dml_plr(x: Sequence, t: Sequence, y: Sequence, learner: Learner, k: int = 5, rng: random.Random | None = None, treatment_learner: Learner | None = None, alpha: float = 0.05) -> DMLResult:
    """Cross-fitted partially linear model: theta = sum (T - m)(Y - l) / sum (T - m)^2.
    The standard error is the sandwich sqrt(mean(psi^2) / n) / mean((T - m)^2)."""
    n = len(t)
    if not (n == len(x) == len(y)):
        raise ValueError("x, t and y must have the same length")
    tl = treatment_learner or learner
    label = make_folds(n, k, rng)
    rt = [None] * n
    ry = [None] * n
    for fold in range(k):
        train, test = _train_test(label, fold, k)
        l_hat = learner([x[i] for i in train], [y[i] for i in train])
        m_hat = tl([x[i] for i in train], [t[i] for i in train])
        for i in test:
            ry[i] = y[i] - l_hat(x[i])
            rt[i] = t[i] - m_hat(x[i])
    j = sum(v * v for v in rt)
    if j == 0:
        raise ValueError("the treatment residuals are all 0: T is a function of X in the fit")
    theta = sum(a * b for a, b in zip(rt, ry)) / j
    psi = [(b - theta * a) * a for a, b in zip(rt, ry)]
    var = (sum(p * p for p in psi) / n) / ((j / n) ** 2) / n
    se, lo, hi = _interval(theta, var, alpha)
    return DMLResult(theta, se, lo, hi, psi)


# ----------------------------------------------------------------- learners


def solve(a: list[list], b: list) -> list:
    """Solve a x = b by Gaussian elimination with partial pivoting (exact for Fractions)."""
    k = len(b)
    m = [list(row) + [bi] for row, bi in zip(a, b)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ValueError("singular system")
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, k):
            f = m[r][c] / m[c][c]
            if f != 0:
                for jj in range(c, k + 1):
                    m[r][jj] -= f * m[c][jj]
    out = [0] * k
    for c in range(k - 1, -1, -1):
        out[c] = (m[c][k] - sum(m[c][jj] * out[jj] for jj in range(c + 1, k))) / m[c][c]
    return out


def linear_learner(features: Callable) -> Learner:
    """Least squares on features(x), by the normal equations."""

    def fit(xs, ys):
        rows = [features(v) for v in xs]
        p = len(rows[0])
        xtx = [[sum(r[a] * r[b] for r in rows) for b in range(p)] for a in range(p)]
        xty = [sum(r[a] * yi for r, yi in zip(rows, ys)) for a in range(p)]
        coef = solve(xtx, xty)
        return lambda v: sum(c * f for c, f in zip(coef, features(v)))

    return fit


def binned_learner(n_bins: int, lo: float = 0.0, hi: float = 1.0) -> Learner:
    """Regressogram: the mean of y in each of n_bins equal bins of [lo, hi]; the overall mean in an empty bin."""

    def fit(xs, ys):
        s = [0.0] * n_bins
        c = [0] * n_bins
        for v, yi in zip(xs, ys):
            b = min(n_bins - 1, max(0, int((v - lo) / (hi - lo) * n_bins)))
            s[b] += yi
            c[b] += 1
        overall = sum(ys) / len(ys)
        means = [s[b] / c[b] if c[b] else overall for b in range(n_bins)]
        return lambda v: means[min(n_bins - 1, max(0, int((v - lo) / (hi - lo) * n_bins)))]

    return fit


def oracle_learner(f: Callable) -> Learner:
    """Ignores the training data and returns f; used to check the estimator against AIPW."""
    return lambda xs, ys: f
