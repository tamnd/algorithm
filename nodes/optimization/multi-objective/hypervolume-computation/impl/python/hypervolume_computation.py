# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hypervolume-computation/. The authors are listed in prov/BQ3B9A.jsonl.

"""Exact hypervolume computation (minimization).

HV(A, r) is the volume of the union of the boxes [a, r] over the points a of
A with a < r in every coordinate. With int or Fraction input the result is
exact.

- hv2d: sort and sweep, O(N log N).
- hv3d: the dimension sweep of Beume, Fonseca, Lopez-Ibanez, Paquete and
  Vahrenhold (2009). The 2D staircase is a Python list searched with bisect,
  so an insertion or deletion moves O(N) entries; a balanced search tree
  gives the O(N log N) bound of the paper.
- hypervolume: slices along the last objective down to hv3d, O(N^(p-2) log N)
  with a balanced tree.
"""

from bisect import bisect_right
from typing import Callable, Iterable, Sequence

Vector = Sequence


def inside(points: Iterable[Vector], ref: Vector) -> list:
    return [tuple(x) for x in points if all(u < v for u, v in zip(x, ref))]


def hv2d(points: Iterable[Vector], ref: Vector):
    pts = sorted(inside(points, ref))
    total, low = 0, ref[1]
    for x, y in pts:
        if y < low:
            total += (ref[0] - x) * (low - y)
            low = y
    return total


def hv3d(points: Iterable[Vector], ref: Vector, on_point: Callable | None = None):
    """Sweep in the third objective with a 2D staircase of (x, y), x rising and y falling."""
    pts = sorted(inside(points, ref), key=lambda q: q[2])  # @line L1
    if not pts:
        return 0
    xs, ys = [], []  # the staircase
    area, vol, z_prev = 0, 0, pts[0][2]  # @line L2
    r1, r2 = ref[0], ref[1]
    for q in pts:  # @line L3
        x, y, z = q
        vol += area * (z - z_prev)  # @line L4
        z_prev = z
        i = bisect_right(xs, x)  # the points of S with first coordinate <= x are xs[:i]
        if i > 0 and ys[i - 1] <= y:  # @line L5
            if on_point is not None:
                on_point(q, vol, area)
            continue
        # predecessor: the last point with first coordinate < x; its y bounds the new strip
        j = i
        while j > 0 and xs[j - 1] == x:
            j -= 1
        cur_x, cur_h = x, (ys[j - 1] if j > 0 else r2)
        k = j
        while k < len(xs) and ys[k] >= y:  # @line L6
            area += (xs[k] - cur_x) * (cur_h - y)
            cur_x, cur_h = xs[k], ys[k]
            k += 1
        nxt = xs[k] if k < len(xs) else r1
        area += (nxt - cur_x) * (cur_h - y)
        xs[j:k] = [x]  # @line L7
        ys[j:k] = [y]
        if on_point is not None:
            on_point(q, vol, area)
    return vol + area * (ref[2] - z_prev)  # @line L8


def hypervolume(points: Iterable[Vector], ref: Vector):
    """Exact hypervolume in any dimension p >= 1."""
    pts = inside(points, ref)
    if not pts:
        return 0
    p = len(ref)
    if p == 1:
        return ref[0] - min(x[0] for x in pts)
    if p == 2:
        return hv2d(pts, ref)
    if p == 3:
        return hv3d(pts, ref)
    pts.sort(key=lambda x: x[-1])
    total = 0
    for i, x in enumerate(pts):
        top = pts[i + 1][-1] if i + 1 < len(pts) else ref[-1]
        if top > x[-1]:
            total += (top - x[-1]) * hypervolume([y[:-1] for y in pts[: i + 1]], ref[:-1])
    return total
