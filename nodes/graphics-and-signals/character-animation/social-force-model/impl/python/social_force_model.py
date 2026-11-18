# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/social-force-model/. The authors are listed in prov/4BAJB2.jsonl.
"""The social force model in the form of Helbing, Farkas and Vicsek (2000).

Each person i has a position x_i, a velocity v_i, a radius r_i, a mass m,
a desired speed v0 and a goal. The force on i is

    F_i = m (v0 e_i - v_i) / tau + sum over j != i of f_ij,

with e_i the unit vector from x_i to the goal, and for d = |x_i - x_j|,
n = (x_i - x_j) / d, t = (-n_y, n_x), r = r_i + r_j and g(z) = max(z, 0):

    f_ij = (A exp((r - d) / B) + k g(r - d)) n + kappa g(r - d) ((v_j - v_i) . t) t.

The first part is the social repulsion, the second the body force and the
third the sliding friction; the last two act only when the bodies touch.
Walls are left out. The defaults are the constants of the 2000 paper;
they are fitted or tuned values, not laws. The step is symplectic Euler
(velocity first). The plane is x-y; there is no gravity in the model.
"""

import math

PARAMS = {
    "A": 2.0e3,      # N
    "B": 0.08,       # m
    "k": 1.2e5,      # kg / s^2
    "kappa": 2.4e5,  # kg / (m s)
    "tau": 0.5,      # s
    "m": 80.0,       # kg
}


def pair_force(xi, xj, vi, vj, ri, rj, p=PARAMS):
    dx, dy = xi[0] - xj[0], xi[1] - xj[1]
    d = math.hypot(dx, dy)
    nx, ny = dx / d, dy / d
    tx, ty = -ny, nx
    over = max(ri + rj - d, 0.0)
    a = p["A"] * math.exp((ri + rj - d) / p["B"]) + p["k"] * over
    dvt = (vj[0] - vi[0]) * tx + (vj[1] - vi[1]) * ty
    f = p["kappa"] * over * dvt
    return (a * nx + f * tx, a * ny + f * ty)


def driving_force(x, v, goal, v0, p=PARAMS):
    ex, ey = goal[0] - x[0], goal[1] - x[1]
    n = math.hypot(ex, ey)
    if n > 0:
        ex, ey = ex / n, ey / n
    return (p["m"] * (v0 * ex - v[0]) / p["tau"], p["m"] * (v0 * ey - v[1]) / p["tau"])


def forces(X, V, R, goals, v0, p=PARAMS):
    n = len(X)
    F = [list(driving_force(X[i], V[i], goals[i], v0[i], p)) for i in range(n)]  # @line L1
    for i in range(n):
        for j in range(i + 1, n):
            fx, fy = pair_force(X[i], X[j], V[i], V[j], R[i], R[j], p)  # @line L2
            F[i][0] += fx
            F[i][1] += fy
            F[j][0] -= fx  # @line L3
            F[j][1] -= fy
    return F


def step(X, V, R, goals, v0, dt, p=PARAMS):
    F = forces(X, V, R, goals, v0, p)
    V = [(v[0] + dt * f[0] / p["m"], v[1] + dt * f[1] / p["m"]) for v, f in zip(V, F)]  # @line L4
    X = [(x[0] + dt * v[0], x[1] + dt * v[1]) for x, v in zip(X, V)]  # @line L5
    return X, V


def min_gap(X, R):
    """The smallest d_ij - r_i - r_j over all pairs (negative if bodies overlap)."""
    best = math.inf
    for i in range(len(X)):
        for j in range(i + 1, len(X)):
            best = min(best, math.dist(X[i], X[j]) - R[i] - R[j])
    return best


def simulate(X, V, R, goals, v0, dt, steps, p=PARAMS):
    gap = min_gap(X, R)
    for _ in range(steps):
        X, V = step(X, V, R, goals, v0, dt, p)
        gap = min(gap, min_gap(X, R))
    return X, V, gap
