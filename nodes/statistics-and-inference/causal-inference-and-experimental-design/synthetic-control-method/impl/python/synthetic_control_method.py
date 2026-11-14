# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/synthetic-control-method/. The authors are listed in prov/1N66SX.jsonl.

"""Synthetic control weights by projected gradient on the simplex.

The treated unit has k pre-period features x1 (outcomes or predictors). The J donors have
the k x J matrix X0 (row r holds feature r for every donor). The weights solve

    minimize f(w) = sum_r v_r (x1_r - sum_j X0[r][j] w_j)^2   subject to w_j >= 0, sum_j w_j = 1,

with feature weights v (all 1 by default). This is a convex quadratic program.

synth runs projected gradient descent with step 1/L in floating point and stops when the
Frank-Wolfe gap g.w - min_j g_j, an upper bound on f(w) - min f, is at most tol. It then
polishes: on the support of w it solves the equality-constrained least squares problem
exactly in the input arithmetic (Fractions stay exact) and keeps the result if it satisfies
the KKT conditions. placebo_pvalue gives the in-space placebo p-value.
"""

from collections.abc import Sequence
from typing import NamedTuple


class SynthResult(NamedTuple):
    w: list  # donor weights, nonnegative, summing to 1
    loss: object  # f(w)
    gap: float  # Frank-Wolfe gap at the end of the gradient phase
    iterations: int
    polished: bool  # True if the KKT polish succeeded


def project_simplex(v: Sequence) -> list:
    """Euclidean projection onto {w : w >= 0, sum w = 1}, by sorting. Exact for Fractions."""
    u = sorted(v, reverse=True)
    css, theta = 0, 0
    for i, a in enumerate(u):
        css += a
        t = (css - 1) / (i + 1)
        if a - t > 0:
            theta = t
    return [max(a - theta, a * 0) for a in v]


def residual(x1, x0, w):
    return [a - sum(r[j] * w[j] for j in range(len(w))) for a, r in zip(x1, x0)]


def loss(x1: Sequence, x0: list[list], w: Sequence, v: Sequence | None = None) -> object:
    v = v if v is not None else [1] * len(x1)
    return sum(vi * e * e for vi, e in zip(v, residual(x1, x0, w)))


def gradient(x1: Sequence, x0: list[list], w: Sequence, v: Sequence | None = None) -> list:
    v = v if v is not None else [1] * len(x1)
    e = residual(x1, x0, w)
    return [-2 * sum(vi * r[j] * ei for vi, r, ei in zip(v, x0, e)) for j in range(len(w))]


def fw_gap(g: Sequence, w: Sequence) -> object:
    """g.w - min_j g_j. For a convex f with gradient g at w, f(w) - min f <= this gap."""
    return sum(a * b for a, b in zip(g, w)) - min(g)


def _solve(a, b):
    k = len(a)
    m = [list(r) + [c] for r, c in zip(a, b)]
    for col in range(k):
        p = max(range(col, k), key=lambda r: abs(m[r][col]))
        if m[p][col] == 0:
            raise ValueError("singular")
        m[col], m[p] = m[p], m[col]
        for r in range(k):
            if r != col and m[r][col] != 0:
                f = m[r][col] / m[col][col]
                for j in range(col, k + 1):
                    m[r][j] -= f * m[col][j]
    return [m[r][k] / m[r][r] for r in range(k)]


def kkt_polish(x1, x0, w, v=None, tol=1e-9):
    """Solve 2 A'VA w_S - nu 1 = 2 A'V x1, 1'w_S = 1 on the support S of w (A = columns S of x0)
    in the input arithmetic. Return the full weight vector if w_S > 0 and every gradient
    entry off S is >= nu; otherwise None."""
    jn = len(w)
    v = v if v is not None else [1] * len(x1)
    one = x1[0] * 0 + 1
    s = [j for j in range(jn) if w[j] > tol]
    m = len(s)
    a = [[2 * sum(vi * r[i] * r[j] for vi, r in zip(v, x0)) for j in s] + [-one] for i in s]
    a.append([one] * m + [one - one])
    b = [2 * sum(vi * r[i] * xi for vi, r, xi in zip(v, x0, x1)) for i in s] + [one]
    try:
        sol = _solve(a, b)
    except ValueError:
        return None
    ws, nu = sol[:m], sol[m]
    if any(c <= 0 for c in ws):
        return None
    full = [one - one] * jn
    for j, c in zip(s, ws):
        full[j] = c
    g = gradient(x1, x0, full, v)
    if any(g[j] < nu - tol * (1 + abs(nu)) for j in range(jn) if j not in s):
        return None
    return full


def synth(
    x1: Sequence, x0: list[list], v: Sequence | None = None, tol: float = 1e-10, max_iter: int = 50000, check_every: int = 20
) -> SynthResult:
    """Synthetic control weights. Cost per iteration: Theta(k J + J log J). Every check_every
    iterations the KKT system on the current support is tried in floating point; once the
    support is right it succeeds and the loop stops before the gap reaches tol."""
    k, jn = len(x1), len(x0[0])
    if len(x0) != k or any(len(r) != jn for r in x0):
        raise ValueError("x0 must be k x J with k = len(x1)")
    vf = [float(a) for a in v] if v is not None else [1.0] * k
    xf1 = [float(a) for a in x1]
    xf0 = [[float(a) for a in r] for r in x0]
    w = [1.0 / jn] * jn  # @line L1
    lip = 2 * sum(vi * a * a for vi, r in zip(vf, xf0) for a in r) or 1.0
    it, gap = 0, float("inf")
    while it < max_iter:  # @line L2
        g = gradient(xf1, xf0, w, vf)  # @line L3
        gap = fw_gap(g, w)  # @line L4
        if gap <= tol * (1 + loss(xf1, xf0, w, vf)) or (it % check_every == check_every - 1 and kkt_polish(xf1, xf0, w, vf) is not None):  # @line L5
            break
        w = project_simplex([a - b / lip for a, b in zip(w, g)])  # @line L6
        it += 1
    exact = kkt_polish(x1, x0, w, v)  # @line L7
    if exact is not None:
        return SynthResult(exact, loss(x1, x0, exact, v), gap, it, True)  # @line L8
    return SynthResult(w, loss(xf1, xf0, w, vf), gap, it, False)


def gaps(y1: Sequence, y0: list[list], w: Sequence) -> list:
    """Treated minus synthetic outcome for each period (rows of y0 are periods)."""
    return residual(y1, y0, w)


def rmspe(e: Sequence) -> float:
    return (sum(float(a) ** 2 for a in e) / len(e)) ** 0.5


def placebo_pvalue(pre: list[list], post: list[list], v: Sequence | None = None) -> tuple:
    """In-space placebo test. pre[t][u] and post[t][u] are outcomes of unit u (unit 0 treated).
    Each unit in turn is fitted from the others on the pre periods; its statistic is post RMSPE
    over pre RMSPE. Returns (p, ratios) with p = #{u : ratio_u >= ratio_0} / (J + 1)."""
    units = len(pre[0])
    ratios = []
    for u in range(units):
        others = [j for j in range(units) if j != u]
        x1 = [r[u] for r in pre]
        x0 = [[r[j] for j in others] for r in pre]
        res = synth(x1, x0, v)
        e_pre = residual(x1, x0, res.w)
        e_post = residual([r[u] for r in post], [[r[j] for j in others] for r in post], res.w)
        rp = rmspe(e_pre)
        ratios.append(rmspe(e_post) / rp if rp > 0 else float("inf"))
    p = sum(1 for a in ratios if a >= ratios[0]) / units
    return p, ratios
