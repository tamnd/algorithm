# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/potential-field-method/. The authors are listed in prov/6TE8NF.jsonl.

"""Artificial potential field planning for a point robot among convex polygons (Khatib 1986).

U(q) = zeta/2 |q - goal|^2 + sum over obstacles i with rho_i(q) <= rho0 of eta/2 (1/rho_i(q) - 1/rho0)^2,
where rho_i(q) is the distance from q to obstacle i. The planner follows the negative gradient with a
bounded step. It stops at the goal, or at a point where the gradient is almost zero (a local minimum).
"""

import math


def closest_point_on_segment(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    return (a[0] + t * dx, a[1] + t * dy)


def inside_convex(p, poly):
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) < 0:
            return False
    return True


def distance_to_convex(p, poly):
    """Distance from p to the closed convex polygon, and the closest point. Zero inside."""
    if inside_convex(p, poly):
        return 0.0, p
    best, arg = math.inf, None
    n = len(poly)
    for i in range(n):
        c = closest_point_on_segment(p, poly[i], poly[(i + 1) % n])
        d = math.hypot(p[0] - c[0], p[1] - c[1])
        if d < best:
            best, arg = d, c
    return best, arg


class Field:
    def __init__(self, goal, obstacles, zeta=1.0, eta=1.0, rho0=1.0):
        self.goal = goal
        self.obstacles = obstacles
        self.zeta, self.eta, self.rho0 = zeta, eta, rho0

    def potential(self, q):
        u = 0.5 * self.zeta * ((q[0] - self.goal[0]) ** 2 + (q[1] - self.goal[1]) ** 2)
        for ob in self.obstacles:
            rho, _ = distance_to_convex(q, ob)
            if rho == 0.0:
                return math.inf
            if rho <= self.rho0:
                u += 0.5 * self.eta * (1.0 / rho - 1.0 / self.rho0) ** 2
        return u

    def gradient(self, q):
        gx = self.zeta * (q[0] - self.goal[0])
        gy = self.zeta * (q[1] - self.goal[1])
        for ob in self.obstacles:
            rho, c = distance_to_convex(q, ob)
            if 0.0 < rho <= self.rho0:
                k = self.eta * (1.0 / self.rho0 - 1.0 / rho) / (rho * rho)
                gx += k * (q[0] - c[0]) / rho
                gy += k * (q[1] - c[1]) / rho
        return gx, gy


def descend(field, start, step=0.02, tol=1e-3, grad_tol=1e-4, max_iter=20000):
    """Gradient descent on the field. Returns (path, status) with status "goal" or "stuck".

    Each move is -alpha * grad U with alpha = step, cut to length step, and halved while it enters an
    obstacle or raises U. The run is stuck when the gradient norm falls below grad_tol away from the goal.
    """
    q = start  # @line L1
    path = [q]
    for _ in range(max_iter):  # @line L2
        if math.dist(q, field.goal) < tol:  # @line L3
            return path, "goal"
        gx, gy = field.gradient(q)  # @line L4
        norm = math.hypot(gx, gy)
        if norm < grad_tol:  # @line L5
            return path, "stuck"
        length = min(step * norm, step)  # @line L6
        u = field.potential(q)
        while True:  # @line L7
            nxt = (q[0] - length * gx / norm, q[1] - length * gy / norm)
            if field.potential(nxt) < u:
                break
            length /= 2  # @line L8
            if length < 1e-12:  # @line L9
                return path, "stuck"
        q = nxt  # @line L10
        path.append(q)
    return path, "stuck"  # @line L11
