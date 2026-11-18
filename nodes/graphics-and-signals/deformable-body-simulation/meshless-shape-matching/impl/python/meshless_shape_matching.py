# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/meshless-shape-matching/. The authors are listed in prov/CV2R4Y.jsonl.

"""Meshless shape matching (Mueller, Heidelberger, Teschner and Gross 2005), in 2D.

A body is a set of particles with masses m_i and rest positions x0_i. In each
step the goal positions are the best rigid (or linear) map of the rest shape
onto the current positions x_i, in the mass weighted least squares sense:

    q_i = x0_i - x0_cm,  p_i = x_i - x_cm,  A_pq = sum m_i p_i q_i^T,
    R = the rotation factor of the polar decomposition of A_pq,
    g_i = G q_i + x_cm  with G = R (rigid) or G = beta A~ + (1 - beta) R (linear),

where A = A_pq (sum m_i q_i q_i^T)^(-1) and A~ = A / sqrt(det A) has det 1 in
2D (if det A <= 0 the code uses R instead of A~). The step is equation (9)
of the paper:

    v_i <- v_i + alpha (g_i - x_i) / dt + dt f_ext,i / m_i,   x_i <- x_i + dt v_i.

The 2D rotation is the closed form of anim.polar, the rotation that maximizes
trace(R^T A_pq). It is always a rotation, also when det A_pq < 0. A step
costs Theta(n) time and the memory is Theta(n) for n particles.
"""

import math

from anim import det, inv, mul, polar

GRAVITY = (0.0, -9.81)


def center(x, m):
    total = sum(m)
    return (sum(mi * p[0] for mi, p in zip(m, x)) / total, sum(mi * p[1] for mi, p in zip(m, x)) / total)


def outer_sum(m, a, b):
    """sum m_i a_i b_i^T as a 2 by 2 list of rows."""
    s = [[0.0, 0.0], [0.0, 0.0]]
    for mi, u, w in zip(m, a, b):
        for r in range(2):
            for c in range(2):
                s[r][c] += mi * u[r] * w[c]
    return s


class RestShape:
    """The rest positions with their center of mass, the vectors q_i and (sum m q q^T)^(-1)."""

    def __init__(self, x0, m):
        self.m = list(m)
        self.cm = center(x0, m)
        self.q = [(p[0] - self.cm[0], p[1] - self.cm[1]) for p in x0]
        self.aqq = inv(outer_sum(self.m, self.q, self.q))


def match(rest, x, mode="rigid", beta=0.0):
    """Return (G, x_cm): the matrix of the goal map and the current center of mass."""
    m = rest.m
    xcm = center(x, m)  # @line L1
    p = [(u[0] - xcm[0], u[1] - xcm[1]) for u in x]
    apq = outer_sum(m, p, rest.q)  # @line L2
    r, _ = polar(apq)  # @line L3
    if mode == "rigid":
        return r, xcm
    a = mul(apq, rest.aqq)
    d = det(a)
    if d <= 0.0:
        a_vol = r
    else:
        s = 1.0 / math.sqrt(d)
        a_vol = [[s * a[0][0], s * a[0][1]], [s * a[1][0], s * a[1][1]]]
    g = [[beta * a_vol[i][j] + (1.0 - beta) * r[i][j] for j in range(2)] for i in range(2)]  # @line L4
    return g, xcm


def goals(rest, x, mode="rigid", beta=0.0):
    g, xcm = match(rest, x, mode, beta)
    return [(g[0][0] * q[0] + g[0][1] * q[1] + xcm[0], g[1][0] * q[0] + g[1][1] * q[1] + xcm[1])
            for q in rest.q]  # @line L5


def step(rest, x, v, alpha, dt, mode="rigid", beta=0.0, gravity=GRAVITY):
    """One step of equation (9). Return (x, v)."""
    g = goals(rest, x, mode, beta)
    v_new = [(u[0] + alpha * (gi[0] - xi[0]) / dt + dt * gravity[0], u[1] + alpha * (gi[1] - xi[1]) / dt + dt * gravity[1])
             for u, gi, xi in zip(v, g, x)]  # @line L6
    x_new = [(xi[0] + dt * u[0], xi[1] + dt * u[1]) for xi, u in zip(x, v_new)]  # @line L7
    return x_new, v_new


def momentum(x, v, m):
    """Return (P_x, P_y, L) with L = sum m x cross v about the origin."""
    px = sum(mi * u[0] for mi, u in zip(m, v))
    py = sum(mi * u[1] for mi, u in zip(m, v))
    ang = sum(mi * (xi[0] * u[1] - xi[1] * u[0]) for mi, xi, u in zip(m, x, v))
    return px, py, ang


def fit_error(rest, x, g):
    """sum m_i |G q_i + x_cm - x_i|^2 for a 2 by 2 matrix G."""
    xcm = center(x, rest.m)
    e = 0.0
    for mi, q, xi in zip(rest.m, rest.q, x):
        gx = g[0][0] * q[0] + g[0][1] * q[1] + xcm[0] - xi[0]
        gy = g[1][0] * q[0] + g[1][1] * q[1] + xcm[1] - xi[1]
        e += mi * (gx * gx + gy * gy)
    return e


def amplification(alpha, dt):
    """The matrix of equation (11) for one particle and a fixed goal, on (v, x - g)."""
    return [[1.0, -alpha / dt], [dt, 1.0 - alpha]]
