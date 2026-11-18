# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/small-steps-physics/. The authors are listed in prov/R4RWDE.jsonl.

"""Small steps (Macklin et al. 2019): split a frame into substeps with one XPBD iteration each.

A frame of length dt is split into n substeps of length h = dt / n. Each
substep predicts the positions with the external force, runs a number of
Gauss-Seidel iterations over the distance constraints with the XPBD update

    dlambda = (-C - alpha~ lambda) / (w_a + w_b + alpha~),  alpha~ = alpha / h^2,

(equation (7) of the paper) and sets v = (x - x_prev) / h. With the same total
number of constraint sweeps per frame, the code compares many iterations in
one step against many substeps with one iteration each. The chain is 2D and
hangs from a pinned first particle.
"""

import math

GRAVITY = (0.0, -9.81)


def chain(count, spacing, masses=None, alpha=0.0):
    """A horizontal chain from the origin; particle 0 is pinned (inverse mass 0)."""
    x = [(i * spacing, 0.0) for i in range(count)]
    m = list(masses) if masses is not None else [1.0] * count
    w = [0.0] + [1.0 / mi for mi in m[1:]]
    cons = [(i, i + 1, spacing, alpha) for i in range(count - 1)]
    return x, w, cons


def solve_constraints(x, w, cons, lam, h):
    """One Gauss-Seidel sweep of XPBD distance constraints."""
    for k, (a, b, rest, alpha) in enumerate(cons):
        dx, dy = x[a][0] - x[b][0], x[a][1] - x[b][1]
        ln = math.hypot(dx, dy)
        wsum = w[a] + w[b]
        at = alpha / (h * h)
        if ln == 0.0 or wsum + at == 0.0:
            continue
        c = ln - rest
        dl = (-c - at * lam[k]) / (wsum + at)  # @line L7
        lam[k] += dl
        n = (dx / ln, dy / ln)
        x[a] = (x[a][0] + w[a] * dl * n[0], x[a][1] + w[a] * dl * n[1])  # @line L8
        x[b] = (x[b][0] - w[b] * dl * n[0], x[b][1] - w[b] * dl * n[1])


def frame(x, v, w, cons, dt, substeps, iterations, gravity=GRAVITY):
    """Advance one frame. Return (x, v)."""
    h = dt / substeps  # @line L1
    x, v = list(x), list(v)
    for _ in range(substeps):  # @line L2
        prev = list(x)
        for i in range(len(x)):
            if w[i] > 0.0:
                v[i] = (v[i][0] + h * gravity[0], v[i][1] + h * gravity[1])  # @line L3
                x[i] = (x[i][0] + h * v[i][0], x[i][1] + h * v[i][1])  # @line L4
        lam = [0.0] * len(cons)  # @line L5
        for _ in range(iterations):  # @line L6
            solve_constraints(x, w, cons, lam, h)
        v = [((a[0] - b[0]) / h, (a[1] - b[1]) / h) for a, b in zip(x, prev)]  # @line L9
    return x, v


def simulate(x, v, w, cons, dt, frames, substeps, iterations, gravity=GRAVITY):
    for _ in range(frames):
        x, v = frame(x, v, w, cons, dt, substeps, iterations, gravity)
    return x, v


def stretch(x, cons):
    """The largest relative constraint error |l - r| / r."""
    return max(abs(math.dist(x[a], x[b]) - r) / r for a, b, r, _ in cons)


def total_stretch(x, cons):
    """The sum of the length errors, in metres."""
    return sum(abs(math.dist(x[a], x[b]) - r) for a, b, r, _ in cons)


def energy(x, v, w, cons, gravity=GRAVITY):
    """Kinetic plus gravitational plus compliant constraint energy of the free particles."""
    e = 0.0
    for p, u, wi in zip(x, v, w):
        if wi > 0.0:
            m = 1.0 / wi
            e += 0.5 * m * (u[0] ** 2 + u[1] ** 2) - m * (gravity[0] * p[0] + gravity[1] * p[1])
    for a, b, r, alpha in cons:
        if alpha > 0.0:
            e += 0.5 / alpha * (math.dist(x[a], x[b]) - r) ** 2
    return e
