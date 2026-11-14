# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/box-cox-transformation/. The authors are listed in prov/KHKPKJ.jsonl.
"""Box-Cox transformation with lambda chosen by profile likelihood.

The model is y_i^(lambda) = x_i^T b + e_i with e_i iid N(0, sigma^2), where
y^(lambda) = (y^lambda - 1) / lambda for lambda != 0 and log y for lambda = 0.
With b and sigma^2 maximized out, the log-likelihood of lambda is

    l(lambda) = -(n / 2) log(RSS(lambda) / n) + (lambda - 1) sum log y_i,

up to the constant -(n / 2)(log(2 pi) + 1). X is factored once by Householder
QR; each l(lambda) then costs O(n p). The maximizer comes from a grid search
followed by golden-section refinement, and the likelihood ratio interval
{lambda : 2 (l(lambda_hat) - l(lambda)) <= chi^2_(1, level)} from bisection.

For accuracy the transform is evaluated on centered logs: with L_i = log y_i
and G the mean of the L_i,

    y_i^(lambda) / gdot^(lambda - 1) = gdot * (expm1(lambda (L_i - G)) - expm1(-lambda G)) / lambda,

where gdot = exp(G) is the geometric mean. The second term is a constant
vector; it is dropped when the column space of X contains the constants.
"""

import math
from typing import Sequence

from stdist import chi2_ppf

RANK_TOL = 1e-10
_INV_PHI = (math.sqrt(5.0) - 1.0) / 2.0  # 0.618...


def box_cox(y: Sequence[float], lam: float) -> list[float]:
    """The transform y^(lambda) of each entry; every y_i must be positive."""
    if any(not v > 0.0 for v in y):
        raise ValueError("Box-Cox needs y > 0")
    if lam == 0.0:
        return [math.log(v) for v in y]
    return [math.expm1(lam * math.log(v)) / lam for v in y]


class _Householder:
    """The Householder QR factor of X, kept to compute residual sums of squares."""

    def __init__(self, X: Sequence[Sequence[float]]):
        n = len(X)
        p = len(X[0]) if n else 0
        if n == 0 or p == 0 or any(len(row) != p for row in X):
            raise ValueError("X must be n x p with p >= 1")
        if n <= p:
            raise ValueError("need n > p")
        A = [[float(v) for v in row] for row in X]
        scale = max(math.sqrt(math.fsum(A[i][j] ** 2 for i in range(n))) for j in range(p))
        self.n, self.p = n, p
        self.vs: list[tuple[list[float], float]] = []
        for j in range(p):
            norm = math.sqrt(math.fsum(A[i][j] ** 2 for i in range(j, n)))
            if norm <= RANK_TOL * scale:
                raise ValueError("X does not have full column rank")
            alpha = -norm if A[j][j] >= 0.0 else norm
            v = [0.0] * n
            v[j] = A[j][j] - alpha
            for i in range(j + 1, n):
                v[i] = A[i][j]
            vv = math.fsum(v[i] * v[i] for i in range(j, n))
            for k in range(j, p):
                s = 2.0 * math.fsum(v[i] * A[i][k] for i in range(j, n)) / vv
                for i in range(j, n):
                    A[i][k] -= s * v[i]
            self.vs.append((v, vv))

    def rss(self, z: Sequence[float]) -> float:
        """The residual sum of squares of the least squares fit of z on X."""
        c = list(z)
        n = self.n
        for j, (v, vv) in enumerate(self.vs):
            s = 2.0 * math.fsum(v[i] * c[i] for i in range(j, n)) / vv
            for i in range(j, n):
                c[i] -= s * v[i]
        return math.fsum(c[i] * c[i] for i in range(self.p, n))


