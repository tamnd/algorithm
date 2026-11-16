# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/so3-logarithm-map/. The authors are listed in prov/7X28ZK.jsonl.
"""Logarithm map of SO(3), written out in full.

so3_log(R) returns the exponential coordinates w = omega_hat * theta of a
rotation matrix R, with theta in [0, pi], so that exp([w]) = R. It reads
cos(theta) from the trace and sin(theta) omega_hat from the skew part, and
takes theta = atan2(sin, cos). It has three branches:

* theta < SMALL_THETA: w = s * theta / sin(theta), with the ratio taken from
  its Taylor series, so that R = I gives w = 0 and not 0 / 0.
* SMALL_THETA <= theta <= pi - NEAR_PI: w = s * theta / |s|.
* theta > pi - NEAR_PI: the skew part is small and has a large relative
  error, so the axis comes from the symmetric part of R, and only its sign
  comes from the skew part.

log_textbook(R) is the three-case method as it is usually printed (arccos of
the trace, and the special cases R = I and trace(R) = -1). It is here to
show the loss of accuracy that the branches above avoid.

Matrices are lists of rows. Vectors are lists.
"""

import math

# Below this angle, theta / sin(theta) is replaced by 1 + t^2/6 + 7 t^4/360.
# The first omitted term is 31 t^6 / 15120, below 3e-21 here, so the series
# is exact to the last bit. The closed form theta / |s| is also accurate
# down to tiny angles, because theta comes from atan2; the series is only
# there so that R = I gives w = 0 without a division by zero.
SMALL_THETA = 1e-3

# Above pi - NEAR_PI, the axis comes from the symmetric part of R. At the
# switch, the skew part has |s| = sin(theta), near 1e-2, so its rounding
# error of about 1e-16 gives an axis error of about 1e-14 in either branch.
NEAR_PI = 1e-2


def _norm(x):
    return math.sqrt(sum(a * a for a in x))


def so3_log(r):
    """Return w = omega_hat * theta with exp([w]) = r and theta = |w| in [0, pi].

    r must be a rotation matrix. At theta = pi, both w and -w are valid.
    Near pi, the sign comes from the skew part s; if s is exactly zero, the
    component of w with the largest magnitude is positive.
    """
    c = (r[0][0] + r[1][1] + r[2][2] - 1.0) / 2.0  # @line L1
    c = max(-1.0, min(1.0, c))
    s = [(r[2][1] - r[1][2]) / 2.0, (r[0][2] - r[2][0]) / 2.0, (r[1][0] - r[0][1]) / 2.0]  # @line L2
    sn = _norm(s)
    theta = math.atan2(sn, c)  # @line L3
    if theta < SMALL_THETA:  # @line L4
        t2 = theta * theta
        return [(1.0 + t2 / 6.0 + 7.0 * t2 * t2 / 360.0) * x for x in s]  # @line L5
    if theta <= math.pi - NEAR_PI:  # @line L6
        return [theta / sn * x for x in s]  # @line L7
    # b = (r + r^T) / 2 - c I = (1 - c) omega_hat omega_hat^T.
    b = [[(r[i][j] + r[j][i]) / 2.0 - (c if i == j else 0.0) for j in range(3)] for i in range(3)]  # @line L8
    # Column k of b is (1 - c) omega_k omega_hat. With the largest diagonal
    # entry, omega_k^2 >= 1/3, so the column is far from zero.
    k = max(range(3), key=lambda i: b[i][i])  # @line L9
    col = [b[i][k] for i in range(3)]
    n = _norm(col)
    axis = [x / n for x in col]  # @line L10
    if sum(a * x for a, x in zip(axis, s)) < 0.0:  # @line L11
        axis = [-a for a in axis]
    return [theta * a for a in axis]  # @line L12


def axis_angle(r):
    """Return (omega_hat, theta) for a rotation matrix r.

    omega_hat is None when theta = 0, because every axis is valid there.
    """
    w = so3_log(r)
    theta = _norm(w)
    if theta == 0.0:
        return None, 0.0
    return [x / theta for x in w], theta


def log_textbook(r):
    """Return w by the three-case method with arccos, for comparison only.

    (a) r = I gives w = 0. (b) trace(r) = -1 gives theta = pi and the axis
    from a column of r + I. (c) Otherwise theta = arccos((trace(r) - 1) / 2)
    and [omega_hat] = (r - r^T) / (2 sin(theta)). The tests are exact
    equality tests, as in the printed method.
    """
    tr = r[0][0] + r[1][1] + r[2][2]
    if tr == 3.0:
        return [0.0, 0.0, 0.0]
    if tr == -1.0:
        k = max(range(3), key=lambda i: r[i][i])
        col = [r[i][k] + (1.0 if i == k else 0.0) for i in range(3)]
        n = _norm(col)
        return [math.pi * x / n for x in col]
    theta = math.acos(max(-1.0, min(1.0, (tr - 1.0) / 2.0)))
    f = theta / (2.0 * math.sin(theta))
    return [f * (r[2][1] - r[1][2]), f * (r[0][2] - r[2][0]), f * (r[1][0] - r[0][1])]
