# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pose-compounding-operators/. The authors are listed in prov/Z8QZF9.jsonl.
"""The compounding operators of Smith, Self and Cheeseman for planar poses.

A planar pose is a list (x, y, phi), with phi in radians, wrapped to
[-pi, pi). x_ij is the pose of frame j in frame i.

- oplus(a, b) is the head-to-tail compound x_ik = x_ij (+) x_jk.
- ominus(a) is the inverse x_ji = (-) x_ij.
- jac_oplus and jac_ominus are their Jacobians, written with the result
  as in the paper.
- compound(...) and invert(...) carry a mean and a covariance through the
  operators to first order. This is a linearization: it is exact only
  when the operators are linear over the spread of the inputs.
- tail_to_tail(...) gives x_jk = (-) x_ij (+) x_ik from two poses that
  share their first frame.

Matrices are lists of rows.
"""

import math


def wrap(a):
    """Return a + 2 pi k in [-pi, pi)."""
    w = math.fmod(a + math.pi, 2.0 * math.pi)
    if w < 0.0:
        w += 2.0 * math.pi
    w -= math.pi
    if w >= math.pi:
        w -= 2.0 * math.pi
    return w


def _mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def _t(a):
    return [list(c) for c in zip(*a)]


def _add(*ms):
    return [[sum(m[i][j] for m in ms) for j in range(len(ms[0][0]))] for i in range(len(ms[0]))]


def _sandwich(j, c, k=None):
    """Return j c k^T (k = j if not given)."""
    return _mul(_mul(j, c), _t(j if k is None else k))


def oplus(a, b):
    """Return the head-to-tail compound a (+) b."""
    xa, ya, pa = a
    xb, yb, pb = b
    c, s = math.cos(pa), math.sin(pa)
    return [xa + c * xb - s * yb, ya + s * xb + c * yb, wrap(pa + pb)]


def ominus(a):
    """Return the inverse (-) a, the pose of frame i in frame j."""
    x, y, p = a
    c, s = math.cos(p), math.sin(p)
    return [-c * x - s * y, s * x - c * y, wrap(-p)]


def jac_oplus(a, b):
    """Return (J1, J2), the 3x3 Jacobians of a (+) b in a and in b."""
    xa, ya, pa = a
    x3, y3, _ = oplus(a, b)
    c, s = math.cos(pa), math.sin(pa)
    j1 = [[1.0, 0.0, -(y3 - ya)], [0.0, 1.0, x3 - xa], [0.0, 0.0, 1.0]]
    j2 = [[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]]
    return j1, j2


def jac_ominus(a):
    """Return the 3x3 Jacobian of (-) a."""
    c, s = math.cos(a[2]), math.sin(a[2])
    xi, yi, _ = ominus(a)
    return [[-c, -s, yi], [s, -c, -xi], [0.0, 0.0, -1.0]]


def compound(a, ca, b, cb, cab=None):
    """Return (mean, covariance) of x_ik = x_ij (+) x_jk to first order.

    a = x_ij with covariance ca, b = x_jk with covariance cb, and cab the
    cross-covariance E[(a - mean a)(b - mean b)^T] (zero if not given).
    """
    xa, ya, pa = a  # @line L1
    c, s = math.cos(pa), math.sin(pa)  # @line L1
    x3 = oplus(a, b)  # @line L2
    j1 = [[1.0, 0.0, -(x3[1] - ya)], [0.0, 1.0, x3[0] - xa], [0.0, 0.0, 1.0]]  # @line L3
    j2 = [[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]]  # @line L4
    c3 = _add(_sandwich(j1, ca), _sandwich(j2, cb))  # @line L5
    if cab is not None:  # @line L5
        cross = _sandwich(j1, cab, j2)  # @line L5
        c3 = _add(c3, cross, _t(cross))  # @line L5
    return x3, c3  # @line L6


def invert(a, ca):
    """Return (mean, covariance) of x_ji = (-) x_ij to first order."""
    c, s = math.cos(a[2]), math.sin(a[2])  # @line I1
    xi = [-c * a[0] - s * a[1], s * a[0] - c * a[1], wrap(-a[2])]  # @line I2
    j = [[-c, -s, xi[1]], [s, -c, -xi[0]], [0.0, 0.0, -1.0]]  # @line I3
    return xi, _sandwich(j, ca)  # @line I4


def tail_to_tail(a, ca, b, cb, cab=None):
    """Return (mean, covariance) of x_jk = (-) x_ij (+) x_ik to first order.

    a = x_ij and b = x_ik share the frame i; cab is their cross-covariance.
    The Jacobian in (a, b) is [J1 Jm, J2], with Jm = jac_ominus(a).
    """
    ai = ominus(a)
    j1, j2 = jac_oplus(ai, b)
    jm = jac_ominus(a)
    ja = _mul(j1, jm)
    out = _add(_sandwich(ja, ca), _sandwich(j2, cb))
    if cab is not None:
        cross = _sandwich(ja, cab, j2)
        out = _add(out, cross, _t(cross))
    return oplus(ai, b), out


def head_to_head(a, ca, b, cb, cab=None):
    """Return (mean, covariance) of x_ik = x_ij (+) (-) x_kj to first order.

    a = x_ij and b = x_kj share the frame j; cab is their cross-covariance.
    """
    bi, cbi = invert(b, cb)
    jm = jac_ominus(b)
    cross = None if cab is None else _mul(cab, _t(jm))
    return compound(a, ca, bi, cbi, cross)
