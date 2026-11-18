# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimization-time-integration/. The authors are listed in prov/VE7FP8.jsonl.

"""Optimization time integration (Gast, Schroeder, Stomakhin, Jiang and Teran 2015) on a 2D spring chain.

The backward Euler step x_{n+1} = x_n + dt v_{n+1}, M (v_{n+1} - v_n) = dt f(x_{n+1})
is the minimizer of

    E(x) = 1/(2 dt^2) (x - xh)^T M (x - xh) + Phi(x),  xh = x_n + dt v_n,

where Phi is the potential energy, here springs plus gravity. The solver is
Newton's method with the safeguards of Section 3.1 of Gast and Schroeder
(2014): stop when |grad E| < tau; if the Newton direction d is not clearly
downhill (d . g >= -kappa |d| |g|, kappa = 1e-2), try -d, and else use -g;
clamp the length of d; then do a line search. The paper uses conjugate
gradients and a strong Wolfe line search; this code uses a dense solve and a
backtracking Armijo line search.
"""

import math

GRAVITY = (0.0, -9.81)


def gauss_solve(a, b):
    """Solve a x = b by Gaussian elimination with partial pivoting. Return None if a is singular."""
    n = len(b)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[piv][c]) < 1e-300:
            return None
        m[c], m[piv] = m[piv], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            if f != 0.0:
                for k in range(c, n + 1):
                    m[r][k] -= f * m[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][k] * x[k] for k in range(r + 1, n))) / m[r][r]
    return x


class Chain:
    def __init__(self, rest, springs, masses, pinned=(), gravity=GRAVITY):
        """springs are tuples (a, b, rest_length, stiffness). rest_length 0 gives a linear spring."""
        self.rest = [tuple(p) for p in rest]
        self.springs = [tuple(s) for s in springs]
        self.mass = list(masses)
        self.pinned = set(pinned)
        self.free = [i for i in range(len(rest)) if i not in self.pinned]
        self.col = {v: k for k, v in enumerate(self.free)}
        self.g = gravity


def potential(ch, x):
    e = 0.0
    for a, b, r, k in ch.springs:
        e += 0.5 * k * (math.dist(x[a], x[b]) - r) ** 2
    for i in ch.free:
        e -= ch.mass[i] * (ch.g[0] * x[i][0] + ch.g[1] * x[i][1])
    return e


def potential_grad_hess(ch, x):
    """The gradient and Hessian of Phi on the free coordinates (no projection)."""
    nf = 2 * len(ch.free)
    g = [0.0] * nf
    h = [[0.0] * nf for _ in range(nf)]
    for i in ch.free:
        g[2 * ch.col[i]] -= ch.mass[i] * ch.g[0]
        g[2 * ch.col[i] + 1] -= ch.mass[i] * ch.g[1]
    for a, b, r, k in ch.springs:
        dx, dy = x[a][0] - x[b][0], x[a][1] - x[b][1]
        ln = math.hypot(dx, dy)
        if r == 0.0:
            gs = (k * dx, k * dy)
            blk = [[k, 0.0], [0.0, k]]
        else:
            n = (dx / ln, dy / ln)
            gs = (k * (ln - r) * n[0], k * (ln - r) * n[1])
            s = 1.0 - r / ln
            blk = [[k * (n[p] * n[q] + s * ((1.0 if p == q else 0.0) - n[p] * n[q])) for q in range(2)] for p in range(2)]
        for v, sv in ((a, 1.0), (b, -1.0)):
            if v not in ch.col:
                continue
            for p in range(2):
                g[2 * ch.col[v] + p] += sv * gs[p]
            for u, su in ((a, 1.0), (b, -1.0)):
                if u in ch.col:
                    for p in range(2):
                        for q in range(2):
                            h[2 * ch.col[v] + p][2 * ch.col[u] + q] += sv * su * blk[p][q]
    return g, h


