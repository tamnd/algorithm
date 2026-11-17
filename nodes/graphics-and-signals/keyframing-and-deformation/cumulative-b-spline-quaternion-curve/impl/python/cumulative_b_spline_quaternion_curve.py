# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cumulative-b-spline-quaternion-curve/. The authors are listed in prov/7V1M8B.jsonl.
"""Cumulative uniform cubic B-spline curve of unit quaternions (Kim, Kim and Shin 1995).

The control quaternions are q_0, ..., q_(n-1), n >= 4. Segment j, for
j = 0, ..., n - 4 and the local parameter u in [0, 1], is

    q(u) = q_j exp(B1(u) w_(j+1)) exp(B2(u) w_(j+2)) exp(B3(u) w_(j+3)),

with w_k = log(q_(k-1)* q_k) and the cumulative basis functions

    B1(u) = (5 + 3u - 3u^2 + u^3) / 6,
    B2(u) = (1 + 3u + 3u^2 - 2u^3) / 6,
    B3(u) = u^3 / 6.

On a line of real numbers the same formula, with sums in place of the
products, is the uniform cubic B-spline in cumulative form.
"""

from anim import q_conj, q_dot, q_exp, q_log, q_mul


def cumulative_basis(u):
    """Return (B1, B2, B3) of the uniform cubic B-spline at u in [0, 1]."""
    u2 = u * u
    u3 = u2 * u
    return (5.0 + 3.0 * u - 3.0 * u2 + u3) / 6.0, (1.0 + 3.0 * u + 3.0 * u2 - 2.0 * u3) / 6.0, u3 / 6.0


def cumulative_basis_derivative(u):
    """Return the derivatives of (B1, B2, B3) with respect to u."""
    u2 = u * u
    return (3.0 - 6.0 * u + 3.0 * u2) / 6.0, (3.0 + 6.0 * u - 6.0 * u2) / 6.0, u2 / 2.0


def _vexp(w, b):
    return q_exp((0.0, b * w[1], b * w[2], b * w[3]))


class CumulativeBSplineQuaternionCurve:
    """The C2 curve of unit quaternions with the control quaternions keys."""

    def __init__(self, keys):
        if len(keys) < 4:
            raise ValueError("a cubic curve needs at least four control quaternions")
        q = [tuple(keys[0])]
        for k in keys[1:]:
            k = tuple(k)
            if q_dot(q[-1], k) < 0.0:  # @line L1
                k = (-k[0], -k[1], -k[2], -k[3])  # @line L2
            q.append(k)
        self.keys = q
        self.omega = [None] + [q_log(q_mul(q_conj(q[k - 1]), q[k])) for k in range(1, len(q))]  # @line L3

    def segments(self):
        """Return the number of segments, n - 3."""
        return len(self.keys) - 3

    def segment(self, j, u):
        """Return the point of segment j at the local parameter u in [0, 1]."""
        b = cumulative_basis(u)  # @line L4
        q = self.keys[j]  # @line L5
        for k in range(3):  # @line L6
            q = q_mul(q, _vexp(self.omega[j + k + 1], b[k]))  # @line L7
        return q  # @line L8

    def __call__(self, t):
        """Return the point at the global parameter t in [0, n - 3]."""
        m = self.segments()
        if t >= m:
            return self.segment(m - 1, 1.0)
        if t <= 0.0:
            return self.segment(0, 0.0)
        j = int(t)
        return self.segment(j, t - j)

    def body_angular_velocity(self, j, u):
        """Return 2 vec(q* dq/du), the body angular velocity per unit of u.

        With A_k = exp(B_k w_k), q* q' = A3* A2* (B1' w1) A2 A3 + A3* (B2' w2) A3 + B3' w3,
        since the factor A_k commutes with w_k.
        """
        b = cumulative_basis(u)
        db = cumulative_basis_derivative(u)
        w = [self.omega[j + k + 1] for k in range(3)]
        a = [_vexp(w[k], b[k]) for k in range(3)]
        acc = (0.0, 0.0, 0.0, 0.0)
        for k in range(3):
            term = (0.0, db[k] * w[k][1], db[k] * w[k][2], db[k] * w[k][3])
            for m in range(k + 1, 3):
                term = q_mul(q_mul(q_conj(a[m]), term), a[m])
            acc = tuple(x + y for x, y in zip(acc, term))
        return (2.0 * acc[1], 2.0 * acc[2], 2.0 * acc[3])
