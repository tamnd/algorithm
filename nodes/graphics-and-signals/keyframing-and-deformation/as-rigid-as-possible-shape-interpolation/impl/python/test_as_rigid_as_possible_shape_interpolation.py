# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/as-rigid-as-possible-shape-interpolation/. The authors are listed in prov/B6HGFM.jsonl.
import math
import random

import pytest

import anim
from as_rigid_as_possible_shape_interpolation import (
    ARAPShapeInterpolation,
    affine_part,
    consistent_angles,
)


def grid(nx, ny):
    pts = [(float(x), float(y)) for y in range(ny) for x in range(nx)]
    tris = []
    for y in range(ny - 1):
        for x in range(nx - 1):
            a, b, c, d = y * nx + x, y * nx + x + 1, (y + 1) * nx + x, (y + 1) * nx + x + 1
            tris.append((a, b, d))
            tris.append((a, d, c))
    return pts, tris


def rigid(points, ang, shift):
    c, s = math.cos(ang), math.sin(ang)
    return [(c * x - s * y + shift[0], s * x + c * y + shift[1]) for x, y in points]


def area(points, tri):
    i, j, k = tri
    return 0.5 * anim.cross2(anim.sub(points[j], points[i]), anim.sub(points[k], points[i]))


def max_gap(ps, qs):
    return max(anim.norm(anim.sub(p, q)) for p, q in zip(ps, qs))


def bent(points, rng):
    return [(x + 0.15 * y * y + rng.uniform(-0.05, 0.05), 1.2 * y + 0.1 * x + rng.uniform(-0.05, 0.05)) for x, y in points]


def test_ends_are_the_source_and_the_target(rng=random.Random(1)):
    src, tris = grid(4, 3)
    tgt = rigid(bent(src, rng), 1.1, (2.0, -1.0))
    interp = ARAPShapeInterpolation(src, tgt, tris)
    assert max_gap(interp(0.0), src) < 1e-12
    assert max_gap(interp(1.0), tgt) < 1e-12


def test_rigid_motion_gives_a_rigid_morph():
    src, tris = grid(3, 3)
    ang, shift = 2.5, (4.0, 1.0)
    tgt = rigid(src, ang, shift)
    interp = ARAPShapeInterpolation(src, tgt, tris)
    for t in (0.2, 0.5, 0.9):
        v0 = anim.lerp(src[0], tgt[0], t)
        ref = [anim.add(v0, p) for p in rigid([anim.sub(p, src[0]) for p in src], t * ang, (0.0, 0.0))]
        assert max_gap(interp(t), ref) < 1e-12


def test_solution_minimizes_the_energy(rng=random.Random(2)):
    src, tris = grid(4, 4)
    tgt = rigid(bent(src, rng), -0.7, (1.0, 1.0))
    interp = ARAPShapeInterpolation(src, tgt, tris)
    t = 0.4
    v = interp(t)
    flat = [c for p in v[1:] for c in p]

    def e(x):
        pts = [v[0]] + [(x[2 * i], x[2 * i + 1]) for i in range(len(v) - 1)]
        return interp.energy(pts, t)

    g = anim.num_grad(e, flat)
    assert max(abs(x) for x in g) < 1e-6
    e0 = e(flat)
    for _ in range(20):
        d = [rng.gauss(0, 1e-2) for _ in flat]
        assert e([a + b for a, b in zip(flat, d)]) > e0


def test_single_triangle_follows_the_matrix_path():
    src = [(0.0, 0.0), (2.0, 0.0), (0.0, 1.0)]
    tgt = [(1.0, 1.0), (1.0, 4.0), (0.0, 1.0)]
    interp = ARAPShapeInterpolation(src, tgt, [(0, 1, 2)])
    for t in (0.0, 0.3, 0.5, 1.0):
        v = interp(t)
        b = affine_part(src, v, (0, 1, 2))
        a = interp.triangle_targets(t)[0]
        assert max(abs(b[r][c] - a[r][c]) for r in range(2) for c in range(2)) < 1e-12


def test_polar_path_keeps_the_area_better_than_linear_interpolation():
    src, tris = grid(3, 3)
    tgt = rigid(src, 3.0, (0.0, 0.0))
    interp = ARAPShapeInterpolation(src, tgt, tris)
    mid = interp(0.5)
    lin = [anim.lerp(p, q, 0.5) for p, q in zip(src, tgt)]
    total = sum(area(src, tri) for tri in tris)
    assert sum(area(mid, tri) for tri in tris) == pytest.approx(total, rel=1e-12)
    # Linear interpolation of a turn by almost 180 degrees nearly collapses the shape.
    assert abs(sum(area(lin, tri) for tri in tris)) < 0.01 * total


def test_consistent_angles_on_a_strip():
    tris = [(0, 1, 2), (1, 3, 2), (2, 3, 4), (3, 5, 4)]
    angles = [3.0, -3.1, 3.05, -3.0]
    out = consistent_angles(angles, tris)
    assert out[0] == 3.0
    for a, b in zip(out, out[1:]):
        assert abs(a - b) < math.pi
    assert out[1] == pytest.approx(-3.1 + 2 * math.pi)


def test_consistent_angles_make_the_triangles_turn_the_same_way(rng=random.Random(3)):
    src, tris = grid(4, 3)
    # A turn by nearly 180 degrees with a small bend: some polar angles wrap around to near -pi.
    tgt = rigid([(x + rng.uniform(-0.1, 0.1), y + 0.05 * x * x) for x, y in src], math.pi - 0.03, (0.0, 0.0))
    raw = ARAPShapeInterpolation(src, tgt, tris, consistent=False)
    assert max(raw.angles) > 0 and min(raw.angles) < 0
    good = ARAPShapeInterpolation(src, tgt, tris)
    assert max(good.angles) - min(good.angles) < 0.5
    mid = good(0.5)
    assert all(area(mid, tri) > 0 for tri in tris)
    bad = raw(0.5)
    assert min(area(bad, tri) for tri in tris) < 0.5 * min(area(mid, tri) for tri in tris)


def test_bad_input():
    with pytest.raises(ValueError):
        ARAPShapeInterpolation([(0.0, 0.0), (1.0, 0.0)], [(0.0, 0.0), (1.0, 0.0)], [(0, 1, 0)])
    pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (5.0, 5.0), (6.0, 5.0), (5.0, 6.0)]
    with pytest.raises(ValueError):
        ARAPShapeInterpolation(pts, pts, [(0, 1, 2), (3, 4, 5)])
