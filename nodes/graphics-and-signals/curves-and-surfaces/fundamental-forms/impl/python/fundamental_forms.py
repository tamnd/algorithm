# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fundamental-forms/. The authors are listed in prov/XRW8YW.jsonl.

"""The first and second fundamental forms of a parametric surface.

The surface is a Python function f(u, v) that returns three coordinates and
uses only +, -, *, /, ** with an integer power, and the functions sin, cos and
sqrt of this module. The module runs f on second order jets in (u, v), which
carry a value, its two first partials and its three second partials, so the
partials of the surface come out to rounding error, with no step size.
"""

import math
from typing import Callable, Tuple


class Jet:
    """A truncated Taylor expansion to order 2 in two variables."""

    __slots__ = ("f", "u", "v", "uu", "uv", "vv")

    def __init__(self, f, u=0.0, v=0.0, uu=0.0, uv=0.0, vv=0.0):
        self.f, self.u, self.v, self.uu, self.uv, self.vv = f, u, v, uu, uv, vv

    @staticmethod
    def lift(x) -> "Jet":
        return x if isinstance(x, Jet) else Jet(x)

    def __add__(self, o):
        o = Jet.lift(o)
        return Jet(self.f + o.f, self.u + o.u, self.v + o.v,
                   self.uu + o.uu, self.uv + o.uv, self.vv + o.vv)

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.f, -self.u, -self.v, -self.uu, -self.uv, -self.vv)

    def __sub__(self, o):
        return self + (-Jet.lift(o))

    def __rsub__(self, o):
        return Jet.lift(o) - self

    def __mul__(self, o):
        o = Jet.lift(o)
        return Jet(self.f * o.f,
                   self.u * o.f + self.f * o.u,
                   self.v * o.f + self.f * o.v,
                   self.uu * o.f + 2 * self.u * o.u + self.f * o.uu,
                   self.uv * o.f + self.u * o.v + self.v * o.u + self.f * o.uv,
                   self.vv * o.f + 2 * self.v * o.v + self.f * o.vv)

    __rmul__ = __mul__

    def chain(self, g0, g1, g2) -> "Jet":
        """g(self) for a function g with g(x) = g0, g'(x) = g1, g''(x) = g2."""
        return Jet(g0, g1 * self.u, g1 * self.v,
                   g1 * self.uu + g2 * self.u * self.u,
                   g1 * self.uv + g2 * self.u * self.v,
                   g1 * self.vv + g2 * self.v * self.v)

    def reciprocal(self) -> "Jet":
        x = self.f
        return self.chain(1 / x, -1 / (x * x), 2 / (x * x * x))

    def __truediv__(self, o):
        return self * Jet.lift(o).reciprocal()

    def __rtruediv__(self, o):
        return Jet.lift(o) * self.reciprocal()

    def __pow__(self, k: int):
        if not isinstance(k, int) or k < 0:
            raise ValueError("only powers by integers k >= 0")
        out = Jet(1)
        for _ in range(k):
            out = out * self
        return out


def sin(x):
    if isinstance(x, Jet):
        return x.chain(math.sin(x.f), math.cos(x.f), -math.sin(x.f))
    return math.sin(x)


def cos(x):
    if isinstance(x, Jet):
        return x.chain(math.cos(x.f), -math.sin(x.f), -math.cos(x.f))
    return math.cos(x)


def sqrt(x):
    if isinstance(x, Jet):
        r = math.sqrt(x.f)
        return x.chain(r, 0.5 / r, -0.25 / (r * x.f))
    return math.sqrt(x)


Vec = Tuple[float, float, float]


def _dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def partials(f: Callable, u: float, v: float):
    """S_u, S_v, S_uu, S_uv, S_vv of the surface f at (u, v)."""
    out = f(Jet(u, 1.0, 0.0), Jet(v, 0.0, 1.0))
    out = [Jet.lift(c) for c in out]
    return tuple(tuple(getattr(c, k) for c in out) for k in ("u", "v", "uu", "uv", "vv"))


def fundamental_forms(f: Callable, u: float, v: float) -> Tuple[float, ...]:
    """(E, F, G, L, M, N) at (u, v), with the unit normal n = S_u x S_v / |S_u x S_v|."""
    su, sv, suu, suv, svv = partials(f, u, v)  # @line L1
    e, ff, g = _dot(su, su), _dot(su, sv), _dot(sv, sv)  # @line L2
    nn = _cross(su, sv)  # @line L3
    w = math.sqrt(_dot(nn, nn))
    if w == 0:  # @line L4
        raise ValueError("the parametrization is not regular at this point")
    n = (nn[0] / w, nn[1] / w, nn[2] / w)  # @line L5
    return e, ff, g, _dot(suu, n), _dot(suv, n), _dot(svv, n)  # @line L6


def first_form(forms, a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """I(a, b) = E a1 b1 + F (a1 b2 + a2 b1) + G a2 b2 for directions a, b in the (u, v) plane."""
    e, f, g = forms[:3]
    return e * a[0] * b[0] + f * (a[0] * b[1] + a[1] * b[0]) + g * a[1] * b[1]


def second_form(forms, a: Tuple[float, float], b: Tuple[float, float]) -> float:
    ell, m, n = forms[3:]
    return ell * a[0] * b[0] + m * (a[0] * b[1] + a[1] * b[0]) + n * a[1] * b[1]


def normal_curvature(forms, d: Tuple[float, float]) -> float:
    """II(d, d) / I(d, d): the curvature of the normal section in the direction d."""
    return second_form(forms, d, d) / first_form(forms, d, d)


def curve_length(f: Callable, path: Callable, dpath: Callable, t0: float, t1: float, n: int = 200) -> float:
    """The length of the surface curve f(path(t)), from the first form, by composite Simpson."""
    if n % 2:
        n += 1
    h = (t1 - t0) / n

    def speed(t):
        u, v = path(t)
        du, dv = dpath(t)
        return math.sqrt(first_form(fundamental_forms(f, u, v), (du, dv), (du, dv)))

    acc = speed(t0) + speed(t1)
    for k in range(1, n):
        acc += (4 if k % 2 else 2) * speed(t0 + k * h)
    return acc * h / 3


def area(f: Callable, u0: float, u1: float, v0: float, v1: float, n: int = 60) -> float:
    """The integral of sqrt(EG - F^2) over the rectangle, by the product Simpson rule."""
    if n % 2:
        n += 1
    hu, hv = (u1 - u0) / n, (v1 - v0) / n
    w = [1 if k in (0, n) else (4 if k % 2 else 2) for k in range(n + 1)]
    acc = 0.0
    for i in range(n + 1):
        for j in range(n + 1):
            su, sv = partials(f, u0 + i * hu, v0 + j * hv)[:2]
            acc += w[i] * w[j] * math.sqrt(max(0.0, _dot(su, su) * _dot(sv, sv) - _dot(su, sv) ** 2))
    return acc * hu * hv / 9
