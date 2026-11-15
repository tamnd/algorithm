# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backstepping/. The authors are listed in prov/W1XYZE.jsonl.

"""Integrator backstepping for a system in strict feedback form

    x_i' = f_i(x_1, ..., x_i) + g_i(x_1, ..., x_i) x_(i+1),   i = 1, ..., n - 1,
    x_n' = f_n(x_1, ..., x_n) + g_n(x_1, ..., x_n) u,

with g_i != 0. Step i treats x_(i+1) as a virtual input and defines

    z_i     = x_i - alpha_(i-1)(x_1, ..., x_(i-1)),      alpha_0 = 0,
    D_i     = sum over j < i of (d alpha_(i-1) / d x_j) (f_j + g_j x_(j+1)),
    alpha_i = (-c_i z_i - g_(i-1) z_(i-1) - f_i + D_i) / g_i,

with z_0 = 0 and g_0 = 0. The feedback is u = alpha_n. Along the closed loop
z_i' = -c_i z_i - g_(i-1) z_(i-1) + g_i z_(i+1), so V = sum z_i^2 / 2 has
V' = -sum c_i z_i^2.

D_i is computed exactly by forward-mode differentiation: alpha_(i-1) is
evaluated at x + e v with a new infinitesimal e (e^2 = 0), where
v_j = f_j + g_j x_(j+1), and D_i is the coefficient of e. The numbers are
nested dual numbers with tags, so that the derivatives of different steps do
not mix. With Fraction inputs and rational f_i, g_i every value is exact.

Precondition: f and g are lists of n functions; f[i] and g[i] take the list
[x_1, ..., x_(i+1)] (0-based i) and use only +, -, *, / and integer powers,
or the functions sin, cos and exp of this module. c holds n positive gains.

Cost: step i evaluates step i - 1 once on dual numbers with one more level,
and a dual number with d levels has 2^d parts. One evaluation of the
feedback therefore costs O(2^n) evaluations of the f_i and g_i, up to a
factor n.
"""

import itertools
import math
from fractions import Fraction

__all__ = [
    "Dual",
    "new_tag",
    "sin",
    "cos",
    "exp",
    "real_part",
    "eps_part",
    "virtual_controls",
    "backstepping",
    "lyapunov",
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


def sin(x):
    """sin that accepts Dual numbers."""
    if isinstance(x, Dual):
        return Dual(x.tag, sin(x.re), cos(x.re) * x.eps)
    return math.sin(x)


def cos(x):
    """cos that accepts Dual numbers."""
    if isinstance(x, Dual):
        return Dual(x.tag, cos(x.re), -sin(x.re) * x.eps)
    return math.cos(x)


def exp(x):
    """exp that accepts Dual numbers."""
    if isinstance(x, Dual):
        e = exp(x.re)
        return Dual(x.tag, e, e * x.eps)
    return math.exp(x)


def real_part(x, t):
    """The part of x without the infinitesimal of tag t."""
    return _split(x, t)[0]


def eps_part(x, t):
    """The coefficient of the infinitesimal of tag t in x."""
    return _split(x, t)[1]


def _alphas(f, g, c, i, x):
    """Return [alpha_0(x), ..., alpha_i(x)] as values at the point x."""
    if i == 0:
        return [0]  # @line L1
    t = new_tag()
    xd = list(x)
    for j in range(i - 1):
        v = f[j](x[:j + 1]) + g[j](x[:j + 1]) * x[j + 1]
        xd[j] = Dual(t, x[j], v)
    prev = _alphas(f, g, c, i - 1, xd)  # @line L2
    a = [real_part(p, t) for p in prev]
    z_i = x[i - 1] - a[i - 1]  # @line L3
    d_i = eps_part(prev[i - 1], t)  # @line L4
    if i >= 2:
        z_prev = x[i - 2] - a[i - 2]
        g_prev = g[i - 2](x[:i - 1])
    else:
        z_prev = 0  # @line L1
        g_prev = 0  # @line L1
    alpha_i = _div(-c[i - 1] * z_i - g_prev * z_prev - f[i - 1](x[:i]) + d_i, g[i - 1](x[:i]))  # @line L5
    return a + [alpha_i]


def virtual_controls(f, g, c, x):
    """Return [alpha_0(x), ..., alpha_n(x)], the virtual controls at x."""
    return _alphas(f, g, c, len(f), list(x))


def backstepping(f, g, c, x):
    """Return (u, z): the feedback u = alpha_n(x) and the errors z_1..z_n."""
    a = virtual_controls(f, g, c, x)
    z = [x[i] - a[i] for i in range(len(f))]
    return a[-1], z  # @line L6


def lyapunov(f, g, c, x):
    """Return V(x) = sum z_i^2 / 2."""
    _, z = backstepping(f, g, c, x)
    return _div(sum(zi * zi for zi in z), 2)


def closed_loop(f, g, c):
    """Return F(t, x, u) of the closed loop for the simulation helper.

    The feedback is evaluated inside the right side; u is ignored.
    """
    n = len(f)

    def F(t, x, u=None):
        uu, _ = backstepping(f, g, c, x)
        dx = [f[i](x[:i + 1]) + g[i](x[:i + 1]) * x[i + 1] for i in range(n - 1)]
        dx.append(f[n - 1](x) + g[n - 1](x) * uu)
        return dx
    return F
