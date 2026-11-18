# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallax-occlusion-mapping/. The authors are listed in prov/2N7VM7.jsonl.

"""Parallax occlusion mapping: a linear march through a depth map, then a secant step.

Conventions (tangent space):
- The depth map m(u, v) is in [0, 1]. Depth 0 is the top of the surface (the
  polygon) and depth 1 is the deepest point, at `scale` texture units below it.
- view = (vx, vy, vz) points from the surface point toward the viewer, vz > 0.
- Going one unit of depth down along the view ray moves the texture coordinate
  by delta = -scale * (vx, vy) / vz.

The ray at depth r is at uv0 + r * delta. It is below the surface when
r >= m(uv0 + r * delta), so the hit is a root of f(r) = r - m(uv0 + r * delta).
Since f(0) <= 0 and f(1) >= 0, a root always exists in [0, 1] for a continuous m.
"""

from fractions import Fraction
from math import floor


def pom(depth, uv0, view, scale, steps, exact=False):
    """Return (uv, r): the texture coordinate of the hit and its depth r in [0, 1].

    With exact=True the sample depths are Fractions, so that rational inputs
    and a rational depth map give an exact result.
    """
    vx, vy, vz = view
    if vz <= 0:
        raise ValueError("the view vector must point out of the surface")
    du, dv = -scale * vx / vz, -scale * vy / vz  # @line L1
    r_prev, f_prev = 0, 0 - depth(uv0[0], uv0[1])  # @line L2
    if f_prev >= 0:  # @line L3
        return (uv0[0], uv0[1]), 0
    for i in range(1, steps + 1):  # @line L4
        r = Fraction(i, steps) if exact else i / steps
        f = r - depth(uv0[0] + r * du, uv0[1] + r * dv)  # @line L5
        if f >= 0:  # @line L6
            t = f_prev / (f_prev - f)  # @line L7
            rh = r_prev + t * (r - r_prev)  # @line L8
            return (uv0[0] + rh * du, uv0[1] + rh * dv), rh
        r_prev, f_prev = r, f  # @line L9
    raise AssertionError("unreachable for a depth map with values in [0, 1]")


def depth_texture(texels):
    """A bilinear, wrapping sampler for a depth image given as rows of values in [0, 1].

    Texel (x, y) has its center at ((x + 0.5) / w, (y + 0.5) / h).
    """
    h, w = len(texels), len(texels[0])

    def sample(u, v):
        x, y = u * w - 0.5, v * h - 0.5
        x0, y0 = floor(x), floor(y)
        fx, fy = x - x0, y - y0
        def t(i, j):
            return texels[j % h][i % w]
        top = t(x0, y0) * (1 - fx) + t(x0 + 1, y0) * fx
        bot = t(x0, y0 + 1) * (1 - fx) + t(x0 + 1, y0 + 1) * fx
        return top * (1 - fy) + bot * fy

    return sample


def first_hit_dense(depth, uv0, view, scale, samples=20000):
    """A reference: the first sample of a very fine march, then bisection to full precision."""
    vx, vy, vz = view
    du, dv = -scale * vx / vz, -scale * vy / vz

    def f(r):
        return r - depth(uv0[0] + r * du, uv0[1] + r * dv)

    if f(0.0) >= 0:
        return 0.0
    prev = 0.0
    for i in range(1, samples + 1):
        r = i / samples
        if f(r) >= 0:
            lo, hi = prev, r
            for _ in range(60):
                mid = (lo + hi) / 2
                if f(mid) >= 0:
                    hi = mid
                else:
                    lo = mid
            return hi
        prev = r
    return 1.0
