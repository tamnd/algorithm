# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/remez-algorithm/. The authors are listed in prov/VZ77TJ.jsonl.

"""Remez exchange algorithm for the best uniform polynomial approximation.

The polynomial is kept in the Chebyshev basis of [a, b] for conditioning.
The search for extrema uses a grid plus golden-section refinement, so the
result is the best approximation up to that search, not a certified one.
"""

import math


def _to_unit(x, a, b):
    return (2.0 * x - a - b) / (b - a)


def cheb_eval(c, t):
    """Clenshaw's recurrence for sum c[k] T_k(t), t in [-1, 1]."""
    b1 = b2 = 0.0
    for ck in reversed(c[1:]):
        b1, b2 = 2.0 * t * b1 - b2 + ck, b1
    return t * b1 - b2 + c[0]


def _solve(m, rhs):
    """Gaussian elimination with partial pivoting; m is square, copied."""
    n = len(m)
    a = [row[:] + [rhs[i]] for i, row in enumerate(m)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(a[r][col]))
        if a[piv][col] == 0.0:
            raise ZeroDivisionError("singular reference system")
        a[col], a[piv] = a[piv], a[col]
        for r in range(col + 1, n):
            f = a[r][col] / a[col][col]
            if f:
                for k in range(col, n + 1):
                    a[r][k] -= f * a[col][k]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = a[i][n] - sum(a[i][j] * x[j] for j in range(i + 1, n))
        x[i] = s / a[i][i]
    return x


def _levelled_fit(f, ref, n, a, b):
    """Solve sum_j c_j T_j(x_i) + (-1)^i h = f(x_i), i = 0..n+1."""
    rows, rhs = [], []
    for i, x in enumerate(ref):
        t = _to_unit(x, a, b)
        row = [math.cos(j * math.acos(max(-1.0, min(1.0, t)))) for j in range(n + 1)]
        rows.append(row + [(-1.0) ** i])
        rhs.append(f(x))
    sol = _solve(rows, rhs)
    return sol[:n + 1], sol[n + 1]


def _golden_max(g, lo, hi, iters=60):
    """Maximize a unimodal g on [lo, hi] by golden-section search."""
    r = (math.sqrt(5.0) - 1.0) / 2.0
    x1, x2 = hi - r * (hi - lo), lo + r * (hi - lo)
    g1, g2 = g(x1), g(x2)
    for _ in range(iters):
        if g1 < g2:
            lo, x1, g1 = x1, x2, g2
            x2 = lo + r * (hi - lo)
            g2 = g(x2)
        else:
            hi, x2, g2 = x2, x1, g1
            x1 = hi - r * (hi - lo)
            g1 = g(x1)
    return (x1, g1) if g1 >= g2 else (x2, g2)


def _alternating_extrema(err, n, a, b, m):
    """Local extrema of err, one per sign run, alternating in sign."""
    xs = [a + (b - a) * k / (m - 1) for k in range(m)]
    es = [err(x) for x in xs]
    runs = []  # (index of largest |e| in the run, sign)
    for k, e in enumerate(es):
        s = 1 if e >= 0 else -1
        if runs and runs[-1][1] == s:
            if abs(e) > abs(es[runs[-1][0]]):
                runs[-1][0] = k
        else:
            runs.append([k, s])
    pts = []
    for k, s in runs:
        if k == 0 or k == m - 1:
            pts.append((xs[k], es[k]))
            continue
        x, _ = _golden_max(lambda x: s * err(x), xs[k - 1], xs[k + 1])
        # keep the grid point if the refinement did not improve it
        pts.append((x, err(x)) if abs(err(x)) >= abs(es[k]) else (xs[k], es[k]))
    return pts


def remez(f, n, a=-1.0, b=1.0, tol=1e-10, max_iter=60, grid=None):
    """Best uniform approximation of degree <= n to f on [a, b].

    Returns (c, E, ref, iterations): Chebyshev coefficients c of p on [a, b]
    (use evaluate(c, x, a, b)), the maximum error E found, the final
    reference of n + 2 points, and the number of iterations.
    """
    if n < 0 or not a < b:
        raise ValueError("need n >= 0 and a < b")
    m = grid or max(2001, 40 * (n + 2))
    # L1: initial reference at the Chebyshev extreme points
    ref = [(a + b) / 2 - (b - a) / 2 * math.cos(math.pi * i / (n + 1))  # @line L1
           for i in range(n + 2)]
    for it in range(1, max_iter + 1):  # @line L2
        c, h = _levelled_fit(f, ref, n, a, b)  # @line L3
        err = lambda x: f(x) - cheb_eval(c, _to_unit(x, a, b))  # @line L4
        pts = _alternating_extrema(err, n, a, b, m)  # @line L5
        emax = max(abs(e) for _, e in pts)
        scale = max(abs(f(x)) for x in ref) or 1.0
        if emax - abs(h) <= tol * emax + 1e-14 * scale:  # @line L6
            return c, emax, ref, it  # @line L7
        g = max(range(len(pts)), key=lambda k: abs(pts[k][1]))
        if len(pts) < n + 2:
            # degenerate reference (for example h = 0 by symmetry): exchange
            # the reference point nearest to the global maximum for it
            xg = pts[g][0]
            j = min(range(n + 2), key=lambda i: abs(ref[i] - xg))
            ref = sorted(ref[:j] + [xg] + ref[j + 1:])
            continue
        # choose n + 2 consecutive alternating points containing the global
        # maximum, preferring the window whose smallest error is largest
        best = None
        for s in range(max(0, g - n - 1), min(g, len(pts) - n - 2) + 1):  # @line L8
            w = pts[s:s + n + 2]
            key = min(abs(e) for _, e in w)
            if best is None or key > best[0]:
                best = (key, s)
        ref = [x for x, _ in pts[best[1]:best[1] + n + 2]]  # @line L9
    return c, emax, ref, max_iter


def evaluate(c, x, a=-1.0, b=1.0):
    """Value at x of the polynomial with Chebyshev coefficients c on [a, b]."""
    return cheb_eval(c, _to_unit(x, a, b))
