# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pd-control-with-gravity-compensation/. The authors are listed in prov/0ACG13.jsonl.

"""PD control with gravity compensation for a set point, with a planar 2R arm.

The arm obeys M(q) q'' + C(q, q') q' + g(q) = tau. The law is
tau = Kp (qd - q) - Kd q' + g_model(q). With an exact gravity model and
symmetric positive definite gains, the set point qd is globally
asymptotically stable. V = 1/2 q'^T M q' + 1/2 e^T Kp e is a Lyapunov
function with V' = -q'^T Kd q'.

Matrices are lists of rows and vectors are lists. Only the standard library.
"""

import math

GRAVITY = 9.81


class TwoLinkArm:
    """Planar 2R arm in a vertical plane, with point masses at the link ends.

    q1 is measured from the horizontal x axis, q2 from link 1. Gravity acts
    along -y. C is built from the Christoffel symbols.
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

    def accel(self, q, qd, tau):
        """Solve M q'' = tau - C q' - g for q''."""
        m = self.mass(q)
        c = self.coriolis(q, qd)
        g = self.gravity(q)
        r = [tau[i] - c[i][0] * qd[0] - c[i][1] * qd[1] - g[i] for i in range(2)]
        return solve2(m, r)


class NoGravity:
    """A gravity model that returns zero: plain PD control."""

    def gravity(self, q):
        return [0.0] * len(q)


def solve2(a, b):
    """Solve the 2 by 2 system a x = b by Cramer's rule."""
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if det == 0.0:
        raise ValueError("singular 2 by 2 matrix")
    return [(b[0] * a[1][1] - a[0][1] * b[1]) / det, (a[0][0] * b[1] - b[0] * a[1][0]) / det]


def pd_gravity(model, q, qd, q_des, kp, kd):
    """Return tau = Kp (q_des - q) - Kd q' + g_model(q).

    kp and kd are lists of diagonal gains. model only needs gravity(q).
    """
    n = len(q)
    e = [q_des[i] - q[i] for i in range(n)]  # @line L1
    g = model.gravity(q)  # @line L2
    tau = [kp[i] * e[i] - kd[i] * qd[i] + g[i] for i in range(n)]
    return tau  # @line L3


def lyapunov(arm, q, qd, q_des, kp):
    """V = 1/2 q'^T M(q) q' + 1/2 e^T Kp e with diagonal Kp."""
    m = arm.mass(q)
    n = len(q)
    kin = 0.5 * sum(qd[i] * m[i][j] * qd[j] for i in range(n) for j in range(n))
    pot = 0.5 * sum(kp[i] * (q_des[i] - q[i]) ** 2 for i in range(n))
    return kin + pot


def rk4_step(f, t, x, dt):
    """One classical Runge-Kutta step for x' = f(t, x)."""
    k1 = f(t, x)
    k2 = f(t + dt / 2, [x[i] + dt / 2 * k1[i] for i in range(len(x))])
    k3 = f(t + dt / 2, [x[i] + dt / 2 * k2[i] for i in range(len(x))])
    k4 = f(t + dt, [x[i] + dt * k3[i] for i in range(len(x))])
    return [x[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(x))]


def simulate(arm, model, q_des, q0, qd0, kp, kd, dt, steps):
    """Simulate the closed loop with RK4. Return the list of (t, q, qd)."""

    def f(t, x):
        q, qd = x[:2], x[2:]
        tau = pd_gravity(model, q, qd, q_des, kp, kd)
        return qd + arm.accel(q, qd, tau)

    x = list(q0) + list(qd0)
    out = [(0.0, x[:2], x[2:])]
    for k in range(steps):
        x = rk4_step(f, k * dt, x, dt)
        out.append(((k + 1) * dt, x[:2], x[2:]))
    return out
