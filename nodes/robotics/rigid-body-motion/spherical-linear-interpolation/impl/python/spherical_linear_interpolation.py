# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spherical-linear-interpolation/. The authors are listed in prov/BJ0DKQ.jsonl.
"""Spherical linear interpolation (slerp) of unit quaternions.

Quaternions use the Hamilton convention, scalar first, q = (w, x, y, z).
slerp(q0, q1, t) returns the point at the fraction t of the great arc from
q0 to q1 on the unit sphere of R^4:

    slerp(q0, q1, t) = sin((1 - t) W) / sin(W) q0 + sin(t W) / sin(W) q1,

where W is the angle between q0 and q1 in R^4. This equals q0 (q0* q1)^t.
If q0 . q1 < 0, q1 is replaced by -q1 first. Both give the same rotation,
and the replacement makes the arc the short one, so the rotation turns by
at most pi. W comes from atan2 of |q1 - q0| and |q1 + q0|, which is
accurate at every angle. For W below SMALL_ANGLE, the normalized linear
interpolation is used. Its point lies on the same arc, at an angle that
differs from t W by -t (1 - t) (1 - 2 t) W^3 / 6 to leading order, which is
at most about 0.016 W^3.

slerp_power(q0, q1, t) is the second method: q0 (q0* q1)^t with the power
taken through the axis and the angle. It is here for the tests.
"""

import math

# Below this angle (in radians, on the sphere of R^4), slerp is replaced by
# the normalized linear interpolation. Its error there is below 2e-20.
SMALL_ANGLE = 1e-6


def _norm(q):
    return math.sqrt(sum(a * a for a in q))


def slerp(q0, q1, t):
    """Return the unit quaternion at the fraction t of the short arc from q0 to q1."""
    d = sum(a * b for a, b in zip(q0, q1))  # @line L1
    if d < 0.0:  # @line L2
        q1 = [-a for a in q1]  # @line L3
    a = _norm([y - x for x, y in zip(q0, q1)])
    b = _norm([y + x for x, y in zip(q0, q1)])
    big_w = 2.0 * math.atan2(a, b)  # @line L4
    if big_w < SMALL_ANGLE:  # @line L5
        q = [(1.0 - t) * x + t * y for x, y in zip(q0, q1)]  # @line L6
        n = _norm(q)
        return [x / n for x in q]  # @line L7
    s = math.sin(big_w)
    c0 = math.sin((1.0 - t) * big_w) / s  # @line L8
    c1 = math.sin(t * big_w) / s  # @line L9
    return [c0 * x + c1 * y for x, y in zip(q0, q1)]  # @line L10


def _mul(q, r):
    a1, b1, c1, d1 = q
    a2, b2, c2, d2 = r
    return [
        a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
        a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
        a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
        a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2,
    ]


def quat_pow(q, t):
    """Return q^t for a unit quaternion q = (cos h, sin h u) with q[0] >= 0.

    q^t = (cos(t h), sin(t h) u), with h = atan2(|v|, w) in [0, pi / 2].
    For q = (1, 0, 0, 0) the result is (1, 0, 0, 0).
    """
    v = q[1:]
    s = _norm(v)
    if s == 0.0:
        return [1.0, 0.0, 0.0, 0.0]
    h = math.atan2(s, q[0])
    f = math.sin(t * h) / s
    return [math.cos(t * h)] + [f * x for x in v]


def slerp_power(q0, q1, t):
    """Return q0 (q0* q1)^t, after the sign flip of q1 for the short arc."""
    if sum(a * b for a, b in zip(q0, q1)) < 0.0:
        q1 = [-a for a in q1]
    rel = _mul([q0[0], -q0[1], -q0[2], -q0[3]], q1)
    return _mul(q0, quat_pow(rel, t))
