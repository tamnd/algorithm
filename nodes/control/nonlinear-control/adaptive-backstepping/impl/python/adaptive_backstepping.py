# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-backstepping/. The authors are listed in prov/5JZM0E.jsonl.

"""Adaptive backstepping with tuning functions for a system in parametric
strict feedback form

    x_i' = x_(i+1) + phi_i(x_1, ..., x_i)^T theta,      i = 1, ..., n - 1,
    x_n' = beta(x) u + phi_n(x)^T theta,

with theta in R^p constant and unknown, and beta(x) != 0 known. With the
estimate thetahat and alpha_0 = 0, z_0 = 0, tau_0 = 0, step i computes

    z_i     = x_i - alpha_(i-1)(x_1, ..., x_(i-1), thetahat)
    w_i     = phi_i - sum_(k<i) (d alpha_(i-1) / d x_k) phi_k
    tau_i   = tau_(i-1) + w_i z_i
    alpha_i = -z_(i-1) - c_i z_i - w_i^T thetahat
              + sum_(k<i) (d alpha_(i-1) / d x_k) x_(k+1)
              + (d alpha_(i-1) / d thetahat) Gamma tau_i
              + sum_(k=2..i-1) z_k (d alpha_(k-1) / d thetahat) Gamma w_i

and the controller is u = alpha_n / beta(x), thetahat' = Gamma tau_n. Along
the closed loop, V = |z|^2 / 2 + (theta - thetahat)^T Gamma^(-1)
(theta - thetahat) / 2 has V' = -sum c_i z_i^2.

The partial derivatives are computed exactly by forward-mode
differentiation with tagged nested dual numbers: one dual direction for
each of x_1, ..., x_(i-1) and thetahat_1, ..., thetahat_p. With Fraction
inputs and rational phi_i, beta every value is exact.

Precondition: phi is a list of n functions; phi[i] takes [x_1, ..., x_(i+1)]
(0-based i) and returns a list of p numbers, using only +, -, *, / and
integer powers. beta(x) is never zero. c holds n positive gains, and Gamma
is a symmetric positive definite p by p matrix (a list of rows).

Cost: step i evaluates step i - 1 at i - 1 + p + 1 points, one level deeper
in the dual numbers, so one evaluation of the controller costs a number of
operations that grows like the product of (i + p) over the steps, times a
power of 3 for the nested dual products. It is meant for small n.
"""

import itertools
from fractions import Fraction

__all__ = [
    "Dual",
    "new_tag",
    "real_part",
    "eps_part",
    "stages",
    "adaptive_backstepping",
    "closed_loop",
]

_TAGS = itertools.count(1)


def new_tag():
    """Return a tag larger than every tag handed out before."""
    return next(_TAGS)


def _tag(x):
    return x.tag if isinstance(x, Dual) else 0


def _div(p, q):
    # int / int would give a float; keep exact values exact.
    if isinstance(p, int) and isinstance(q, int):
        return Fraction(p, q)
    return p / q


def _split(x, t):
    if isinstance(x, Dual) and x.tag == t:
        return x.re, x.eps
    return x, 0


class Dual:
    """re + eps e with e^2 = 0. re and eps may be Duals with smaller tags."""

    __slots__ = ("tag", "re", "eps")

    def __init__(self, tag, re, eps):
        self.tag = tag
        self.re = re
        self.eps = eps

    def __add__(self, other):
        t = max(_tag(self), _tag(other))
        a, b = _split(self, t)
        c, d = _split(other, t)
        return Dual(t, a + c, b + d)

    __radd__ = __add__

    def __neg__(self):
        return Dual(self.tag, -self.re, -self.eps)

    def __pos__(self):
        return self

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        t = max(_tag(self), _tag(other))
        a, b = _split(self, t)
        c, d = _split(other, t)
        return Dual(t, a * c, a * d + b * c)

    __rmul__ = __mul__

    def __truediv__(self, other):
        t = max(_tag(self), _tag(other))
        a, b = _split(self, t)
        c, d = _split(other, t)
        return Dual(t, _div(a, c), _div(b * c - a * d, c * c))

    def __rtruediv__(self, other):
        t = self.tag
        a, b = _split(other, t)
        c, d = self.re, self.eps
        return Dual(t, _div(a, c), _div(b * c - a * d, c * c))

    def __pow__(self, k):
        if not isinstance(k, int) or k < 0:
            raise ValueError("only nonnegative integer powers")
        result = 1
        for _ in range(k):
            result = result * self
        return result


