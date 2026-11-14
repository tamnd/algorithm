# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/triangle-mesh-slicing/. The authors are listed in prov/ETJZAW.jsonl.

import random
from collections import Counter
from fractions import Fraction

import pytest

from triangle_mesh_slicing import crossing, edge_point, signed_area, slice_mesh

# ---- meshes ----


def box(x0, y0, z0, x1, y1, z1):
    v = [(x, y, z) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    f = [(0, 2, 1), (1, 2, 3), (4, 5, 6), (5, 7, 6), (0, 1, 4), (1, 5, 4),
         (2, 6, 3), (3, 6, 7), (0, 4, 2), (2, 4, 6), (1, 3, 5), (3, 7, 5)]
    return v, f


def tetrahedron():
    v = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    f = [(0, 2, 1), (0, 1, 3), (1, 2, 3), (0, 3, 2)]
    return v, f


def ring_solid(rings, cap_low, cap_high, rng=None):
    """Closed mesh from horizontal rings of points around the z axis.

    rings is a list of (z, [(x, y), ...]) with z strictly increasing and the
    points in counterclockwise order. The caps are fans from (0, 0, cap_low)
    and (0, 0, cap_high). If rng is given, each quad gets a random diagonal.
    """
    v, f = [], []
    c = len(rings[0][1])
    for z, pts in rings:
        v.extend((x, y, z) for x, y in pts)
    idx = lambda i, j: i * c + (j % c)
    for i in range(len(rings) - 1):
        for j in range(c):
            a, b, cc, d = idx(i, j), idx(i, j + 1), idx(i + 1, j + 1), idx(i + 1, j)
            if rng is not None and rng.random() < 0.5:
                f += [(a, b, d), (b, cc, d)]
            else:
                f += [(a, b, cc), (a, cc, d)]
    lo, hi = len(v), len(v) + 1
    v += [(0, 0, cap_low), (0, 0, cap_high)]
    top = len(rings) - 1
    for j in range(c):
        f.append((lo, idx(0, j + 1), idx(0, j)))
        f.append((hi, idx(top, j), idx(top, j + 1)))
    return v, f


DIRS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


def random_ring_solid(rng):
    heights = sorted(rng.sample(range(0, 12), 4))
    rings = [(z, [(r * dx, r * dy) for dx, dy in DIRS for r in [rng.randint(1, 4)]]) for z in heights]
    low = heights[0] - rng.randint(0, 2)
    high = heights[-1] + rng.randint(0, 2)
    return ring_solid(rings, low, high, rng)


def frame():
    """Square frame [0,4]^2 minus [1,3]^2, height 2 (a torus, genus 1)."""
    outer = [(0, 0), (4, 0), (4, 4), (0, 4)]
    inner = [(1, 1), (3, 1), (3, 3), (1, 3)]
    v = [(x, y, z) for z in (0, 2) for x, y in outer + inner]
    O = lambda z, j: (0 if z == 0 else 8) + j % 4
    I = lambda z, j: (0 if z == 0 else 8) + 4 + j % 4
    f = []
    for j in range(4):
        f += [(O(0, j), O(0, j + 1), O(2, j + 1)), (O(0, j), O(2, j + 1), O(2, j))]  # outer walls
        f += [(I(0, j + 1), I(0, j), I(2, j)), (I(0, j + 1), I(2, j), I(2, j + 1))]  # inner walls
        f += [(O(2, j), O(2, j + 1), I(2, j + 1)), (O(2, j), I(2, j + 1), I(2, j))]  # top
        f += [(O(0, j + 1), O(0, j), I(0, j)), (O(0, j + 1), I(0, j), I(0, j + 1))]  # bottom
    return v, f


def check_closed_oriented(v, f):
    directed = Counter()
    for a, b, c in f:
        for e in ((a, b), (b, c), (c, a)):
            directed[e] += 1
    assert all(n == 1 for n in directed.values())
    assert all(directed[(b, a)] == 1 for a, b in directed)
    # signed volume by the divergence theorem must be positive
    vol = 0
    for a, b, c in f:
        p, q, r = v[a], v[b], v[c]
        vol += (p[0] * (q[1] * r[2] - q[2] * r[1]) - p[1] * (q[0] * r[2] - q[2] * r[0])
                + p[2] * (q[0] * r[1] - q[1] * r[0]))
    assert vol > 0


# ---- independent checks ----


def brute_segments(v, f, z):
    """Directed segments of every face at height z, without buckets or a sweep."""
    out = Counter()
    for face in f:
        lo = min(v[i][2] for i in face)
        hi = max(v[i][2] for i in face)
        if not (lo < z <= hi):
            continue
        ends = {}
        for i in range(3):
            a, b = face[i], face[(i + 1) % 3]
            sa, sb = v[a][2] >= z, v[b][2] >= z
            if sa != sb:
                ends["out" if sa else "in"] = edge_point(v[a], v[b], z)
        out[(ends["out"], ends["in"])] += 1
    return out


def loop_segments(loops):
    out = Counter()
    for lp in loops:
        for i in range(len(lp)):
            out[(lp[i], lp[(i + 1) % len(lp)])] += 1
    return out


def orient2d(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def on_segment(p, a, b):
    return (orient2d(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def winding(p, loops):
    w = 0
    for lp in loops:
        for i in range(len(lp)):
            a, b = lp[i], lp[(i + 1) % len(lp)]
            if a[1] <= p[1] < b[1] and orient2d(a, b, p) > 0:
                w += 1
            elif b[1] <= p[1] < a[1] and orient2d(a, b, p) < 0:
                w -= 1
    return w


def inside_by_vertical_ray(v, f, p, z):
    """Parity of the faces above (p, z - eps) on the vertical line through p.

    Returns None if the line meets a face boundary, so the sample is skipped.
    """
    count = 0
    for face in f:
        a, b, c = (v[i] for i in face)
        a2, b2, c2 = a[:2], b[:2], c[:2]
        area = orient2d(a2, b2, c2)
        if any(on_segment(p, s, t) for s, t in ((a2, b2), (b2, c2), (c2, a2))):
            return None
        if area == 0:
            continue
        u, w, x = orient2d(b2, c2, p), orient2d(c2, a2, p), orient2d(a2, b2, p)
        if (u > 0 and w > 0 and x > 0) or (u < 0 and w < 0 and x < 0):
            h = (Fraction(u) * a[2] + Fraction(w) * b[2] + Fraction(x) * c[2]) / area
            if h >= z:
                count += 1
    return count % 2 == 1


# ---- tests ----


def test_page_example_cube():
    v, f = box(0, 0, 0, 2, 2, 2)
    out = slice_mesh(v, f, [0, 1, 2])
    assert out[0] == []
    assert [signed_area(lp) for lp in out[1]] == [4]
    assert [signed_area(lp) for lp in out[2]] == [4]
    assert len(out[1][0]) == 8  # each side face gives one segment


def test_meshes_are_closed_and_oriented():
    for v, f in [box(0, 0, 0, 2, 2, 2), tetrahedron(), frame()]:
        check_closed_oriented(v, f)
    rng = random.Random(5)
    for _ in range(10):
        check_closed_oriented(*random_ring_solid(rng))


def test_tetrahedron_area_exact():
    v, f = tetrahedron()
    zs = [Fraction(i, 7) for i in range(-1, 9)]
    for z, loops in zip(zs, slice_mesh(v, f, zs)):
        want = (1 - z) ** 2 / 2 if 0 < z <= 1 else 0
        assert sum(signed_area(lp) for lp in loops) == want
        assert len(loops) == (1 if 0 < z <= 1 else 0)


def test_frame_has_a_hole():
    v, f = frame()
    out = slice_mesh(v, f, [Fraction(1, 2), 1, 2])
    for loops in out:
        areas = sorted(signed_area(lp) for lp in loops)
        assert areas == [-4, 16]  # hole clockwise, outer counterclockwise
        assert sum(areas) == 12
    # Euler characteristic of the torus
    edges = {tuple(sorted(e)) for a, b, c in f for e in ((a, b), (b, c), (c, a))}
    assert len(v) - len(edges) + len(f) == 0


def test_against_direct_slicing():
    rng = random.Random(11)
    for _ in range(25):
        v, f = random_ring_solid(rng)
        zs = sorted({vz for _, _, vz in v} | {Fraction(rng.randrange(-6, 45), 3) for _ in range(6)})
        out = slice_mesh(v, f, zs)
        for z, loops in zip(zs, out):
            assert loop_segments(loops) == brute_segments(v, f, z)


def test_every_contour_is_closed_and_consistent():
    rng = random.Random(3)
    for _ in range(25):
        v, f = random_ring_solid(rng)
        zs = sorted({vz for _, _, vz in v})  # planes through vertices only
        for z, loops in zip(zs, slice_mesh(v, f, zs)):
            for lp in loops:
                assert len(lp) >= 2
            segs = loop_segments(loops)
            starts = Counter(s for s, _ in segs.elements())
            ends = Counter(e for _, e in segs.elements())
            assert starts == ends  # every point is entered as often as it is left


def test_point_membership_against_vertical_rays():
    rng = random.Random(7)
    checked = 0
    for _ in range(8):
        v, f = random_ring_solid(rng)
        zs = sorted({vz for _, _, vz in v} | {Fraction(rng.randrange(0, 36), 3) for _ in range(3)})
        for z, loops in zip(zs, slice_mesh(v, f, zs)):
            for _ in range(15):
                p = (Fraction(rng.randrange(-4500, 4500), 997), Fraction(rng.randrange(-4500, 4500), 997))
                inside = inside_by_vertical_ray(v, f, p, z)
                if inside is None:
                    continue
                if any(on_segment(p, lp[i], lp[(i + 1) % len(lp)]) for lp in loops for i in range(len(lp))):
                    continue
                assert winding(p, loops) == (1 if inside else 0)
                checked += 1
    assert checked > 500


def test_vertex_on_plane_counts_as_above():
    v, f = tetrahedron()
    face = (0, 1, 3)  # vertices at z = 0, 0, 1
    assert crossing(v, face, 0) is None
    e_out, p, e_in = crossing(v, face, 1)
    assert p == (0, 0)  # both crossing points are the apex
    assert edge_point(v[0], v[3], 1) == (0, 0)


def test_planes_must_increase():
    v, f = box(0, 0, 0, 1, 1, 1)
    with pytest.raises(ValueError):
        slice_mesh(v, f, [1, 1])


def test_float_points_depend_on_edge_direction():
    """Why loops are linked by edge keys and not by rounded points."""
    rng = random.Random(1)
    differ = 0
    for _ in range(2000):
        a = (rng.random(), rng.random(), rng.random())
        b = (rng.random(), rng.random(), rng.random() + 1.0)
        z = rng.uniform(a[2], b[2])
        ta = (z - a[2]) / (b[2] - a[2])
        tb = (z - b[2]) / (a[2] - b[2])
        pa = (a[0] + (b[0] - a[0]) * ta, a[1] + (b[1] - a[1]) * ta)
        pb = (b[0] + (a[0] - b[0]) * tb, b[1] + (a[1] - b[1]) * tb)
        if pa != pb:
            differ += 1
    assert differ > 0
