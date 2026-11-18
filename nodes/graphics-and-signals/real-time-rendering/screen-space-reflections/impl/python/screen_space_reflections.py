# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/screen-space-reflections/. The authors are listed in prov/4JP2C2.jsonl.

"""Screen-space reflections: a perspective-correct DDA through the depth buffer.

The camera is at the origin and looks along -z with a perspective projection.
The view depth of a point p is d = -p_z > 0. The screen has W x H pixels, the
pixel (i, j) has its center at (i + 1/2, j + 1/2) with j counted from the
bottom, and a point with depth d projects to

    s_x = (p_x / (d a tan(theta)) + 1) W / 2,   s_y = (p_y / (d tan(theta)) + 1) H / 2

with a = W / H. D[j][i] is the depth buffer, None for the background.

The march follows the method of McGuire and Mara (2014): project both ends of
the ray, step one pixel at a time along the major screen axis, and
interpolate k = 1/d and Q = p/d linearly in screen space, which is exact for a
3D line. A pixel is a hit if the depth range of the ray across that pixel
overlaps [D, D + thickness]. A ray that leaves the screen or reaches its end
is a miss, and the caller falls back to an environment map.
"""

import math
from typing import List, Optional, Sequence, Tuple

Vec = Tuple[float, float, float]
Grid = List[List[Optional[float]]]


class Camera:
    def __init__(self, width: int, height: int, tan_half: float, near: float) -> None:
        self.width, self.height = width, height
        self.tan_half = tan_half
        self.aspect = width / height
        self.near = near

    def project(self, p: Vec) -> Tuple[float, float, float]:
        """Screen position (s_x, s_y) and k = 1/d of a point in front of the camera."""
        k = -1.0 / p[2]
        sx = (p[0] * k / (self.aspect * self.tan_half) + 1) * self.width / 2
        sy = (p[1] * k / self.tan_half + 1) * self.height / 2
        return sx, sy, k

    def pixel_ray(self, sx: float, sy: float) -> Vec:
        """The point at depth 1 on the view ray through a screen position."""
        u = (2 * sx / self.width - 1) * self.aspect * self.tan_half
        v = (2 * sy / self.height - 1) * self.tan_half
        return (u, v, -1.0)


def reflect(dirn: Vec, n: Vec) -> Vec:
    dn = sum(a * b for a, b in zip(dirn, n))
    return tuple(a - 2 * dn * b for a, b in zip(dirn, n))


def trace(
    D: Grid,
    cam: Camera,
    origin: Vec,
    dirn: Vec,
    max_dist: float,
    thickness: float,
    max_steps: int = 10000,
):
    """Return (i, j, point) of the first hit, or None for a miss."""
    length = max_dist
    if origin[2] + dirn[2] * length > -cam.near:  # @line L1
        length = (-cam.near - origin[2]) / dirn[2]
    end = tuple(o + t * length for o, t in zip(origin, dirn))
    x0, y0, k0 = cam.project(origin)  # @line L2
    x1, y1, k1 = cam.project(end)
    Q0 = tuple(c * k0 for c in origin)
    Q1 = tuple(c * k1 for c in end)
    if (x1 - x0) ** 2 + (y1 - y0) ** 2 < 1e-8:
        x1 += 0.01
    steep = abs(y1 - y0) > abs(x1 - x0)  # @line L3
    if steep:
        x0, y0, x1, y1 = y0, x0, y1, x1
    sgn = 1.0 if x1 > x0 else -1.0
    inv = sgn / (x1 - x0)
    dy = (y1 - y0) * inv
    dQ = tuple((b - a) * inv for a, b in zip(Q0, Q1))
    dk = (k1 - k0) * inv
    px, py, Q, k = x0, y0, Q0, k0
    prev_d = 1.0 / k0
    for _ in range(max_steps):
        px, py = px + sgn, py + dy  # @line L4
        Q = tuple(a + b for a, b in zip(Q, dQ))
        k = k + dk
        if (px - x1) * sgn > 0:
            return None  # the end of the ray  # @line L7
        next_d = 1.0 / (k + 0.5 * dk)
        rmin, rmax = min(prev_d, next_d), max(prev_d, next_d)
        prev_d = next_d
        sx, sy = (py, px) if steep else (px, py)
        i, j = int(math.floor(sx)), int(math.floor(sy))
        if not (0 <= i < cam.width and 0 <= j < cam.height):  # @line L5
            return None
        scene = D[j][i]
        if scene is not None and rmax >= scene and rmin <= scene + thickness:  # @line L6
            return i, j, tuple(c / k for c in Q)
    return None


def reflection(D: Grid, color: Sequence[Sequence], cam: Camera, i: int, j: int, normal: Vec, environment, max_dist: float, thickness: float):
    """The reflected color of pixel (i, j): the color at the hit, or the
    environment in the reflected direction on a miss."""
    d = D[j][i]
    view = cam.pixel_ray(i + 0.5, j + 0.5)
    origin = tuple(c * d for c in view)
    L = math.sqrt(sum(c * c for c in view))
    r = reflect(tuple(c / L for c in view), normal)
    hit = trace(D, cam, origin, r, max_dist, thickness)
    if hit is None:
        return environment(r)  # @line L8
    return color[hit[1]][hit[0]]
