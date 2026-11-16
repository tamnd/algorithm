# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shepperd-method/. The authors are listed in prov/DK6ZQE.jsonl.
"""Shepperd's method: the unit quaternion of a rotation matrix.

Quaternions use the Hamilton convention, scalar first, q = (w, x, y, z),
and q acts on a vector v by (0, R v) = q (0, v) q*. For such a q,

    4 w^2 = 1 + t           4 w x = r32 - r23     4 x y = r21 + r12
    4 x^2 = 1 + 2 r11 - t   4 w y = r13 - r31     4 x z = r13 + r31
    4 y^2 = 1 + 2 r22 - t   4 w z = r21 - r12     4 y z = r32 + r23
    4 z^2 = 1 + 2 r33 - t

where t = r11 + r22 + r33 is the trace (indices from 1 in the comments,
from 0 in the code). The four squares sum to 4, so the largest one is at
least 1. Shepperd's method takes the square root of the largest one, and
gets the other three components from the off-diagonal sums and differences,
divided by four times that component, which is at least 2.

shepperd(R) is the method. quat_textbook(R) is the method that always
divides by 4 w; it is here to show the loss of accuracy near the angle pi.

Matrices are lists of rows. Vectors and quaternions are lists.
"""

import math


def shepperd(r):
    """Return the unit quaternion (w, x, y, z), with w >= 0, of the rotation r."""
    t = r[0][0] + r[1][1] + r[2][2]  # @line L1
    k = max(range(4), key=lambda i: (t, r[0][0], r[1][1], r[2][2])[i])  # @line L2
    if k == 0:  # @line L3
        w = math.sqrt(1.0 + t) / 2.0  # @line L4
        f = 4.0 * w
        q = [w, (r[2][1] - r[1][2]) / f, (r[0][2] - r[2][0]) / f, (r[1][0] - r[0][1]) / f]  # @line L5
    elif k == 1:  # @line L6
        x = math.sqrt(1.0 + 2.0 * r[0][0] - t) / 2.0  # @line L7
        f = 4.0 * x
        q = [(r[2][1] - r[1][2]) / f, x, (r[1][0] + r[0][1]) / f, (r[0][2] + r[2][0]) / f]  # @line L8
    elif k == 2:  # @line L9
        y = math.sqrt(1.0 + 2.0 * r[1][1] - t) / 2.0  # @line L10
        f = 4.0 * y
        q = [(r[0][2] - r[2][0]) / f, (r[1][0] + r[0][1]) / f, y, (r[2][1] + r[1][2]) / f]  # @line L11
    else:  # @line L12
        z = math.sqrt(1.0 + 2.0 * r[2][2] - t) / 2.0  # @line L13
        f = 4.0 * z
        q = [(r[1][0] - r[0][1]) / f, (r[0][2] + r[2][0]) / f, (r[2][1] + r[1][2]) / f, z]  # @line L14
    if q[0] < 0.0:  # @line L15
        q = [-a for a in q]
    return q  # @line L16


def branch(r):
    """Return the index (0 for w, 1 for x, 2 for y, 3 for z) that line L2 picks."""
    t = r[0][0] + r[1][1] + r[2][2]
    return max(range(4), key=lambda i: (t, r[0][0], r[1][1], r[2][2])[i])


def quat_textbook(r):
    """Return the quaternion by the formula that always divides by 4 w.

    w = sqrt(1 + t) / 2, and x, y, z from the skew part. It fails at w = 0
    (a rotation by pi) and loses accuracy when w is small.
    """
    t = r[0][0] + r[1][1] + r[2][2]
    w = math.sqrt(max(0.0, 1.0 + t)) / 2.0
    f = 4.0 * w
    return [w, (r[2][1] - r[1][2]) / f, (r[0][2] - r[2][0]) / f, (r[1][0] - r[0][1]) / f]
