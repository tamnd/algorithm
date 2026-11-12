# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/watkins-scanline-algorithm/. The authors are listed in prov/Z8FKJW.jsonl.

import random
from fractions import Fraction

import pytest

from watkins_scanline_algorithm import watkins

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


def brute(width, height, tris, background=None):
    """Per pixel center: the nearest covering triangle over all triangles."""
    out = [[background] * width for _ in range(height)]
    for j in range(height):
        for i in range(width):
            hits = [(plane_depth(t, i + HALF, j + HALF), k) for k, t in enumerate(tris)
                    if inside_perturbed(t, i + HALF, j + HALF)]
            if hits:
                out[j][i] = min(hits)[1]
    return out


def rand_scene(rng, n, w, h):
    # x has denominator 1, 2 or 3; y has denominator 1 or 3, so never j + 1/2.
    def vert():
        dx, dy = rng.choice([1, 2, 3]), rng.choice([1, 3])
        return (Fraction(rng.randint(-2 * dx, (w + 2) * dx), dx),
                Fraction(rng.randint(-2 * dy, (h + 2) * dy), dy),
                Fraction(rng.randint(0, 30), rng.choice([1, 2])))
    return [tuple(vert() for _ in range(3)) for _ in range(n)]


def test_example():
    a = ((0, 0, 0), (8, 0, 0), (4, 6, 12))
    b = ((0, 6, 0), (8, 6, 0), (4, 0, 12))
    img, splits = watkins(8, 6, [a, b], ".")
    rows = ["".join(c if c == "." else "AB"[c] for c in row) for row in img]
    assert rows == ["AAAAAAAA", ".AAAAAA.", "..AAAA..", "..BBBB..", ".BBBBBB.", "BBBBBBBB"]
    assert splits == 0  # each span has one nearest triangle at both ends


def test_crossing_inside_a_span():
    # Two triangles cross along the line x = 4: the span is cut there.
    a = ((0, 0, 0), (8, 0, 8), (0, 2, 0))
    b = ((0, 0, 4), (8, 0, 4), (8, 2, 4))
    img, splits = watkins(8, 2, [a, b], ".")
    rows = ["".join(c if c == "." else "AB"[c] for c in row) for row in img]
    assert rows == ["AAAABBBB", "AA....BB"]
    assert img == brute(8, 2, [a, b], ".")
    assert splits == 1


def test_against_brute_force():
    rng = random.Random(1970)
    for _ in range(120):
        w, h = rng.randint(1, 11), rng.randint(1, 9)
        tris = rand_scene(rng, rng.randint(0, 6), w, h)
        img, _ = watkins(w, h, tris)
        assert img == brute(w, h, tris)


def test_vertex_on_scanline_is_rejected():
    with pytest.raises(ValueError):
        watkins(4, 4, [((0, HALF, 0), (4, 0, 0), (0, 4, 0))])
