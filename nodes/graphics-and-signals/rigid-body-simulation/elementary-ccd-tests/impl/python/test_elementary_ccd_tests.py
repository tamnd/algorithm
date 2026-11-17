# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elementary-ccd-tests/. The authors are listed in prov/RXJ8EY.jsonl.

import math
import random
from fractions import Fraction

import pytest

from elementary_ccd import (
    closest_point_on_triangle,
    closest_points_segments,
    cubic_roots_01,
    edge_edge_ccd,
    edge_edge_cubic,
    poly_eval,
    sturm_count,
    vertex_face_ccd,
    vertex_face_cubic,
)


def sub(p, q):
    return tuple(x - y for x, y in zip(p, q))


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def dot(u, v):
    return sum(x * y for x, y in zip(u, v))


def lerp(p0, p1, t):
    return tuple(x + t * (y - x) for x, y in zip(p0, p1))


def dist(p, q):
    return math.sqrt(dot(sub(p, q), sub(p, q)))


def rand_point(rng, lo=-3, hi=3, exact=False):
    if exact:
        return tuple(Fraction(rng.randint(8 * lo, 8 * hi), 8) for _ in range(3))
    return tuple(rng.uniform(lo, hi) for _ in range(3))


EXAMPLE = dict(
    p0=(3, 1, 3), p1=(1, 0, 0), a0=(0, 0, 0), a1=(0, 0, 0), b0=(4, 0, 0), b1=(5, 2, 3), c0=(0, 4, 0), c1=(1, -2, 0)
)


def example_args():
    e = EXAMPLE
    return e["p0"], e["p1"], e["a0"], e["a1"], e["b0"], e["b1"], e["c0"], e["c1"]


def test_page_example():
    c = vertex_face_cubic(*example_args())
    assert c == [48, -144, 117, -15]
    roots = cubic_roots_01(c)
    assert len(roots) == 2
    assert abs(roots[0] - (7 - math.sqrt(33)) / 2) < 1e-15 and abs(roots[1] - 0.8) < 1e-15
    assert sturm_count([Fraction(x) for x in c], Fraction(0), Fraction(1)) == 2
    # the first root is outside the triangle, the second one is the hit
    p0, p1, a0, a1, b0, b1, c0, c1 = example_args()
    t = roots[0]
    p, a, b, cc = lerp(p0, p1, t), lerp(a0, a1, t), lerp(b0, b1, t), lerp(c0, c1, t)
    assert abs(dist(p, closest_point_on_triangle(p, a, b, cc)) - 0.40047538) < 1e-8
    t = vertex_face_ccd(*example_args())
    assert 0.8 - 1e-15 <= t <= 0.8
    # the exact contact point at t = 4/5 has the barycentric coordinates (1/2, 1/4, 1/4)
    T = Fraction(4, 5)
    P = lerp(EXAMPLE["p0"], EXAMPLE["p1"], T)
    B, C = lerp(EXAMPLE["b0"], EXAMPLE["b1"], T), lerp(EXAMPLE["c0"], EXAMPLE["c1"], T)
    assert P == tuple(Fraction(1, 4) * x + Fraction(1, 4) * y for x, y in zip(B, C))


def test_cubic_equals_the_triple_product_exactly():
    rng = random.Random(11)
    for _ in range(100):
        pts = [rand_point(rng, exact=True) for _ in range(8)]
        cvf = vertex_face_cubic(*pts)
        cee = edge_edge_cubic(*pts)
        for _ in range(4):
            t = Fraction(rng.randint(0, 100), 100)
            x = [lerp(pts[2 * i], pts[2 * i + 1], t) for i in range(4)]
            p, a, b, c = x
            assert poly_eval(cvf, t) == dot(sub(p, a), cross(sub(b, a), sub(c, a)))
            a, b, c, d = x
            assert poly_eval(cee, t) == dot(sub(c, a), cross(sub(b, a), sub(d, c)))


