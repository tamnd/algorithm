# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extended-position-based-dynamics/. The authors are listed in prov/553NT7.jsonl.

"""Extended position based dynamics (Macklin, Mueller and Chentanez 2016), in 2D.

Each constraint C_j has a compliance alpha_j (the inverse of a stiffness) and a
Lagrange multiplier lambda_j that starts at zero in every step. With
alpha~ = alpha / dt^2, one Gauss-Seidel sweep visits each constraint and
applies (equation (18) of the paper)

    dlambda = (-C_j(x) - alpha~ lambda_j) / (sum_i w_i |grad_i C_j(x)|^2 + alpha~),
    x_i <- x_i + w_i grad_i C_j(x) dlambda,   lambda_j <- lambda_j + dlambda.

This is a Gauss-Seidel solve of the Newton system of backward Euler for the
energy U = sum 1/(2 alpha_j) C_j^2, with the geometric stiffness dropped
(K ~ M) and the residual g = M (x - x~) - grad C^T lambda taken as zero.
With alpha_j = 0 the update is the PBD projection with stiffness 1.

The particles are lists of 2D points, w are inverse masses (0 for a pinned
particle) and a constraint is a tuple (i, j, rest, alpha) for the distance
constraint C = |x_i - x_j| - rest. One sweep costs Theta(c) for c
constraints, a step O(n + k c) for k sweeps, and the memory is O(n + c).
"""

import math

GRAVITY = (0.0, -9.81)


def distance_value_and_gradient(x, i, j, rest):
    """C = |x_i - x_j| - rest and the unit vector n = grad_i C = -grad_j C."""
    dx, dy = x[i][0] - x[j][0], x[i][1] - x[j][1]
    ln = math.hypot(dx, dy)
    if ln == 0.0:
        return -rest, (0.0, 0.0)
    return ln - rest, (dx / ln, dy / ln)


def xpbd_step(x, v, w, constraints, dt, iterations, gravity=GRAVITY):
    """One XPBD step. Return (x, v, lam) with the final multipliers."""
    n = len(x)
    xn = [tuple(p) for p in x]
    xt = [(xn[i][0] + dt * v[i][0] + dt * dt * gravity[0], xn[i][1] + dt * v[i][1] + dt * dt * gravity[1])
          if w[i] > 0.0 else xn[i] for i in range(n)]  # @line L1
    lam = [0.0] * len(constraints)  # @line L2
    p = list(xt)  # @line L3
    for _ in range(iterations):  # @line L4
        for k, (i, j, rest, alpha) in enumerate(constraints):  # @line L5
            at = alpha / (dt * dt)
            c, nrm = distance_value_and_gradient(p, i, j, rest)
            denom = w[i] + w[j] + at
            if denom == 0.0 or nrm == (0.0, 0.0):
                continue
            dl = (-c - at * lam[k]) / denom  # @line L6
            p[i] = (p[i][0] + w[i] * nrm[0] * dl, p[i][1] + w[i] * nrm[1] * dl)  # @line L7
            p[j] = (p[j][0] - w[j] * nrm[0] * dl, p[j][1] - w[j] * nrm[1] * dl)
            lam[k] += dl  # @line L8
    v_new = [((p[i][0] - xn[i][0]) / dt, (p[i][1] - xn[i][1]) / dt) for i in range(n)]  # @line L9
    return p, v_new, lam


def energy_objective(x, xt, w, constraints, dt):
    """The backward Euler objective 1/2 |x - x~|_M^2 + dt^2 sum 1/(2 alpha) C^2 (free particles only)."""
    g = 0.0
    for i, (p, q) in enumerate(zip(x, xt)):
        if w[i] > 0.0:
            g += 0.5 / w[i] * ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
    for i, j, rest, alpha in constraints:
        c = math.dist(x[i], x[j]) - rest
        g += dt * dt * 0.5 / alpha * c * c
    return g


def constraint_force(x, constraints, lam, dt):
    """The force of each constraint: grad C^T lambda / dt^2, per particle."""
    f = [[0.0, 0.0] for _ in x]
    for k, (i, j, rest, alpha) in enumerate(constraints):
        _, nrm = distance_value_and_gradient(x, i, j, rest)
        s = lam[k] / (dt * dt)
        f[i][0] += s * nrm[0]
        f[i][1] += s * nrm[1]
        f[j][0] -= s * nrm[0]
        f[j][1] -= s * nrm[1]
    return [tuple(u) for u in f]


def chain(count, spacing, alpha, mass=1.0, vertical=False):
    """A chain pinned at particle 0, horizontal or hanging along -y. Return (x, v, w, constraints)."""
    if vertical:
        x = [(0.0, -i * spacing) for i in range(count)]
    else:
        x = [(i * spacing, 0.0) for i in range(count)]
    v = [(0.0, 0.0)] * count
    w = [0.0] + [1.0 / mass] * (count - 1)
    cons = [(i, i + 1, spacing, alpha) for i in range(count - 1)]
    return x, v, w, cons
