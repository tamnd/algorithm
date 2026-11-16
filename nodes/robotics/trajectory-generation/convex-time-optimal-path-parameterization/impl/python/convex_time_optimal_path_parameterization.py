# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convex-time-optimal-path-parameterization/. The authors are listed in prov/KKZDAS.jsonl.
"""Time-optimal path parameterization as one convex program (Verscheure,
Demeulenaere, Swevers, De Schutter and Diehl 2009).

Grid s_0 < ... < s_N. Variables b_k = s'^2 at the grid points, with
b_0 = b_N = 0 (rest to rest). The path acceleration a_k = s'' is constant on
[s_k, s_(k+1)], so a_k = (b_(k+1) - b_k) / (2 Delta_k) is eliminated. The
constraint rows (A, B, c, lo, hi) at s_k mean lo <= A a_k + B b_k + c <= hi;
they are linear in b. The traversal time

    T(b) = sum_k 2 Delta_k / (sqrt(b_k) + sqrt(b_(k+1)))

is convex. The program is solved by a log-barrier interior point method:
Newton's method on t T(b) - sum log(slack), with t increased by a factor mu.
Each constraint and each term of T couples only b_k and b_(k+1), so the
Newton system is tridiagonal and costs O(N) to solve (Thomas algorithm).
One Newton step costs O(N m) for m rows per grid point.

The start point b_k = delta must be strictly feasible for a small delta;
this holds when every row is strictly met at zero speed (lo < c < hi).
"""

import math

INF = math.inf


def _constraints(grid, rows):
    """Linear inequalities p * b_k + q * b_(k+1) + r <= 0 over the full vector b."""
    n = len(grid) - 1
    out = []
    for k in range(n):
        d2 = 2.0 * (grid[k + 1] - grid[k])
        for a, bb, c, lo, hi in rows[k]:
            p, q = bb - a / d2, a / d2  # A a_k + B b_k = p b_k + q b_(k+1)
            if hi < INF:
                out.append((k, p, q, c - hi))
            if lo > -INF:
                out.append((k, -p, -q, lo - c))
    for k in range(1, n):
        out.append((k, -1.0, 0.0, 0.0))  # b_k > 0
    return out


def _slacks(cons, b):
    """Values -g_j(b) > 0 for a strictly feasible b, else None."""
    out = []
    for k, p, q, r in cons:
        v = -(p * b[k] + q * b[k + 1] + r)
        if v <= 0.0:
            return None
        out.append(v)
    return out


def traversal_time(grid, b):
    """T(b); infinite if two neighbours are both zero."""
    t = 0.0
    for k in range(len(grid) - 1):
        den = math.sqrt(max(b[k], 0.0)) + math.sqrt(max(b[k + 1], 0.0))
        if den == 0.0:
            return INF
        t += 2.0 * (grid[k + 1] - grid[k]) / den
    return t


def _time_derivs(grid, b):
    """Gradient and tridiagonal Hessian (diag, off) of T with respect to b."""
    n = len(grid) - 1
    g = [0.0] * (n + 1)
    dg = [0.0] * (n + 1)
    off = [0.0] * n  # off[k] couples b_k and b_(k+1)
    for k in range(n):
        w = 2.0 * (grid[k + 1] - grid[k])
        x, y = b[k], b[k + 1]
        if x == 0.0 or y == 0.0:  # one end fixed at 0: w * z^(-1/2)
            j, z = (k + 1, y) if x == 0.0 else (k, x)
            g[j] += -0.5 * w * z ** -1.5
            dg[j] += 0.75 * w * z ** -2.5
            continue
        p, q = math.sqrt(x), math.sqrt(y)
        s = p + q
        g[k] += -w / (2.0 * p * s * s)
        g[k + 1] += -w / (2.0 * q * s * s)
        dg[k] += w * (1.0 / (4.0 * p ** 3 * s * s) + 1.0 / (2.0 * p * p * s ** 3))
        dg[k + 1] += w * (1.0 / (4.0 * q ** 3 * s * s) + 1.0 / (2.0 * q * q * s ** 3))
        off[k] += w / (2.0 * p * q * s ** 3)
    return g, dg, off


