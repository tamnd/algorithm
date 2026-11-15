# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-mpc/. The authors are listed in prov/1PY7EN.jsonl.

"""Hybrid MPC for a small piecewise affine (PWA) system, by enumeration of
the mode sequences and one convex QP per sequence.

A PWA system is a list of modes. A mode is a dict with the keys
"A" (n by n), "B" (n by m), "f" (n), "H" (q by n) and "h" (q). In mode i the
dynamics are x+ = A x + B u + f, and the mode is active on the closed cell
{x : H x <= h}. The cells must cover the state set and may only share
boundary points.

At each sampling instant the controller solves

    min  sum_{k=0}^{N-1} (x_k' Q x_k + u_k' R u_k) + x_N' P x_N
    s.t. x_0 = the measured state, x_{k+1} = the PWA dynamics,
         umin <= u_k <= umax, xmin <= x_k <= xmax for k = 1, ..., N,

and applies u_0. This is a mixed-integer QP. For a fixed mode sequence
(sigma_0, ..., sigma_{N-1}) the states are affine in U = (u_0, ..., u_{N-1}),
and the problem is a convex QP in N m variables with 2 N m input bounds,
2 N n state bounds and the cell rows of x_1, ..., x_{N-1}. The code solves
all s^N of them (s modes) with the dual active-set method of Goldfarb and
Idnani (1983) and keeps the best. This is exact but exponential in N; real
solvers use branch and bound on the mixed logical dynamical (MLD) form.

pwa_to_mld writes the same PWA system as big-M inequalities in the binary
variables delta_i (mode i is on) and the real variables z_i (the next state
if mode i is on), as in Bemporad and Morari (1999).
"""

import itertools
import math

from ctlmat import inv, matvec, mul, solve, transpose

__all__ = [
    "qp_solve", "qp_cost", "predict", "condense", "mpc_step", "pwa_step",
    "mode_of", "closed_loop", "pwa_to_mld", "mld_rows_hold", "rotation_example",
]


# ---------------------------------------------------------------- the QP solver

def qp_cost(h, f, x):
    """Return 1/2 x' H x + f' x."""
    hx = matvec(h, x)
    return 0.5 * sum(a * b for a, b in zip(x, hx)) + sum(a * b for a, b in zip(f, x))


def qp_solve(h, f, c, b, tol=1e-9, max_iter=500):
    """Solve min 1/2 x' H x + f' x subject to C x <= b, for H positive definite.

    Goldfarb-Idnani dual active-set method. It starts at the unconstrained
    minimum and adds the most violated constraint; a partial step drops an
    active constraint whose multiplier would become negative. Returns
    (x, lam) with H x + f + C' lam = 0, lam >= 0 and lam_i = 0 off the
    active set, or None if the constraints have no common point.
    """
    n = len(f)
    hinv = inv([[float(v) for v in row] for row in h])
    x = [-v for v in matvec(hinv, f)]
    normals = [[-v for v in row] for row in c]  # n_i . x + b_i >= 0 is row i
    scale = [math.sqrt(sum(v * v for v in row)) or 1.0 for row in c]
    active, u = [], []
    for _ in range(max_iter):
        slack = [sum(a * xi for a, xi in zip(nr, x)) + bi for nr, bi in zip(normals, b)]
        viol = [(s / sc, i) for i, (s, sc) in enumerate(zip(slack, scale)) if s < -tol * sc and i not in active]
        if not viol:
            lam = [0.0] * len(c)
            for i, ui in zip(active, u):
                lam[i] = ui
            return x, lam
        _, p = min(viol)
        u_plus = u + [0.0]
        npv = normals[p]
        while True:
            hn = matvec(hinv, npv)
            if active:
                nmat = [normals[i] for i in active]
                gram = [[sum(a * bb for a, bb in zip(ni, matvec(hinv, nj))) for nj in nmat] for ni in nmat]
                r = solve(gram, [sum(a * bb for a, bb in zip(ni, hn)) for ni in nmat])
                z = matvec(hinv, [npv[k] - sum(r[j] * nmat[j][k] for j in range(len(active))) for k in range(n)])
            else:
                r, z = [], hn
            t1, drop = math.inf, None
            for j, rj in enumerate(r):
                if rj > tol and u_plus[j] / rj < t1:
                    t1, drop = u_plus[j] / rj, j
            zn = sum(a * bb for a, bb in zip(z, npv))
            sp = sum(a * xi for a, xi in zip(npv, x)) + b[p]
            ref = sum(a * bb for a, bb in zip(npv, hn))
            t2 = -sp / zn if zn > 1e-12 * ref else math.inf
            t = min(t1, t2)
            if t == math.inf:
                return None
            for j in range(len(r)):
                u_plus[j] -= t * r[j]
            u_plus[-1] += t
            if t2 < math.inf:
                x = [xi + t * zi for xi, zi in zip(x, z)]
            if t2 <= t1:
                active.append(p)
                u = u_plus
                break
            del active[drop]
            del u_plus[drop]
    raise RuntimeError("qp_solve: no convergence")


