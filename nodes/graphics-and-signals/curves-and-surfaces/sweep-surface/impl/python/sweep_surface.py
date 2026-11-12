# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sweep-surface/. The authors are listed in prov/5W3KF8.jsonl.

"""Sweep surfaces: a planar profile moved along a spine curve by a moving frame.

S(u, v) = c(u) + x(v) r(u) + y(v) s(u), where (t, r, s) is an orthonormal
frame at c(u) with t the unit tangent, and (x(v), y(v)) is the profile in the
normal plane. The frame is the Frenet frame or a rotation minimizing frame
(RMF) from the double reflection method of Wang, Juttler, Zheng and Liu (2008).
"""

import math
from typing import Callable, List, Sequence, Tuple

Vec = Tuple[float, float, float]


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _scale(k, a):
    return (k * a[0], k * a[1], k * a[2])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _unit(a):
    return _scale(1 / math.sqrt(_dot(a, a)), a)


def frenet_frame(dc: Vec, ddc: Vec) -> Tuple[Vec, Vec, Vec]:
    """(T, N, B) from c' and c''. Raises ValueError where c' x c'' = 0 (an inflection or a line)."""
    b = _cross(dc, ddc)
    if _dot(b, b) == 0:
        raise ValueError("the Frenet frame is not defined where c' and c'' are parallel")
    t, bn = _unit(dc), _unit(b)
    return t, _cross(bn, t), bn


def rmf_double_reflection(points: Sequence[Vec], tangents: Sequence[Vec], r0: Vec) -> List[Tuple[Vec, Vec, Vec]]:
    """Frames (t_i, r_i, s_i) at the sample points, with r_0 = r0 made normal to t_0.

    Each step reflects the frame in the bisector plane of x_i x_{i+1}, then in
    the plane that takes the reflected tangent to t_{i+1}. Two reflections make
    a rotation, so the frame stays orthonormal and keeps its handedness.
    """
    ts = [_unit(t) for t in tangents]
    r = _unit(_sub(r0, _scale(_dot(r0, ts[0]), ts[0])))  # @line L1
    frames = [(ts[0], r, _cross(ts[0], r))]
    for i in range(len(points) - 1):  # @line L2
        v1 = _sub(points[i + 1], points[i])  # @line L3
        c1 = _dot(v1, v1)
        rl = _sub(r, _scale(2 * _dot(v1, r) / c1, v1))  # @line L4
        tl = _sub(ts[i], _scale(2 * _dot(v1, ts[i]) / c1, v1))
        v2 = _sub(ts[i + 1], tl)  # @line L5
        c2 = _dot(v2, v2)
        r = rl if c2 == 0 else _sub(rl, _scale(2 * _dot(v2, rl) / c2, v2))  # @line L6
        frames.append((ts[i + 1], r, _cross(ts[i + 1], r)))  # @line L7
    return frames


def sweep_point(c: Vec, frame: Tuple[Vec, Vec, Vec], x: float, y: float) -> Vec:
    """c + x r + y s for the frame (t, r, s)."""
    _, r, s = frame
    return _add(c, _add(_scale(x, r), _scale(y, s)))


def sweep_grid(curve: Callable, dcurve: Callable, profile: Sequence[Tuple[float, float]],
               u0: float, u1: float, n: int, r0: Vec) -> List[List[Vec]]:
    """Rows of surface points: n + 1 stations of the spine, one point per profile point."""
    us = [u0 + (u1 - u0) * k / n for k in range(n + 1)]
    pts = [curve(u) for u in us]
    frames = rmf_double_reflection(pts, [dcurve(u) for u in us], r0)
    return [[sweep_point(p, f, x, y) for x, y in profile] for p, f in zip(pts, frames)]


def tube_jacobian_factor(kappa: float, rho: float, phi: float) -> float:
    """|S_u x S_v| / (|c'| rho) for a tube of radius rho: 1 - kappa rho cos(phi).

    phi is the angle of the profile point from the principal normal. The tube
    folds over itself where this factor is 0 or negative, which happens on
    some parallel as soon as rho > 1 / kappa.
    """
    return 1 - kappa * rho * math.cos(phi)
