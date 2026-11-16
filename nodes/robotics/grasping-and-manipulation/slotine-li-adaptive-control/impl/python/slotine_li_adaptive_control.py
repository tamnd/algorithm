# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slotine-li-adaptive-control/. The authors are listed in prov/RN7MPK.jsonl.

"""The Slotine-Li adaptive controller, with a planar 2R arm to test it.

The arm obeys M(q) q'' + C(q, q') q' + g(q) = tau, and the dynamics are
linear in a parameter vector: M(q) a + C(q, q') v + g(q) = Y(q, q', v, a) pi.
The law uses the reference velocity qr' = qd' - Lambda (q - qd) and the
sliding variable s = q' - qr':

    tau = Y(q, q', qr', qr'') pi_hat - Kd s,    pi_hat' = -Gamma Y^T s.

C must be the Christoffel matrix, so that M' - 2 C is skew-symmetric.
Matrices are lists of rows and vectors are lists. Only the standard library.
"""

import math

GRAVITY = 9.81


class TwoLinkArm:
    """Planar 2R arm in a vertical plane, with point masses at the link ends.

    The parameter vector is pi = (a1, a2, a3, b1, b2) with
    a1 = (m1 + m2) l1^2 + m2 l2^2, a2 = m2 l1 l2, a3 = m2 l2^2,
    b1 = (m1 + m2) l1 g and b2 = m2 l2 g.
    """

    def __init__(self, m1=1.0, m2=1.0, l1=1.0, l2=1.0, grav=GRAVITY):
        self.m1, self.m2, self.l1, self.l2, self.grav = m1, m2, l1, l2, grav

    def params(self):
        m1, m2, l1, l2, gr = self.m1, self.m2, self.l1, self.l2, self.grav
        return [
            (m1 + m2) * l1 * l1 + m2 * l2 * l2,
            m2 * l1 * l2,
            m2 * l2 * l2,
            (m1 + m2) * l1 * gr,
            m2 * l2 * gr,
        ]

    def mass(self, q):
        a1, a2, a3, _, _ = self.params()
        c2 = math.cos(q[1])
        return [[a1 + 2 * a2 * c2, a3 + a2 * c2], [a3 + a2 * c2, a3]]

    def coriolis(self, q, qd):
        h = self.params()[1] * math.sin(q[1])
        return [[-h * qd[1], -h * (qd[0] + qd[1])], [h * qd[0], 0.0]]

    def gravity(self, q):
        _, _, _, b1, b2 = self.params()
        c1, c12 = math.cos(q[0]), math.cos(q[0] + q[1])
        return [b1 * c1 + b2 * c12, b2 * c12]

    def accel(self, q, qd, tau):
        """Solve M q'' = tau - C q' - g for q''."""
        m = self.mass(q)
        c = self.coriolis(q, qd)
        g = self.gravity(q)
        r = [tau[i] - c[i][0] * qd[0] - c[i][1] * qd[1] - g[i] for i in range(2)]
        return solve2(m, r)


def regressor(q, qd, v, a):
    """Y(q, q', v, a) with Y pi = M(q) a + C(q, q') v + g(q) for the 2R arm."""
    c1, c2 = math.cos(q[0]), math.cos(q[1])
    s2 = math.sin(q[1])
    c12 = math.cos(q[0] + q[1])
    row1 = [
        a[0],
        2 * c2 * a[0] + c2 * a[1] - s2 * qd[1] * v[0] - s2 * (qd[0] + qd[1]) * v[1],
        a[1],
        c1,
        c12,
    ]
    row2 = [0.0, c2 * a[0] + s2 * qd[0] * v[0], a[0] + a[1], 0.0, c12]
    return [row1, row2]


def solve2(a, b):
    """Solve the 2 by 2 system a x = b by Cramer's rule."""
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if det == 0.0:
        raise ValueError("singular 2 by 2 matrix")
    return [(b[0] * a[1][1] - a[0][1] * b[1]) / det, (a[0][0] * b[1] - b[0] * a[1][0]) / det]


def slotine_li(q, qd, q_des, qd_des, qdd_des, pi_hat, lam, kd, gamma):
    """Return (tau, pi_hat_dot) of the Slotine-Li law.

    lam, kd and gamma are lists of diagonal gains. pi_hat is the current
    estimate of the parameter vector.
    """
    n = len(q)
    qt = [q[i] - q_des[i] for i in range(n)]  # @line L1
    qr_d = [qd_des[i] - lam[i] * qt[i] for i in range(n)]  # @line L2
    qr_dd = [qdd_des[i] - lam[i] * (qd[i] - qd_des[i]) for i in range(n)]  # @line L3
    s = [qd[i] - qr_d[i] for i in range(n)]  # @line L4
    y = regressor(q, qd, qr_d, qr_dd)  # @line L5
    p = len(pi_hat)
    tau = [sum(y[i][k] * pi_hat[k] for k in range(p)) - kd[i] * s[i] for i in range(n)]
    pi_dot = [-gamma[k] * sum(y[i][k] * s[i] for i in range(n)) for k in range(p)]  # @line L6
    return tau, pi_dot  # @line L7


def lyapunov(arm, q, qd, q_des, qd_des, pi_hat, lam, gamma):
    """V = 1/2 s^T M s + 1/2 (pi_hat - pi)^T Gamma^(-1) (pi_hat - pi)."""
    s = [qd[i] - qd_des[i] + lam[i] * (q[i] - q_des[i]) for i in range(2)]
    m = arm.mass(q)
    pi = arm.params()
    kin = 0.5 * sum(s[i] * m[i][j] * s[j] for i in range(2) for j in range(2))
    est = 0.5 * sum((pi_hat[k] - pi[k]) ** 2 / gamma[k] for k in range(len(pi)))
    return kin + est


def rk4_step(f, t, x, dt):
    """One classical Runge-Kutta step for x' = f(t, x)."""
    k1 = f(t, x)
    k2 = f(t + dt / 2, [x[i] + dt / 2 * k1[i] for i in range(len(x))])
    k3 = f(t + dt / 2, [x[i] + dt / 2 * k2[i] for i in range(len(x))])
    k4 = f(t + dt, [x[i] + dt * k3[i] for i in range(len(x))])
    return [x[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(x))]


def closed_loop(arm, traj, lam, kd, gamma):
    """Right side of the closed loop on the state (q, q', pi_hat)."""

    def f(t, x):
        q, qd, pi_hat = x[:2], x[2:4], x[4:]
        qs, qds, qdds = traj(t)
        tau, pi_dot = slotine_li(q, qd, qs, qds, qdds, pi_hat, lam, kd, gamma)
        return qd + arm.accel(q, qd, tau) + pi_dot

    return f


def simulate(arm, traj, q0, qd0, pi0, lam, kd, gamma, dt, steps):
    """Simulate with RK4. Return the list of (t, q, qd, pi_hat)."""
    f = closed_loop(arm, traj, lam, kd, gamma)
    x = list(q0) + list(qd0) + list(pi0)
    out = [(0.0, x[:2], x[2:4], x[4:])]
    for k in range(steps):
        x = rk4_step(f, k * dt, x, dt)
        out.append(((k + 1) * dt, x[:2], x[2:4], x[4:]))
    return out
