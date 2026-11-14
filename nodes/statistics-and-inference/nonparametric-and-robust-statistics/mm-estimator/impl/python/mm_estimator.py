# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mm-estimator/. The authors are listed in prov/MBJNZK.jsonl.

import itertools
import math
import random

# Biweight constants with rho normalized to a maximum of 1.
C0 = 1.54764  # S-step: E rho_C0(Z) = 1/2 at N(0, 1), breakdown point 1/2
B = 0.5
C1 = 4.685  # M-step: 95% efficiency at the normal


def rho(u, c):
    """Biweight rho normalized to max 1: 1 - (1 - (u/c)^2)^3 inside, 1 outside."""
    v = (u / c) ** 2
    if v >= 1.0:
        return 1.0
    return 1.0 - (1.0 - v) ** 3


def weight(u, c):
    """psi(u)/u up to a constant factor: (1 - (u/c)^2)^2 inside, 0 outside."""
    v = (u / c) ** 2
    return 0.0 if v >= 1.0 else (1.0 - v) ** 2


def psi(u, c):
    return u * weight(u, c)


def solve(a, b):
    """Solve the square system a z = b by Gaussian elimination with partial pivoting.

    Returns None if the matrix is singular (to rounding).
    """
    p = len(a)
    m = [list(map(float, row)) + [float(v)] for row, v in zip(a, b)]
    scale = max((abs(v) for row in a for v in row), default=0.0) or 1.0
    for col in range(p):
        piv = max(range(col, p), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) <= 1e-12 * scale:
            return None
        m[col], m[piv] = m[piv], m[col]
        for r in range(col + 1, p):
            f = m[r][col] / m[col][col]
            if f:
                for k in range(col, p + 1):
                    m[r][k] -= f * m[col][k]
    z = [0.0] * p
    for r in range(p - 1, -1, -1):
        z[r] = (m[r][p] - sum(m[r][k] * z[k] for k in range(r + 1, p))) / m[r][r]
    return z


def residuals(x, y, beta):
    return [yi - sum(a * b for a, b in zip(row, beta)) for row, yi in zip(x, y)]


def m_scale(r, c=C0, b=B, iters=200):
    """The M-scale s > 0 with mean(rho_c(r_i / s)) = b, by bisection.

    Returns 0 if at most n b residuals are nonzero (an exact fit of that many points).
    """
    n = len(r)
    nz = [abs(v) for v in r if v != 0]
    if len(nz) <= n * b:  # @line L12
        return 0.0
    lo = min(nz) / c  # h(lo) = len(nz)/n > b
    hi = math.sqrt(3.0 * sum(v * v for v in r) / (n * b)) / c + max(nz)  # h(hi) <= b
    for _ in range(iters):  # @line L13
        mid = (lo + hi) / 2
        if mid in (lo, hi):
            break
        if sum(rho(v / mid, c) for v in r) / n > b:  # @line L14
            lo = mid
        else:
            hi = mid
    return hi


def weighted_ls(x, y, w):
    p = len(x[0])
    a = [[sum(wi * row[i] * row[j] for wi, row in zip(w, x)) for j in range(p)] for i in range(p)]
    rhs = [sum(wi * row[i] * yi for wi, row, yi in zip(w, x, y)) for i in range(p)]
    return solve(a, rhs)


def s_estimate(x, y, subsets=500, seed=0):
    """Approximate S-estimate: the elemental fit with the least M-scale over random p-subsets.

    If subsets is None, all p-subsets are tried.
    """
    n, p = len(x), len(x[0])
    rng = random.Random(seed)
    if subsets is None:
        pool = itertools.combinations(range(n), p)
    else:
        pool = (rng.sample(range(n), p) for _ in range(subsets))
    best = None
    for idx in pool:  # @line L1
        beta = solve([x[i] for i in idx], [y[i] for i in idx])  # @line L2
        if beta is None:
            continue
        s = m_scale(residuals(x, y, beta))  # @line L3
        if best is None or s < best[1]:  # @line L4
            best = (beta, s)
    if best is None:
        raise ValueError("every subset was singular")
    return best


def m_objective(x, y, beta, s, c=C1):
    return sum(rho(v / s, c) for v in residuals(x, y, beta))


def mm_estimate(x, y, subsets=500, seed=0, tol=1e-10, max_iter=500, trace=None):
    """MM-estimate of regression: S-start and M-scale, then biweight IRLS with c = 4.685.

    x is a list of n rows of length p (put a column of ones in it for an intercept).
    Returns (beta, s). If trace is a list, the M-step iterates are appended to it.
    """
    beta, s = s_estimate(x, y, subsets, seed)  # @line L5
    if s == 0:
        return beta, s  # @line L5
    if trace is not None:
        trace.append(beta)
    for _ in range(max_iter):  # @line L6
        r = residuals(x, y, beta)  # @line L7
        w = [weight(v / s, C1) for v in r]  # @line L8
        new = weighted_ls(x, y, w)  # @line L9
        if new is None:
            raise ValueError("the weighted design is singular")
        if trace is not None:
            trace.append(new)
        done = max(abs(a - b) for a, b in zip(new, beta)) <= tol * (1.0 + max(abs(v) for v in beta))
        beta = new  # @line L11
        if done:  # @line L10
            break
    return beta, s


def ols(x, y):
    return weighted_ls(x, y, [1.0] * len(y))
