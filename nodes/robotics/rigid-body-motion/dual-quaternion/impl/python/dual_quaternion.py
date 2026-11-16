# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-quaternion/. The authors are listed in prov/YTDVB1.jsonl.
"""Unit dual quaternions as rigid motions.

A quaternion is a list (w, x, y, z), Hamilton convention, scalar first.
A dual quaternion is a pair (r, d) of quaternions, r + eps d with eps^2 = 0.
It is a unit dual quaternion when |r| = 1 and r . d = 0.

- from_pose(q, t) gives the unit dual quaternion of the rigid motion
  x -> R(q) x + t, and to_pose inverts it.
- mul is the product, which composes motions: mul(a_of(T1), a_of(T2))
  is the dual quaternion of T1 T2.
- apply moves a point by sigma (1 + eps x) conj_both(sigma).
- from_screw builds cos(theta_hat / 2) + s_hat sin(theta_hat / 2) from a
  screw axis line, a pitch and an angle.
- to_matrix gives the 4x4 pose matrix.

sigma and -sigma give the same rigid motion.
"""

import math


def qmul(a, b):
    """Return the Hamilton product a b."""
    a1, b1, c1, d1 = a
    a2, b2, c2, d2 = b
    return [
        a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
        a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
        a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
        a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2,
    ]


def qconj(a):
    """Return the quaternion conjugate (w, -x, -y, -z)."""
    return [a[0], -a[1], -a[2], -a[3]]


def mul(a, b):
    """Return the dual quaternion product a b."""
    r1, d1 = a  # @line L1
    r2, d2 = b  # @line L1
    rd = qmul(r1, d2)  # @line L2
    dr = qmul(d1, r2)  # @line L2
    return [qmul(r1, r2), [x + y for x, y in zip(rd, dr)]]  # @line L2


def conj_both(a):
    """Return r* - eps d*, the conjugate used to move points."""
    return [qconj(a[0]), [-x for x in qconj(a[1])]]


def from_pose(q, t):
    """Return the unit dual quaternion of x -> R(q) x + t for a unit q."""
    return [list(q), [0.5 * x for x in qmul([0.0, t[0], t[1], t[2]], q)]]  # @line L3


def to_pose(a):
    """Return (q, t) with the unit quaternion q and the translation t."""
    r, d = a  # @line L4
    t = qmul(d, qconj(r))  # @line L4
    return list(r), [2.0 * t[1], 2.0 * t[2], 2.0 * t[3]]  # @line L4


def apply(a, x):
    """Return R x + t, from sigma (1 + eps x) conj_both(sigma)."""
    point = [[1.0, 0.0, 0.0, 0.0], [0.0, x[0], x[1], x[2]]]  # @line L5
    out = mul(mul(a, point), conj_both(a))  # @line L5
    return out[1][1:]  # @line L6


def from_screw(s, q, h, theta):
    """Return the dual quaternion of the screw motion about the line through
    q with unit direction s, with pitch h and angle theta.

    The dual angle is theta + eps d with d = h theta, and the dual axis is
    s + eps m with the moment m = q x s.
    """
    m = [q[1] * s[2] - q[2] * s[1], q[2] * s[0] - q[0] * s[2], q[0] * s[1] - q[1] * s[0]]
    d = h * theta
    c, sn = math.cos(theta / 2.0), math.sin(theta / 2.0)
    real = [c, sn * s[0], sn * s[1], sn * s[2]]
    dual = [-0.5 * d * sn] + [sn * m[i] + 0.5 * d * c * s[i] for i in range(3)]
    return [real, dual]


def to_matrix(a):
    """Return the 4x4 pose matrix [[R, t], [0, 1]] of a unit dual quaternion."""
    (w, x, y, z), t = to_pose(a)
    rot = [
        [1.0 - 2.0 * (y * y + z * z), 2.0 * (x * y - w * z), 2.0 * (x * z + w * y)],
        [2.0 * (x * y + w * z), 1.0 - 2.0 * (x * x + z * z), 2.0 * (y * z - w * x)],
        [2.0 * (x * z - w * y), 2.0 * (y * z + w * x), 1.0 - 2.0 * (x * x + y * y)],
    ]
    return [rot[0] + [t[0]], rot[1] + [t[1]], rot[2] + [t[2]], [0.0, 0.0, 0.0, 1.0]]
