# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/watertight-ray-triangle-intersection/. The authors are listed in prov/Y50EDX.jsonl.

import random
from fractions import Fraction

from watertight_ray_triangle_intersection import ShearedRay, intersect, watertight_intersect


def det3(c0, c1, c2):
    return (c0[0] * (c1[1] * c2[2] - c1[2] * c2[1])
            - c1[0] * (c0[1] * c2[2] - c0[2] * c2[1])
            + c2[0] * (c0[1] * c1[2] - c0[2] * c1[1]))


def exact_hit(o, d, a, b, c):
    """Reference: Cramer's rule in Fraction for o + t d = a + u (b - a) + v (c - a)."""
    o, d, a, b, c = ([Fraction(x) for x in p] for p in (o, d, a, b, c))
    e1 = [b[i] - a[i] for i in range(3)]
    e2 = [c[i] - a[i] for i in range(3)]
    md = [-x for x in d]
    r = [o[i] - a[i] for i in range(3)]
    den = det3(e1, e2, md)
    if den == 0:
        return None
    u = det3(r, e2, md) / den
    v = det3(e1, r, md) / den
    t = det3(e1, e2, r) / den
    if u < 0 or v < 0 or u + v > 1 or t < 0:
        return None
    return (t, 1 - u - v, u, v)       # t and the weights of a, b, c


def test_simple_hit():
    hit = intersect((0.25, 0.25, 1.0), (0.0, 0.0, -1.0), (0, 0, 0), (1, 0, 0), (0, 1, 0))
    assert hit == (1.0, 0.5, 0.25, 0.25)


def test_two_sided_and_culling():
    a, b, c = (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)
    down = ((0.2, 0.2, 1.0), (0.0, 0.0, -1.0))
    up = ((0.2, 0.2, -1.0), (0.0, 0.0, 1.0))
    assert intersect(*down, a, b, c) is not None
    assert intersect(*up, a, b, c) is not None
    hits = [intersect(*r, a, b, c, cull_backfaces=True) is not None for r in (down, up)]
    assert hits.count(True) == 1
    assert intersect(*down, a, b, c, tmax=0.5) is None
    assert intersect((0.2, 0.2, -1.0), (0.0, 0.0, -1.0), a, b, c) is None


def test_random_against_cramer():
    rng = random.Random(2013)
    hits = 0
    for _ in range(3000):
        o, d, a, b, c = ([rng.uniform(-5, 5) for _ in range(3)] for _ in range(5))
        if rng.random() < 0.6:
            w = (rng.uniform(-0.2, 1.0), rng.uniform(-0.2, 1.0))
            d = [a[i] + w[0] * (b[i] - a[i]) + w[1] * (c[i] - a[i]) - o[i] for i in range(3)]
        got = intersect(o, d, a, b, c)
        want = exact_hit(o, d, a, b, c)
        if want is None:
            if got is not None:
                assert min(got[1:]) < 1e-9
            continue
        t = float(want[0])
        if min(want[1:]) < 1e-9:
            continue
        assert got is not None
        hits += 1
        assert abs(got[0] - t) <= 1e-9 * max(1.0, t)
        for x, y in zip(got[1:], want[1:]):
            assert abs(x - float(y)) <= 1e-9
        # the weights give the hit point
        for i in range(3):
            p = got[1] * a[i] + got[2] * b[i] + got[3] * c[i]
            assert abs(p - (o[i] + got[0] * d[i])) <= 1e-8 * max(1.0, abs(p))
    assert hits > 500


