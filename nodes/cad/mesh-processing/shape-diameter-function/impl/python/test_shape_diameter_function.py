# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shape-diameter-function/. The authors are listed in prov/WRAPDK.jsonl.

import math
from fractions import Fraction

from mx1mesh import box_mesh, centroid, cross, dot, exact, mat_vec, sub, to_float
from shape_diameter_function import normalize, ray_lengths, ray_triangle, shape_diameter


def slab(h):
    """The box 6 x 6 x h, cut into unit squares on the big sides, and a face of the top side near its centre."""
    p, f = box_mesh((6, 6, h), (6, 6, 1))
    top = [g for g in range(len(f)) if all(p[v][2] == Fraction(h) / 2 for v in f[g])]
    centre = [g for g in top if all(abs(x) <= 1 for x in centroid(p, f[g])[:2])]
    return p, f, centre[0]


def slab_sdf(h):
    """The SDF of a slab of thickness h from the formula: all 25 rays hit the far side, at the lengths h / cos(theta)."""
    lengths = [h] + [h / math.cos(math.radians(a)) for a in (20, 40, 60) for _ in range(8)]
    lengths.sort()
    m = lengths[12]
    s = math.sqrt(sum((x - sum(lengths) / 25) ** 2 for x in lengths) / 25)
    kept = [x for x in lengths if abs(x - m) <= s]
    return sum(kept) / len(kept)


def float_ray_triangle(o, d, a, b, c):
    """The same test as ray_triangle, in floating point."""
    e1, e2 = sub(b, a), sub(c, a)
    pv = cross(d, e2)
    det = dot(e1, pv)
    if det == 0:
        return None
    s = sub(o, a)
    u = dot(s, pv) / det
    if u < 0 or u > 1:
        return None
    qv = cross(s, e1)
    v = dot(d, qv) / det
    if v < 0 or u + v > 1:
        return None
    t = dot(e2, qv) / det
    return t if t > 0 else None


def test_the_ray_triangle_test_is_exact_on_edges_and_vertices() -> None:
    a, b, c = (0, 0, 0), (1, 0, 0), (0, 1, 0)
    assert ray_triangle((Fraction(1, 2), Fraction(1, 2), 1), (0, 0, -1), a, b, c) == 1  # on the edge bc
    assert ray_triangle((1, 0, 2), (0, 0, -1), a, b, c) == 2  # through the vertex b
    assert ray_triangle((Fraction(1, 2), Fraction(1, 2) + Fraction(1, 10**30), 1), (0, 0, -1), a, b, c) is None
    assert ray_triangle((0, 0, 1), (1, 0, 0), a, b, c) is None  # parallel to the plane
    assert ray_triangle((Fraction(1, 4), Fraction(1, 4), -1), (0, 0, -1), a, b, c) is None  # the plane is behind


def test_a_ray_through_a_shared_edge_does_not_leak() -> None:
    a = (0.07695759147568859, 0.24697890559501023, 0.22490492956545127)
    b = (-0.08370639980055117, -0.9440500318323153, -0.5407899374459522)
    c = (-0.6455774821228346, 0.16892174155688267, 0.7220177217066497)
    o = (0.5968778811548521, 0.5941951252709925, 0.6328747411213818)
    mid = tuple((x + y) / 2 for x, y in zip(b, c))
    assert exact(mid) == tuple((Fraction(x) + Fraction(y)) / 2 for x, y in zip(b, c))  # mid is exactly on the edge bc
    d = sub(mid, o)
    assert exact(d) == tuple(Fraction(x) - Fraction(y) for x, y in zip(mid, o))
    e = tuple(2 * m - x for m, x in zip(mid, a))  # abc and cbe share the edge bc
    assert ray_triangle(o, d, a, b, c) == 1 and ray_triangle(o, d, c, b, e) == 1
    assert float_ray_triangle(o, d, a, b, c) is None and float_ray_triangle(o, d, c, b, e) is None


def test_one_ray_gives_the_thickness_of_a_slab() -> None:
    for h in (1, Fraction(1, 2), Fraction(3, 7)):
        p, f, g = slab(h)
        assert ray_lengths(p, f, g, rays=1) == [float(h)]


def test_the_sdf_of_a_slab_follows_the_formula() -> None:
    for h in (1, Fraction(1, 2)):
        p, f, g = slab(h)
        lengths = ray_lengths(p, f, g)
        assert len(lengths) == 25  # every ray reaches the bottom side
        assert abs(shape_diameter(p, f, g) - slab_sdf(float(h))) < 1e-12
    p, f, g = slab(1)
    assert abs(shape_diameter(to_float(p), f, g) - slab_sdf(1.0)) < 1e-12  # float input, the same exact tests


def test_the_sdf_does_not_change_under_a_rational_rotation() -> None:
    p, f, g = slab(1)
    R1 = [[Fraction(3, 5), Fraction(-4, 5), 0], [Fraction(4, 5), Fraction(3, 5), 0], [0, 0, 1]]
    R2 = [[1, 0, 0], [0, Fraction(5, 13), Fraction(-12, 13)], [0, Fraction(12, 13), Fraction(5, 13)]]
    q = [tuple(mat_vec(R2, mat_vec(R1, x))) for x in p]
    assert abs(shape_diameter(q, f, g) - slab_sdf(1.0)) < 1e-9


def test_rays_that_reach_a_face_from_outside_are_dropped() -> None:
    p, f, g = slab(1)
    bottom = {k for k in range(len(f)) if all(p[v][2] == Fraction(-1, 2) for v in f[k])}
    flipped = [(a, c, b) if k in bottom else (a, b, c) for k, (a, b, c) in enumerate(f)]
    assert ray_lengths(p, flipped, g) == []
    assert shape_diameter(p, flipped, g) is None


def test_every_ray_of_a_cube_leaves_the_solid() -> None:
    p, f = box_mesh((2, 2, 2), (2, 2, 2))
    for g in range(0, len(f), 7):
        lengths = ray_lengths(p, f, g)
        assert len(lengths) == 25
        assert all(0 < x <= math.sqrt(12) for x in lengths)
        assert 0 < shape_diameter(p, f, g) < slab_sdf(2.0)


def test_the_normalization_keeps_the_order() -> None:
    v = [0.3, 1.2, 0.5, 0.9, 0.3]
    n = normalize(v)
    assert n[0] == 0.0 and n[1] == 1.0
    assert all((a < b) == (x < y) for a, x in zip(v, n) for b, y in zip(v, n))
    assert normalize([2.0, 2.0]) == [0.0, 0.0]
