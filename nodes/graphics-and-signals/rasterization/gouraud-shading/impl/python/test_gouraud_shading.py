# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gouraud-shading/. The authors are listed in prov/43E96Q.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction

import pytest

from gouraud_shading import gouraud_triangle, lambert_intensity, vertex_normals


def covers_center(tri, cx, cy) -> bool:
    """Top-left rule from its Direct3D wording, with Fractions (independent of the scanline code)."""
    pts = [(Fraction(x), Fraction(y)) for x, y in tri]
    for k in range(3):
        a, b, c = pts[k], pts[(k + 1) % 3], pts[(k + 2) % 3]
        side_c = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        if side_c == 0:
            return False
        side_p = (b[0] - a[0]) * (cy - a[1]) - (b[1] - a[1]) * (cx - a[0])
        if side_p * side_c < 0:
            return False
        if side_p == 0:
            if a[1] == b[1]:
                ok = c[1] > a[1]
            else:
                ok = c[0] > a[0] + (b[0] - a[0]) * (c[1] - a[1]) / (b[1] - a[1])
            if not ok:
                return False
    return True


def brute(verts, intens, width, height, sub):
    """Each covered center with the barycentric combination of the vertex intensities."""
    (x0, y0), (x1, y1), (x2, y2) = verts
    area2 = (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)
    out = []
    for j in range(height):
        for i in range(width):
            cx, cy = Fraction(2 * i + 1, 2) * sub, Fraction(2 * j + 1, 2) * sub
            if not covers_center(verts, cx, cy):
                continue
            l0 = ((x2 - x1) * (cy - y1) - (y2 - y1) * (cx - x1)) / area2
            l1 = ((x0 - x2) * (cy - y2) - (y0 - y2) * (cx - x2)) / area2
            l2 = 1 - l0 - l1
            out.append((i, j, l0 * intens[0] + l1 * intens[1] + l2 * intens[2]))
    return out


EX_VERTS = ((8, 8), (72, 8), (8, 72))  # (0.5, 0.5), (4.5, 0.5), (0.5, 4.5) with sub = 16
EX_I = (Fraction(82, 100), Fraction(1), Fraction(676, 1000))


def test_worked_example() -> None:
    got = gouraud_triangle(EX_VERTS, EX_I, 5, 5, 16)
    assert [(i, j) for i, j, _ in got] == [(i, j) for j in range(4) for i in range(4) if i + j <= 3]
    values = {(i, j): x for i, j, x in got}
    assert values[0, 0] == Fraction(82, 100)
    assert values[3, 0] == Fraction(82, 100) + Fraction(3, 4) * Fraction(18, 100)
    assert values[1, 1] == Fraction(82, 100) + Fraction(1, 4) * Fraction(18, 100) + Fraction(1, 4) * Fraction(-144, 1000)
    assert got == brute(EX_VERTS, EX_I, 5, 5, 16)


def test_lighting_of_the_example() -> None:
    light = (0.6, 0.0, 0.8)
    normals = [(0.0, 0.0, 1.0), (0.6, 0.0, 0.8), (0.0, 0.6, 0.8)]
    got = [lambert_intensity(n, light, 0.1, 0.9) for n in normals]
    assert got == pytest.approx([0.82, 1.0, 0.676])
    assert lambert_intensity((0.0, 0.0, -1.0), light, 0.1, 0.9) == pytest.approx(0.1)


def test_vertex_normals() -> None:
    flat = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0)]
    for n in vertex_normals(flat, [(0, 1, 2), (0, 2, 3)]):
        assert n == pytest.approx((0.0, 0.0, 1.0))
    # Two faces at a right angle: the shared vertices get the bisector.
    pos = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
    ns = vertex_normals(pos, [(0, 1, 2), (0, 3, 1)])
    s = 1 / math.sqrt(2)
    assert ns[0] == pytest.approx((0.0, s, s))
    assert ns[2] == pytest.approx((0.0, 0.0, 1.0))
    assert ns[3] == pytest.approx((0.0, 1.0, 0.0))


def test_edge_cases() -> None:
    assert gouraud_triangle(((0, 0), (16, 16), (32, 32)), (1, 2, 3), 4, 4) == []
    assert gouraud_triangle(((-99, -99), (-50, -99), (-99, -50)), (1, 2, 3), 4, 4) == []
    flat = gouraud_triangle(((-999, -999), (3000, -999), (-999, 3000)), (Fraction(1, 2),) * 3, 4, 4)
    assert [(i, j) for i, j, _ in flat] == [(i, j) for j in range(4) for i in range(4)]
    assert all(x == Fraction(1, 2) for _, _, x in flat)


def test_against_brute_force() -> None:
    rng = random.Random(2)
    for n in range(600):
        sub = rng.choice([2, 4, 16])
        step = rng.choice([1, sub // 2])
        verts = tuple((rng.randrange(-sub, 6 * sub) // step * step, rng.randrange(-sub, 6 * sub) // step * step) for _ in range(3))
        intens = tuple(Fraction(rng.randrange(0, 256), 255) for _ in range(3))
        assert gouraud_triangle(verts, intens, 5, 5, sub) == brute(verts, intens, 5, 5, sub), (n, verts, sub)


def test_float_intensities_match_exact_ones() -> None:
    rng = random.Random(3)
    for _ in range(100):
        verts = tuple((rng.randrange(-16, 100), rng.randrange(-16, 100)) for _ in range(3))
        ints = [rng.randrange(0, 256) for _ in range(3)]
        exact = gouraud_triangle(verts, tuple(Fraction(x, 255) for x in ints), 6, 6)
        approx = gouraud_triangle(verts, tuple(x / 255 for x in ints), 6, 6)
        assert [p[:2] for p in exact] == [p[:2] for p in approx]
        for e, a in zip(exact, approx):
            assert float(e[2]) == pytest.approx(a[2], abs=1e-9)


@pytest.mark.parametrize("seed", range(4))
def test_shared_edges_cover_each_pixel_once(seed: int) -> None:
    rng = random.Random(seed)
    cell, cells = 32, 6
    grid = {}
    for gy in range(cells + 1):
        for gx in range(cells + 1):
            inner = 0 < gx < cells and 0 < gy < cells
            jx = rng.choice([-8, 0, 8, -5, 6]) if inner else 0
            jy = rng.choice([-8, 0, 8, -5, 6]) if inner else 0
            grid[gx, gy] = ((gx - 1) * cell + jx, (gy - 1) * cell + jy)
    count = Counter()
    for gy in range(cells):
        for gx in range(cells):
            a, b, c, d = grid[gx, gy], grid[gx + 1, gy], grid[gx + 1, gy + 1], grid[gx, gy + 1]
            for t in ([(a, b, c), (a, c, d)] if rng.random() < 0.5 else [(a, b, d), (b, c, d)]):
                count.update((i, j) for i, j, _ in gouraud_triangle(tuple(t), (0, 0, 0), 8, 8, 16))
    assert all(count[i, j] == 1 for j in range(8) for i in range(8))
    assert sum(count.values()) == 64
