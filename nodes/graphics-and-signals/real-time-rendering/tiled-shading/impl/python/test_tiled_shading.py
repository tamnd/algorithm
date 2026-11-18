# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tiled-shading/. The authors are listed in prov/TE6F11.jsonl.

"""Tiled shading against brute-force shading of every light at every pixel."""

import math
import random

from tiled_shading import (
    Camera,
    Light,
    affects,
    brute_force,
    build_light_lists,
    shade,
    side_planes,
    tiled_shading,
)


def room(cam: Camera, box: bool = True):
    """Depth and normals of a room seen from the origin: a floor at y = -1,
    side walls at x = -4 and x = 4, a back wall at z = -12 with an open
    window, and a small box face at z = -3."""
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
            if box and -1.0 <= 3.0 * u <= 0.5 and -1.0 <= 3.0 * v <= 0.5:
                hits.append((3.0, (0.0, 0.0, 1.0)))
            if hits:
                d, n = min(hits)
                depth[j][i] = d
                normals[j][i] = n
    return depth, normals


def random_lights(rng: random.Random, count: int) -> list[Light]:
    return [
        Light(
            (rng.uniform(-4.0, 4.0), rng.uniform(-1.0, 3.0), rng.uniform(-12.0, -1.0)),
            rng.uniform(0.5, 3.0),
            rng.uniform(0.5, 2.0),
        )
        for _ in range(count)
    ]


def test_no_light_is_missed() -> None:
    rng = random.Random(21)
    cam = Camera(48, 32, 1.0)
    depth, _ = room(cam)
    for tile in (4, 8, 16):
        lights = random_lights(rng, 40)
        lists = build_light_lists(depth, cam, lights, tile)
        for j in range(cam.height):
            for i in range(cam.width):
                if depth[j][i] == math.inf:
                    continue
                p = cam.position(i, j, depth[j][i])
                kept = set(lists[(i // tile, j // tile)])
                for idx, light in enumerate(lights):
                    if affects(p, light):
                        assert idx in kept


def test_equals_brute_force_exactly() -> None:
    rng = random.Random(22)
    cam = Camera(40, 24, 0.7)
    depth, normals = room(cam)
    lights = random_lights(rng, 30)
    ref = brute_force(depth, normals, cam, lights)
    out, _ = tiled_shading(depth, normals, cam, lights, tile=8)
    assert out == ref


def test_pixel_centers_are_inside_their_tile_frustum() -> None:
    cam = Camera(32, 32, 1.0)
    tile = 8
    for j in range(cam.height):
        for i in range(cam.width):
            x0, y0 = (i // tile) * tile, (j // tile) * tile
            planes = side_planes(cam, x0, x0 + tile, y0, y0 + tile)
            p = cam.position(i, j, 5.0)
            assert all(m[0] * p[0] + m[1] * p[1] + m[2] * p[2] >= -1e-12 for m in planes)


def test_light_outside_the_view_is_culled_everywhere() -> None:
    cam = Camera(32, 32, 1.0)
    depth, _ = room(cam)
    behind = Light((0.0, 0.0, 5.0), 2.0, 1.0)
    lists = build_light_lists(depth, cam, [behind], 8)
    assert all(not v for v in lists.values())


def test_depth_gap_gives_false_positives() -> None:
    """A tile that holds the box (d = 3) and the back wall (d = 12) keeps a
    small light at d = 7 in front of the wall, although it reaches no pixel."""
    cam = Camera(32, 32, 1.0)
    depth, normals = room(cam)
    light = Light((-0.3, -0.2, -7.0), 0.5, 1.0)
    lists = build_light_lists(depth, cam, [light], 16)
    holders = [t for t, v in lists.items() if v]
    assert holders
    for j in range(cam.height):
        for i in range(cam.width):
            if depth[j][i] != math.inf:
                p = cam.position(i, j, depth[j][i])
                assert shade(p, normals[j][i], light) == 0.0
