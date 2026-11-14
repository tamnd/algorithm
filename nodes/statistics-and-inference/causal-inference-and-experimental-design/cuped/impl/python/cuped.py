# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cuped/. The authors are listed in prov/Y9J2V9.jsonl.

"""CUPED: variance reduction for a randomized experiment with a pre-experiment covariate.

Each unit has a metric y measured during the experiment and a covariate x measured
before it (often the same metric in an earlier period). The adjusted metric is

    y_cv = y - theta (x - mean of x over all units),

and the effect estimate is the difference of the arm means of y_cv:

    delta = (ybar_t - ybar_c) - theta (xbar_t - xbar_c).

theta can be a number fixed in advance, "pooled" (the slope of y on x over all units,
ignoring the arms) or "within" (the pooled within-arm slope). With "within", delta is
exactly the treatment coefficient of the regression of y on (1, T, x) (ANCOVA).
All functions are exact for Fraction inputs, except the interval.
"""

import math
from collections.abc import Sequence
from statistics import NormalDist
from typing import NamedTuple


class CupedResult(NamedTuple):
    delta: object  # the adjusted difference in means
    theta: object  # the coefficient used
    var: object  # the estimated variance of delta (Welch form, divisors n_t - 1 and n_c - 1)
    naive_delta: object  # ybar_t - ybar_c
    naive_var: object  # its estimated variance


def _mean(v):
    return sum(v) / len(v)


def _svar(v):
    m = _mean(v)
    return sum((a - m) ** 2 for a in v) / (len(v) - 1)


def theta_pooled(y: Sequence, x: Sequence) -> object:
    """Slope of y on x over all units: sum (x - xbar)(y - ybar) / sum (x - xbar)^2."""
    mx, my = _mean(x), _mean(y)
    sxx = sum((a - mx) ** 2 for a in x)
    if sxx == 0:
        raise ValueError("the covariate is constant")
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / sxx


def theta_within(yt, xt, yc, xc) -> object:
    """Pooled within-arm slope: the coefficient of x in the regression of y on (1, T, x)."""
    mxt, myt, mxc, myc = _mean(xt), _mean(yt), _mean(xc), _mean(yc)
    sxx = sum((a - mxt) ** 2 for a in xt) + sum((a - mxc) ** 2 for a in xc)
    if sxx == 0:
        raise ValueError("the covariate is constant within both arms")
    sxy = sum((a - mxt) * (b - myt) for a, b in zip(xt, yt)) + sum((a - mxc) * (b - myc) for a, b in zip(xc, yc))
    return sxy / sxx


def cuped(yt: Sequence, xt: Sequence, yc: Sequence, xc: Sequence, theta="pooled") -> CupedResult:
    """CUPED estimate of the treatment effect. Cost: Theta(n) time, Theta(n) space for the adjusted values."""
    if len(yt) != len(xt) or len(yc) != len(xc):
        raise ValueError("each arm needs one covariate per outcome")
    if len(yt) < 2 or len(yc) < 2:
        raise ValueError("each arm needs at least two units")
    if theta == "pooled":  # @line L1
        th = theta_pooled(list(yt) + list(yc), list(xt) + list(xc))
    elif theta == "within":
        th = theta_within(yt, xt, yc, xc)
    else:
        th = theta
    xbar = _mean(list(xt) + list(xc))  # @line L2
    at = [b - th * (a - xbar) for a, b in zip(xt, yt)]  # @line L3
    ac = [b - th * (a - xbar) for a, b in zip(xc, yc)]
    delta = _mean(at) - _mean(ac)  # @line L4
    var = _svar(at) / len(at) + _svar(ac) / len(ac)  # @line L5
    naive = _mean(yt) - _mean(yc)
    nvar = _svar(yt) / len(yt) + _svar(yc) / len(yc)
    return CupedResult(delta, th, var, naive, nvar)  # @line L6


def interval(res: CupedResult, alpha: float = 0.05) -> tuple[float, float]:
    """Normal interval delta +- z sqrt(var), approximate level 1 - alpha."""
    z = NormalDist().inv_cdf(1 - alpha / 2)
    se = math.sqrt(float(res.var))
    return float(res.delta) - z * se, float(res.delta) + z * se


# ----------------------------------------------------------------- reference: ANCOVA by least squares


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
    out = [0] * k
    for c in range(k - 1, -1, -1):
        out[c] = (m[c][k] - sum(m[c][j] * out[j] for j in range(c + 1, k))) / m[c][c]
    return out


def ancova(yt, xt, yc, xc) -> list:
    """Coefficients (intercept, T, x) of the least squares regression of y on (1, T, x)."""
    one = xt[0] * 0 + 1  # 1 in the number type of the input, so Fractions stay exact
    zero = one - one
    rows = [[one, one, a] for a in xt] + [[one, zero, a] for a in xc]
    y = list(yt) + list(yc)
    xtx = [[sum(r[i] * r[j] for r in rows) for j in range(3)] for i in range(3)]
    xty = [sum(r[i] * v for r, v in zip(rows, y)) for i in range(3)]
    return solve(xtx, xty)
