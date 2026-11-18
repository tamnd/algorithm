# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tiled-shading/. The authors are listed in prov/TE6F11.jsonl.

"""Tiled light culling and shading, after Olsson and Assarsson (2011).

The screen is cut into square tiles. For each tile the method finds the
smallest and the largest view depth of its pixels, forms the four side planes
of the tile frustum through the eye, and keeps every point light whose sphere
of influence is not fully outside one of these planes or outside the depth
range. Each pixel then loops only over the lights of its tile.

Conventions: the camera is at the origin and looks along -z. The depth buffer
holds the linear view depth d = -z > 0, or math.inf for the background. Pixel
(i, j) has its center at (i + 1/2, j + 1/2), with j counted from the bottom.
A light reaches a point only if the distance is below its radius: the falloff
is exactly 0 from the radius on, so a culled light changes nothing.
"""

import math
from dataclasses import dataclass

Vec3 = tuple[float, float, float]


@dataclass(frozen=True)
class Camera:
    width: int
    height: int
    tan_half: float  # tan of half the vertical field of view

    def ndc_to_slope(self, sx: float, sy: float) -> tuple[float, float]:
        """Screen position in pixels to the slopes x / d and y / d of the ray."""
        aspect = self.width / self.height
        u = (2.0 * sx / self.width - 1.0) * aspect * self.tan_half
        v = (2.0 * sy / self.height - 1.0) * self.tan_half
        return u, v

    def position(self, i: int, j: int, d: float) -> Vec3:
        """View-space position of the center of pixel (i, j) at view depth d."""
        u, v = self.ndc_to_slope(i + 0.5, j + 0.5)
        return (u * d, v * d, -d)


@dataclass(frozen=True)
class Light:
    center: Vec3
    radius: float
    intensity: float


def dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def shade(p: Vec3, n: Vec3, light: Light) -> float:
    """Lambert term times a falloff that is 0 for distances >= radius."""
    lx, ly, lz = light.center[0] - p[0], light.center[1] - p[1], light.center[2] - p[2]
    dist2 = lx * lx + ly * ly + lz * lz
    r2 = light.radius * light.radius
    if dist2 >= r2:
        return 0.0
    dist = math.sqrt(dist2)
    cos_t = 0.0 if dist == 0.0 else max(0.0, (n[0] * lx + n[1] * ly + n[2] * lz) / dist)
    w = 1.0 - dist2 / r2
    return light.intensity * cos_t * w * w


def affects(p: Vec3, light: Light) -> bool:
    c = light.center
    return (c[0] - p[0]) ** 2 + (c[1] - p[1]) ** 2 + (c[2] - p[2]) ** 2 < light.radius * light.radius


def brute_force(depth, normals, cam: Camera, lights: list[Light]) -> list[list[float]]:
    """Shade every pixel with every light, in the order of the light list."""
    out = [[0.0] * cam.width for _ in range(cam.height)]
    for j in range(cam.height):
        for i in range(cam.width):
            d = depth[j][i]
            if d == math.inf:
                continue
            p = cam.position(i, j, d)
            c = 0.0
            for light in lights:
                c += shade(p, normals[j][i], light)
            out[j][i] = c
    return out


def side_planes(cam: Camera, x0: float, x1: float, y0: float, y1: float) -> list[Vec3]:
    """Unit inward normals of the four planes through the eye that bound the
    screen rectangle [x0, x1] x [y0, y1] (in pixels). Each plane is m . x = 0."""
    u0, v0 = cam.ndc_to_slope(x0, y0)
    u1, v1 = cam.ndc_to_slope(x1, y1)
    planes = []
    # x / d >= u0, with d = -z, is x + u0 z >= 0; the other three are alike.
    for m in ((1.0, 0.0, u0), (-1.0, 0.0, -u1), (0.0, 1.0, v0), (0.0, -1.0, -v1)):
        length = math.sqrt(dot(m, m))
        planes.append((m[0] / length, m[1] / length, m[2] / length))
    return planes


def sphere_in_frustum(planes: list[Vec3], dmin: float, dmax: float, light: Light) -> bool:
    """Conservative test: False only if the sphere misses the tile frustum.
    The radius gets a small slack so that rounding cannot drop a light."""
    c, r = light.center, light.radius * (1.0 + 1e-9) + 1e-12
    for m in planes:  # @line L11
        if dot(m, c) < -r:
            return False
    dc = -c[2]  # @line L12
    if dc + r < dmin or dc - r > dmax:
        return False
    return True  # @line L13


def tile_depth_range(depth, x0: int, x1: int, y0: int, y1: int) -> tuple[float, float] | None:
    dmin, dmax = math.inf, -math.inf
    for j in range(y0, y1):
        for i in range(x0, x1):
            d = depth[j][i]
            if d != math.inf:
                dmin = min(dmin, d)
                dmax = max(dmax, d)
    if dmin == math.inf:
        return None
    return dmin, dmax


def build_light_lists(depth, cam: Camera, lights: list[Light], tile: int) -> dict[tuple[int, int], list[int]]:
    """The light list of every tile, in increasing light index."""
    lists = {}
    for ty in range((cam.height + tile - 1) // tile):  # @line L1
        for tx in range((cam.width + tile - 1) // tile):
            x0, y0 = tx * tile, ty * tile
            x1, y1 = min(x0 + tile, cam.width), min(y0 + tile, cam.height)
            rng = tile_depth_range(depth, x0, x1, y0, y1)  # @line L2
            chosen = []  # @line L4
            if rng is not None:
                planes = side_planes(cam, x0, x1, y0, y1)  # @line L3
                for idx, light in enumerate(lights):  # @line L5
                    if sphere_in_frustum(planes, rng[0], rng[1], light):  # @line L6
                        chosen.append(idx)
            lists[(tx, ty)] = chosen
    return lists


def tiled_shading(depth, normals, cam: Camera, lights: list[Light], tile: int = 16):
    """Shade with the tile light lists. Returns the image and the lists."""
    lists = build_light_lists(depth, cam, lights, tile)
    out = [[0.0] * cam.width for _ in range(cam.height)]
    for j in range(cam.height):  # @line L7
        for i in range(cam.width):
            d = depth[j][i]
            if d == math.inf:
                continue
            p = cam.position(i, j, d)  # @line L8
            c = 0.0
            for idx in lists[(i // tile, j // tile)]:  # @line L9
                c += shade(p, normals[j][i], lights[idx])
            out[j][i] = c  # @line L10
    return out, lists
