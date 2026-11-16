# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/se3-exponential-map/. The authors are listed in prov/25FNCG.jsonl.
"""Exponential map of SE(3), written out in full.

A screw axis S = (omega, v) has |omega| = 1, or omega = 0 and |v| = 1.
exp_screw(S, theta) is the closed form of Lynch and Park, Modern Robotics,
Section 3.3.3. exp_coords(xi) takes general exponential coordinates
xi = S * theta, and uses a Taylor series when the rotation angle is small.
log_coords(T) is the inverse map, with theta in [0, pi].

Matrices are lists of rows. The 4x4 result is [[R, p], [0, 0, 0, 1]].
"""

import math

# Below this rotation angle, exp_coords and log_coords use Taylor series.
# The first omitted term of each series is of order theta^6, below 3e-16
# for theta < 1e-2. Above the threshold, exp_screw divides u by theta, and
# the rounding error of 1 - cos(theta) grows like 1e-16 |u| / theta, which
# is near 1e-14 |u| at the threshold.
SERIES_THETA = 1e-2


def _hat(w):
    return [[0.0, -w[2], w[1]], [w[2], 0.0, -w[0]], [-w[1], w[0], 0.0]]


def _mul3(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def _comb(c0, c1, w, c2, w2):
    """Return c0 I + c1 w + c2 w2 for 3x3 matrices w and w2."""
    return [[(c0 if i == j else 0.0) + c1 * w[i][j] + c2 * w2[i][j] for j in range(3)] for i in range(3)]


def _pose(r, p):
    return [r[0] + [p[0]], r[1] + [p[1]], r[2] + [p[2]], [0.0, 0.0, 0.0, 1.0]]


def _apply(m, x):
    return [sum(m[i][k] * x[k] for k in range(3)) for i in range(3)]


def exp_screw(s, theta):
    """Return exp([S] theta) for a screw axis S = (omega, v) and a distance theta.

    Raise ValueError if S is not a screw axis: |omega| must be 1, or
    omega = 0 and |v| = 1, within 1e-9.
    """
    w, v = list(s[:3]), list(s[3:])  # @line L1
    nw = math.sqrt(sum(x * x for x in w))
    nv = math.sqrt(sum(x * x for x in v))
    if nw <= 1e-9:  # @line L2
        if abs(nv - 1.0) > 1e-9:
            raise ValueError("omega = 0 needs |v| = 1")
        return _pose([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], [x * theta for x in v])  # @line L3
    if abs(nw - 1.0) > 1e-9:
        raise ValueError("omega must be a unit vector")
    k = _hat(w)  # @line L4
    k2 = _mul3(k, k)
    r = _comb(1.0, math.sin(theta), k, 1.0 - math.cos(theta), k2)  # @line L5
    g = _comb(theta, 1.0 - math.cos(theta), k, theta - math.sin(theta), k2)  # @line L6
    p = _apply(g, v)  # @line L7
    return _pose(r, p)  # @line L8


def exp_coords(xi):
    """Return exp([xi]) for exponential coordinates xi = (w, u) = S * theta.

    With theta = |w|: if theta >= SERIES_THETA, normalize and call
    exp_screw. If 0 < theta < SERIES_THETA, use the series
    R = I + a [w] + b [w]^2 and p = (I + b [w] + c [w]^2) u, where
    a = sin(theta) / theta, b = (1 - cos(theta)) / theta^2 and
    c = (theta - sin(theta)) / theta^3 are replaced by their Taylor series.
    If w = 0, the result is the translation by u.
    """
    w, u = list(xi[:3]), list(xi[3:])  # @line E1
    theta = math.sqrt(sum(x * x for x in w))  # @line E2
    if theta >= SERIES_THETA:  # @line E3
        return exp_screw([x / theta for x in xi], theta)  # @line E4
    t2 = theta * theta  # @line E5
    a = 1.0 - t2 / 6.0 + t2 * t2 / 120.0
    b = 0.5 - t2 / 24.0 + t2 * t2 / 720.0
    c = 1.0 / 6.0 - t2 / 120.0 + t2 * t2 / 5040.0
    k = _hat(w)  # @line E6
    k2 = _mul3(k, k)
    r = _comb(1.0, a, k, b, k2)
    p = _apply(_comb(1.0, b, k, c, k2), u)
    return _pose(r, p)  # @line E7


def log_coords(t):
    """Return xi = (w, u) with exp_coords(xi) = t and |w| in [0, pi].

    w is the logarithm of R (see the so3-logarithm-map page), and
    u = G^(-1) p with G^(-1) = I - [w] / 2 + d [w]^2 and
    d = (1 - (theta / 2) cot(theta / 2)) / theta^2.
    """
    r = [row[:3] for row in t[:3]]
    p = [t[0][3], t[1][3], t[2][3]]
    c = max(-1.0, min(1.0, (r[0][0] + r[1][1] + r[2][2] - 1.0) / 2.0))
    s = [(r[2][1] - r[1][2]) / 2.0, (r[0][2] - r[2][0]) / 2.0, (r[1][0] - r[0][1]) / 2.0]
    sn = math.sqrt(sum(x * x for x in s))
    theta = math.atan2(sn, c)
    if theta < SERIES_THETA:
        t2 = theta * theta
        w = [x * (1.0 + t2 / 6.0 + 7.0 * t2 * t2 / 360.0) for x in s]
    elif theta <= math.pi - 1e-2:
        w = [theta / sn * x for x in s]
    else:
        b = [[(r[i][j] + r[j][i]) / 2.0 - (c if i == j else 0.0) for j in range(3)] for i in range(3)]
        k = max(range(3), key=lambda i: b[i][i])
        col = [b[i][k] for i in range(3)]
        ncol = math.sqrt(sum(x * x for x in col))
        axis = [x / ncol for x in col]
        if sum(x * y for x, y in zip(axis, s)) < 0.0:
            axis = [-x for x in axis]
        w = [theta * x for x in axis]
    if theta < SERIES_THETA:
        t2 = theta * theta
        d = 1.0 / 12.0 + t2 / 720.0 + t2 * t2 / 30240.0
    else:
        half = theta / 2.0
        d = (1.0 - half * math.cos(half) / math.sin(half)) / (theta * theta)
    k = _hat(w)
    gi = _comb(1.0, -0.5, k, d, _mul3(k, k))
    return w + _apply(gi, p)


def screw_axis(q, s_hat, h):
    """Return the screw axis (omega, -omega x q + h omega) of a rotation about
    the unit axis s_hat through the point q, with pitch h."""
    w = list(s_hat)
    wxq = [w[1] * q[2] - w[2] * q[1], w[2] * q[0] - w[0] * q[2], w[0] * q[1] - w[1] * q[0]]
    return w + [-a + h * b for a, b in zip(wxq, w)]
