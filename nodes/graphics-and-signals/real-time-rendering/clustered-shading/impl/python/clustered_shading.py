# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clustered-shading/. The authors are listed in prov/82B7J9.jsonl.

"""Clustered deferred shading, after Olsson, Billeter and Assarsson (2012).

Each pixel gets a cluster key (i, j, k): the screen tile (i, j) and the depth
slice k. The slices grow exponentially with the depth, so that each cluster is
about as deep as it is wide (Equations 1 and 2 of the paper):

    near_k = near * (1 + 2 tan(theta) / S_y) ** k
    k = floor(log(d / near) / log(1 + 2 tan(theta) / S_y))

where 2 theta is the vertical field of view and S_y the number of tiles in y.
Only the clusters that hold at least one pixel get a light list. A light is
kept for a cluster unless its sphere is outside one of the four side planes
of the tile or outside the depth slab of the slice.

Conventions as on the tiled shading page: the camera looks along -z, the depth
buffer holds the view depth d = -z > 0 or math.inf for the background, and
pixel (i, j) has its center at (i + 1/2, j + 1/2).
"""

import math
from dataclasses import dataclass

Vec3 = tuple[float, float, float]


@dataclass(frozen=True)
class Camera:
    width: int
    height: int
    tan_half: float
    near: float

    def ndc_to_slope(self, sx: float, sy: float) -> tuple[float, float]:
        aspect = self.width / self.height
        return (2.0 * sx / self.width - 1.0) * aspect * self.tan_half, (2.0 * sy / self.height - 1.0) * self.tan_half

    def position(self, i: int, j: int, d: float) -> Vec3:
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


def slice_ratio(cam: Camera, tile: int) -> float:
    """1 + 2 tan(theta) / S_y, with S_y = height / tile tiles in y."""
    s_y = cam.height / tile
    return 1.0 + 2.0 * cam.tan_half / s_y


def slice_near(cam: Camera, tile: int, k: int) -> float:
    """Equation 1: the near depth of slice k."""
    return cam.near * slice_ratio(cam, tile) ** k


def slice_index(cam: Camera, tile: int, d: float) -> int:
    """Equation 2, with a correction step against rounding at the borders."""
    q = slice_ratio(cam, tile)
    k = int(math.floor(math.log(d / cam.near) / math.log(q)))
    while k > 0 and slice_near(cam, tile, k) > d:
        k -= 1
    while slice_near(cam, tile, k + 1) <= d:
        k += 1
    return k


def side_planes(cam: Camera, x0: float, x1: float, y0: float, y1: float) -> list[Vec3]:
    u0, v0 = cam.ndc_to_slope(x0, y0)
    u1, v1 = cam.ndc_to_slope(x1, y1)
    planes = []
    for m in ((1.0, 0.0, u0), (-1.0, 0.0, -u1), (0.0, 1.0, v0), (0.0, -1.0, -v1)):
        length = math.sqrt(dot(m, m))
        planes.append((m[0] / length, m[1] / length, m[2] / length))
    return planes


def sphere_in_cluster(planes: list[Vec3], d0: float, d1: float, light: Light) -> bool:
    """Conservative: False only if the sphere misses the cluster frustum."""
    c, r = light.center, light.radius * (1.0 + 1e-9) + 1e-12
    for m in planes:
        if dot(m, c) < -r:
            return False
    dc = -c[2]
    return not (dc + r < d0 or dc - r > d1)


def cluster_keys(depth, cam: Camera, tile: int) -> dict[tuple[int, int], tuple[int, int, int]]:
    """Step 2 of the paper: the cluster key of every pixel with geometry."""
    keys = {}
    for j in range(cam.height):
        for i in range(cam.width):
            d = depth[j][i]
            if d != math.inf:
                keys[(i, j)] = (i // tile, j // tile, slice_index(cam, tile, d))  # @line L2
    return keys


def assign_lights(cam: Camera, tile: int, clusters, lights: list[Light]) -> dict[tuple[int, int, int], list[int]]:
    """Step 4: the light list of every occupied cluster, in light order."""
    lists = {}
    for key in sorted(clusters):  # @line L4
        ti, tj, k = key
        x0, y0 = ti * tile, tj * tile
        planes = side_planes(cam, x0, min(x0 + tile, cam.width), y0, min(y0 + tile, cam.height))  # @line L5
        d0, d1 = slice_near(cam, tile, k), slice_near(cam, tile, k + 1)
        lists[key] = [idx for idx, light in enumerate(lights) if sphere_in_cluster(planes, d0, d1, light)]  # @line L6
    return lists


def clustered_shading(depth, normals, cam: Camera, lights: list[Light], tile: int = 16):
    """The five steps. Returns the image, the cluster lists and the number of
    (pixel, light) pairs that the shading loop evaluated."""
    keys = cluster_keys(depth, cam, tile)  # @line L1
    clusters = set(keys.values())  # @line L3
    lists = assign_lights(cam, tile, clusters, lights)
    out = [[0.0] * cam.width for _ in range(cam.height)]
    pairs = 0
    for (i, j), key in keys.items():  # @line L7
        p = cam.position(i, j, depth[j][i])
        c = 0.0
        for idx in lists[key]:  # @line L8
            c += shade(p, normals[j][i], lights[idx])
        pairs += len(lists[key])
        out[j][i] = c  # @line L9
    return out, lists, pairs