def objective(ch, x, xh, dt):
    e = potential(ch, x)
    for i in ch.free:
        e += ch.mass[i] / (2.0 * dt * dt) * ((x[i][0] - xh[i][0]) ** 2 + (x[i][1] - xh[i][1]) ** 2)
    return e


def objective_grad_hess(ch, x, xh, dt):
    g, h = potential_grad_hess(ch, x)
    for i in ch.free:
        c = ch.mass[i] / (dt * dt)
        for d in range(2):
            r = 2 * ch.col[i] + d
            g[r] += c * (x[i][d] - xh[i][d])
            h[r][r] += c
    return g, h


def moved(ch, x, d, t):
    y = list(x)
    for i in ch.free:
        c = ch.col[i]
        y[i] = (x[i][0] + t * d[2 * c], x[i][1] + t * d[2 * c + 1])
    return y


def oti_step(ch, x, v, dt, tau=1e-6, kappa=1e-2, max_len=1e3, max_iter=100, safeguards=True, history=None):
    """One backward Euler step by minimizing E with safeguarded Newton. Return (x, v, iterations)."""
    xh = [(p[0] + dt * u[0], p[1] + dt * u[1]) if i in ch.col else tuple(p)
          for i, (p, u) in enumerate(zip(x, v))]  # @line L1
    g0, _ = potential_grad_hess(ch, x)
    z = moved(ch, xh, [-dt * dt * gi / ch.mass[ch.free[k // 2]] for k, gi in enumerate(g0)], 1.0)  # @line L2
    e = objective(ch, z, xh, dt)
    if history is not None:
        history.append(e)
    it = 0
    while it < max_iter:  # @line L3
        g, h = objective_grad_hess(ch, z, xh, dt)  # @line L4
        gn = math.sqrt(sum(c * c for c in g))
        if gn < tau:  # @line L5
            break
        d = gauss_solve(h, [-c for c in g])  # @line L6
        if safeguards:
            if d is None:
                d = [-c for c in g]
            dn = math.sqrt(sum(c * c for c in d))
            if sum(a * b for a, b in zip(d, g)) >= -kappa * dn * gn:  # @line L7
                d = [-c for c in d]
                if sum(a * b for a, b in zip(d, g)) >= -kappa * dn * gn:
                    d = [-c for c in g]
            dn = math.sqrt(sum(c * c for c in d))
            if dn > max_len:  # @line L8
                d = [c * max_len / dn for c in d]
            slope = sum(a * b for a, b in zip(d, g))
            if -slope <= 1e-15 * (1.0 + abs(e)):
                break  # the predicted decrease is below the rounding level of E
            t = 1.0
            while True:  # @line L9
                trial = moved(ch, z, d, t)
                et = objective(ch, trial, xh, dt)
                if et <= e + 1e-4 * t * slope or t < 1e-14:
                    break
                t *= 0.5
            if t < 1e-14:
                break  # no sufficient decrease is possible at the level of rounding: keep z
        else:
            if d is None:
                break
            trial = moved(ch, z, d, 1.0)
            et = objective(ch, trial, xh, dt)
        z, e = trial, et  # @line L10
        if history is not None:
            history.append(e)
        it += 1
    v_new = [((a[0] - b[0]) / dt, (a[1] - b[1]) / dt) for a, b in zip(z, x)]  # @line L11
    return z, v_new, it


def total_energy(ch, x, v):
    return potential(ch, x) + sum(0.5 * ch.mass[i] * (v[i][0] ** 2 + v[i][1] ** 2) for i in ch.free)


def hanging_chain(count, spacing, stiffness, mass, rest_zero=False):
    """A horizontal chain pinned at particle 0. rest_zero gives linear springs (a convex potential)."""
    rest = [(i * spacing, 0.0) for i in range(count)]
    r = 0.0 if rest_zero else spacing
    springs = [(i, i + 1, r, stiffness) for i in range(count - 1)]
    return Chain(rest, springs, [mass] * count, pinned=[0])
