# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pure-pursuit/. The authors are listed in prov/RC03NN.jsonl.

"""Pure pursuit path tracking (Wallace et al. 1985, Amidi 1990, Coulter 1992).

The vehicle is the kinematic bicycle model with its reference point at the center of the
rear axle: x' = v cos(theta), y' = v sin(theta), theta' = v tan(delta) / L, with the
wheelbase L in meters and the steering angle delta in radians. The path is a polyline.

At each step the controller picks the goal point: the first point of the path, ahead of
the point closest to the rear axle, at distance ld (the lookahead) from the rear axle.
It steers along the circle arc that starts at the rear axle, is tangent to the heading
and passes through the goal point. That arc has curvature kappa = 2 y_g / ld^2, where
y_g is the lateral coordinate of the goal point in the vehicle frame, and the steering
angle is delta = atan(kappa L).
"""

import math


def wrap(a):
    return (a + math.pi) % (2.0 * math.pi) - math.pi


def closest_on_path(path, p, start):
    """Index i and parameter u in [0, 1] of the point of segment i closest to p,
    searching the segments from index start onward."""
    best = (math.inf, start, 0.0)
    for i in range(start, len(path) - 1):
        ax, ay = path[i]
        bx, by = path[i + 1]
        dx, dy = bx - ax, by - ay
        den = dx * dx + dy * dy
        u = 0.0 if den == 0.0 else max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / den))
        qx, qy = ax + u * dx, ay + u * dy
        d2 = (qx - p[0]) ** 2 + (qy - p[1]) ** 2
        if d2 < best[0]:
            best = (d2, i, u)
    return best[1], best[2]


def goal_point(path, p, i, u, ld):
    """First point of the path after (i, u) at distance ld from p, or the last point."""
    for j in range(i, len(path) - 1):
        ax, ay = path[j]
        bx, by = path[j + 1]
        dx, dy = bx - ax, by - ay
        fx, fy = ax - p[0], ay - p[1]
        a = dx * dx + dy * dy
        if a == 0.0:
            continue
        b = 2.0 * (fx * dx + fy * dy)
        c = fx * fx + fy * fy - ld * ld
        disc = b * b - 4.0 * a * c
        if disc < 0.0:
            continue
        s = (-b + math.sqrt(disc)) / (2.0 * a)  # the exit point of the circle
        lo = u if j == i else 0.0
        if lo <= s <= 1.0:
            return ax + s * dx, ay + s * dy
    return path[-1]


class PurePursuit:
    """Pure pursuit controller for a polyline path."""

    def __init__(self, path, lookahead, wheelbase, max_steer=math.pi / 2.0):
        self.path = [tuple(p) for p in path]
        self.ld = lookahead
        self.L = wheelbase
        self.max_steer = max_steer
        self.index = 0
        self.goal = None
        self.kappa = 0.0

    def steer(self, pose):
        """Steering angle for the rear axle pose (x, y, theta)."""
        x, y, th = pose
        i, u = closest_on_path(self.path, (x, y), self.index)  # @line L1
        self.index = i  # @line L1
        gx, gy = goal_point(self.path, (x, y), i, u, self.ld)  # @line L2
        self.goal = (gx, gy)
        dx, dy = gx - x, gy - y  # @line L3
        xv = math.cos(th) * dx + math.sin(th) * dy  # @line L3
        yv = -math.sin(th) * dx + math.cos(th) * dy  # @line L3
        d2 = xv * xv + yv * yv
        self.kappa = 0.0 if d2 == 0.0 else 2.0 * yv / d2  # @line L4
        delta = math.atan(self.kappa * self.L)  # @line L5
        return max(-self.max_steer, min(self.max_steer, delta))  # @line L5


def bicycle_rhs(state, v, delta, wheelbase):
    x, y, th = state
    return v * math.cos(th), v * math.sin(th), v * math.tan(delta) / wheelbase


def rk4_step(state, v, delta, wheelbase, dt):
    """One RK4 step of the rear-axle kinematic bicycle with v and delta held constant."""
    def add(s, k, h):
        return s[0] + h * k[0], s[1] + h * k[1], s[2] + h * k[2]

    k1 = bicycle_rhs(state, v, delta, wheelbase)
    k2 = bicycle_rhs(add(state, k1, dt / 2.0), v, delta, wheelbase)
    k3 = bicycle_rhs(add(state, k2, dt / 2.0), v, delta, wheelbase)
    k4 = bicycle_rhs(add(state, k3, dt), v, delta, wheelbase)
    return tuple(state[j] + dt / 6.0 * (k1[j] + 2.0 * k2[j] + 2.0 * k3[j] + k4[j]) for j in range(3))


def simulate(controller, pose, v, dt, steps):
    """Closed loop: compute the steering, hold it for dt, integrate with RK4."""
    poses = [tuple(pose)]
    steers = []
    for _ in range(steps):  # @line L6
        delta = controller.steer(pose)  # @line L6
        pose = rk4_step(pose, v, delta, controller.L, dt)  # @line L7
        poses.append(pose)
        steers.append(delta)
    return poses, steers
