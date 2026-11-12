# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/surface-of-revolution/. The authors are listed in prov/R4J4XX.jsonl.

"""Surfaces of revolution about the z axis.

The profile curve lies in the xz plane as (r(u), 0, z(u)) with r(u) >= 0.
Turning it by the angle v gives S(u, v) = (r(u) cos v, r(u) sin v, z(u)).
The functions that take (c, s) = (cos v, sin v) instead of v are exact on
Fraction input when c and s are rational with c^2 + s^2 = 1.
"""

import math
from typing import Callable, Tuple

Fn = Callable[[object], object]


def revolve(r, z, c, s) -> Tuple:
    """The point of the parallel of radius r at height z, at the angle with cosine c and sine s."""
    return (r * c, r * s, z)


def revolve_point(r: Fn, z: Fn, u, v: float) -> Tuple:
    return revolve(r(u), z(u), math.cos(v), math.sin(v))


def partials(r, dr, dz, c, s) -> Tuple[Tuple, Tuple]:
    """S_u = (r' c, r' s, z') and S_v = (-r s, r c, 0)."""
    return (dr * c, dr * s, dz), (-r * s, r * c, 0)


def first_form(r, dr, dz) -> Tuple:
    """E = r'^2 + z'^2, F = 0, G = r^2. Meridians and parallels are orthogonal."""
    return dr * dr + dz * dz, 0, r * r


def second_form(r, dr, ddr, dz, ddz) -> Tuple:
    """L, M, N for the unit normal (-z' cos v, -z' sin v, r') / sqrt(E).

    This normal is S_u x S_v / |S_u x S_v| when r > 0.
    """
    e = math.sqrt(dr * dr + dz * dz)
    return (dr * ddz - ddr * dz) / e, 0.0, r * dz / e


def gaussian_curvature(r, dr, ddr, dz, ddz):
    """K = z' (r' z'' - r'' z') / (r (r'^2 + z'^2)^2). Exact on Fraction input."""
    if r == 0:  # @line L1
        raise ValueError("the point is on the axis, where the surface can be singular")
    e = dr * dr + dz * dz  # @line L2
    if e == 0:  # @line L3
        raise ValueError("the profile curve has a zero tangent here")
    delta = dr * ddz - ddr * dz  # @line L4
    return dz * delta / (r * e * e)  # @line L5


def mean_curvature(r, dr, ddr, dz, ddz):
    """H = (r (r' z'' - r'' z') + z' E) / (2 r E^(3/2)) for the normal of second_form."""
    e = dr * dr + dz * dz
    return (r * (dr * ddz - ddr * dz) + dz * e) / (2 * r * e ** 1.5)


def area(r: Fn, dr: Fn, dz: Fn, u0: float, u1: float, n: int = 200) -> float:
    """2 pi times the integral of r sqrt(r'^2 + z'^2) du, by composite Simpson with n even."""
    if n % 2:
        n += 1
    h = (u1 - u0) / n

    def f(u):
        return r(u) * math.hypot(dr(u), dz(u))

    acc = f(u0) + f(u1)
    for k in range(1, n):
        acc += (4 if k % 2 else 2) * f(u0 + k * h)
    return 2 * math.pi * acc * h / 3
