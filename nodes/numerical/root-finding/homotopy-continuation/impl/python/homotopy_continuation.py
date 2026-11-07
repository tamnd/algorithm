# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/homotopy-continuation/. The authors are listed in prov/DVD26W.jsonl.

"""Homotopy continuation for square polynomial systems F(x) = 0 in C^n.

The total degree homotopy with the gamma trick is
    H(x, t) = (1 - t) gamma G(x) + t F(x),   G_i(x) = x_i^(d_i) - 1,
where d_i is the degree of F_i. At t = 0 its solutions are the d_1 ... d_n
tuples of roots of unity. Each one is tracked to t = 1 by a predictor
(classical Runge-Kutta on the Davidenko equation H_x dx/dt = -H_t) and a
corrector (Newton's method on H(., t)) with adaptive step size.

Vectors are lists of complex numbers, matrices are lists of rows. F(x)
returns a vector and JF(x) the Jacobian matrix.
"""

import cmath
import itertools
import math
import random
from collections import namedtuple

PathResult = namedtuple("PathResult", "x t steps evals status")
# status: "success" (reached t = 1 and the end point was refined),
#         "singular-end" (the step size collapsed within end_zone of t = 1,
#                         or Newton at t = 1 did not converge fast; typical
#                         for a root of multiplicity m > 1),
#         "diverged" (|x| exceeded the radius: a solution at infinity),
#         "failed" (step size below h_min or step cap reached).


def norm(v):
    return max((abs(c) for c in v), default=0.0)