# ---------------------------------------------------------------- PWA model

def mode_of(modes, x, tol=0.0):
    """Return the first mode whose cell holds x."""
    for i, md in enumerate(modes):
        if all(sum(a * v for a, v in zip(row, x)) <= hi + tol for row, hi in zip(md["H"], md["h"])):
            return i
    raise ValueError("mode_of: x is in no cell")


def pwa_step(modes, x, u, mode=None):
    """Return x+ = A x + B u + f of the mode of x (or of the given mode)."""
    md = modes[mode_of(modes, x) if mode is None else mode]
    return [ax + bu + fi for ax, bu, fi in zip(matvec(md["A"], x), matvec(md["B"], u), md["f"])]


def predict(modes, x0, us, seq):
    """States x_0, ..., x_N under the mode sequence seq (cells not checked)."""
    xs = [list(x0)]
    for u, s in zip(us, seq):
        xs.append(pwa_step(modes, xs[-1], u, mode=s))
    return xs


def condense(modes, seq, x0):
    """Return lists phi_d, gam: x_k = d_k + Gam_k U for k = 0, ..., N.

    d_k is the free response under the modes of seq (with the affine terms),
    and Gam_k is n by N m.
    """
    n = len(x0)
    m = len(modes[0]["B"][0])
    big = len(seq) * m
    d = [list(map(float, x0))]
    gam = [[[0.0] * big for _ in range(n)]]
    for k, s in enumerate(seq):
        md = modes[s]
        a = md["A"]
        d.append([v + fi for v, fi in zip(matvec(a, d[-1]), md["f"])])
        g = mul(a, gam[-1])
        for i in range(n):
            for j in range(m):
                g[i][k * m + j] += md["B"][i][j]
        gam.append(g)
    return d, gam


def _quad(q, x):
    return sum(x[i] * q[i][j] * x[j] for i in range(len(x)) for j in range(len(x)))


def mpc_step(modes, x0, horizon, q, r, p, umin, umax, xmin=None, xmax=None, sequences=None):
    """Return (U, seq, J): the optimal input sequence, its mode sequence and its cost.

    Returns None if no mode sequence is feasible. sequences, if given,
    restricts the search to these mode sequences.
    """
    n = len(x0)
    m = len(modes[0]["B"][0])
    big = horizon * m
    if sequences is None:
        sequences = itertools.product(range(len(modes)), repeat=horizon)
    best = None  # @line L1
    for seq in sequences:  # @line L2
        md0 = modes[seq[0]]
        if any(sum(a * v for a, v in zip(row, x0)) > hi for row, hi in zip(md0["H"], md0["h"])):
            continue  # @line L3
        d, gam = condense(modes, seq, x0)  # @line L4
        hmat = [[0.0] * big for _ in range(big)]
        fvec = [0.0] * big
        const = 0.0
        for k in range(horizon + 1):
            w = p if k == horizon else q
            gt = transpose(gam[k])
            hmat = [[a + 2 * bb for a, bb in zip(ra, rb)] for ra, rb in zip(hmat, mul(mul(gt, w), gam[k]))]
            fvec = [a + 2 * bb for a, bb in zip(fvec, matvec(gt, matvec(w, d[k])))]
            const += _quad(w, d[k])
        for k in range(horizon):
            for i in range(m):
                for j in range(m):
                    hmat[k * m + i][k * m + j] += 2 * r[i][j]
        rows, rhs = [], []
        for k in range(horizon):
            for j in range(m):
                e = [0.0] * big
                e[k * m + j] = 1.0
                rows.append(e)
                rhs.append(umax[j])
                rows.append([-v for v in e])
                rhs.append(-umin[j])
        for k in range(1, horizon + 1):
            if k < horizon:
                md = modes[seq[k]]
                for row, hi in zip(md["H"], md["h"]):
                    rows.append([sum(row[i] * gam[k][i][j] for i in range(n)) for j in range(big)])
                    rhs.append(hi - sum(a * v for a, v in zip(row, d[k])))
            if xmax is not None:
                for i in range(n):
                    rows.append(list(gam[k][i]))
                    rhs.append(xmax[i] - d[k][i])
                    rows.append([-v for v in gam[k][i]])
                    rhs.append(d[k][i] - xmin[i])
        sol = qp_solve(hmat, fvec, rows, rhs)  # @line L5
        if sol is None:
            continue
        cost = qp_cost(hmat, fvec, sol[0]) + const
        if best is None or cost < best[2]:  # @line L6
            best = (sol[0], seq, cost)
    return best  # @line L7


