# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/triangle-triangle-intersection/. The authors are listed in prov/QR3KY9.jsonl.

import random
from fractions import Fraction

from triangle_triangle_intersection import cross, dot, normal, orient3d, orient3d_float, sub, tri_tri

# ---- independent oracles (no orientation predicates) ----


def det3(a, b, c):
    return dot(a, cross(b, c))


def segment_meets_triangle(a, b, t):
    """Closed segment ab against closed triangle t, by a one-variable linear program.

    Write a + s (b - a) - t0 = u e1 + v e2 + w n with the basis e1, e2, n of the
    triangle. Then u, v and w are affine in s, and the segment meets t if some
    s in [0, 1] has w = 0, u >= 0, v >= 0 and u + v <= 1.
    """
    e1, e2 = sub(t[1], t[0]), sub(t[2], t[0])
    n = cross(e1, e2)
    big = det3(e1, e2, n)  # = |n|^2 > 0
    y0, y1 = sub(a, t[0]), sub(b, a)
    u = (Fraction(det3(y0, e2, n), big), Fraction(det3(y1, e2, n), big))
    v = (Fraction(det3(e1, y0, n), big), Fraction(det3(e1, y1, n), big))
    w = (Fraction(det3(e1, e2, y0), big), Fraction(det3(e1, e2, y1), big))
    lo, hi = Fraction(0), Fraction(1)
    # w0 + s w1 = 0
    if w[1] == 0:
        if w[0] != 0:
            return False
    else:
        s = -w[0] / w[1]
        lo, hi = max(lo, s), min(hi, s)
    # c0 + s c1 >= 0
    for c0, c1 in (u, v, (1 - u[0] - v[0], -u[1] - v[1])):
        if c1 == 0:
            if c0 < 0:
                return False
        elif c1 > 0:
            lo = max(lo, -c0 / c1)
        else:
            hi = min(hi, -c0 / c1)
    return lo <= hi


def by_segments(p, q):
    """Two closed triangles meet iff an edge of one meets the other triangle."""
    for s, t in ((p, q), (q, p)):
        for i in range(3):
            if segment_meets_triangle(s[i], s[(i + 1) % 3], t):
                return True
    return False


def by_separating_axes(p, q):
    """Separating axis test: face normals, edge cross products and in-plane edge normals."""
    ep = [sub(p[(i + 1) % 3], p[i]) for i in range(3)]
    eq = [sub(q[(i + 1) % 3], q[i]) for i in range(3)]
    n1, n2 = normal(p), normal(q)
    axes = [n1, n2] + [cross(a, b) for a in ep for b in eq]
    axes += [cross(n1, a) for a in ep] + [cross(n2, b) for b in eq]
    for ax in axes:
        if ax == (0, 0, 0):
            continue
        sp = [dot(ax, v) for v in p]
        sq = [dot(ax, v) for v in q]
        if max(sp) < min(sq) or max(sq) < min(sp):
            return False
    return True


def degenerate(t):
    return normal(t) == (0, 0, 0)


def rand_tri(rng, r, flat=False):
    while True:
        t = [tuple(rng.randint(-r, r) if (k < 2 or not flat) else 0 for k in range(3)) for _ in range(3)]
        if not degenerate(t):
            return t


# ---- tests ----


def test_page_example():
    p = [(0, 0, 0), (4, 0, 0), (0, 4, 0)]
    q = [(1, 1, -1), (1, 1, 3), (3, 3, 1)]
    assert tri_tri(p, q)
    q_far = [(5, 5, -1), (5, 5, 3), (7, 7, 1)]
    assert not tri_tri(p, q_far)
    q_touch = [(2, 2, 0), (2, 2, 3), (5, 5, 3)]  # touches the hypotenuse at (2, 2, 0)
    assert tri_tri(p, q_touch)


def test_coplanar_cases():
    p = [(0, 0, 0), (4, 0, 0), (0, 4, 0)]
    assert tri_tri(p, [(1, 1, 0), (2, 1, 0), (1, 2, 0)])  # inside
    assert tri_tri([(1, 1, 0), (2, 1, 0), (1, 2, 0)], p)  # contains
    assert tri_tri(p, [(4, 0, 0), (6, 0, 0), (5, 2, 0)])  # shared vertex only
    assert not tri_tri(p, [(3, 3, 0), (6, 3, 0), (3, 6, 0)])  # beyond the hypotenuse
    assert tri_tri(p, [(2, 2, 0), (6, 2, 0), (2, 6, 0)])  # touches the hypotenuse at (2, 2)


def test_shared_edge_and_vertex():
    p = [(0, 0, 0), (2, 0, 0), (0, 2, 0)]
    assert tri_tri(p, [(0, 0, 0), (2, 0, 0), (1, 0, 5)])  # shared edge, other plane
    assert tri_tri(p, [(0, 0, 0), (-1, -1, 3), (-2, 1, 3)])  # shared vertex


def test_parallel_planes():
    p = [(0, 0, 0), (2, 0, 0), (0, 2, 0)]
    assert not tri_tri(p, [(0, 0, 1), (2, 0, 1), (0, 2, 1)])


def test_float_orientation_can_be_wrong():
    # The example of the page: a is almost on the line through b and c.
    u = 2.0**-53
    a = (0.5 + 41 * u, 0.5 + 48 * u, 0.0)
    b, c, d = (12.0, 12.0, 0.0), (24.0, 24.0, 0.0), (0.0, 0.0, 1.0)
    exact = orient3d(*[tuple(Fraction(x) for x in v) for v in (a, b, c, d)])
    assert exact > 0
    assert orient3d_float(a, b, c, d) < 0


def test_against_oracles_random():
    rng = random.Random(1997)
    hits = 0
    for it in range(4000):
        flat = it % 4 == 0
        p = rand_tri(rng, 3, flat)
        q = rand_tri(rng, 3, flat)
        got = tri_tri(p, q)
        assert got == by_segments(p, q), (p, q)
        assert got == by_separating_axes(p, q), (p, q)
        assert got == tri_tri(q, p)
        assert got == tri_tri([p[1], p[2], p[0]], [q[2], q[1], q[0]])
        hits += got
    assert 500 < hits < 3500


def test_against_oracles_fractions():
    rng = random.Random(2003)
    for _ in range(600):
        p = [tuple(Fraction(rng.randint(-8, 8), rng.randint(1, 4)) for _ in range(3)) for _ in range(3)]
        q = [tuple(Fraction(rng.randint(-8, 8), rng.randint(1, 4)) for _ in range(3)) for _ in range(3)]
        if degenerate(p) or degenerate(q):
            continue
        assert tri_tri(p, q) == by_segments(p, q) == by_separating_axes(p, q)


def test_touching_cases_from_shared_vertices():
    rng = random.Random(7)
    for _ in range(800):
        p = rand_tri(rng, 2)
        q = rand_tri(rng, 2)
        q = [p[rng.randrange(3)], q[1], q[2]]  # force a shared vertex
        if degenerate(q):
            continue
        assert tri_tri(p, q)
        assert by_segments(p, q) and by_separating_axes(p, q)
