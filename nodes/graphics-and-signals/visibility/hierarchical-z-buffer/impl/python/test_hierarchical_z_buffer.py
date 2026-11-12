# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hierarchical-z-buffer/. The authors are listed in prov/EAKK9Q.jsonl.

import random
from fractions import Fraction

from hierarchical_z_buffer import FAR, ZPyramid, hzb_render

HALF = Fraction(1, 2)


def inside_perturbed(tri, px, py):
    a, b, c = [(v[0], v[1]) for v in tri]
    area = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if area == 0:
        return False
    if area < 0:
        b, c = c, b
    for (ax, ay), (bx, by) in ((b, c), (c, a), (a, b)):
        e0 = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
        lead = next((x for x in (e0, -(by - ay), bx - ax) if x != 0), 0)
        if lead <= 0:
            return False
    return True


def plane_depth(tri, px, py):
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = tri
    ux, uy, uz = bx - ax, by - ay, bz - az
    vx, vy, vz = cx - ax, cy - ay, cz - az
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    return az - Fraction(nx * (px - ax) + ny * (py - ay), nz)


def brute(width, height, objects):
    """Per pixel: all (depth, object) pairs over all triangles, sorted."""
    return [[sorted((plane_depth(t, i + HALF, j + HALF), o) for o, ob in enumerate(objects)
                    for t in ob if inside_perturbed(t, i + HALF, j + HALF))
             for i in range(width)] for j in range(height)]


def rand_objects(rng, n, w, h):
    objs = []
    for _ in range(n):
        cx, cy, cz = rng.randint(0, w), rng.randint(0, h), rng.randint(0, 40)
        objs.append([tuple((Fraction(cx + rng.randint(-3, 3) * 2 + rng.randint(0, 1), 2) * 2,
                            Fraction(cy + rng.randint(-3, 3) * 2, 2) * 2,
                            Fraction(cz + rng.randint(0, 6), 2)) for _ in range(3))
                     for _ in range(rng.randint(1, 3))])
    return objs


def test_example():
    # A near wall over the whole 8 by 8 screen, then a far box behind it.
    wall = [((0, 0, 1), (8, 0, 1), (8, 8, 1)), ((0, 0, 1), (8, 8, 1), (0, 8, 1))]
    box = [((2, 2, 5), (5, 2, 5), (5, 5, 6)), ((2, 2, 5), (5, 5, 6), (2, 5, 6))]
    color, depth, culled = hzb_render(8, 8, [wall, box], ["W", "B"])
    assert culled == {"objects": 1, "triangles": 0}
    assert all(c == "W" for row in color for c in row)


def test_query_is_exact_on_rectangles():
    rng = random.Random(1993)
    for _ in range(200):
        w, h = rng.randint(1, 9), rng.randint(1, 9)
        p = ZPyramid(w, h)
        for _ in range(rng.randint(0, w * h)):
            p.write(rng.randrange(w), rng.randrange(h), rng.randint(0, 9))
        i0, i1 = sorted((rng.randrange(w), rng.randrange(w)))
        j0, j1 = sorted((rng.randrange(h), rng.randrange(h)))
        zmin = rng.randint(0, 10)
        want = all(zmin >= p.depth(i, j) for i in range(i0, i1 + 1) for j in range(j0, j1 + 1))
        assert p.hidden((i0, j0, i1, j1), zmin) == want


def test_pyramid_holds_farthest_depth():
    rng = random.Random(4)
    p = ZPyramid(6, 5)
    for _ in range(40):
        p.write(rng.randrange(6), rng.randrange(5), rng.randint(0, 99))
    for l in range(1, p.levels + 1):
        s = 1 << l
        for y in range(len(p.z[l])):
            for x in range(len(p.z[l])):
                block = [p.z[0][yy][xx] for yy in range(y * s, y * s + s) for xx in range(x * s, x * s + s)]
                assert p.z[l][y][x] == max(block)


def test_render_against_brute_force():
    rng = random.Random(231)
    total_culled = 0
    for _ in range(40):
        w, h = rng.randint(2, 10), rng.randint(2, 10)
        objs = rand_objects(rng, rng.randint(1, 6), w, h)
        color, depth, culled = hzb_render(w, h, objs, list(range(len(objs))))
        total_culled += culled["objects"] + culled["triangles"]
        frags = brute(w, h, objs)
        for j in range(h):
            for i in range(w):
                f = frags[j][i]
                assert depth[j][i] == (f[0][0] if f else None)
                if len(f) == 1 or (len(f) > 1 and f[0][0] < f[1][0]):
                    assert color[j][i] == f[0][1]
    assert total_culled > 0


def test_culling_never_hides_a_visible_triangle():
    # Each culled triangle has no fragment nearer than the final depth.
    rng = random.Random(77)
    for _ in range(30):
        w, h = rng.randint(2, 8), rng.randint(2, 8)
        objs = rand_objects(rng, 5, w, h)
        _, depth, _ = hzb_render(w, h, objs, [0] * 5)
        for ob in objs:
            for t in ob:
                for j in range(h):
                    for i in range(w):
                        if inside_perturbed(t, i + HALF, j + HALF):
                            assert depth[j][i] <= plane_depth(t, i + HALF, j + HALF)
    assert FAR == float("inf")
