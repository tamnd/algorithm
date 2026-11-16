# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-position-force-control/. The authors are listed in prov/YQZW8R.jsonl.

"""Hybrid position/force control of a planar 2R arm against a wall.

The wall is the line x = x_w, and the tool slides on it without friction.
The x direction (the wall normal) is force controlled and the y direction
is position controlled, with the selection matrices S_f = diag(1, 0) and
S_p = I - S_f. The law works in task space with the task inertia
Lam = (J M^-1 J^T)^-1:

    F_cmd = Lam S_p a_p + S_f F_f + mu,    tau = J^T F_cmd.

Matrices are lists of rows and vectors are lists. Only the standard library.
"""

import math

GRAVITY = 9.81


class TwoLinkArm:
    """Planar 2R arm in a vertical plane, with point masses at the link ends."""

    def __init__(self, m1=1.0, m2=1.0, l1=1.0, l2=1.0, grav=GRAVITY):
        self.m1, self.m2, self.l1, self.l2, self.grav = m1, m2, l1, l2, grav

    def mass(self, q):
        m1, m2, l1, l2 = self.m1, self.m2, self.l1, self.l2
        c2 = math.cos(q[1])
        a = (m1 + m2) * l1 * l1 + m2 * l2 * l2 + 2.0 * m2 * l1 * l2 * c2
        b = m2 * l2 * l2 + m2 * l1 * l2 * c2
        return [[a, b], [b, m2 * l2 * l2]]

    def coriolis(self, q, qd):
        h = self.m2 * self.l1 * self.l2 * math.sin(q[1])
        return [[-h * qd[1], -h * (qd[0] + qd[1])], [h * qd[0], 0.0]]

    def gravity(self, q):
        m1, m2, l1, l2, gr = self.m1, self.m2, self.l1, self.l2, self.grav
        c1, c12 = math.cos(q[0]), math.cos(q[0] + q[1])
        return [(m1 + m2) * gr * l1 * c1 + m2 * gr * l2 * c12, m2 * gr * l2 * c12]

    def fk(self, q):
        q12 = q[0] + q[1]
        return [
            self.l1 * math.cos(q[0]) + self.l2 * math.cos(q12),
            self.l1 * math.sin(q[0]) + self.l2 * math.sin(q12),
        ]

    def jacobian(self, q):
        s1, c1 = math.sin(q[0]), math.cos(q[0])
        s12, c12 = math.sin(q[0] + q[1]), math.cos(q[0] + q[1])
        l1, l2 = self.l1, self.l2
        return [[-l1 * s1 - l2 * s12, -l2 * s12], [l1 * c1 + l2 * c12, l2 * c12]]

    def jdot_qdot(self, q, qd):
        w1, w12 = qd[0], qd[0] + qd[1]
        s1, c1 = math.sin(q[0]), math.cos(q[0])
        s12, c12 = math.sin(q[0] + q[1]), math.cos(q[0] + q[1])
        l1, l2 = self.l1, self.l2
        return [
            -l1 * c1 * w1 * w1 - l2 * c12 * w12 * w12,
            -l1 * s1 * w1 * w1 - l2 * s12 * w12 * w12,
        ]

    def ik(self, x, elbow=1.0):
        l1, l2 = self.l1, self.l2
        c2 = (x[0] ** 2 + x[1] ** 2 - l1 * l1 - l2 * l2) / (2 * l1 * l2)
        q2 = elbow * math.acos(c2)
        q1 = math.atan2(x[1], x[0]) - math.atan2(l2 * math.sin(q2), l1 + l2 * math.cos(q2))
        return [q1, q2]

    def accel(self, q, qd, tau, f_ext):
        """Solve M q'' = tau + J^T F_ext - C q' - g for q''."""
        m, c, g, j = self.mass(q), self.coriolis(q, qd), self.gravity(q), self.jacobian(q)
        r = [
            tau[i] + j[0][i] * f_ext[0] + j[1][i] * f_ext[1] - c[i][0] * qd[0] - c[i][1] * qd[1] - g[i]
            for i in range(2)
        ]
        return solve2(m, r)


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if det == 0.0:
        raise ValueError("singular 2 by 2 matrix")
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def mul2(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def matvec2(a, v):
    return [a[0][0] * v[0] + a[0][1] * v[1], a[1][0] * v[0] + a[1][1] * v[1]]


def solve2(a, b):
    return matvec2(inv2(a), b)


def transpose2(a):
    return [[a[0][0], a[1][0]], [a[0][1], a[1][1]]]


def task_inertia(model, q, qd):
    """Return Lam = (J M^-1 J^T)^-1 and mu = Lam (J M^-1 (C q' + g) - J' q')."""
    j = model.jacobian(q)
    minv = inv2(model.mass(q))
    lam = inv2(mul2(mul2(j, minv), transpose2(j)))
    c, g = model.coriolis(q, qd), model.gravity(q)
    h = [c[i][0] * qd[0] + c[i][1] * qd[1] + g[i] for i in range(2)]
    jm = matvec2(mul2(j, minv), h)
    jq = model.jdot_qdot(q, qd)
    return lam, matvec2(lam, [jm[i] - jq[i] for i in range(2)])


def hybrid_control(model, q, qd, x_des, xd_des, xdd_des, f_des, f_meas, f_int, sf, gains):
    """Return the joint torques of hybrid position/force control.

    sf is the diagonal of S_f (1 for a force direction, 0 for a position
    direction). f_des and f_meas are the desired and measured forces that the
    tool applies to the environment, and f_int is the integral of
    f_des - f_meas. gains = (kp, kd, kfi, kv) are lists of diagonal gains.
    """
    kp, kd, kfi, kv = gains
    j = model.jacobian(q)
    x, xd = model.fk(q), matvec2(j, qd)  # @line L1
    ap = [xdd_des[i] + kd[i] * (xd_des[i] - xd[i]) + kp[i] * (x_des[i] - x[i]) for i in range(2)]  # @line L2
    ff = [f_des[i] + kfi[i] * f_int[i] - kv[i] * xd[i] for i in range(2)]  # @line L3
    lam, mu = task_inertia(model, q, qd)  # @line L4
    pa = matvec2(lam, [(1.0 - sf[i]) * ap[i] for i in range(2)])  # @line L5
    fcmd = [pa[i] + sf[i] * ff[i] + mu[i] for i in range(2)]
    tau = matvec2(transpose2(j), fcmd)  # @line L6
    return tau  # @line L7


def wall(x_wall, k_env):
    """Force of a frictionless spring wall x >= x_wall on the tool."""

    def force(x):
        pen = x[0] - x_wall
        return [-k_env * pen, 0.0] if pen > 0.0 else [0.0, 0.0]

    return force


def rk4_step(f, t, x, dt):
    k1 = f(t, x)
    k2 = f(t + dt / 2, [x[i] + dt / 2 * k1[i] for i in range(len(x))])
    k3 = f(t + dt / 2, [x[i] + dt / 2 * k2[i] for i in range(len(x))])
    k4 = f(t + dt, [x[i] + dt * k3[i] for i in range(len(x))])
    return [x[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(x))]


def simulate(arm, model, env, goal, f_des, sf, gains, q0, dt, steps):
    """Simulate the closed loop; the state is (q, q', integral of the force error).

    goal(t) returns (x_des, xd_des, xdd_des). The sensor reads the true
    force that the tool applies, -F_ext. Return a list of (t, q, qd, f_applied).
    """

    def f(t, s):
        q, qd, fi = s[:2], s[2:4], s[4:]
        fe = env(arm.fk(q))
        applied = [-fe[0], -fe[1]]
        xs, xds, xdds = goal(t)
        tau = hybrid_control(model, q, qd, xs, xds, xdds, f_des, applied, fi, sf, gains)
        err = [sf[i] * (f_des[i] - applied[i]) for i in range(2)]
        return qd + arm.accel(q, qd, tau, fe) + err

    s = list(q0) + [0.0, 0.0, 0.0, 0.0]
    out = []
    for k in range(steps + 1):
        fe = env(arm.fk(s[:2]))
        out.append((k * dt, s[:2], s[2:4], [-fe[0], -fe[1]]))
        if k < steps:
            s = rk4_step(f, k * dt, s, dt)
    return out
