# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/augmented-inverse-probability-weighting/. The authors are listed in prov/T508RZ.jsonl.

"""Augmented inverse probability weighting (AIPW) estimate of the average treatment effect.

Unit i has a treatment t[i] in {0, 1}, an outcome y[i], a propensity e[i]
(the probability of treatment given the covariates) and two outcome
predictions m1[i] and m0[i] (the predicted outcome under treatment and under
control). The estimate is the mean of the AIPW scores

    psi_i = m1_i - m0_i + t_i (y_i - m1_i) / e_i - (1 - t_i)(y_i - m0_i) / (1 - e_i).

The nuisance values e, m1, m0 are inputs. fit_aipw fits them with a logistic
regression for e and one least squares regression per arm for m1 and m0.
With Fraction or int inputs, aipw_ate and aipw_scores are exact.
"""

import math
from collections.abc import Sequence
from statistics import NormalDist
from typing import NamedTuple


class AIPWEstimate(NamedTuple):
    tau: object  # the AIPW estimate of E[Y(1) - Y(0)]
    mu1: object  # the AIPW estimate of E[Y(1)]
    mu0: object  # the AIPW estimate of E[Y(0)]


def aipw_scores(t: Sequence[int], y: Sequence, e: Sequence, m1: Sequence, m0: Sequence) -> list:
    """The scores psi_i, one per unit. Cost: Theta(n) time."""
    n = len(t)
    if not (n == len(y) == len(e) == len(m1) == len(m0)):
        raise ValueError("t, y, e, m1 and m0 must have the same length")
    if n == 0:
        raise ValueError("no units")
    out = []
    for ti, yi, ei, a, b in zip(t, y, e, m1, m0):
        if ti not in (0, 1):
            raise ValueError("every treatment must be 0 or 1")
        if not 0 < ei < 1:
            raise ValueError("positivity fails: every propensity must be strictly between 0 and 1")
        if ti == 1:
            out.append(a - b + (yi - a) / ei)
        else:
            out.append(a - b - (yi - b) / (1 - ei))
    return out


def aipw_ate(t: Sequence[int], y: Sequence, e: Sequence, m1: Sequence, m0: Sequence) -> AIPWEstimate:
    """AIPW estimate of the ATE and of the two arm means. Cost: Theta(n) time, O(1) extra space."""
    n = len(t)
    if not (n == len(y) == len(e) == len(m1) == len(m0)):
        raise ValueError("t, y, e, m1 and m0 must have the same length")
    if n == 0:
        raise ValueError("no units")
    s1 = s0 = 0  # @line L1
    for ti, yi, ei, a, b in zip(t, y, e, m1, m0):  # @line L2
        if ti not in (0, 1):
            raise ValueError("every treatment must be 0 or 1")
        if not 0 < ei < 1:  # @line L3
            raise ValueError("positivity fails: every propensity must be strictly between 0 and 1")
        if ti == 1:  # @line L4
            s1 += a + (yi - a) / ei
            s0 += b
        else:  # @line L5
            s1 += a
            s0 += b + (yi - b) / (1 - ei)
    mu1, mu0 = s1 / n, s0 / n  # @line L6
    return AIPWEstimate(mu1 - mu0, mu1, mu0)  # @line L7


def aipw_variance(t, y, e, m1, m0):
    """Estimated variance of the AIPW estimate: S_psi^2 / n, with divisor n - 1 in S_psi^2."""
    psi = aipw_scores(t, y, e, m1, m0)
    n = len(psi)
    if n < 2:
        raise ValueError("need at least two units")
    mean = sum(psi) / n
    return sum((p - mean) ** 2 for p in psi) / (n - 1) / n


def aipw_interval(t, y, e, m1, m0, alpha: float = 0.05) -> tuple[float, float, float]:
    """(estimate, lower, upper) of the normal interval with nominal coverage 1 - alpha."""
    tau = float(aipw_ate(t, y, e, m1, m0).tau)
    se = math.sqrt(float(aipw_variance(t, y, e, m1, m0)))
    z = NormalDist().inv_cdf(1 - alpha / 2)
    return tau, tau - z * se, tau + z * se


# ----------------------------------------------------------------- nuisance fits


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
                for j in range(c, k + 1):
                    m[r][j] -= f * m[c][j]
    x = [0] * k
    for c in range(k - 1, -1, -1):
        s = m[c][k] - sum(m[c][j] * x[j] for j in range(c + 1, k))
        x[c] = s / m[c][c]
    return x


def fit_least_squares(rows: Sequence[Sequence], y: Sequence) -> list:
    """Coefficients b that minimize sum (y_i - rows_i . b)^2, by the normal equations."""
    p = len(rows[0])
    xtx = [[sum(r[i] * r[j] for r in rows) for j in range(p)] for i in range(p)]
    xty = [sum(r[i] * yi for r, yi in zip(rows, y)) for i in range(p)]
    return solve(xtx, xty)


def _expit(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


def fit_logistic(rows: Sequence[Sequence[float]], t: Sequence[int], tol: float = 1e-10, max_iter: int = 50) -> list[float]:
    """Logistic regression coefficients by Newton-Raphson. Stops when the largest step is below tol."""
    p = len(rows[0])
    b = [0.0] * p
    for _ in range(max_iter):
        grad = [0.0] * p
        hess = [[0.0] * p for _ in range(p)]
        for r, ti in zip(rows, t):
            q = _expit(sum(bj * rj for bj, rj in zip(b, r)))
            w = q * (1.0 - q)
            for i in range(p):
                grad[i] += (ti - q) * r[i]
                for j in range(i + 1):
                    hess[i][j] += w * r[i] * r[j]
        for i in range(p):
            for j in range(i + 1, p):
                hess[i][j] = hess[j][i]
        step = solve(hess, grad)
        b = [bj + sj for bj, sj in zip(b, step)]
        if max(abs(s) for s in step) < tol:
            return b
    raise ArithmeticError("Newton-Raphson did not converge; check for separation")


def fit_aipw(x: Sequence, t: Sequence[int], y: Sequence, outcome_features, propensity_features) -> tuple[list, list, list]:
    """Fit e by logistic regression on propensity_features(x) and m1, m0 by least squares on
    outcome_features(x) within each arm. Returns the lists (e, m1, m0) evaluated at every unit."""
    prow = [propensity_features(xi) for xi in x]
    orow = [outcome_features(xi) for xi in x]
    g = fit_logistic(prow, t)
    e = [_expit(sum(gj * rj for gj, rj in zip(g, r))) for r in prow]
    b1 = fit_least_squares([r for r, ti in zip(orow, t) if ti == 1], [yi for yi, ti in zip(y, t) if ti == 1])
    b0 = fit_least_squares([r for r, ti in zip(orow, t) if ti == 0], [yi for yi, ti in zip(y, t) if ti == 0])
    m1 = [sum(bj * rj for bj, rj in zip(b1, r)) for r in orow]
    m0 = [sum(bj * rj for bj, rj in zip(b0, r)) for r in orow]
    return e, m1, m0