def thomas(diag, off, rhs):
    """Solve a symmetric tridiagonal system (diag, off) x = rhs in O(n)."""
    n = len(diag)
    c = [0.0] * n
    d = [0.0] * n
    m = diag[0]
    c[0] = off[0] / m if n > 1 else 0.0
    d[0] = rhs[0] / m
    for i in range(1, n):
        m = diag[i] - off[i - 1] * c[i - 1]
        c[i] = off[i] / m if i < n - 1 else 0.0
        d[i] = (rhs[i] - off[i - 1] * d[i - 1]) / m
    x = [0.0] * n
    x[-1] = d[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d[i] - c[i] * x[i + 1]
    return x


def convex_topp(grid, rows, eps=1e-9, t0=1.0, mu=20.0, newton_tol=1e-9, max_newton=60):
    """Return (b, a, info) with the optimal b_k = s'^2 and a_k = s'', or None.

    The barrier problem for each t is solved until half the squared Newton
    decrement is below newton_tol, or for at most max_newton steps.
    info: {"newton": total Newton steps, "gap": M / t at the end}.
    """
    n = len(grid) - 1
    cons = _constraints(grid, rows)
    m_total = len(cons)
    delta = 1.0
    b = None
    for _ in range(80):  # @line L1
        cand = [0.0] + [delta] * (n - 1) + [0.0]
        if _slacks(cons, cand) is not None:
            b = cand
            break
        delta *= 0.5
    if b is None:
        return None
    t = t0  # @line L2
    steps = 0
    while True:  # @line L3
        inner = 0
        while True:  # @line L4
            slack = _slacks(cons, b)
            g, dg, off = _time_derivs(grid, b)  # @line L5
            grad = [t * v for v in g]
            dia = [t * v for v in dg]
            offd = [t * v for v in off]
            for (k, p, q, r), sl in zip(cons, slack):
                grad[k] += p / sl
                grad[k + 1] += q / sl
                dia[k] += p * p / (sl * sl)
                dia[k + 1] += q * q / (sl * sl)
                offd[k] += p * q / (sl * sl)
            # interior variables 1..n-1 only (b_0 and b_n are fixed)
            step_dir = thomas(dia[1:n], offd[1:n - 1] + [0.0], [-v for v in grad[1:n]])  # @line L6
            lam2 = -sum(gv * dv for gv, dv in zip(grad[1:n], step_dir))  # @line L7
            if lam2 / 2.0 <= newton_tol or inner >= max_newton:
                break
            step = 1.0  # @line L8
            f0 = _barrier_value(grid, cons, b, t)
            while True:
                cand = [0.0] + [b[i] + step * step_dir[i - 1] for i in range(1, n)] + [0.0]
                f1 = _barrier_value(grid, cons, cand, t)
                if f1 is not None and f1 <= f0 - 0.25 * step * lam2:
                    break
                step *= 0.5
                if step < 1e-20:
                    break
            if step < 1e-20:
                break
            b = cand  # @line L9
            steps += 1
            inner += 1
        if m_total / t < eps:  # @line L10
            a = [(b[k + 1] - b[k]) / (2.0 * (grid[k + 1] - grid[k])) for k in range(n)]
            return b, a, {"newton": steps, "gap": m_total / t}
        t *= mu  # @line L11


def _barrier_value(grid, cons, b, t):
    """t T(b) - sum log(slack), or None if b is not strictly feasible."""
    slack = _slacks(cons, b)
    if slack is None:
        return None
    return t * traversal_time(grid, b) - sum(math.log(s) for s in slack)


def max_violation(rows, a, b):
    """Largest amount by which (a_k, b_k) breaks a row, over k < N."""
    worst = 0.0
    for k in range(len(a)):
        for aa, bb, c, lo, hi in rows[k]:
            v = aa * a[k] + bb * b[k] + c
            worst = max(worst, v - hi, lo - v)
    return max(worst, -min(b))


# ---------------------------------------------------------------- examples


def uniform_grid(n):
    return [i / n for i in range(n + 1)]


def single_axis_rows(grid, dist, vmax, amax):
    """q(s) = dist * s with |q'| <= vmax and |q''| <= amax."""
    rows = []
    for _ in grid:
        r = [(dist, 0.0, 0.0, -amax, amax)]
        if vmax < INF:
            r.append((0.0, dist * dist, 0.0, -INF, vmax * vmax))
        rows.append(r)
    return rows


def arm2r_rows(grid, q0, q1, tau_max):
    """Torque rows of the planar 2R arm (unit links, unit end masses, no
    gravity) along q(s) = q0 + s (q1 - q0): tau = M q_s a + C(q, q_s) q_s b."""
    dq = [q1[0] - q0[0], q1[1] - q0[1]]
    rows = []
    for s in grid:
        q2 = q0[1] + s * dq[1]
        c2, s2 = math.cos(q2), math.sin(q2)
        m11, m12 = 3.0 + 2.0 * c2, 1.0 + c2
        aa = [m11 * dq[0] + m12 * dq[1], m12 * dq[0] + dq[1]]
        bb = [-s2 * (2.0 * dq[0] * dq[1] + dq[1] * dq[1]), s2 * dq[0] * dq[0]]
        rows.append([(aa[j], bb[j], 0.0, -tau_max[j], tau_max[j]) for j in range(2)])
    return rows
