# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stanley-controller/. The authors are listed in prov/8QP9X9.jsonl.

"""Stanley steering law (Thrun et al. 2006, Hoffmann et al. 2007).

The vehicle is the kinematic bicycle model with its reference point at the center of the
front axle. The front wheels move with speed u > 0 in the direction theta + delta, and the
heading turns at theta' = u sin(delta) / L:

    xf' = u cos(theta + delta),  yf' = u sin(theta + delta),  theta' = u sin(delta) / L.

The path is a polyline. At each step the controller finds the point of the path closest
to the front axle, the signed cross-track error e (positive when the front axle is to the
right of the path, so that a left turn reduces it) and the heading error psi = path
heading - theta. It steers with

    delta = psi + atan(k e / (ks + u)),

clamped to [-max_steer, max_steer]. The gain k is in 1/s; ks >= 0 is an optional softening
speed in m/s (ks = 0 gives the law of the paper).
"""

import math


def wrap(a):
    return (a + math.pi) % (2.0 * math.pi) - math.pi


def closest_on_path(path, p, start, window=None):
    """(segment index, parameter in [0, 1]) of the closest point of the path to p, over the
    segments from index start onward, or over the next window segments if window is set."""
    best = (math.inf, start, 0.0)
    stop = len(path) - 1 if window is None else min(len(path) - 1, start + window)
    for i in range(start, stop):
        ax, ay = path[i]
        bx, by = path[i + 1]
        dx, dy = bx - ax, by - ay
        den = dx * dx + dy * dy
        u = 0.0 if den == 0.0 else max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / den))
        d2 = (ax + u * dx - p[0]) ** 2 + (ay + u * dy - p[1]) ** 2
        if d2 < best[0]:
            best = (d2, i, u)
    return best[1], best[2]


class Stanley:
    """Stanley controller for a polyline path."""

    def __init__(self, path, gain, wheelbase, max_steer=math.pi / 2.0, soft=0.0, window=None):
        self.path = [tuple(p) for p in path]
        self.k = gain
        self.L = wheelbase
        self.max_steer = max_steer
        self.ks = soft
        self.window = window
        self.index = 0
        self.error = 0.0
        self.heading_error = 0.0

    def errors(self, pose):
        """Cross-track error e (positive: path to the left) and heading error psi."""
        x, y, th = pose
        i, u = closest_on_path(self.path, (x, y), self.index, self.window)  # @line L1
        self.index = i
        ax, ay = self.path[i]
        bx, by = self.path[i + 1]
        seg = math.atan2(by - ay, bx - ax)  # @line L2
        qx, qy = ax + u * (bx - ax), ay + u * (by - ay)
        e = math.sin(seg) * (x - qx) - math.cos(seg) * (y - qy)  # @line L2
        psi = wrap(seg - th)  # @line L3
        return e, psi

    def steer(self, pose, speed):
        """Steering angle for the front axle pose (x, y, theta) and the front wheel speed."""
        e, psi = self.errors(pose)
        self.error, self.heading_error = e, psi
        delta = psi + math.atan2(self.k * e, self.ks + speed)  # @line L4
        return max(-self.max_steer, min(self.max_steer, delta))  # @line L5


def front_rhs(state, u, delta, wheelbase):
    x, y, th = state
    return u * math.cos(th + delta), u * math.sin(th + delta), u * math.sin(delta) / wheelbase


def _add(s, k, h):
    return s[0] + h * k[0], s[1] + h * k[1], s[2] + h * k[2]


def _rk4(f, state, dt):
    k1 = f(state)
    k2 = f(_add(state, k1, dt / 2.0))
    k3 = f(_add(state, k2, dt / 2.0))
    k4 = f(_add(state, k3, dt))
    return tuple(state[j] + dt / 6.0 * (k1[j] + 2.0 * k2[j] + 2.0 * k3[j] + k4[j]) for j in range(3))


def simulate(controller, pose, u, dt, steps, hold=True):
    """Closed loop with front wheel speed u. With hold=True the steering is computed once per
    step and held for dt (a digital controller). With hold=False it is recomputed inside each
    RK4 stage, which integrates the continuous closed loop."""
    poses = [tuple(pose)]
    steers = []
    for _ in range(steps):  # @line L6
        if hold:
            delta = controller.steer(pose, u)  # @line L6
            pose = _rk4(lambda s: front_rhs(s, u, delta, controller.L), pose, dt)  # @line L7
        else:
            delta = controller.steer(pose, u)
            pose = _rk4(lambda s: front_rhs(s, u, controller.steer(s, u), controller.L), pose, dt)
        poses.append(pose)
        steers.append(delta)
    return poses, steers


def implicit_time(s0, s):
    """Time for the scaled error s = k e / u to go from s0 to s (same sign, |s| <= |s0|) under
    e' = -k e / sqrt(1 + (k e / u)^2), multiplied by k. Uses
    F(s) = sqrt(1 + s^2) + ln(s / (1 + sqrt(1 + s^2))) and k t = F(s0) - F(s)."""
    def F(z):
        z = abs(z)
        r = math.sqrt(1.0 + z * z)
        return r + math.log(z / (1.0 + r))

    return F(s0) - F(s)
