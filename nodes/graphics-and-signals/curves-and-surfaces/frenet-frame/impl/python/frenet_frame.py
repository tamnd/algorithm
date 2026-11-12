# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frenet-frame/. The authors are listed in prov/CY1Y34.jsonl.

"""The Frenet-Serret frame of a space curve, its curvature and torsion, and a
rotation-minimizing frame by the double reflection method.

The frame at a parameter value is computed from the first three derivatives
d1 = C'(t), d2 = C''(t), d3 = C'''(t), in any parametrization:

    T = d1 / |d1|,  B = (d1 x d2) / |d1 x d2|,  N = B x T,
    kappa = |d1 x d2| / |d1|^3,  tau = (d1 x d2) . d3 / |d1 x d2|^2.

The frame does not exist where d1 x d2 = 0, that is, where the curve is not
regular or its curvature is zero; frenet() raises ValueError there.
curvature_squared() and torsion() are rational in the derivatives, so they
are exact for Fraction input.
"""

import math
from typing import List, Sequence, Tuple

Vec = Tuple


def cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a: Vec, b: Vec):
    return sum(x * y for x, y in zip(a, b))


def _unit(a: Vec) -> Vec:
    n = math.sqrt(dot(a, a))
    return tuple(x / n for x in a)


def curvature_squared(d1: Vec, d2: Vec):
    """kappa^2 = |d1 x d2|^2 / |d1|^6 (exact for exact input)."""
    c = cross(d1, d2)
    s = dot(d1, d1)
    return dot(c, c) / (s * s * s)


def torsion(d1: Vec, d2: Vec, d3: Vec):
    """tau = (d1 x d2) . d3 / |d1 x d2|^2 (exact for exact input)."""
    c = cross(d1, d2)
    w = dot(c, c)
    if w == 0:
        raise ValueError("torsion is undefined where the curvature is zero")
    return dot(c, d3) / w


def frenet(d1: Vec, d2: Vec, d3: Vec, eps: float = 0.0):
    """(T, N, B, kappa, tau) from the first three derivatives (floats)."""
    c = cross(d1, d2)
    w = math.sqrt(dot(c, c))
    s = math.sqrt(dot(d1, d1))
    if s == 0 or w <= eps * s * math.sqrt(dot(d2, d2)):
        raise ValueError("the Frenet frame is undefined: zero velocity or zero curvature")
    T = tuple(x / s for x in d1)
    B = tuple(x / w for x in c)
    N = cross(B, T)
    return T, N, B, w / s ** 3, dot(c, d3) / (w * w)


def signed_curvature(d1: Vec, d2: Vec):
    """The signed curvature (x'y'' - y'x'') / |C'|^3 of a plane curve."""
    s = math.sqrt(d1[0] * d1[0] + d1[1] * d1[1])
    return (d1[0] * d2[1] - d1[1] * d2[0]) / s ** 3


def double_reflection(points: Sequence[Vec], tangents: Sequence[Vec], r0: Vec) -> List[Vec]:
    """Reference vectors r_i of a rotation-minimizing frame along sampled points.

    points[i] and the unit tangents[i] sample the curve; r0 is a unit vector
    normal to tangents[0]. Each step reflects in the plane bisecting the chord,
    then in the plane that maps the reflected tangent onto the next tangent.
    The frame is (t_i, r_i, t_i x r_i).
    """
    rs = [tuple(r0)]
    for i in range(len(points) - 1):
        v1 = tuple(b - a for a, b in zip(points[i], points[i + 1]))
        c1 = dot(v1, v1)
        r = rs[-1]
        t = tangents[i]
        if c1 == 0:
            rL, tL = r, t
        else:
            rL = tuple(x - (2 / c1) * dot(v1, r) * y for x, y in zip(r, v1))
            tL = tuple(x - (2 / c1) * dot(v1, t) * y for x, y in zip(t, v1))
        v2 = tuple(b - a for a, b in zip(tL, tangents[i + 1]))
        c2 = dot(v2, v2)
        if c2 == 0:
            rs.append(rL)
        else:
            rs.append(tuple(x - (2 / c2) * dot(v2, rL) * y for x, y in zip(rL, v2)))
    return rs
