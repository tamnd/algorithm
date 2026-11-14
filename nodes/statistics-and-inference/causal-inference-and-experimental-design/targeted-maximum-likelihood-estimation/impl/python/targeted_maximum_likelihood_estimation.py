# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/targeted-maximum-likelihood-estimation/. The authors are listed in prov/SKN7EC.jsonl.

"""Targeted maximum likelihood estimation (TMLE) of the average treatment effect.

The outcome y is scaled to [0, 1] (pass bounds=(a, b) for an outcome in
[a, b]). The inputs are the propensities e[i] and initial predictions q1[i] and
q0[i] of E[Y | T = 1, X_i] and E[Y | T = 0, X_i], on the scale of y. The
targeting step fits one number eps along the clever covariate

    H(t, x) = t / e(x) - (1 - t) / (1 - e(x)),

with the logistic fluctuation logit Q*(t, x) = logit Q(t, x) + eps H(t, x), or
the linear fluctuation Q*(t, x) = Q(t, x) + eps H(t, x). The estimate is the
mean of Q*(1, X_i) - Q*(0, X_i). The linear fluctuation is exact for Fraction
inputs; the logistic one is solved by Newton-Raphson in floating point.
"""

import math
from collections.abc import Sequence
from statistics import NormalDist
from typing import NamedTuple


class TMLEResult(NamedTuple):
    tau: object  # the TMLE estimate of E[Y(1) - Y(0)], on the scale of the input y
    mu1: object  # the estimate of E[Y(1)]
    mu0: object  # the estimate of E[Y(0)]
    eps: object  # the fitted fluctuation parameter
    q1_star: list  # the targeted predictions Q*(1, X_i), on the [0, 1] scale for the logistic fluctuation
    q0_star: list  # the targeted predictions Q*(0, X_i)
    se: float  # the influence-function standard error of tau


