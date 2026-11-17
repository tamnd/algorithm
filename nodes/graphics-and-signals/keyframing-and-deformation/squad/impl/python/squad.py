# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/squad/. The authors are listed in prov/5MKSXN.jsonl.
"""Spherical quadrangle interpolation (squad) of unit quaternion keys.

Keys q_0, ..., q_(n-1) are unit quaternions (Hamilton, scalar first) at the
times 0, 1, ..., n - 1. The curve on segment i, for t in [0, 1], is

    squad(q_i, q_(i+1), s_i, s_(i+1), t)
        = arc(arc(q_i, q_(i+1), t), arc(s_i, s_(i+1), t), 2 t (1 - t)),

where arc(p, q, t) = p exp(t log(p* q)) is slerp without a sign flip, and

    s_i = q_i exp(-(log(q_i* q_(i+1)) + log(q_i* q_(i-1))) / 4)

for the inner keys. The end keys use s_0 = q_0 and s_(n-1) = q_(n-1).
Before this, the keys are made sign consistent: q_i is replaced by -q_i if
q_(i-1) . q_i < 0. The curve passes through the keys and has a continuous
first derivative at each inner key (Shoemake 1987; Dam, Koch and Lillholm
1998).
"""

import math

from anim import q_conj, q_dot, q_exp, q_log, q_mul


def arc(p, q, t):
    """Return p (p* q)^t, the point at the fraction t of the arc from p to q.

    No sign flip is done. For p . q >= 0 this is slerp on the short arc.
    """
    lg = q_log(q_mul(q_conj(p), q))
    return q_mul(p, q_exp((0.0, t * lg[1], t * lg[2], t * lg[3])))


def align_signs(keys):
    """Return the keys with q_i replaced by -q_i where q_(i-1) . q_i < 0."""
    out = [tuple(keys[0])]
    for q in keys[1:]:
        q = tuple(q)
        if q_dot(out[-1], q) < 0.0:  # @line L1
            q = (-q[0], -q[1], -q[2], -q[3])  # @line L2
        out.append(q)
    return out


def control_points(keys):
    """Return the inner control quaternions s_0, ..., s_(n-1) of aligned keys."""
    n = len(keys)
    s = [keys[0]] + [None] * (n - 2) + [keys[-1]] if n > 1 else [keys[0]]  # @line L3
    for i in range(1, n - 1):  # @line L4
        qi_c = q_conj(keys[i])
        a = q_log(q_mul(qi_c, keys[i + 1]))  # @line L5
        b = q_log(q_mul(qi_c, keys[i - 1]))  # @line L6
        e = (0.0, -(a[1] + b[1]) / 4.0, -(a[2] + b[2]) / 4.0, -(a[3] + b[3]) / 4.0)
        s[i] = q_mul(keys[i], q_exp(e))  # @line L7
    return s


def squad_segment(qi, qj, si, sj, t):
    """Return squad(q_i, q_(i+1), s_i, s_(i+1), t) for t in [0, 1]."""
    a = arc(qi, qj, t)  # @line L8
    b = arc(si, sj, t)  # @line L9
    return arc(a, b, 2.0 * t * (1.0 - t))  # @line L10


class Squad:
    """A squad curve through keys at the times 0, 1, ..., n - 1."""

    def __init__(self, keys):
        if len(keys) < 2:
            raise ValueError("squad needs at least two keys")
        self.keys = align_signs(keys)
        self.ctrl = control_points(self.keys)

    def __call__(self, u):
        """Return the unit quaternion at the time u in [0, n - 1]."""
        n = len(self.keys)
        if u <= 0.0:
            i, t = 0, 0.0
        elif u >= n - 1:
            i, t = n - 2, 1.0
        else:
            i = int(math.floor(u))
            t = u - i
        return squad_segment(self.keys[i], self.keys[i + 1], self.ctrl[i], self.ctrl[i + 1], t)

    def segment(self, i, t):
        """Return the point at the local time t in [0, 1] of segment i."""
        return squad_segment(self.keys[i], self.keys[i + 1], self.ctrl[i], self.ctrl[i + 1], t)
