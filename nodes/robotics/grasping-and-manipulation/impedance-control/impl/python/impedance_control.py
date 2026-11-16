# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/impedance-control/. The authors are listed in prov/TVY2W5.jsonl.

"""Impedance control of the end point of a planar 2R arm.

The arm obeys M(q) q'' + C(q, q') q' + g(q) = tau + J(q)^T F_ext, where
F_ext is the force of the environment on the end point. The law with a
force sensor makes the end point error x~ = x - x0 obey

    Md x~'' + Dd x~' + Kd x~ = F_ext.

The law without a force sensor, tau = J^T (Kd (x0 - x) - Dd x') + g(q), gives
the same spring and damper at rest but not the chosen mass.

Matrices are lists of rows and vectors are lists. Only the standard library.
"""

import math

GRAVITY = 9.81


class TwoLinkArm:
    """Planar 2R arm in a vertical plane, with point masses at the link ends.

    q1 is measured from the horizontal x axis, q2 from link 1. The y axis
    points up, and gravity acts along -y.
    """

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
        """Position of the end point."""
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
        """The term J'(q, q') q' of the end point acceleration."""
        w1, w12 = qd[0], qd[0] + qd[1]
        s1, c1 = math.sin(q[0]), math.cos(q[0])
        s12, c12 = math.sin(q[0] + q[1]), math.cos(q[0] + q[1])
        l1, l2 = self.l1, self.l2
        return [
            -l1 * c1 * w1 * w1 - l2 * c12 * w12 * w12,
            -l1 * s1 * w1 * w1 - l2 * s12 * w12 * w12,
        ]

    def ik(self, x, elbow=1.0):
        """Joint angles that put the end point at x (elbow = +1 or -1)."""
        l1, l2 = self.l1, self.l2
        c2 = (x[0] ** 2 + x[1] ** 2 - l1 * l1 - l2 * l2) / (2 * l1 * l2)
        if abs(c2) > 1.0:
            raise ValueError("point out of reach")
        q2 = elbow * math.acos(c2)
        q1 = math.atan2(x[1], x[0]) - math.atan2(l2 * math.sin(q2), l1 + l2 * math.cos(q2))
        return [q1, q2]

    def accel(self, q, qd, tau, f_ext):
        """Solve M q'' = tau + J^T F_ext - C q' - g for q''."""
        m = self.mass(q)
        c = self.coriolis(q, qd)
        g = self.gravity(q)
        j = self.jacobian(q)
        r = [
            tau[i] + j[0][i] * f_ext[0] + j[1][i] * f_ext[1] - c[i][0] * qd[0] - c[i][1] * qd[1] - g[i]
            for i in range(2)
        ]
        return solve2(m, r)


def solve2(a, b):
    """Solve the 2 by 2 system a x = b by Cramer's rule."""
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if det == 0.0:
        raise ValueError("singular 2 by 2 matrix")
    return [(b[0] * a[1][1] - a[0][1] * b[1]) / det, (a[0][0] * b[1] - b[0] * a[1][0]) / det]


def matvec2(a, v):
    return [a[0][0] * v[0] + a[0][1] * v[1], a[1][0] * v[0] + a[1][1] * v[1]]


def impedance_control(arm, q, qd, x0, x0d, x0dd, f_ext, md, dd, kd):
    """Impedance law with a force sensor and a full dynamic model.

    f_ext is the measured force of the environment on the end point.
    md, dd and kd are lists of diagonal task-space gains.
    """
    j = arm.jacobian(q)
    x, xd = arm.fk(q), matvec2(j, qd)  # @line L1
    xt = [x[i] - x0[i] for i in range(2)]  # @line L2
    xtd = [xd[i] - x0d[i] for i in range(2)]
    ax = [x0dd[i] + (f_ext[i] - dd[i] * xtd[i] - kd[i] * xt[i]) / md[i] for i in range(2)]  # @line L3
    jq = arm.jdot_qdot(q, qd)
    aq = solve2(j, [ax[i] - jq[i] for i in range(2)])  # @line L4
    m, c, g = arm.mass(q), arm.coriolis(q, qd), arm.gravity(q)  # @line L5
    tau = [
        sum(m[i][k] * aq[k] + c[i][k] * qd[k] for k in range(2)) + g[i] - (j[0][i] * f_ext[0] + j[1][i] * f_ext[1])
        for i in range(2)
    ]
    return tau  # @line L6


def simple_impedance(arm, q, qd, x0, dd, kd):
    """Impedance law without a force sensor: tau = J^T (Kd (x0 - x) - Dd x') + g(q)."""
    j = arm.jacobian(q)
    x, xd = arm.fk(q), matvec2(j, qd)
    f = [kd[i] * (x0[i] - x[i]) - dd[i] * xd[i] for i in range(2)]
    g = arm.gravity(q)
    return [j[0][i] * f[0] + j[1][i] * f[1] + g[i] for i in range(2)]


def wall(x_wall, k_env):
    """A frictionless wall x <= x_wall with stiffness k_env, as F_ext(x, x')."""

    def force(x, xd):
        pen = x[0] - x_wall
        return [-k_env * pen, 0.0] if pen > 0.0 else [0.0, 0.0]

    return force


def free_space(x, xd):
    return [0.0, 0.0]


def rk4_step(f, t, x, dt):
    """One classical Runge-Kutta step for x' = f(t, x)."""
    k1 = f(t, x)
    k2 = f(t + dt / 2, [x[i] + dt / 2 * k1[i] for i in range(len(x))])
    k3 = f(t + dt / 2, [x[i] + dt / 2 * k2[i] for i in range(len(x))])
    k4 = f(t + dt, [x[i] + dt * k3[i] for i in range(len(x))])
    return [x[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(x))]


def simulate(arm, law, env, q0, qd0, dt, steps):
    """Simulate the arm with law(t, q, qd, f_ext) and the environment env.

    The sensor reads the true contact force. Return the list of (t, q, qd).
    """

    def f(t, s):
        q, qd = s[:2], s[2:]
        x, xd = arm.fk(q), matvec2(arm.jacobian(q), qd)
        fe = env(x, xd)
        tau = law(t, q, qd, fe)
        return qd + arm.accel(q, qd, tau, fe)

    s = list(q0) + list(qd0)
    out = [(0.0, s[:2], s[2:])]
    for k in range(steps):
        s = rk4_step(f, k * dt, s, dt)
        out.append(((k + 1) * dt, s[:2], s[2:]))
    return out