def real_part(x, t):
    """The part of x without the infinitesimal of tag t."""
    return _split(x, t)[0]


def eps_part(x, t):
    """The coefficient of the infinitesimal of tag t in x."""
    return _split(x, t)[1]


def _matvec(M, v):
    return [sum((M[r][s] * v[s] for s in range(len(v))), 0) for r in range(len(M))]


def _dot(a, b):
    return sum((ai * bi for ai, bi in zip(a, b)), 0)


def stages(phi, c, Gamma, i, x, th):
    """Return (alpha, z, w, tau) of steps 0..i at the point (x, thetahat).

    alpha has i + 1 entries (alpha[0] = 0); z and w have i entries (z[k] is
    z_(k+1)); tau has i + 1 entries of length p (tau[0] = 0).
    """
    p = len(th)
    if i == 0:
        return [0], [], [], [[0] * p]  # @line L1
    A, Z, W, T = stages(phi, c, Gamma, i - 1, x, th)  # @line L2
    # dx[k][j] = d alpha_k / d x_(j+1), dth[k][l] = d alpha_k / d thetahat_l
    dx = [[0] * (i - 1) for _ in range(i)]
    dth = [[0] * p for _ in range(i)]
    if i >= 2:
        for j in range(i - 1):
            t = new_tag()
            xd = list(x)
            xd[j] = Dual(t, x[j], 1)
            Ad = stages(phi, c, Gamma, i - 1, xd, th)[0]
            for k in range(i):
                dx[k][j] = eps_part(Ad[k], t)
        for l in range(p):
            t = new_tag()
            thd = list(th)
            thd[l] = Dual(t, th[l], 1)
            Ad = stages(phi, c, Gamma, i - 1, x, thd)[0]
            for k in range(i):
                dth[k][l] = eps_part(Ad[k], t)
    z_i = x[i - 1] - A[i - 1]  # @line L3
    phi_i = phi[i - 1](x[:i])
    w_i = list(phi_i)  # @line L4
    for k in range(i - 1):
        phi_k = phi[k](x[:k + 1])
        w_i = [w_i[l] - dx[i - 1][k] * phi_k[l] for l in range(p)]  # @line L4
    tau_i = [T[i - 1][l] + w_i[l] * z_i for l in range(p)]  # @line L5
    z_prev = Z[i - 2] if i >= 2 else 0
    alpha_i = -z_prev - c[i - 1] * z_i - _dot(w_i, th)  # @line L6
    for k in range(i - 1):
        alpha_i = alpha_i + dx[i - 1][k] * x[k + 1]  # @line L6
    alpha_i = alpha_i + _dot(dth[i - 1], _matvec(Gamma, tau_i))  # @line L6
    Gw = _matvec(Gamma, w_i)
    for k in range(2, i):
        alpha_i = alpha_i + Z[k - 1] * _dot(dth[k - 1], Gw)  # @line L6
    return A + [alpha_i], Z + [z_i], W + [w_i], T + [tau_i]


def adaptive_backstepping(phi, beta, c, Gamma, x, th):
    """Return (u, thetahat_dot, z) at the state x and the estimate th."""
    n = len(phi)
    A, Z, _, T = stages(phi, c, Gamma, n, list(x), list(th))
    u = _div(A[n], beta(list(x)))  # @line L7
    th_dot = _matvec(Gamma, T[n])  # @line L7
    return u, th_dot, Z


def closed_loop(phi, beta, c, Gamma, theta):
    """Return F(t, s, u) for the simulation helper, with s = (x, thetahat).

    theta is the true parameter, used only by the plant. u is ignored; the
    controller is evaluated inside the right side.
    """
    n = len(phi)

    def F(t, s, u=None):
        x, th = list(s[:n]), list(s[n:])
        uu, th_dot, _ = adaptive_backstepping(phi, beta, c, Gamma, x, th)
        dx = [x[i + 1] + _dot(phi[i](x[:i + 1]), theta) for i in range(n - 1)]
        dx.append(beta(x) * uu + _dot(phi[n - 1](x), theta))
        return dx + list(th_dot)
    return F
