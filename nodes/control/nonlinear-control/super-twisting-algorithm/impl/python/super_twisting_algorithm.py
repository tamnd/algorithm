# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/super-twisting-algorithm/. The authors are listed in prov/QDH2NE.jsonl.

"""The super-twisting algorithm for a sliding variable with

    s' = u + d(t),   |d'(t)| <= L,

in its sampled form with sampling period h:

    u_j     = -k1 |s_j|^(1/2) sgn(s_j) + w_j,
    w_(j+1) = w_j - h k2 sgn(s_j).

In continuous time the closed loop is s' = -k1 |s|^(1/2) sgn(s) + v,
v' = -k2 sgn(s) + d' with v = w + d. With z = (|s|^(1/2) sgn(s), v) the
quadratic form V = z^T P z,

    P = [[2 k2 + k1^2 / 2, -k1 / 2], [-k1 / 2, 1]],

decreases along every solution when k1 > 0 and k2 > L + 2 L^2 / k1^2, and
s = v = 0 is reached in finite time T <= 2 sqrt(lambda_max(P)) sqrt(V(0)) / q,
where q is the smaller of the least eigenvalues of Q(1) and Q(-1) below.

lyapunov_matrix, q_matrix and certified are exact for Fraction input.
"""

import math

__all__ = ["sgn", "SuperTwisting", "lyapunov_matrix", "q_matrix", "certified", "time_bound"]


def sgn(s):
    """Return -1, 0 or 1."""
    return (s > 0) - (s < 0)


class SuperTwisting:
    """Sampled super-twisting controller with gains k1, k2 and period h."""

    def __init__(self, k1, k2, h, w0=0):
        if k1 <= 0 or k2 <= 0:
            raise ValueError("k1 and k2 must be positive")
        if h <= 0:
            raise ValueError("h must be positive")
        self.k1 = k1
        self.k2 = k2
        self.h = h
        self.w = w0

    def step(self, s):
        """Return u_j for the measured s_j and advance the integral state."""
        sg = sgn(s)
        u = -self.k1 * math.sqrt(abs(s)) * sg + self.w  # @line L1
        self.w = self.w - self.h * self.k2 * sg  # @line L2
        return u  # @line L3


def lyapunov_matrix(k1, k2):
    """P of the quadratic Lyapunov function V = z^T P z."""
    return [[2 * k2 + k1 * k1 / 2, -k1 / 2], [-k1 / 2, 1]]


def q_matrix(k1, k2, L, theta):
    """Q(theta) = -(A^T P + P A) for A = [[-k1/2, 1/2], [-k2 + theta L, 0]]."""
    a = k1 * k2 + k1 ** 3 / 2 + theta * L * k1
    b = -k1 * k1 / 2 - theta * L
    return [[a, b], [b, k1 / 2]]


def certified(k1, k2, L):
    """True if Q(1) and Q(-1) are positive definite, that is k2 > L + 2 L^2 / k1^2."""
    for theta in (1, -1):
        q = q_matrix(k1, k2, L, theta)
        if not (q[1][1] > 0 and q[0][0] * q[1][1] - q[0][1] * q[1][0] > 0):
            return False
    return True


def _eig2(m):
    a, b, d = float(m[0][0]), float(m[0][1]), float(m[1][1])
    r = math.hypot((a - d) / 2, b)
    return (a + d) / 2 - r, (a + d) / 2 + r


def time_bound(k1, k2, L, s0, v0):
    """Upper bound on the time to reach s = v = 0 from s(0) = s0, v(0) = v0."""
    if not certified(k1, k2, L):
        raise ValueError("the gains are not certified for this L")
    p = lyapunov_matrix(k1, k2)
    z1 = math.sqrt(abs(s0)) * sgn(s0)
    v0 = float(v0)
    V0 = float(p[0][0]) * z1 * z1 + 2 * float(p[0][1]) * z1 * v0 + v0 * v0
    lmax = _eig2(p)[1]
    q = min(_eig2(q_matrix(k1, k2, L, 1))[0], _eig2(q_matrix(k1, k2, L, -1))[0])
    return 2 * math.sqrt(lmax) * math.sqrt(V0) / q