def test_decision_is_exact_for_the_transformed_vertices():
    # The inside decision equals the exact 2D test on the rounded, sheared vertices.
    rng = random.Random(5)
    for _ in range(3000):
        o = [rng.uniform(-2, 2) for _ in range(3)]
        a, b, c = ([rng.uniform(-2, 2) for _ in range(3)] for _ in range(3))
        k = rng.randrange(3)
        tgt = [x + rng.choice([0.0, 0.5, 1.0]) * (y - x) for x, y in zip((a, b, c)[k], (a, b, c)[(k + 1) % 3])]
        d = [tgt[i] - o[i] for i in range(3)]
        ray = ShearedRay(o, d)
        ta, tb, tc = (ray.transform(p) for p in (a, b, c))
        f = [Fraction(x) for x in ta[:2] + tb[:2] + tc[:2]]
        ax, ay, bx, by, cx, cy = f
        u, v, w = cx * by - cy * bx, ax * cy - ay * cx, bx * ay - by * ax
        mixed = (u < 0 or v < 0 or w < 0) and (u > 0 or v > 0 or w > 0)
        got = watertight_intersect(ray, a, b, c)
        if mixed or u + v + w == 0:
            assert got is None
        elif got is None:
            # the only other reason to miss is the depth test
            t_scaled = (u * Fraction(ray.sz) * Fraction(ta[2]) + v * Fraction(ray.sz) * Fraction(tb[2])
                        + w * Fraction(ray.sz) * Fraction(tc[2]))
            assert t_scaled * (u + v + w) <= 0 or abs(t_scaled) < 1e-12


def height_field(rng, n, scale):
    z = [[scale * rng.uniform(-0.3, 0.3) for _ in range(n + 1)] for _ in range(n + 1)]
    v = [[(float(i), float(j), z[i][j]) for j in range(n + 1)] for i in range(n + 1)]
    tris = []
    for i in range(n):
        for j in range(n):
            p, q, r, s = v[i][j], v[i + 1][j], v[i + 1][j + 1], v[i][j + 1]
            if rng.random() < 0.5:
                tris += [(p, q, r), (p, r, s)]
            else:
                tris += [(p, q, s), (q, r, s)]
    return v, tris


def test_mesh_has_no_cracks():
    # Rays aimed at interior edges and vertices of a mesh always hit some triangle.
    rng = random.Random(7)
    n = 3
    for trial in range(400):
        v, tris = height_field(rng, n, 1.0)
        edges = {}
        for t in tris:
            for k in range(3):
                e = tuple(sorted((t[k], t[(k + 1) % 3])))
                edges[e] = edges.get(e, 0) + 1
        shared = [e for e, cnt in edges.items() if cnt == 2]
        for _ in range(10):
            o = (rng.uniform(-2, n + 2), rng.uniform(-2, n + 2), rng.uniform(5, 10))
            if rng.random() < 0.5:
                p, q = rng.choice(shared)
                s = rng.choice([0.5, rng.random()])
                tgt = tuple(p[i] + s * (q[i] - p[i]) for i in range(3))
            else:
                tgt = v[rng.randint(1, n - 1)][rng.randint(1, n - 1)]
            d = tuple(tgt[i] - o[i] for i in range(3))
            ray = ShearedRay(o, d)
            assert any(watertight_intersect(ray, *t) is not None for t in tris)


def test_exact_edge_points_hit_both_or_one():
    # Integer mesh, ray through the exact midpoint of the shared diagonal. The
    # rays are steeper than both faces, so the two triangles lie on the two
    # sides of the edge as seen from the ray (the edge is not a silhouette).
    rng = random.Random(11)
    for _ in range(2000):
        p = (0.0, 0.0, float(rng.randint(-1, 1)))
        q = (4.0, 4.0, float(rng.randint(-1, 1)))
        a = (4.0, 0.0, float(rng.randint(-1, 1)))
        b = (0.0, 4.0, float(rng.randint(-1, 1)))
        m = tuple((p[i] + q[i]) / 2 for i in range(3))
        o = (float(rng.randint(-8, 8)), float(rng.randint(-8, 8)), float(rng.randint(20, 40)))
        d = tuple(m[i] - o[i] for i in range(3))
        h1 = intersect(o, d, p, a, q)
        h2 = intersect(o, d, p, q, b)
        assert h1 is not None or h2 is not None