def test_float_roots_against_an_exact_sturm_count():
    rng = random.Random(1997)
    total = 0
    for _ in range(400):
        pts = [rand_point(rng, exact=True) for _ in range(8)]
        c = (vertex_face_cubic if rng.random() < 0.5 else edge_edge_cubic)(*pts)
        if c[0] == 0 or sum(c) == 0 or all(x == 0 for x in c):
            continue
        roots = cubic_roots_01(c)
        n = sturm_count(c, Fraction(0), Fraction(1))
        assert len(roots) == n
        total += n
        for r in roots:  # the exact sign changes across each float root
            lo, hi = Fraction(max(0.0, r - 1e-9)), Fraction(min(1.0, r + 1e-9))
            assert poly_eval(c, lo) * poly_eval(c, hi) <= 0
    assert total >= 100


SAMPLES = 600


def reference_first_hit(f, contact, samples=SAMPLES):
    """Dense sampling of f for sign changes, bisection, and the contact check."""
    prev_t, prev_f = 0.0, f(0.0)
    if prev_f == 0 and contact(0.0):
        return 0.0
    for i in range(1, samples + 1):
        t = i / samples
        ft = f(t)
        if (ft < 0) != (prev_f < 0) or ft == 0:
            lo, hi, flo = prev_t, t, prev_f
            for _ in range(60):
                mid = (lo + hi) / 2
                fm = f(mid)
                if (fm < 0) == (flo < 0) and fm != 0:
                    lo, flo = mid, fm
                else:
                    hi = mid
            if contact(lo) or contact(hi):
                return lo
        prev_t, prev_f = t, ft
    return None


def vf_reference(pts, delta):
    p0, p1, a0, a1, b0, b1, c0, c1 = pts

    def at(t):
        return lerp(p0, p1, t), lerp(a0, a1, t), lerp(b0, b1, t), lerp(c0, c1, t)

    def f(t):
        p, a, b, c = at(t)
        return dot(sub(p, a), cross(sub(b, a), sub(c, a)))

    def contact(t):
        p, a, b, c = at(t)
        return dist(p, closest_point_on_triangle(p, a, b, c)) <= delta

    return reference_first_hit(f, contact)


def ee_reference(pts, delta):
    a0, a1, b0, b1, c0, c1, d0, d1 = pts

    def at(t):
        return lerp(a0, a1, t), lerp(b0, b1, t), lerp(c0, c1, t), lerp(d0, d1, t)

    def f(t):
        a, b, c, d = at(t)
        return dot(sub(c, a), cross(sub(b, a), sub(d, c)))

    def contact(t):
        a, b, c, d = at(t)
        x, y = closest_points_segments(a, b, c, d)
        return dist(x, y) <= delta

    return reference_first_hit(f, contact)


def planted(rng, kind):
    """A random linear motion with a contact at a known time t*."""
    t_star = rng.uniform(0.1, 0.9)
    vel = [rand_point(rng, -2, 2) for _ in range(4)]
    if kind == "vf":
        a, b, c = (rand_point(rng) for _ in range(3))
        w = [rng.uniform(0.05, 1) for _ in range(3)]
        s = sum(w)
        p = tuple((w[0] * x + w[1] * y + w[2] * z) / s for x, y, z in zip(a, b, c))
        at_star = [p, a, b, c]
    else:
        a, b, c = (rand_point(rng) for _ in range(3))
        u, v = rng.uniform(0.05, 0.95), rng.uniform(0.05, 0.95)
        x = lerp(a, b, u)  # the meeting point, on ab, and on cd at the parameter v
        d = tuple(c[i] + (x[i] - c[i]) / v for i in range(3))
        at_star = [a, b, c, d]
    pts = []
    for q, w in zip(at_star, vel):
        pts += [tuple(q[i] - t_star * w[i] for i in range(3)), tuple(q[i] + (1 - t_star) * w[i] for i in range(3))]
    return t_star, pts


@pytest.mark.parametrize("kind", ["vf", "ee"])
def test_planted_contacts(kind):
    rng = random.Random(7 if kind == "vf" else 8)
    test = vertex_face_ccd if kind == "vf" else edge_edge_ccd
    sampling_missed = 0
    for _ in range(80):
        t_star, pts = planted(rng, kind)
        t = test(*pts, delta=1e-7)
        assert t is not None and t <= t_star + 1e-12
        ref = (vf_reference if kind == "vf" else ee_reference)(pts, 1e-7)
        if ref is None:
            sampling_missed += 1
            assert close_pair_of_roots(kind, pts)
        else:
            assert abs(t - ref) < 1e-6
    assert sampling_missed <= 2


