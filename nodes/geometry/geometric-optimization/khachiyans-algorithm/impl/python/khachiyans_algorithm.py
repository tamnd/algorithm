# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/khachiyans-algorithm/. The authors are listed in prov/QERG9C.jsonl.

"""Khachiyan's algorithm for an approximate minimum volume enclosing ellipsoid.

This is a numerical method in floating point. The points a_1..a_n in R^d are
lifted to q_i = (a_i, 1) in R^(d+1). The algorithm keeps weights p
on the points and moves weight to the point with the largest
w_i = q_i^T Lambda(p)^-1 q_i, where Lambda(p) = sum p_i q_i q_i^T, until
max w_i <= (1 + eps)(d + 1). The result is an ellipsoid
E = {x : (x - c)^T Q (x - c) <= 1} that contains every point and whose volume
is at most (1 + eps (d + 1) / d)^(d / 2) times the minimum.
"""

import math


def _inverse(m: list) -> list:
    """The inverse of a square matrix by Gauss-Jordan elimination with partial pivoting."""
    n = len(m)
    a = [list(map(float, row)) + [float(i == j) for j in range(n)] for i, row in enumerate(m)]
    scale = max((abs(x) for row in m for x in row), default=0.0) or 1.0
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(a[r][col]))
        if abs(a[piv][col]) <= 1e-12 * scale:
            raise ValueError("the points do not span R^d affinely")
        a[col], a[piv] = a[piv], a[col]
        f = a[col][col]
        a[col] = [x / f for x in a[col]]
        for r in range(n):
            if r != col and a[r][col] != 0.0:
                g = a[r][col]
                a[r] = [x - g * y for x, y in zip(a[r], a[col])]
    return [row[n:] for row in a]


def _quad(m: list, v: list) -> float:
    """v^T m v."""
    return sum(v[i] * sum(m[i][j] * v[j] for j in range(len(v))) for i in range(len(v)))


def _lam(qs: list, p: list) -> list:
    n = len(qs[0])
    lam = [[0.0] * n for _ in range(n)]
    for pi, q in zip(p, qs):
        if pi:
            for r in range(n):
                pr = pi * q[r]
                row = lam[r]
                for s in range(n):
                    row[s] += pr * q[s]
    return lam


def log_det(m: list) -> float:
    """The natural log of the determinant of a symmetric positive definite matrix (Cholesky)."""
    n = len(m)
    low = [[0.0] * n for _ in range(n)]
    total = 0.0
    for i in range(n):
        for j in range(i + 1):
            s = m[i][j] - sum(low[i][k] * low[j][k] for k in range(j))
            if i == j:
                if s <= 0.0:
                    raise ValueError("matrix is not positive definite")
                low[i][i] = math.sqrt(s)
                total += math.log(s)
            else:
                low[i][j] = s / low[j][j]
    return total


def khachiyan(points, eps: float = 1e-3, max_iter: int = 1_000_000, trace: list | None = None):
    """Return (c, Q, p, iterations) for points in R^d that span R^d affinely.

    E = {x : (x - c)^T Q (x - c) <= 1} contains all points, and p are the final
    weights; the points with positive weight form a core set. If trace is a
    list, log det Lambda(p) is appended after each iteration.
    """
    pts = [tuple(map(float, a)) for a in points]
    n = len(pts)
    if n == 0:
        raise ValueError("no points")
    d = len(pts[0])
    d1 = d + 1
    qs = [list(a) + [1.0] for a in pts]  # @line L1
    p = [1.0 / n] * n
    it = 0
    while True:  # @line L2
        lam_inv = _inverse(_lam(qs, p))  # @line L3
        w = [_quad(lam_inv, q) for q in qs]  # @line L4
        j = max(range(n), key=w.__getitem__)
        kappa = w[j]
        if kappa <= (1.0 + eps) * d1 or it >= max_iter:  # @line L5
            break
        beta = (kappa - d1) / (d1 * (kappa - 1.0))  # @line L6
        p = [(1.0 - beta) * pi for pi in p]  # @line L7
        p[j] += beta
        it += 1
        if trace is not None:
            trace.append(log_det(_lam(qs, p)))
    c = [sum(pi * a[k] for pi, a in zip(p, pts)) for k in range(d)]  # @line L8
    s = [[sum(pi * a[r] * a[t] for pi, a in zip(p, pts)) - c[r] * c[t] for t in range(d)] for r in range(d)]
    s_inv = _inverse(s)
    radius2 = max(_quad(s_inv, [a[k] - c[k] for k in range(d)]) for a in pts)
    q = [[x / radius2 for x in row] for row in s_inv]  # @line L9
    return c, q, p, it


def volume_lower_bound_ratio(points, c, q, p) -> float:
    """vol(E) / L, where L <= vol(MVEE) is the weak-duality bound from the weights p.

    For S = sum p_i (a_i - c_p)(a_i - c_p)^T with c_p = sum p_i a_i, every
    enclosing ellipsoid has volume at least omega_d det(d S)^(1/2). The ratio is
    at least vol(E) / vol(MVEE) and at least 1.
    """
    pts = [tuple(map(float, a)) for a in points]
    d = len(pts[0])
    cp = [sum(pi * a[k] for pi, a in zip(p, pts)) for k in range(d)]
    s = [[d * (sum(pi * a[r] * a[t] for pi, a in zip(p, pts)) - cp[r] * cp[t]) for t in range(d)] for r in range(d)]
    # vol(E) = omega_d det(Q)^(-1/2); L = omega_d det(d S)^(1/2)
    return math.exp(-0.5 * log_det(q) - 0.5 * log_det(s))
