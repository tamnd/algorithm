# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phong-shading/. The authors are listed in prov/64PX56.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction

import pytest

from phong_shading import phong_triangle, reflection_model


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


def brute(verts, normals, light, view, material, width, height, sub, blinn=False):
    """Per pixel: test the center, take the barycentric sum of the vertex normals, normalize, light."""
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
            lam = (float(l0), float(l1), float(1 - l0 - l1))
            m = [sum(lam[k] * normals[k][q] for k in range(3)) for q in range(3)]
            length = math.sqrt(sum(c * c for c in m))
            unit = (m[0] / length, m[1] / length, m[2] / length)
            out.append((i, j, reflection_model(unit, light, view, *material, blinn=blinn)))
    return out


def same(got, want) -> None:
    assert [p[:2] for p in got] == [p[:2] for p in want]
    for g, w in zip(got, want):
        assert g[2] == pytest.approx(w[2], rel=1e-9, abs=1e-12)


EX_VERTS = ((0, 0), (128, 0), (0, 128))  # (0, 0), (8, 0), (0, 8) in pixels with sub = 16
EX_N = ((-0.48, -0.36, 0.8), (0.6, 0.0, 0.8), (0.0, 0.6, 0.8))
EYE = (0.0, 0.0, 1.0)
EX_MAT = (0.1, 0.5, 0.4, 20)


def test_worked_example() -> None:
    vertex = [reflection_model(n, EYE, EYE, *EX_MAT) for n in EX_N]
    assert vertex == pytest.approx([0.5] * 3, abs=1e-11)
    got = phong_triangle(EX_VERTS, EX_N, EYE, EYE, EX_MAT, 8, 8, 16)
    assert [(i, j) for i, j, _ in got] == [(i, j) for j in range(7) for i in range(7) if i + j <= 6]
    values = {(i, j): x for i, j, x in got}
    assert max(values, key=values.get) == (2, 2)
    assert values[2, 2] == pytest.approx(0.934425, abs=1e-6)
    assert values[0, 0] == pytest.approx(0.530503, abs=1e-6)
    same(got, brute(EX_VERTS, EX_N, EYE, EYE, EX_MAT, 8, 8, 16))


def test_reflection_model() -> None:
    n = (0.0, 0.0, 1.0)
    light = (0.6, 0.0, 0.8)
    # r = 2(n.l)n - l = (-0.6, 0, 0.8); view along r gives the full specular term.
    assert reflection_model(n, light, (-0.6, 0.0, 0.8), 0.1, 0.5, 0.4, 10) == pytest.approx(0.1 + 0.5 * 0.8 + 0.4)
    # Along n: r.v = 0.8 and the half vector is (0.6, 0, 1.8)/|.|, so n.h = 1.8/sqrt(3.6).
    assert reflection_model(n, light, n, 0, 0, 1, 2) == pytest.approx(0.64)
    assert reflection_model(n, light, n, 0, 0, 1, 2, blinn=True) == pytest.approx(1.8**2 / 3.6)
    assert reflection_model((0.0, 0.0, -1.0), light, n, 0.1, 0.5, 0.4, 10) == pytest.approx(0.1)


def test_normals_are_normalized_per_pixel() -> None:
    # The pixel half way between normals (0.6, 0, 0.8) and (-0.6, 0, 0.8) gets (0, 0, 1), not (0, 0, 0.8).
    verts = ((0, 0), (64, 0), (0, 64))
    normals = ((0.6, 0.0, 0.8), (-0.6, 0.0, 0.8), (0.6, 0.0, 0.8))
    values = {(i, j): x for i, j, x in phong_triangle(verts, normals, EYE, EYE, (0, 1, 0, 1), 4, 4, 16)}
    # Center (1.5, 0.5) has l1 = 1.5/4, so m_x = 0.6 (1 - 2 l1) = 0.15 and the unit normal has n_z = 0.8/sqrt(0.6625).
    assert values[1, 0] == pytest.approx(0.8 / math.sqrt(0.15**2 + 0.64))
    flat = phong_triangle(verts, ((0.0, 0.6, 0.8),) * 3, EYE, EYE, (0.1, 0.5, 0.4, 5), 4, 4, 16)
    assert all(x == pytest.approx(reflection_model((0.0, 0.6, 0.8), EYE, EYE, 0.1, 0.5, 0.4, 5)) for _, _, x in flat)


def test_edge_cases() -> None:
    n = ((0.0, 0.0, 1.0),) * 3
    assert phong_triangle(((0, 0), (16, 16), (32, 32)), n, EYE, EYE, EX_MAT, 4, 4) == []
    assert phong_triangle(((-99, -99), (-50, -99), (-99, -50)), n, EYE, EYE, EX_MAT, 4, 4) == []
    big = phong_triangle(((-999, -999), (3000, -999), (-999, 3000)), n, EYE, EYE, EX_MAT, 4, 4)
    assert [(i, j) for i, j, _ in big] == [(i, j) for j in range(4) for i in range(4)]


def random_normal(rng: random.Random) -> tuple[float, float, float]:
    x, y, z = rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(0.3, 1)
    s = math.sqrt(x * x + y * y + z * z)
    return (x / s, y / s, z / s)


@pytest.mark.parametrize("blinn", [False, True])
def test_against_brute_force(blinn: bool) -> None:
    rng = random.Random(5 + blinn)
    for n in range(300):
        sub = rng.choice([2, 4, 16])
        step = rng.choice([1, sub // 2])
        verts = tuple((rng.randrange(-sub, 6 * sub) // step * step, rng.randrange(-sub, 6 * sub) // step * step) for _ in range(3))
        normals = tuple(random_normal(rng) for _ in range(3))
        light, view = random_normal(rng), random_normal(rng)
        material = (rng.uniform(0, 0.2), rng.uniform(0, 0.8), rng.uniform(0, 0.8), rng.choice([1, 5, 20, 60]))
        got = phong_triangle(verts, normals, light, view, material, 5, 5, sub, blinn)
        same(got, brute(verts, normals, light, view, material, 5, 5, sub, blinn))


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
    n = ((0.0, 0.0, 1.0),) * 3
    count = Counter()
    for gy in range(cells):
        for gx in range(cells):
            a, b, c, d = grid[gx, gy], grid[gx + 1, gy], grid[gx + 1, gy + 1], grid[gx, gy + 1]
            for t in ([(a, b, c), (a, c, d)] if rng.random() < 0.5 else [(a, b, d), (b, c, d)]):
                count.update((i, j) for i, j, _ in phong_triangle(tuple(t), n, EYE, EYE, EX_MAT, 8, 8, 16))
    assert all(count[i, j] == 1 for j in range(8) for i in range(8))
    assert sum(count.values()) == 64
