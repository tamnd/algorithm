# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clustered-shading/. The authors are listed in prov/82B7J9.jsonl.

"""Clustered shading against brute-force shading, and the slice formulas."""

import math
import random

from clustered_shading import (
    Camera,
    Light,
    affects,
    brute_force,
    cluster_keys,
    clustered_shading,
    side_planes,
    slice_index,
    slice_near,
    sphere_in_cluster,
)


def room(cam: Camera):
    """The scene of the tiled shading tests: floor, side walls, a back wall
    at d = 12 with an open window, and a box face at d = 3."""
    depth = [[math.inf] * cam.width for _ in range(cam.height)]
    normals = [[(0.0, 0.0, 1.0)] * cam.width for _ in range(cam.height)]
    for j in range(cam.height):
        for i in range(cam.width):
            u, v = cam.ndc_to_slope(i + 0.5, j + 0.5)
            hits = []
            if not (u * 12.0 > 2.0 and v * 12.0 > 1.0):
                hits.append((12.0, (0.0, 0.0, 1.0)))
            if v < 0.0:
                hits.append((-1.0 / v, (0.0, 1.0, 0.0)))
            if u < 0.0 and -4.0 / u <= 12.0:
                hits.append((-4.0 / u, (1.0, 0.0, 0.0)))
            if u > 0.0 and 4.0 / u <= 12.0:
                hits.append((4.0 / u, (-1.0, 0.0, 0.0)))
            if -1.0 <= 3.0 * u <= 0.5 and -1.0 <= 3.0 * v <= 0.5:
                hits.append((3.0, (0.0, 0.0, 1.0)))
            if hits:
                depth[j][i], normals[j][i] = min(hits)
    return depth, normals


def random_lights(rng: random.Random, count: int, r_max: float = 3.0) -> list[Light]:
    return [
        Light(
            (rng.uniform(-4.0, 4.0), rng.uniform(-1.0, 3.0), rng.uniform(-12.0, -1.0)),
            rng.uniform(0.3, r_max),
            rng.uniform(0.5, 2.0),
        )
        for _ in range(count)
    ]


def tiled_pairs(depth, cam: Camera, lights: list[Light], tile: int) -> int:
    """(pixel, light) pairs of plain tiled culling with the tile depth range."""
    total = 0
    for ty in range(cam.height // tile):
        for tx in range(cam.width // tile):
            ds = [depth[j][i] for j in range(ty * tile, ty * tile + tile) for i in range(tx * tile, tx * tile + tile)]
            ds = [d for d in ds if d != math.inf]
            if not ds:
                continue
            planes = side_planes(cam, tx * tile, tx * tile + tile, ty * tile, ty * tile + tile)
            kept = sum(1 for light in lights if sphere_in_cluster(planes, min(ds), max(ds), light))
            total += kept * len(ds)
    return total


def test_slice_formulas() -> None:
    cam = Camera(64, 48, 0.8, 0.5)
    tile = 8
    rng = random.Random(31)
    for _ in range(2000):
        d = math.exp(rng.uniform(math.log(0.5), math.log(200.0)))
        k = slice_index(cam, tile, d)
        assert slice_near(cam, tile, k) <= d < slice_near(cam, tile, k + 1)
    # Self-similar slices: the depth of slice k equals the height of a tile at near_k.
    s_y = cam.height / tile
    for k in range(40):
        n0, n1 = slice_near(cam, tile, k), slice_near(cam, tile, k + 1)
        assert abs((n1 - n0) - 2.0 * n0 * cam.tan_half / s_y) <= 1e-9 * n1


def test_no_light_is_missed() -> None:
    rng = random.Random(32)
    cam = Camera(48, 32, 1.0, 0.5)
    depth, normals = room(cam)
    for tile in (4, 8):
        lights = random_lights(rng, 40)
        _, lists, _ = clustered_shading(depth, normals, cam, lights, tile)
        keys = cluster_keys(depth, cam, tile)
        for (i, j), key in keys.items():
            p = cam.position(i, j, depth[j][i])
            kept = set(lists[key])
            for idx, light in enumerate(lights):
                if affects(p, light):
                    assert idx in kept


def test_equals_brute_force_exactly() -> None:
    rng = random.Random(33)
    cam = Camera(40, 24, 0.7, 0.5)
    depth, normals = room(cam)
    lights = random_lights(rng, 30)
    out, _, _ = clustered_shading(depth, normals, cam, lights, tile=8)
    assert out == brute_force(depth, normals, cam, lights)


def test_only_occupied_clusters_get_lists() -> None:
    cam = Camera(32, 32, 1.0, 0.5)
    depth, normals = room(cam)
    _, lists, _ = clustered_shading(depth, normals, cam, [], tile=8)
    assert set(lists) == set(cluster_keys(depth, cam, 8).values())
    assert len(lists) <= sum(1 for row in depth for d in row if d != math.inf)


def test_fewer_pairs_than_tiles_with_depth_gaps() -> None:
    """A measurement on this scene: many small lights between the box and the
    back wall. Clusters cut the tile depth range, so fewer pairs remain."""
    rng = random.Random(34)
    cam = Camera(32, 32, 1.0, 0.5)
    depth, normals = room(cam)
    lights = random_lights(rng, 60, r_max=0.8)
    _, _, pairs = clustered_shading(depth, normals, cam, lights, tile=8)
    assert pairs < tiled_pairs(depth, cam, lights, 8)