def solve(A, b):
    """Gaussian elimination with partial pivoting; None if A is singular."""
    n = len(b)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[p][c] == 0:
            return None
        M[c], M[p] = M[p], M[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f != 0:
                for j in range(c, n + 1):
                    M[r][j] -= f * M[c][j]
    x = [0j] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = s / M[i][i]
    return x


def total_degree_homotopy(F, JF, degrees, gamma):
    """H, H_x, H_t and the start solutions of the total degree homotopy."""
    n = len(degrees)

    def G(x):
        return [x[i] ** degrees[i] - 1 for i in range(n)]

    def H(x, t):
        g, f = G(x), F(x)
        return [(1 - t) * gamma * g[i] + t * f[i] for i in range(n)]

    def Hx(x, t):
        J = JF(x)
        return [[(1 - t) * gamma * (degrees[i] * x[i] ** (degrees[i] - 1) if i == j else 0)
                 + t * J[i][j] for j in range(n)] for i in range(n)]

    def Ht(x, t):
        g, f = G(x), F(x)
        return [f[i] - gamma * g[i] for i in range(n)]

    roots = [[cmath.exp(2j * math.pi * k / d) for k in range(d)] for d in degrees]
    starts = [list(s) for s in itertools.product(*roots)]
    return H, Hx, Ht, starts


def _tangent(Hx, Ht, x, t):
    """dx/dt from H_x dx/dt = -H_t; None if H_x is singular."""
    try:
        return solve(Hx(x, t), [-c for c in Ht(x, t)])
    except (OverflowError, ZeroDivisionError):
        return None  # a wild predictor point: the step is rejected


def _newton_step(H, Hx, y, t):
    try:
        return solve(Hx(y, t), [-c for c in H(y, t)])
    except (OverflowError, ZeroDivisionError):
        return None


def rk4_predict(Hx, Ht, x, t, h):
    """One classical Runge-Kutta step for dx/dt = -H_x^-1 H_t; None if singular."""
    k1 = _tangent(Hx, Ht, x, t)
    k2 = k1 and _tangent(Hx, Ht, [a + h / 2 * b for a, b in zip(x, k1)], t + h / 2)
    k3 = k2 and _tangent(Hx, Ht, [a + h / 2 * b for a, b in zip(x, k2)], t + h / 2)
    k4 = k3 and _tangent(Hx, Ht, [a + h * b for a, b in zip(x, k3)], t + h)
    if k4 is None:
        return None
    return [a + h / 6 * (p + 2 * q + 2 * r + s) for a, p, q, r, s in zip(x, k1, k2, k3, k4)]


def track(H, Hx, Ht, x0, h0=0.05, h_min=1e-14, max_steps=20000,
          tol=1e-9, radius=1e6, end_zone=1e-4):
    x, t, h = list(x0), 0.0, h0  # @line L1
    steps = evals = 0
    good = 0
    while t < 1.0:  # @line L2
        if steps >= max_steps:  # @line L9
            return PathResult(x, t, steps, evals, "failed")
        steps += 1
        h = min(h, 1.0 - t)  # @line L3
        y = rk4_predict(Hx, Ht, x, t, h)  # @line L4
        evals += 4
        ok = y is not None
        if ok:
            t1 = 1.0 if h == 1.0 - t else t + h
            ok = False
            prev = None
            for _ in range(3):  # @line L5
                d = _newton_step(H, Hx, y, t1)
                evals += 1
                if d is None:
                    break
                y = [a + b for a, b in zip(y, d)]
                nd = norm(d)
                if prev is None and nd > 1e-3 * (1.0 + norm(y)):
                    break  # predictor too far from the path: reject
                if prev is not None and nd > 0.25 * prev:
                    break  # not contracting fast: reject
                prev = nd
                if nd <= tol * (1.0 + norm(y)):
                    ok = True
                    break
        if ok:  # @line L6
            x, t = y, t1
            good += 1
            if good >= 3:
                h, good = min(2.0 * h, 0.1), 0
            if norm(x) > radius:  # @line L8
                return PathResult(x, t, steps, evals, "diverged")
        else:  # @line L7
            h, good = h / 2.0, 0
            if h < h_min:
                st = "singular-end" if 1.0 - t <= end_zone else "failed"
                return PathResult(x, t, steps, evals, st)
    return PathResult(x, t, steps, evals, "success")  # @line L10


def condition(J):
    """||J^-1|| max(1, ||J||) in the max-norm; infinite if J is singular."""
    n = len(J)
    inv_norm = 0.0
    cols = []
    for j in range(n):
        c = solve(J, [1.0 if i == j else 0.0 for i in range(n)])
        if c is None:
            return math.inf
        cols.append(c)
    inv_norm = max(sum(abs(cols[j][i]) for j in range(n)) for i in range(n))
    j_norm = max(sum(abs(v) for v in row) for row in J)
    return inv_norm * max(1.0, j_norm)


def refine(F, JF, x, tol=1e-14, max_iter=50, cond_max=1e8):
    """Newton's method on F at t = 1; returns (x, settled). The end point is
    settled when Newton converged and the Jacobian there is well conditioned;
    a large condition number signals a root of multiplicity m > 1."""
    prev = None
    for _ in range(max_iter):
        d = solve(JF(x), [-c for c in F(x)])
        if d is None:
            return x, False
        x = [a + b for a, b in zip(x, d)]
        nd = norm(d)
        if nd <= tol * (1.0 + norm(x)):
            return x, condition(JF(x)) <= cond_max
        if prev is not None and nd > 0.9 * prev:
            # stagnation in rounding noise: decide by the conditioning
            return x, condition(JF(x)) <= cond_max
        prev = nd
    return x, False


def solve_system(F, JF, degrees, seed=0, **kw):
    """Track all d_1 ... d_n paths and refine their end points."""
    rng = random.Random(seed)
    gamma = cmath.exp(2j * math.pi * rng.random())
    H, Hx, Ht, starts = total_degree_homotopy(F, JF, degrees, gamma)
    out = []
    for s in starts:
        r = track(H, Hx, Ht, s, **kw)
        if r.status in ("success", "singular-end"):
            x, settled = refine(F, JF, r.x)
            ok = settled and r.status == "success"
            r = r._replace(x=x, status="success" if ok else "singular-end")
        out.append(r)
    return out


def polynomial_roots(a, seed=0, **kw):
    """All roots of a0 x^n + ... + an (a0 != 0) by the homotopy from z^n - 1.

    The variable is scaled, x = s z with s = |an/a0|^(1/n), the geometric
    mean of the root moduli, so that the start roots have the right size.
    A root x = 0 of multiplicity k (k trailing zero coefficients) is split
    off first and returned as k exact paths."""
    a = [complex(c) for c in a]
    if any(math.isnan(abs(c)) or math.isinf(abs(c)) for c in a):
        raise ValueError("coefficients must be finite")
    while a and a[0] == 0:
        a.pop(0)
    if len(a) < 2:
        raise ValueError("need a polynomial of degree at least 1")
    zeros = []
    while len(a) > 1 and a[-1] == 0:
        a.pop()
        zeros.append(PathResult([0j], 1.0, 0, 0, "success"))
    n = len(a) - 1
    if n == 0:
        return zeros
    sc = abs(a[n] / a[0]) ** (1.0 / n)
    b = [a[j] * sc ** (n - j) / (a[0] * sc ** n) for j in range(n + 1)]

    def F(z):
        s = 0j
        for c in b:
            s = s * z[0] + c
        return [s]

    def JF(z):
        s = d = 0j
        for c in b:
            d = d * z[0] + s
            s = s * z[0] + c
        return [[d]]

    res = solve_system(F, JF, [n], seed=seed, **kw)
    return [r._replace(x=[sc * r.x[0]]) for r in res] + zeros