def _expit(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


def _logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def _check(t, y, e, q1, q0):
    n = len(t)
    if not (n == len(y) == len(e) == len(q1) == len(q0)):
        raise ValueError("t, y, e, q1 and q0 must have the same length")
    if n < 2:
        raise ValueError("need at least two units")
    for ti, ei in zip(t, e):
        if ti not in (0, 1):
            raise ValueError("every treatment must be 0 or 1")
        if not 0 < ei < 1:
            raise ValueError("positivity fails: every propensity must be strictly between 0 and 1")


def clever_covariate(t: Sequence[int], e: Sequence) -> list:
    """H_i = T_i / e_i - (1 - T_i) / (1 - e_i)."""
    return [1 / ei if ti == 1 else -1 / (1 - ei) for ti, ei in zip(t, e)]


def aipw_estimate(t, y, e, q1, q0):
    """The AIPW estimate with outcome predictions q1, q0 (for comparison with TMLE)."""
    n = len(t)
    s = 0
    for ti, yi, ei, a, b in zip(t, y, e, q1, q0):
        s += a - b + (ti * (yi - a) / ei if ti == 1 else -(yi - b) / (1 - ei))
    return s / n


def fluctuate_logistic(y01: Sequence[float], qa: Sequence[float], h: Sequence[float], tol: float = 1e-12, max_iter: int = 100) -> float:
    """Maximize sum y log q + (1 - y) log(1 - q), q = expit(logit qa + eps h), over eps.

    Newton-Raphson on the score U(eps) = sum h (y - q), with step halving on the
    log-likelihood, which is concave in eps. Stops when the step is below
    tol * (1 + |eps|)."""
    off = [_logit(q) for q in qa]

    def loglik(eps):
        s = 0.0
        for yi, oi, hi in zip(y01, off, h):
            z = oi + eps * hi
            # log expit(z) = -log1p(exp(-z)); log(1 - expit(z)) = -log1p(exp(z))
            lp = -math.log1p(math.exp(-z)) if z > -30 else z
            lq = -math.log1p(math.exp(z)) if z < 30 else -z
            s += yi * lp + (1 - yi) * lq
        return s

    eps = 0.0  # @line L2
    cur = loglik(eps)
    for _ in range(max_iter):  # @line L3
        u = 0.0  # @line L4
        info = 0.0
        for yi, oi, hi in zip(y01, off, h):
            q = _expit(oi + eps * hi)
            u += hi * (yi - q)
            info += hi * hi * q * (1 - q)
        if info <= 0:
            raise ArithmeticError("zero information in the fluctuation")
        step = u / info  # @line L5
        new = eps + step
        val = loglik(new)
        halvings = 0
        while val < cur - 1e-15 * abs(cur) and halvings < 60:
            step /= 2
            new = eps + step
            val = loglik(new)
            halvings += 1
        eps, cur = new, val  # @line L6
        if abs(step) < tol * (1 + abs(eps)):  # @line L7
            return eps
    raise ArithmeticError("the fluctuation did not converge; the outcome may be separated by H")


def tmle_ate(t: Sequence[int], y: Sequence, e: Sequence, q1: Sequence, q0: Sequence, bounds: tuple | None = None, fluctuation: str = "logistic") -> TMLEResult:
    """TMLE of the ATE. Cost: Theta(n) per Newton step, Theta(n) for the rest."""
    _check(t, y, e, q1, q0)
    n = len(t)
    h = clever_covariate(t, e)  # @line L1
    if fluctuation == "linear":
        # least squares of the residual y - Q(T, X) on H, no intercept: eps = sum H r / sum H^2
        r = [yi - (a if ti == 1 else b) for ti, yi, a, b in zip(t, y, q1, q0)]
        eps = sum(hi * ri for hi, ri in zip(h, r)) / sum(hi * hi for hi in h)
        s1 = [a + eps / ei for a, ei in zip(q1, e)]
        s0 = [b - eps / (1 - ei) for b, ei in zip(q0, e)]
        scale, shift = 1, 0
        ys = list(y)
    elif fluctuation == "logistic":
        lo, hi_ = bounds if bounds is not None else (0, 1)
        if not lo < hi_:
            raise ValueError("bounds must satisfy a < b")
        scale, shift = hi_ - lo, lo
        ys = [(float(yi) - lo) / scale for yi in y]
        a1 = [(float(v) - lo) / scale for v in q1]
        a0 = [(float(v) - lo) / scale for v in q0]
        if any(not 0 <= v <= 1 for v in ys):
            raise ValueError("an outcome lies outside the bounds")
        if any(not 0 < v < 1 for v in a1 + a0):
            raise ValueError("initial predictions must lie strictly inside the bounds")
        qa = [u if ti == 1 else v for ti, u, v in zip(t, a1, a0)]
        eps = fluctuate_logistic(ys, qa, h)
        s1 = [_expit(_logit(u) + eps / float(ei)) for u, ei in zip(a1, e)]  # @line L8
        s0 = [_expit(_logit(v) - eps / (1 - float(ei))) for v, ei in zip(a0, e)]
    else:
        raise ValueError("fluctuation must be 'logistic' or 'linear'")
    mu1 = sum(s1) / n
    mu0 = sum(s0) / n
    tau01 = mu1 - mu0  # @line L9
    # influence curve on the [0, 1] scale: H (Y - Q*) + Q*(1, X) - Q*(0, X) - tau
    d = [hi * (yi - (u if ti == 1 else v)) + u - v - tau01 for hi, yi, ti, u, v in zip(h, ys, t, s1, s0)]
    var = sum(float(di) ** 2 for di in d) / (n - 1) / n
    se = math.sqrt(var) * float(scale)
    if fluctuation == "logistic":
        return TMLEResult(tau01 * scale, mu1 * scale + shift, mu0 * scale + shift, eps, s1, s0, se)
    return TMLEResult(tau01, mu1, mu0, eps, s1, s0, se)


def tmle_interval(res: TMLEResult, alpha: float = 0.05) -> tuple[float, float]:
    z = NormalDist().inv_cdf(1 - alpha / 2)
    return float(res.tau) - z * res.se, float(res.tau) + z * res.se


# ----------------------------------------------------------------- nuisance fits


def solve(a: list[list], b: list) -> list:
    """Solve a x = b by Gaussian elimination with partial pivoting."""
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
        x[c] = (m[c][k] - sum(m[c][j] * x[j] for j in range(c + 1, k))) / m[c][c]
    return x


def fit_logistic(rows: Sequence[Sequence[float]], y: Sequence[float], tol: float = 1e-10, max_iter: int = 50) -> list[float]:
    """Logistic (or quasi-binomial, for y in [0, 1]) regression by Newton-Raphson."""
    p = len(rows[0])
    b = [0.0] * p
    for _ in range(max_iter):
        grad = [0.0] * p
        hess = [[0.0] * p for _ in range(p)]
        for r, yi in zip(rows, y):
            q = _expit(sum(bj * rj for bj, rj in zip(b, r)))
            w = q * (1.0 - q)
            for i in range(p):
                grad[i] += (yi - q) * r[i]
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


def fit_nuisances(x, t, y01, outcome_features, propensity_features):
    """Propensity by logistic regression; Q(t, x) by logistic regression of y in [0, 1] within each arm."""
    prow = [propensity_features(xi) for xi in x]
    orow = [outcome_features(xi) for xi in x]
    g = fit_logistic(prow, t)
    e = [_expit(sum(gj * rj for gj, rj in zip(g, r))) for r in prow]
    b1 = fit_logistic([r for r, ti in zip(orow, t) if ti == 1], [yi for yi, ti in zip(y01, t) if ti == 1])
    b0 = fit_logistic([r for r, ti in zip(orow, t) if ti == 0], [yi for yi, ti in zip(y01, t) if ti == 0])
    q1 = [_expit(sum(bj * rj for bj, rj in zip(b1, r))) for r in orow]
    q0 = [_expit(sum(bj * rj for bj, rj in zip(b0, r))) for r in orow]
    return e, q1, q0
