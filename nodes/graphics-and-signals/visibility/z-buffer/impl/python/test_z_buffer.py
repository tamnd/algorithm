# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/z-buffer/. The authors are listed in prov/QPWQ6K.jsonl.

import random
from fractions import Fraction

from z_buffer import z_buffer

HALF = Fraction(1, 2)


def inside_perturbed(tri, px, py):
    """Brute force coverage: p is inside when p + (t, t^2) is strictly inside
    for all small t > 0. This is the top-left rule written as a perturbation."""
    a, b, c = [(v[0], v[1]) for v in tri]
    area = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if area == 0:
        return False
    if area < 0:
        b, c = c, b
    for (ax, ay), (bx, by) in ((b, c), (c, a), (a, b)):
        e0 = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
        coeffs = (e0, -(by - ay), bx - ax)  # E(p + (t, t^2)) = e0 + t c1 + t^2 c2
        lead = next((x for x in coeffs if x != 0), 0)
        if lead <= 0:
            return False
    return True


def plane_depth(tri, px, py):
    """Brute force depth from the plane normal n = (b - a) x (c - a)."""
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = tri
    ux, uy, uz = bx - ax, by - ay, bz - az
    vx, vy, vz = cx - ax, cy - ay, cz - az
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    return az - Fraction(nx * (px - ax) + ny * (py - ay), nz)


def brute(width, height, tris, colors, background=None):
    color = [[background] * width for _ in range(height)]
    depth = [[None] * width for _ in range(height)]
    for j in range(height):
        for i in range(width):
            px, py = i + HALF, j + HALF
            best = None
            for k, t in enumerate(tris):
                if inside_perturbed(t, px, py):
                    key = (plane_depth(t, px, py), k)
                    if best is None or key < best:
                        best = key
            if best is not None:
                depth[j][i] = best[0]
                color[j][i] = colors[best[1]]
    return color, depth


def random_scene(rng, n, width, height, den):
    tris = []
    for _ in range(n):
        tri = tuple(
            (Fraction(rng.randint(-den, (width + 1) * den), den),
             Fraction(rng.randint(-den, (height + 1) * den), den),
             Fraction(rng.randint(0, 20 * den), den))
            for _ in range(3))
        tris.append(tri)
    return tris


def test_example():
    # Two triangles that cross each other in depth, on an 8 by 6 image.
    a = ((0, 0, 0), (8, 0, 0), (4, 6, 12))
    b = ((0, 6, 0), (8, 6, 0), (4, 0, 12))
    for order, names in (([a, b], ["A", "B"]), ([b, a], ["B", "A"])):
        color, depth = z_buffer(8, 6, order, names, ".")
        rows = ["".join(r) for r in color]
        assert rows == ["AAAAAAAA", ".AAAAAA.", "..AAAA..", "..BBBB..",
                        ".BBBBBB.", "BBBBBBBB"]
        assert [depth[j][3] for j in range(6)] == [1, 3, 5, 5, 3, 1]
        assert (color, depth) == brute(8, 6, order, names, ".")


def test_against_brute_force():
    rng = random.Random(1974)
    for _ in range(60):
        w, h = rng.randint(1, 9), rng.randint(1, 8)
        tris = random_scene(rng, rng.randint(0, 6), w, h, rng.choice([1, 2, 4]))
        cols = list(range(len(tris)))
        assert z_buffer(w, h, tris, cols) == brute(w, h, tris, cols)


def test_shared_edges_cover_once():
    # A grid of squares cut into triangles: each center is covered exactly once.
    tris = []
    for gy in range(0, 6, 2):
        for gx in range(0, 8, 2):
            p, q, r, s = (gx, gy, 0), (gx + 2, gy, 0), (gx + 2, gy + 2, 0), (gx, gy + 2, 0)
            tris += [(p, q, r), (p, r, s)]
    count = [[0] * 8 for _ in range(6)]
    from z_buffer import covered_pixels
    for t in tris:
        for i, j, _ in covered_pixels(t, 8, 6):
            count[j][i] += 1
    assert all(c == 1 for row in count for c in row)


def test_order_does_not_matter_for_depth():
    rng = random.Random(7)
    for _ in range(20):
        tris = random_scene(rng, 5, 7, 6, 2)
        d1 = z_buffer(7, 6, tris, [0] * 5)[1]
        rng.shuffle(tris)
        d2 = z_buffer(7, 6, tris, [0] * 5)[1]
        assert d1 == d2


def test_ties_keep_first():
    t = ((0, 0, 5), (4, 0, 5), (0, 4, 5))
    color, _ = z_buffer(4, 4, [t, t], ["first", "second"])
    assert color[0][0] == "first"