class BoxCoxProfile:
    """l(lambda) for fixed y and X, at O(n p) per evaluation after one QR."""

    def __init__(self, y: Sequence[float], X: Sequence[Sequence[float]] | None = None):
        n = len(y)
        if any(not v > 0.0 for v in y):  # @line L1
            raise ValueError("Box-Cox needs y > 0")
        if X is None:
            X = [[1.0] for _ in range(n)]
        if len(X) != n:
            raise ValueError("X and y must have the same number of rows")
        self.n = n
        self.logs = [math.log(v) for v in y]  # @line L2
        self.sum_log = math.fsum(self.logs)
        self.G = self.sum_log / n
        self.centered = [L - self.G for L in self.logs]
        self.qr = _Householder(X)
        # The constant vector is dropped when X spans it.
        self.spans_one = self.qr.rss([1.0] * n) <= (RANK_TOL ** 2) * n
        self.calls = 0

    def loglik(self, lam: float) -> float:
        """-(n/2) log(RSS(lambda)/n) + (lambda - 1) sum log y_i."""  # @line L3
        self.calls += 1
        n = self.n
        if lam == 0.0:
            u = list(self.centered)
            k = self.G
        else:
            u = [math.expm1(lam * d) / lam for d in self.centered]
            k = -math.expm1(-lam * self.G) / lam
        if not self.spans_one:
            u = [ui + k for ui in u]
        rss_u = self.qr.rss(u)
        if rss_u <= 0.0:
            return math.inf
        # RSS(lambda) / gdot^(2 (lambda - 1)) = gdot^2 RSS(u), and gdot = exp(G).
        return -0.5 * n * (math.log(rss_u / n) + 2.0 * self.G)


def _golden_max(f, a: float, b: float, tol: float) -> tuple[float, float]:
    """Golden-section search for a maximum of f on [a, b]; returns (x, f(x))."""
    c = b - _INV_PHI * (b - a)
    d = a + _INV_PHI * (b - a)
    fc, fd = f(c), f(d)
    while b - a > tol:
        if fc >= fd:
            b, d, fd = d, c, fc
            c = b - _INV_PHI * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + _INV_PHI * (b - a)
            fd = f(d)
    return (c, fc) if fc >= fd else (d, fd)


def _bisect_level(f, inside: float, outside: float, target: float, tol: float) -> float:
    """The point between inside (f >= target) and outside (f < target) where f crosses target."""
    while abs(outside - inside) > tol:
        mid = 0.5 * (inside + outside)
        if f(mid) >= target:
            inside = mid
        else:
            outside = mid
    return 0.5 * (inside + outside)


def box_cox_fit(
    y: Sequence[float],
    X: Sequence[Sequence[float]] | None = None,
    lo: float = -2.0,
    hi: float = 2.0,
    grid: int = 81,
    tol: float = 1e-7,
    level: float = 0.95,
):
    """Maximum likelihood lambda on [lo, hi] and its likelihood ratio interval.

    X is the n x p design matrix (default: intercept only). Returns
    (lam_hat, l_max, ci_low, ci_high); ci_low is None when the interval
    reaches past lo, and ci_high is None when it reaches past hi.
    """
    if not lo < hi or grid < 3:
        raise ValueError("need lo < hi and grid >= 3")
    prof = BoxCoxProfile(y, X)
    f = prof.loglik
    lams = [lo + (hi - lo) * j / (grid - 1) for j in range(grid)]
    vals = [f(t) for t in lams]  # @line L4
    k = max(range(grid), key=lambda j: vals[j])
    a = lams[max(k - 1, 0)]
    b = lams[min(k + 1, grid - 1)]
    lam_hat, l_max = _golden_max(f, a, b, tol)  # @line L5
    if vals[k] > l_max:
        lam_hat, l_max = lams[k], vals[k]
    target = l_max - 0.5 * chi2_ppf(level, 1)  # @line L6
    # Lower end: the first grid point below lam_hat with l < target.
    ci_low = None
    inside = lam_hat
    for t, v in zip(reversed(lams), reversed(vals)):  # @line L7
        if t >= lam_hat:
            continue
        if v < target:
            ci_low = _bisect_level(f, inside, t, target, tol)
            break
        inside = t
    ci_high = None
    inside = lam_hat
    for t, v in zip(lams, vals):  # @line L8
        if t <= lam_hat:
            continue
        if v < target:
            ci_high = _bisect_level(f, inside, t, target, tol)
            break
        inside = t
    return lam_hat, l_max, ci_low, ci_high
