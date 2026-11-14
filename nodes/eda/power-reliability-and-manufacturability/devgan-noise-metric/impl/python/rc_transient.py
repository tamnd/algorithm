# SPDX-License-Identifier: MIT
# Shared helper of the pr3 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Reference transient solvers for a victim RC tree with coupling capacitors.

The tree uses the layout of devgan_noise_metric.py: parent[k] < k, r[0] is
the driver resistance to ground, r[k] the wire resistance from parent[k] to
k, cground[k] the grounded capacitance and coupling[k] a list of (cc, a).
Kirchhoff's current law at each node gives the linear system

    C v'(t) + G v(t) = B u'(t),

with G the conductance matrix of the tree, C the diagonal matrix of total
node capacitance (ground plus coupling) and B[k][a] the coupling from node
k to aggressor a. The aggressor voltages u_a(t) are ideal sources.

backward_euler: exact rational arithmetic, any aggressor waveform.
ramp_peaks: the exact solution for piecewise linear ramps, by a symmetric
eigendecomposition, with a sampled and refined peak search in floats.
"""

import math


def matrices(parent, r, cground, coupling, aggressors):
    n = len(parent)
    g = [[0] * n for _ in range(n)]
    g[0][0] += 1 / r[0]  # pass Fractions for exact arithmetic
    for k in range(1, n):
        y = 1 / r[k]
        p = parent[k]
        g[k][k] += y
        g[p][p] += y
        g[k][p] -= y
        g[p][k] -= y
    b = [[0] * aggressors for _ in range(n)]
    cap = list(cground)
    for k in range(n):
        for cc, a in coupling[k]:
            b[k][a] += cc
            cap[k] = cap[k] + cc
    return g, cap, b


def solve(a, y):
    """Gaussian elimination with partial pivoting; exact for Fractions."""
    n = len(a)
    m = [list(a[i]) + [y[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(m[i][c]))
        m[c], m[p] = m[p], m[c]
        for i in range(c + 1, n):
            f = m[i][c] / m[c][c]
            if f:
                for j in range(c, n + 1):
                    m[i][j] -= f * m[c][j]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        s = m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))
        x[i] = s / m[i][i]
    return x


def backward_euler(g, cap, b, waves, h, steps):
    """Backward Euler states v_0 = 0, v_1, ..., v_steps at times j h.

    waves[a](t) is the aggressor voltage at time t. Each step solves
    (C + h G) v_{j+1} = C v_j + B (u(t_{j+1}) - u(t_j)).
    """
    n = len(g)
    m = [[h * g[i][j] + (cap[i] if i == j else 0) for j in range(n)] for i in range(n)]
    v = [0] * n
    out = [v]
    u = [w(0) for w in waves]
    for j in range(1, steps + 1):
        un = [w(j * h) for w in waves]
        rhs = [cap[i] * v[i] + sum(b[i][a] * (un[a] - u[a]) for a in range(len(waves))) for i in range(n)]
        v = solve(m, rhs)
        out.append(v)
        u = un
    return out


def _jacobi_eigen(s):
    n = len(s)
    a = [row[:] for row in s]
    q = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(100):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-30:
            break
        for p in range(n):
            for k in range(p + 1, n):
                if abs(a[p][k]) < 1e-300:
                    continue
                theta = (a[k][k] - a[p][p]) / (2 * a[p][k])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                sn = t * c
                for i in range(n):
                    aip, aik = a[i][p], a[i][k]
                    a[i][p], a[i][k] = c * aip - sn * aik, sn * aip + c * aik
                for i in range(n):
                    api, aki = a[p][i], a[k][i]
                    a[p][i], a[k][i] = c * api - sn * aki, sn * api + c * aki
                for i in range(n):
                    qip, qik = q[i][p], q[i][k]
                    q[i][p], q[i][k] = c * qip - sn * qik, sn * qip + c * qik
    return [a[i][i] for i in range(n)], q


def ramp_peaks(g, cap, b, ramps, samples=400):
    """Peak |v_i(t)| over t >= 0 for ramp aggressors, in floats.

    ramps[a] = (start, rise, swing): u_a goes linearly from 0 to swing over
    [start, start + rise] and is constant outside. The solution is exact on
    each interval where all slopes are constant; the peak is found by
    sampling and a golden-section refinement around the best sample.
    """
    n = len(g)
    g = [[float(x) for x in row] for row in g]
    cap = [float(x) for x in cap]
    b = [[float(x) for x in row] for row in b]
    half = [1 / math.sqrt(c) for c in cap]
    s = [[half[i] * g[i][j] * half[j] for j in range(n)] for i in range(n)]
    lam, q = _jacobi_eigen(s)
    events = sorted({0.0} | {float(t0) for t0, _, _ in ramps} | {float(t0 + tr) for t0, tr, _ in ramps})
    tail = 12 / min(lam)

    def to_z(v):
        return [sum(q[i][m] * v[i] / half[i] for i in range(n)) for m in range(n)]

    def to_v(z):
        return [half[i] * sum(q[i][m] * z[m] for m in range(n)) for i in range(n)]

    pieces = []
    v = [0.0] * n
    for idx, t0 in enumerate(events):
        t1 = events[idx + 1] if idx + 1 < len(events) else t0 + tail
        du = [sw / tr if st <= t0 < st + tr else 0.0 for st, tr, sw in ramps]
        f = [sum(b[i][a] * du[a] for a in range(len(ramps))) for i in range(n)]
        w = solve(g, f)
        zw, zj = to_z(w), to_z(v)
        pieces.append((t0, t1, zw, zj))

        def at(t, t0=t0, zw=zw, zj=zj):
            return to_v([zw[m] + math.exp(-lam[m] * (t - t0)) * (zj[m] - zw[m]) for m in range(n)])

        v = at(t1)
        pieces[-1] = (t0, t1, at)
    peak = [0.0] * n
    for i in range(n):
        for t0, t1, at in pieces:
            grid = [t0 + (t1 - t0) * j / samples for j in range(samples + 1)]
            vals = [abs(at(t)[i]) for t in grid]
            j = max(range(len(vals)), key=vals.__getitem__)
            lo, hi = grid[max(j - 1, 0)], grid[min(j + 1, samples)]
            for _ in range(60):
                m1, m2 = lo + (hi - lo) * 0.382, lo + (hi - lo) * 0.618
                if abs(at(m1)[i]) < abs(at(m2)[i]):
                    lo = m1
                else:
                    hi = m2
            peak[i] = max(peak[i], vals[j], abs(at((lo + hi) / 2)[i]))
    return peak
