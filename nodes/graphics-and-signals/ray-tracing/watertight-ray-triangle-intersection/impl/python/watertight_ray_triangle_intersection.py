# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/watertight-ray-triangle-intersection/. The authors are listed in prov/Y50EDX.jsonl.

"""Watertight ray-triangle intersection (Woop, Benthin and Wald, JCGT 2013).

The ray is o + t d, with float coordinates. The test translates the
triangle by -o, permutes the axes so that the largest component of d is
the z axis, and shears so that the ray becomes the z axis. Then three 2D
edge functions decide the hit. The paper evaluates the edge functions in
single precision and falls back to double precision when one of them is
exactly zero. Python floats are doubles, so here the main path is double
precision and the fallback is exact rational arithmetic (Fraction). In
both cases the fallback gives the exact sign of each edge function of
the transformed (rounded) vertices.
"""

from fractions import Fraction
from typing import Optional, Sequence, Tuple

Vec = Sequence[float]
Hit = Tuple[float, float, float, float]


class ShearedRay:
    """The per-ray constants: the axis order and the shear (lines L1 to L4)."""

    def __init__(self, o: Vec, d: Vec) -> None:
        ad = [abs(x) for x in d]
        kz = max(range(3), key=lambda k: ad[k])      # @line L1
        kx = (kz + 1) % 3
        ky = (kx + 1) % 3
        if d[kz] < 0:                                 # @line L2
            kx, ky = ky, kx
        if d[kz] == 0:
            raise ValueError("the direction is the zero vector")
        self.o = tuple(o)
        self.kx, self.ky, self.kz = kx, ky, kz
        self.sx = d[kx] / d[kz]                       # @line L3
        self.sy = d[ky] / d[kz]
        self.sz = 1.0 / d[kz]                         # @line L4

    def transform(self, p: Vec) -> Tuple[float, float, float]:
        """Translate p by -o and shear it (lines L5 and L6). Not scaled in z."""
        a = (p[0] - self.o[0], p[1] - self.o[1], p[2] - self.o[2])
        az = a[self.kz]
        return (a[self.kx] - self.sx * az, a[self.ky] - self.sy * az, az)   # @line L6


def _edge(px: float, py: float, qx: float, qy: float) -> float:
    return px * qy - py * qx


def _edge_exact(px: float, py: float, qx: float, qy: float) -> float:
    return float(Fraction(px) * Fraction(qy) - Fraction(py) * Fraction(qx))


def watertight_intersect(ray: ShearedRay, a: Vec, b: Vec, c: Vec,
                         tmax: float = float("inf"),
                         cull_backfaces: bool = False) -> Optional[Hit]:
    """Return (t, u, v, w) with 0 <= t <= tmax, or None.

    The hit point is u a + v b + w c with u + v + w = 1. A point on an
    edge or at a vertex counts as inside, so the test is conservative.
    """
    ax, ay, az = ray.transform(a)                     # @line L5
    bx, by, bz = ray.transform(b)
    cx, cy, cz = ray.transform(c)
    u = _edge(cx, cy, bx, by)                         # @line L7
    v = _edge(ax, ay, cx, cy)
    w = _edge(bx, by, ax, ay)
    if u == 0.0 or v == 0.0 or w == 0.0:              # @line L8
        u = _edge_exact(cx, cy, bx, by)
        v = _edge_exact(ax, ay, cx, cy)
        w = _edge_exact(bx, by, ax, ay)
    if cull_backfaces:                                # @line L9
        if u < 0.0 or v < 0.0 or w < 0.0:
            return None
    elif (u < 0.0 or v < 0.0 or w < 0.0) and (u > 0.0 or v > 0.0 or w > 0.0):
        return None
    det = u + v + w                                   # @line L10
    if det == 0.0:
        return None
    t_scaled = u * (ray.sz * az) + v * (ray.sz * bz) + w * (ray.sz * cz)  # @line L11
    if det < 0.0:                                     # @line L12
        t_scaled, det_abs = -t_scaled, -det
    else:
        det_abs = det
    if t_scaled < 0.0 or t_scaled > tmax * det_abs:
        return None
    inv = 1.0 / det                                   # @line L13
    return (t_scaled * (1.0 / det_abs), u * inv, v * inv, w * inv)


def intersect(o: Vec, d: Vec, a: Vec, b: Vec, c: Vec,
              tmax: float = float("inf"), cull_backfaces: bool = False) -> Optional[Hit]:
    """One-shot form: build the sheared ray and test one triangle."""
    return watertight_intersect(ShearedRay(o, d), a, b, c, tmax, cull_backfaces)