def close_pair_of_roots(kind, pts):
    """Two roots in one sample interval: f has no sign change there, so the sampling misses them."""
    roots = cubic_roots_01((vertex_face_cubic if kind == "vf" else edge_edge_cubic)(*pts))
    return any(r2 - r1 < 2 / SAMPLES for r1, r2 in zip(roots, roots[1:]))


@pytest.mark.parametrize("kind", ["vf", "ee"])
def test_random_motions_against_dense_sampling(kind):
    rng = random.Random(21 if kind == "vf" else 22)
    test = vertex_face_ccd if kind == "vf" else edge_edge_ccd
    hits = 0
    for _ in range(150):
        pts = [rand_point(rng) for _ in range(8)]
        t = test(*pts, delta=1e-7)
        ref = (vf_reference if kind == "vf" else ee_reference)(pts, 1e-7)
        if ref is not None:
            assert t is not None and abs(t - ref) < 1e-6
        elif t is not None:
            assert close_pair_of_roots(kind, pts)
        hits += t is not None
    assert hits >= 10


def test_closest_point_routines_against_sampling():
    rng = random.Random(3)
    for _ in range(80):
        a, b, c, p = (rand_point(rng) for _ in range(4))
        q = closest_point_on_triangle(p, a, b, c)
        best = min(
            dist(p, tuple(a[k] + i / 20 * (b[k] - a[k]) + j / 20 * (c[k] - a[k]) for k in range(3)))
            for i in range(21)
            for j in range(21 - i)
        )
        assert dist(p, q) <= best + 1e-12
        n = cross(sub(b, a), sub(c, a))  # q is in the plane of the triangle
        assert abs(dot(sub(q, a), n)) <= 1e-9 * (1 + dot(n, n))
        p1, q1, p2, q2 = (rand_point(rng) for _ in range(4))
        x, y = closest_points_segments(p1, q1, p2, q2)
        best = min(dist(lerp(p1, q1, i / 30), lerp(p2, q2, j / 30)) for i in range(31) for j in range(31))
        assert dist(x, y) <= best + 1e-12


def test_a_hit_on_a_shared_edge_needs_the_tolerance():
    # the vertex goes down through the shared edge bc of the triangles abc and cbd at t = 1/3
    a, b, c, d = (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (1.0, 1.0, 0.0)
    p0, p1 = (0.15, 0.85, 1.0), (0.15, 0.85, -2.0)

    def run(q0, q1, delta):
        return [vertex_face_ccd(q0, q1, *[x for q in tri for x in (q, q)], delta=delta) for tri in ((a, b, c), (c, b, d))]

    assert all(t is not None and abs(t - 1 / 3) < 1e-15 for t in run(p0, p1, 1e-12))
    # with delta = 0, a hit inside a triangle is found, because the root gives z = 0 exactly here
    assert run((0.25, 0.25, 1.0), (0.25, 0.25, -2.0), 0.0)[0] is not None
    # but 0.15 + 0.85 is not 1 after rounding of the inputs, and both triangles miss the hit on bc
    assert run(p0, p1, 0.0) == [None, None]
    # with exact rational input and an exact root, the contact check is exact
    F = Fraction
    P0, P1 = (F(3, 10), F(7, 10), F(1)), (F(3, 10), F(7, 10), F(-2))
    T = F(1, 3)
    P = lerp(P0, P1, T)
    A, B, C = (F(0), F(0), F(0)), (F(1), F(0), F(0)), (F(0), F(1), F(0))
    assert closest_point_on_triangle(P, A, B, C) == P


def test_coplanar_motion_is_reported():
    with pytest.raises(ValueError):
        vertex_face_ccd((0.2, 0.2, 0.0), (0.5, 0.5, 0.0), (0, 0, 0), (0, 0, 0), (1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0))
