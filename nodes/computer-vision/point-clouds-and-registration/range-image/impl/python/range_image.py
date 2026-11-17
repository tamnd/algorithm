# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/range-image/. The authors are listed in prov/M707AA.jsonl.
"""A range image (depth image) of a pinhole camera.

Conventions: the camera frame has X to the right, Y down and Z forward. The
intrinsic matrix is K = [[fx, 0, cx], [0, fy, cy], [0, 0, 1]] (no skew). The
image is indexed img[v][u] with u the column and v the row. Pixel (u, v) has
its center at the point (u, v) of the image plane. A cell stores the depth Z of
the point seen through the pixel center, or None if the pixel has no point.

The range of a point is its distance ||X|| to the camera center. Depth and
range of a cell differ by the fixed factor sqrt(1 + a^2 + b^2) with
a = (u - cx)/fx and b = (v - cy)/fy, the length of the ray (a, b, 1).
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

Point = Tuple[float, float, float]


class RangeImage:
    """A W x H grid of depths with a pinhole camera."""

    def __init__(self, width: int, height: int, fx: float, fy: float,
                 cx: float, cy: float) -> None:
        if width <= 0 or height <= 0 or fx <= 0 or fy <= 0:
            raise ValueError("need a positive size and positive focal lengths")
        self.W, self.H = width, height
        self.fx, self.fy, self.cx, self.cy = fx, fy, cx, cy
        self.depth: List[List[Optional[float]]] = [[None] * width for _ in range(height)]

    # -- build ------------------------------------------------------------

    @classmethod
    def from_points(cls, points: Sequence[Sequence[float]], width: int, height: int,
                    fx: float, fy: float, cx: float, cy: float) -> "RangeImage":
        """Project the points and keep, per pixel, the smallest depth (a z-buffer).

        A point goes to the pixel whose center is nearest to its projection.
        Points with Z <= 0 or outside the image are dropped."""
        img = cls(width, height, fx, fy, cx, cy)  # @line L1
        for X, Y, Z in points:  # @line L2
            if Z <= 0:  # @line L3
                continue
            u = math.floor(fx * X / Z + cx + 0.5)  # @line L4
            v = math.floor(fy * Y / Z + cy + 0.5)
            if not (0 <= u < width and 0 <= v < height):  # @line L5
                continue
            old = img.depth[v][u]
            if old is None or Z < old:  # @line L6
                img.depth[v][u] = Z  # @line L7
        return img  # @line L8

    # -- queries ----------------------------------------------------------

    def ray(self, u: int, v: int) -> Point:
        """The ray (a, b, 1) through the center of pixel (u, v)."""
        return ((u - self.cx) / self.fx, (v - self.cy) / self.fy, 1.0)

    def point(self, u: int, v: int) -> Optional[Point]:
        """Back-project the cell (u, v) to a 3D point, or None if it is empty."""
        z = self.depth[v][u]  # @line L9
        if z is None:
            return None
        a, b, _ = self.ray(u, v)
        return (z * a, z * b, z)  # @line L10

    def range_at(self, u: int, v: int) -> Optional[float]:
        """The range ||X|| of the cell (u, v), or None."""
        z = self.depth[v][u]
        if z is None:
            return None
        a, b, _ = self.ray(u, v)
        return z * math.sqrt(1.0 + a * a + b * b)

    def to_point_cloud(self) -> List[Tuple[int, int, Point]]:
        """All valid cells as (u, v, point), row by row: an organized cloud."""
        out = []
        for v in range(self.H):
            for u in range(self.W):
                p = self.point(u, v)
                if p is not None:
                    out.append((u, v, p))
        return out

    def neighbors(self, u: int, v: int, max_jump: float) -> List[Tuple[int, int]]:
        """The 4-neighbors of (u, v) that are valid and whose depth differs
        from the depth at (u, v) by at most max_jump."""
        z = self.depth[v][u]
        if z is None:
            return []
        out = []
        for du, dv in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # @line L11
            uu, vv = u + du, v + dv
            if not (0 <= uu < self.W and 0 <= vv < self.H):  # @line L12
                continue
            zz = self.depth[vv][uu]
            if zz is not None and abs(zz - z) <= max_jump:  # @line L13
                out.append((uu, vv))  # @line L14
        return out

    def normal(self, u: int, v: int, max_jump: float) -> Optional[Point]:
        """A unit normal at (u, v) from the cross product of the horizontal and
        vertical neighbor differences, turned toward the camera. None if a
        neighbor is missing or across a depth jump."""
        nb = set(self.neighbors(u, v, max_jump))
        p = self.point(u, v)
        if p is None:
            return None
        # Use the central difference if both sides are there, else one side.
        def diff(a: Tuple[int, int], b: Tuple[int, int]) -> Optional[Point]:
            pa = self.point(*a) if a in nb or a == (u, v) else None
            pb = self.point(*b) if b in nb or b == (u, v) else None
            if pa is None or pb is None:
                return None
            return (pa[0] - pb[0], pa[1] - pb[1], pa[2] - pb[2])
        du = diff((u + 1, v), (u - 1, v)) or diff((u + 1, v), (u, v)) or diff((u, v), (u - 1, v))  # @line L15
        dv = diff((u, v + 1), (u, v - 1)) or diff((u, v + 1), (u, v)) or diff((u, v), (u, v - 1))
        if du is None or dv is None:
            return None
        n = (du[1] * dv[2] - du[2] * dv[1],  # @line L16
             du[2] * dv[0] - du[0] * dv[2],
             du[0] * dv[1] - du[1] * dv[0])
        length = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)
        if length == 0.0:
            return None
        n = (n[0] / length, n[1] / length, n[2] / length)  # @line L17
        if n[0] * p[0] + n[1] * p[1] + n[2] * p[2] > 0:  # @line L18
            n = (-n[0], -n[1], -n[2])
        return n  # @line L19
