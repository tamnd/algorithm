# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/empirical-likelihood/. The authors are listed in prov/DSWA0W.jsonl.

import math
from collections.abc import Callable, Sequence
from typing import Any, NamedTuple

from stdist import chi2_ppf


def _solve(a: list, b: list) -> list:
    """Solve a x = b by Gaussian elimination with partial pivoting. Cost O(q^3)."""
    k = len(a)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ZeroDivisionError("singular matrix")
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, k):
            f = m[r][c] / m[c][c]
            for j in range(c, k + 1):
                m[r][j] -= f * m[c][j]
    x = [0.0] * k
    for r in range(k - 1, -1, -1):
        x[r] = (m[r][k] - sum(m[r][j] * x[j] for j in range(r + 1, k))) / m[r][r]
    return x


def _log_star(z: float, n: int) -> tuple[float, float, float]:
    """Owen's pseudo-logarithm and its first two derivatives.

    Equal to log z for z >= 1/n, a quadratic below 1/n with matching value,
    slope and curvature, so it is defined for every real z.
    """
    if z >= 1.0 / n:
        return math.log(z), 1.0 / z, -1.0 / (z * z)
    t = n * z
    return -math.log(n) - 1.5 + 2.0 * t - 0.5 * t * t, 2.0 * n - n * n * z, -float(n * n)


class ELResult(NamedTuple):
    stat: float        # -2 log R(theta); math.inf when 0 is outside the convex hull
    lam: list          # Lagrange multiplier
    weights: list      # w_i = 1 / (n (1 + lam' d_i)); empty when stat is inf
    iterations: int


def el_ratio(d: Sequence[Sequence[float]], tol: float = 1e-24, max_iter: int = 100) -> ELResult:
    """Empirical likelihood ratio statistic for the hypothesis E[d] = 0.

    d holds the n vectors d_i = m(x_i, theta) in R^q. The multiplier lam
    minimizes the convex dual -sum log*(1 + lam' d_i), found by damped Newton
    steps. If the solution puts some 1 + lam' d_i below 1/n, the point 0 is not
    inside the convex hull of the d_i and the result is inf.
    Cost per Newton step: O(n q^2 + q^3).
    """
    n = len(d)  # @line L2
    q = len(d[0])
    lam = [0.0] * q

    def dual(lv: list) -> float:
        return -sum(_log_star(1.0 + sum(a * b for a, b in zip(lv, di)), n)[0] for di in d)

    f = dual(lam)
    it = 0
    for it in range(1, max_iter + 1):  # @line L4
        grad = [0.0] * q
        hess = [[0.0] * q for _ in range(q)]
        for di in d:
            z = 1.0 + sum(a * b for a, b in zip(lam, di))
            _, d1, d2 = _log_star(z, n)
            for r in range(q):
                grad[r] -= d1 * di[r]
                for s in range(q):
                    hess[r][s] -= d2 * di[r] * di[s]
        try:
            step = _solve(hess, [-g for g in grad])
        except ZeroDivisionError:
            break
        dec = -sum(g * s for g, s in zip(grad, step))
        if dec <= tol:
            break
        s = 1.0
        new = [a + s * b for a, b in zip(lam, step)]
        fn = dual(new)
        while fn > f and s > 1e-12:
            s /= 2
            new = [a + s * b for a, b in zip(lam, step)]
            fn = dual(new)
        if fn > f:
            break
        stalled = fn == f
        lam, f = new, fn
        if stalled:
            break
    zs = [1.0 + sum(a * b for a, b in zip(lam, di)) for di in d]
    w = [1.0 / (n * z) if z > 0 else math.inf for z in zs]  # @line L5
    # A true solution has every z_i > 1/n and weights that sum to 1. If 0 is
    # outside the hull, some z_i < 1/n, or the dual has no minimum and the
    # iterates run off with every z_i large, so the weights sum far below 1.
    if min(zs) < 1.0 / n * (1 - 1e-9) or abs(sum(w) - 1.0) > 1e-6:  # @line L3
        return ELResult(math.inf, lam, [], it)
    stat = 2.0 * sum(math.log(z) for z in zs)  # @line L6
    return ELResult(stat, lam, w, it)


def el_test(
    m: Callable[[Any, Sequence[float]], Sequence[float]],
    data: Sequence,
    theta: Sequence[float],
    alpha: float = 0.05,
) -> tuple[float, float, bool]:
    """Test E[m(X, theta)] = 0 with the chi-squared(q) calibration.

    Returns (-2 log R, critical value, reject). Cost: one call of el_ratio.
    """
    d = [list(m(x, theta)) for x in data]  # @line L1
    res = el_ratio(d)
    crit = chi2_ppf(1.0 - alpha, len(d[0]))
    return res.stat, crit, res.stat > crit  # @line L7


def el_mean_stat(x: Sequence[float], mu: float) -> float:
    """-2 log R(mu) for a scalar mean. inf when mu is not strictly inside (min x, max x)."""
    lo, hi = min(x), max(x)
    if lo == hi:
        return 0.0 if mu == lo else math.inf
    if not lo < mu < hi:
        return math.inf
    return el_ratio([[v - mu] for v in x]).stat


def el_mean_interval(x: Sequence[float], alpha: float = 0.05, iters: int = 80) -> tuple[float, float]:
    """Empirical likelihood interval {mu : -2 log R(mu) <= chi2_1(1 - alpha)} for a mean.

    -2 log R is 0 at the sample mean and increases on each side, so each end
    is found by bisection. Precondition: at least two distinct values.
    Cost: O(iters) calls of el_ratio.
    """
    c = chi2_ppf(1.0 - alpha, 1)
    xbar = sum(x) / len(x)
    ends = []
    for edge in (min(x), max(x)):
        inside, outside = xbar, edge
        for _ in range(iters):
            mid = 0.5 * (inside + outside)
            if el_mean_stat(x, mid) <= c:
                inside = mid
            else:
                outside = mid
        ends.append(inside)
    return ends[0], ends[1]
