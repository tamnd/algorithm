# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-snap-trajectory/. The authors are listed in prov/GASDKD.jsonl.
"""Minimum-snap trajectory of one coordinate through waypoints at fixed times.

min_snap(w, T) takes waypoints w[0..m] and segment durations T[1..m] (a list
of length m), and returns m polynomials of degree 7, one per segment, in
local time t in [0, T_i]. The sum of the integrals of the squared fourth
derivative is minimal among all trajectories that pass through the
waypoints at the given times, start and end at rest (velocity,
acceleration and jerk zero), and have continuous derivatives up to order 3.
It solves the equality constrained quadratic program of Mellinger and
Kumar (2011) through its KKT system.

min_snap_free_derivatives(w, T) solves the same problem by the method of
Richter, Bry and Roy: the unknowns are the free derivatives at the inner
waypoints. Both functions are exact when the inputs are Fraction values.
Several coordinates (x, y, z, yaw) are independent: call once per coordinate.
"""

import math

DEG = 7  # degree of each polynomial
R = 4  # order of the derivative in the cost (snap)
NC = 3  # derivatives 1..NC fixed at the ends and continuous at inner waypoints


def solve(m, b):
    """Solve m x = b by Gauss-Jordan elimination with a nonzero pivot (exact for Fraction)."""
    n = len(m)
    a = [list(m[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        if a[p][c] == 0:
            raise ValueError("singular system")
        a[c], a[p] = a[p], a[c]
        for r in range(n):
            if r != c and a[r][c] != 0:
                f = a[r][c] / a[c][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [a[i][n] / a[i][i] for i in range(n)]


def deriv_row(t, d):
    """Row of the d-th derivative of (1, t, ..., t^DEG) at t."""
    return [math.perm(k, d) * t ** (k - d) if k >= d else 0 * t for k in range(DEG + 1)]


def cost_matrix(T):
    """Q with c^T Q c = integral over [0, T] of the squared R-th derivative."""
    n = DEG + 1
    q = [[0 * T for _ in range(n)] for _ in range(n)]
    for i in range(R, n):
        for j in range(R, n):
            e = i + j - 2 * R + 1
            q[i][j] = math.perm(i, R) * math.perm(j, R) * T ** e / e
    return q


def min_snap(w, T):
    """Coefficient lists (one per segment) of the minimum-snap trajectory, by the KKT system."""
    m = len(T)
    if len(w) != m + 1 or m < 1:
        raise ValueError("need m + 1 waypoints for m segments")
    zero = 0 * T[0]
    n = (DEG + 1) * m
    big_q = [[zero] * n for _ in range(n)]
    for i in range(m):  # @line L1
        qi = cost_matrix(T[i])
        for r in range(DEG + 1):  # @line L2
            for c in range(DEG + 1):
                big_q[8 * i + r][8 * i + c] = qi[r][c]
    rows, rhs = [], []

    def put(seg, vec):
        row = [zero] * n
        for k, x in enumerate(vec):
            row[8 * seg + k] += x
        return row

    for i in range(m):  # @line L3
        rows.append(put(i, deriv_row(zero, 0)))
        rhs.append(w[i])
        rows.append(put(i, deriv_row(T[i], 0)))
        rhs.append(w[i + 1])
    for d in range(1, NC + 1):  # @line L4
        rows.append(put(0, deriv_row(zero, d)))
        rhs.append(zero)
        rows.append(put(m - 1, deriv_row(T[m - 1], d)))
        rhs.append(zero)
    for i in range(m - 1):  # @line L5
        for d in range(1, NC + 1):
            a = put(i, deriv_row(T[i], d))
            b = put(i + 1, deriv_row(zero, d))
            rows.append([x - y for x, y in zip(a, b)])
            rhs.append(zero)
    k = len(rows)
    kkt = [[2 * big_q[i][j] for j in range(n)] + [rows[r][i] for r in range(k)] for i in range(n)]  # @line L6
    kkt += [rows[r] + [zero] * k for r in range(k)]
    sol = solve(kkt, [zero] * n + rhs)
    return [sol[8 * i: 8 * i + 8] for i in range(m)]  # @line L7


def _hermite_inverse(T):
    """Inverse of the map from the 8 coefficients to (p, p', p'', p''') at 0 and at T."""
    m = [deriv_row(0 * T, d) for d in range(4)] + [deriv_row(T, d) for d in range(4)]
    cols = [solve(m, [(1 if i == j else 0) * (T / T) for i in range(8)]) for j in range(8)]
    return [[cols[j][i] for j in range(8)] for i in range(8)]


def min_snap_free_derivatives(w, T):
    """The same trajectory, by optimizing over the free derivatives at the inner waypoints."""
    m = len(T)
    zero = 0 * T[0]
    nv = 4 * (m + 1)  # knot k holds (p, p', p'', p''') at variable 4k .. 4k + 3
    g = [[zero] * nv for _ in range(nv)]
    hinv = []
    for i in range(m):
        minv = _hermite_inverse(T[i])
        hinv.append(minv)
        q = cost_matrix(T[i])
        qm = [[sum(q[r][s] * minv[s][c] for s in range(8)) for c in range(8)] for r in range(8)]
        h = [[sum(minv[s][r] * qm[s][c] for s in range(8)) for c in range(8)] for r in range(8)]
        idx = list(range(4 * i, 4 * i + 8))
        for r in range(8):
            for c in range(8):
                g[idx[r]][idx[c]] += h[r][c]
    fixed = {4 * k: w[k] for k in range(m + 1)}
    for d in range(1, 4):
        fixed[d] = zero
        fixed[4 * m + d] = zero
    free = [v for v in range(nv) if v not in fixed]
    x = dict(fixed)
    if free:
        a = [[g[r][c] for c in free] for r in free]
        b = [-sum(g[r][c] * val for c, val in fixed.items()) for r in free]
        for v, val in zip(free, solve(a, b)):
            x[v] = val
    out = []
    for i in range(m):
        d = [x[v] for v in range(4 * i, 4 * i + 8)]
        out.append([sum(hinv[i][r][c] * d[c] for c in range(8)) for r in range(8)])
    return out


def poly_eval(c, t, d=0):
    """Value at t of the d-th derivative of the polynomial with coefficients c."""
    return sum(x * y for x, y in zip(c, deriv_row(t, d)))


def snap_cost(coeffs, T):
    """Total cost: the sum over segments of c^T Q c."""
    total = 0 * T[0]
    for c, t in zip(coeffs, T):
        q = cost_matrix(t)
        total += sum(c[i] * q[i][j] * c[j] for i in range(8) for j in range(8))
    return total
