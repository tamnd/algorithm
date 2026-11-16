# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/computed-torque-control/. The authors are listed in prov/YZJ7AN.jsonl.

"""Computed-torque control of a serial arm, with a planar 2R arm to test it.

The arm obeys the manipulator equation M(q) q'' + C(q, q') q' + g(q) = tau.
The control law is tau = M(q) a + C(q, q') q' + g(q) with
a = qd'' + Kd (qd' - q') + Kp (qd - q). With an exact model the joint error
e = qd - q obeys e'' + Kd e' + Kp e = 0.

Matrices are lists of rows and vectors are lists. Only the standard library.
"""

import math

GRAVITY = 9.81


class TwoLinkArm:
    """Planar 2R arm in a vertical plane, with point masses at the link ends.

    q1 is measured from the horizontal x axis, q2 from link 1. The y axis
    points up, and gravity acts along -y. C is built from the Christoffel
    symbols of the first kind, so M' - 2 C is skew-symmetric.
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

    def energy(self, q, qd):
        """Kinetic plus potential energy, with zero potential at height 0."""
        m = self.mass(q)
        kin = 0.5 * sum(qd[i] * m[i][j] * qd[j] for i in range(2) for j in range(2))
        y1 = self.l1 * math.sin(q[0])
        y2 = y1 + self.l2 * math.sin(q[0] + q[1])
        return kin + self.grav * (self.m1 * y1 + self.m2 * y2)

    def accel(self, q, qd, tau):
        """Solve M q'' = tau - C q' - g for q''."""
        m = self.mass(q)
        c = self.coriolis(q, qd)
        g = self.gravity(q)
        r = [tau[i] - c[i][0] * qd[0] - c[i][1] * qd[1] - g[i] for i in range(2)]
        return solve2(m, r)


def solve2(a, b):
    """Solve the 2 by 2 system a x = b by Cramer's rule."""
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if det == 0.0:
        raise ValueError("singular 2 by 2 matrix")
    return [(b[0] * a[1][1] - a[0][1] * b[1]) / det, (a[0][0] * b[1] - b[0] * a[1][0]) / det]


def computed_torque(model, q, qd, q_des, qd_des, qdd_des, kp, kd):
    """Return the joint torques of computed-torque control.

    model gives mass(q), coriolis(q, qd) and gravity(q); it is the model
    that the controller believes, which can differ from the true arm.
    kp and kd are lists of diagonal gains.
    """
    n = len(q)
    e = [q_des[i] - q[i] for i in range(n)]  # @line L1
    ed = [qd_des[i] - qd[i] for i in range(n)]  # @line L2
    a = [qdd_des[i] + kd[i] * ed[i] + kp[i] * e[i] for i in range(n)]  # @line L3
    m = model.mass(q)  # @line L4
    c = model.coriolis(q, qd)
    g = model.gravity(q)
    tau = [sum(m[i][j] * a[j] + c[i][j] * qd[j] for j in range(n)) + g[i] for i in range(n)]
    return tau  # @line L5


def rk4_step(f, t, x, dt):
    """One classical Runge-Kutta step for x' = f(t, x)."""
    k1 = f(t, x)
    k2 = f(t + dt / 2, [x[i] + dt / 2 * k1[i] for i in range(len(x))])
    k3 = f(t + dt / 2, [x[i] + dt / 2 * k2[i] for i in range(len(x))])
    k4 = f(t + dt, [x[i] + dt * k3[i] for i in range(len(x))])
    return [x[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(x))]


def simulate(arm, model, traj, q0, qd0, kp, kd, dt, steps):
    """Simulate the closed loop with RK4 and the control law inside each stage.

    traj(t) returns (q_des, qd_des, qdd_des). Return the list of
    (t, q, qd) at each step, including the start.
    """

    def f(t, x):
        q, qd = x[:2], x[2:]
        qs, qds, qdds = traj(t)
        tau = computed_torque(model, q, qd, qs, qds, qdds, kp, kd)
        return qd + arm.accel(q, qd, tau)

    x = list(q0) + list(qd0)
    out = [(0.0, x[:2], x[2:])]
    for k in range(steps):
        x = rk4_step(f, k * dt, x, dt)
        out.append(((k + 1) * dt, x[:2], x[2:]))
    return out
