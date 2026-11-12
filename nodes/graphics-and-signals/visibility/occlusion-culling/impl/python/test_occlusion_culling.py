# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/occlusion-culling/. The authors are listed in prov/J4XCZM.jsonl.

import random
from fractions import Fraction

from occlusion_culling import bounding_box, covers, depth_at, occlusion_cull


def rect(x0, y0, x1, y1, z):
    """A rectangle at constant depth z as two triangles."""
    return [((x0, y0, z), (x1, y0, z), (x1, y1, z)), ((x0, y0, z), (x1, y1, z), (x0, y1, z))]


def brute(objects, W, H):
    """Exact per-pixel depth: the largest depth at each center and the objects that reach it."""
    best = [[None] * W for _ in range(H)]
    who = [[set() for _ in range(W)] for _ in range(H)]
    for j in range(H):
        for i in range(W):
            c = (Fraction(2 * i + 1, 2), Fraction(2 * j + 1, 2))
            for k, obj in enumerate(objects):
                for tri in obj:
                    if covers(tri, c):
                        z = depth_at(tri, c)
                        if best[j][i] is None or z > best[j][i]:
                            best[j][i], who[j][i] = z, {k}
                        elif z == best[j][i]:
                            who[j][i].add(k)
    return best, who


def full_zbuffer(objects, W, H, order):
    depth = [[None] * W for _ in range(H)]
    image = [[None] * W for _ in range(H)]
    for k in order:
        for tri in objects[k]:
            for j in range(H):
                for i in range(W):
                    c = (Fraction(2 * i + 1, 2), Fraction(2 * j + 1, 2))
                    if covers(tri, c):
                        z = depth_at(tri, c)
                        if depth[j][i] is None or z > depth[j][i]:
                            depth[j][i], image[j][i] = z, k
    return image


def check(objects, W, H):
    drawn, image, depth = occlusion_cull(objects, W, H)
    best, who = brute(objects, W, H)
    assert depth == best
    visible = set()
    for j in range(H):
        for i in range(W):
            visible |= who[j][i]
            assert (image[j][i] is None) == (not who[j][i])
            assert image[j][i] is None or image[j][i] in who[j][i]
    assert visible <= set(drawn)
    boxes = [bounding_box(o) for o in objects]
    order = sorted(range(len(objects)), key=lambda k: (-boxes[k][1][2], k))
    assert image == full_zbuffer(objects, W, H, order)
    return drawn, visible


def test_worked_example():
    A = rect(0, 0, 8, 4, 5)  # the wall
    D = [((2, 0, 4), (4, 0, 4), (2, 5, 4))]  # behind the wall, but its box reaches row 4
    C = rect(5, 2, 7, 6, 3)  # behind the wall in rows 2 and 3, in front of nothing above it
    B = [((1, 1, 1), (4, 1, 2), (1, 3, 2))]  # wholly behind the wall
    objects = [A, B, C, D]
    drawn, visible = check(objects, 8, 6)
    assert drawn == [0, 3, 2]  # A, D, C; B is culled
    assert visible == {0, 2}  # D is drawn but hidden
    _, image, _ = occlusion_cull(objects, 8, 6)
    rows = ["".join("." if v is None else "ABCD"[v] for v in row) for row in reversed(image)]
    assert rows == [".....CC.", ".....CC.", "AAAAAAAA", "AAAAAAAA", "AAAAAAAA", "AAAAAAAA"]


def random_triangle(rng, W, H, zlo, zhi):
    while True:
        x0, y0 = rng.randint(-1, W), rng.randint(-1, H)
        pts = [(x0 + rng.randint(0, 4), y0 + rng.randint(0, 4), rng.randint(zlo, zhi)) for _ in range(3)]
        a, b, c = pts
        if (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) != 0:
            return tuple(pts)


def random_scene(rng, W, H):
    objects = []
    for _ in range(rng.randint(2, 7)):
        if rng.random() < 0.35:
            x0, y0 = rng.randint(-1, W // 2), rng.randint(-1, H // 2)
            x1, y1 = rng.randint(x0 + 2, W + 1), rng.randint(y0 + 2, H + 1)
            z = rng.randint(5, 9)
            tilt = rng.choice((0, 0, 1, -1))
            objects.append([((x0, y0, z), (x1, y0, z + tilt), (x1, y1, z)),
                            ((x0, y0, z), (x1, y1, z), (x0, y1, z - tilt))])
        else:
            zlo = rng.randint(0, 7)
            objects.append([random_triangle(rng, W, H, zlo, zlo + rng.randint(0, 3))
                            for _ in range(rng.randint(1, 3))])
    return objects


def test_never_drops_a_visible_object():
    rng = random.Random(51)
    culled = extra = 0
    for case in range(500):
        objects = random_scene(rng, 6, 5)
        drawn, visible = check(objects, 6, 5)
        culled += len(objects) - len(drawn)
        extra += len(set(drawn) - visible)
    assert culled > 0 and extra > 0


def test_far_depth_of_the_box_is_the_wrong_bound():
    wall = rect(0, 0, 4, 4, 5)
    spike = [((0, 0, 2), (4, 0, 2), (4, 4, 8))]  # pokes through the wall where z > 5
    drawn, visible = check([wall, spike], 4, 4)
    assert visible == {0, 1} and drawn == [1, 0]
    lo, hi = bounding_box(spike)
    assert lo[2] < 5 < hi[2]  # a test with the farthest point lo z would cull a visible object


def test_ties_are_kept():
    a = rect(0, 0, 3, 3, 4)
    b = rect(0, 0, 3, 3, 4)  # same depth: the box test must be strict
    drawn, visible = check([a, b], 3, 3)
    assert drawn == [0, 1] and visible == {0, 1}


def test_edges():
    assert occlusion_cull([], 3, 3)[0] == []
    off = [((10, 10, 1), (12, 10, 1), (10, 12, 1))]  # outside the image
    tiny = [((Fraction(1, 10), Fraction(1, 10), 3), (Fraction(2, 10), Fraction(1, 10), 3),
             (Fraction(1, 10), Fraction(2, 10), 3))]  # covers no pixel center
    drawn, visible = check([off, tiny, rect(0, 0, 1, 1, 0)], 3, 3)
    assert drawn == [2] and visible == {2}