def closed_loop(modes, x0, steps, horizon, q, r, p, umin, umax, xmin=None, xmax=None):
    """Apply u_0 of mpc_step to the true PWA system for the given number of steps.

    Returns (xs, us). Stops early if a step is infeasible.
    """
    m = len(modes[0]["B"][0])
    xs, us = [list(x0)], []
    for _ in range(steps):
        res = mpc_step(modes, xs[-1], horizon, q, r, p, umin, umax, xmin, xmax)
        if res is None:
            break
        u0 = res[0][:m]  # @line L8
        us.append(u0)
        xs.append(pwa_step(modes, xs[-1], u0))  # @line L9
    return xs, us


# ---------------------------------------------------------------- MLD form

def _range(row, lo, hi):
    """Min and max of row . v over the box lo <= v <= hi."""
    a = sum(c * (l if c >= 0 else h) for c, l, h in zip(row, lo, hi))
    b = sum(c * (h if c >= 0 else l) for c, l, h in zip(row, lo, hi))
    return a, b


def pwa_to_mld(modes, xlo, xhi, ulo, uhi):
    """Big-M MLD form of a PWA system on the box xlo <= x <= xhi, ulo <= u <= uhi.

    Variables w = (x, u, delta_1..delta_s, z_1..z_s), with z_i in R^n. Returns
    (rows, eq): rows is a list of (a, b) meaning a . w <= b, and eq is the
    row of sum delta_i = 1. The next state is x+ = z_1 + ... + z_s.
    For each mode i:
      H_i x - h_i <= M (1 - delta_i)            (delta_i = 1 forces the cell)
      mlo delta_i <= z_i <= mhi delta_i         (delta_i = 0 forces z_i = 0)
      g_i - mhi (1 - delta_i) <= z_i <= g_i - mlo (1 - delta_i),
    where g_i = A_i x + B_i u + f_i and [mlo, mhi] bounds g_i on the box.
    """
    n, m, s = len(xlo), len(ulo), len(modes)
    width = n + m + s + s * n
    lo, hi = list(xlo) + list(ulo), list(xhi) + list(uhi)
    rows = []

    def row():
        return [0.0] * width

    for i, md in enumerate(modes):
        di = n + m + i
        for hrow, hval in zip(md["H"], md["h"]):
            big_m = max(0.0, _range(list(hrow) + [0.0] * m, lo, hi)[1] - hval)
            a = row()
            a[:n] = [float(v) for v in hrow]
            a[di] = big_m
            rows.append((a, hval + big_m))
        for k in range(n):
            g = [float(v) for v in md["A"][k]] + [float(v) for v in md["B"][k]]
            mlo, mhi = _range(g, lo, hi)
            mlo, mhi = mlo + md["f"][k], mhi + md["f"][k]
            zk = n + m + s + i * n + k
            a = row()
            a[zk], a[di] = 1.0, -mhi
            rows.append((a, 0.0))
            a = row()
            a[zk], a[di] = -1.0, mlo
            rows.append((a, 0.0))
            a = row()
            a[:n + m] = [-v for v in g]
            a[zk], a[di] = 1.0, -mlo
            rows.append((a, md["f"][k] - mlo))
            a = row()
            a[:n + m] = g
            a[zk], a[di] = -1.0, mhi
            rows.append((a, mhi - md["f"][k]))
    eq = [0.0] * (n + m) + [1.0] * s + [0.0] * (s * n)
    return rows, eq


def mld_rows_hold(rows, w, tol=1e-9):
    """Return True if every row a . w <= b holds within tol."""
    return all(sum(ai * wi for ai, wi in zip(a, w)) <= b + tol for a, b in rows)


# ---------------------------------------------------------------- the example

def rotation_example(rho=0.8, angle=math.pi / 3):
    """Two modes: x+ = rho R(+angle) x + [0, 1]' u if x_1 >= 0, rho R(-angle) x + [0, 1]' u if x_1 <= 0."""
    def rot(t):
        return [[rho * math.cos(t), -rho * math.sin(t)], [rho * math.sin(t), rho * math.cos(t)]]
    b = [[0.0], [1.0]]
    return [
        {"A": rot(angle), "B": b, "f": [0.0, 0.0], "H": [[-1.0, 0.0]], "h": [0.0]},
        {"A": rot(-angle), "B": b, "f": [0.0, 0.0], "H": [[1.0, 0.0]], "h": [0.0]},
    ]
