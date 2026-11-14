# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-slicing/. The authors are listed in prov/YQA8PY.jsonl.

import math
import random
from fractions import Fraction as F

from direct_slicing import (
    classify,
    cylinder,
    direct_slice,
    ellipse_axes,
    ellipse_polyline,
    half_space,
    inside_2d,
    inside_3d,
    section,
    slice_tree,
    sphere,
    uv_sphere_section_radii,
    vertex_count,
)


def test_sphere_slice_is_the_closed_form_circle() -> None:
    rng = random.Random(1)
    for _ in range(200):
        c = [F(rng.randint(-20, 20), rng.randint(1, 5)) for _ in range(3)]
        r2 = F(rng.randint(1, 400), rng.randint(1, 4))
        z = F(rng.randint(-100, 100), rng.randint(1, 7))
        kind, center, fc, det = classify(section(sphere(c, r2), z))
        want = r2 - (z - c[2]) ** 2
        if want > 0:
            assert kind == "ellipse"
            assert center == (c[0], c[1])
            assert det == 1 and -fc == want  # radius^2 = R^2 - (Z - c_z)^2, exactly
        elif want == 0:
            assert kind == "point" and center == (c[0], c[1])
        else:
            assert kind == "empty"


def test_sphere_pole_gives_a_point() -> None:
    kind, center, fc, _ = classify(section(sphere((0, 0, 0), 25), 5))
    assert kind == "point" and center == (0, 0) and fc == 0
    kind, _, fc, _ = classify(section(sphere((0, 0, 0), 25), 3))
    assert kind == "ellipse" and -fc == 16


def test_cylinder_slice_is_the_closed_form_ellipse() -> None:
    rng = random.Random(2)
    for _ in range(200):
        p = [F(rng.randint(-10, 10)) for _ in range(3)]
        a = [F(rng.randint(-4, 4)) for _ in range(2)] + [F(rng.choice([-3, -2, -1, 1, 2, 3]))]
        r2 = F(rng.randint(1, 50), rng.randint(1, 3))
        z = F(rng.randint(-30, 30), rng.randint(1, 4))
        kind, center, fc, det = classify(section(cylinder(p, a, r2), z))
        assert kind == "ellipse"
        t = (z - p[2]) / a[2]  # the axis meets the plane at p + t a
        assert center == (p[0] + t * a[0], p[1] + t * a[1])
        n2 = sum(v * v for v in a)
        # squared semi-axes r^2 and r^2 |a|^2 / a_z^2
        s1, s2 = r2 * n2 / a[2] ** 2, r2
        assert det == a[2] ** 2 / n2  # eigenvalues 1 and a_z^2 / |a|^2
        assert fc * fc / det == s1 * s2  # product of the squared semi-axes
        trace = section(cylinder(p, a, r2), z)[0][0] + section(cylinder(p, a, r2), z)[1][1]
        assert -fc * trace / det == s1 + s2  # sum of the squared semi-axes
        _, f1, f2, _, _ = ellipse_axes(section(cylinder(p, a, r2), z))
        assert math.isclose(f1, float(s1), rel_tol=1e-9) and math.isclose(f2, float(s2), rel_tol=1e-9)


def test_vertical_cylinder_has_the_same_circle_on_every_layer() -> None:
    q = cylinder((1, 2, 0), (0, 0, 1), 9)
    for z in range(-5, 6):
        kind, center, fc, det = classify(section(q, z))
        assert (kind, center, -fc, det) == ("ellipse", (1, 2), 9, 1)


def random_tree(rng, depth):
    if depth == 0 or rng.random() < 0.3:
        k = rng.randrange(3)
        if k == 0:
            q = sphere([rng.randint(-3, 3) for _ in range(3)], rng.randint(1, 16))
        elif k == 1:
            q = cylinder([rng.randint(-3, 3) for _ in range(3)], [rng.randint(-2, 2), rng.randint(-2, 2), rng.randint(1, 2)], rng.randint(1, 9))
        else:
            q = half_space([rng.randint(-2, 2) for _ in range(3)], rng.randint(-3, 3))
        return ("leaf", q)
    op = rng.choice(["union", "inter", "diff"])
    return (op, random_tree(rng, depth - 1), random_tree(rng, depth - 1))


def test_layer_membership_equals_solid_membership() -> None:
    rng = random.Random(3)
    for _ in range(60):
        tree = random_tree(rng, 3)
        z = F(rng.randint(-12, 12), 4)
        tree2 = slice_tree(tree, z)
        for _ in range(40):
            x, y = F(rng.randint(-24, 24), 4), F(rng.randint(-24, 24), 4)
            assert inside_2d(tree2, (x, y)) == inside_3d(tree, (x, y, z))


def dist_point_segment(p, a, b):
    ax, ay = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * ax + (p[1] - a[1]) * ay) / (ax * ax + ay * ay)
    t = max(0.0, min(1.0, t))
    return math.hypot(p[0] - a[0] - t * ax, p[1] - a[1] - t * ay)


def test_polyline_error_is_within_tolerance() -> None:
    q = cylinder((0, 0, 0), (1, 1, 2), 4)
    m = section(q, F(1, 3))
    (cx, cy), s1, s2, v1, v2 = ellipse_axes(m)
    a1, a2 = math.sqrt(s1), math.sqrt(s2)
    for tol in (0.5, 0.1, 0.01, 0.001):
        poly = ellipse_polyline(m, tol)
        n = len(poly)
        assert n == vertex_count(a1, tol)
        for p in poly:  # vertices lie on the ellipse
            assert abs(float(sum(x * float(m[i][j]) * y for i, x in enumerate((p[0], p[1], 1.0)) for j, y in enumerate((p[0], p[1], 1.0))))) < 1e-9
        worst = 0.0
        for k in range(20 * n):  # ellipse to polygon
            t = 2 * math.pi * k / (20 * n)
            u, w = a1 * math.cos(t), a2 * math.sin(t)
            e = (cx + u * v1[0] + w * v2[0], cy + u * v1[1] + w * v2[1])
            worst = max(worst, min(dist_point_segment(e, poly[i], poly[(i + 1) % n]) for i in range(n)))
        assert worst <= tol + 1e-12
        if n > 3:  # one vertex fewer would break the bound
            assert a1 * (1 - math.cos(math.pi / (n - 1))) > tol


def test_trimmed_contours_lie_on_the_boundary() -> None:
    # a ball minus a vertical hole: the layer is an annulus with two loops
    tree = ("diff", ("leaf", sphere((0, 0, 0), 100)), ("leaf", cylinder((0, 0, 0), (0, 0, 1), 9)))
    tree2, contours = direct_slice(tree, 6, 0.01)
    assert len(contours) == 2
    radii = sorted(round(math.hypot(*c[0]), 9) for c in contours)
    assert radii == [3.0, 8.0]  # 8 = sqrt(100 - 36)
    # two overlapping balls: each circle keeps only its outer arc
    tree = ("union", ("leaf", sphere((0, 0, 0), 25)), ("leaf", sphere((6, 0, 0), 25)))
    tree2, contours = direct_slice(tree, 0, 0.001)
    assert len(contours) == 2
    for run in contours:
        for p in run:
            d0, d1 = math.hypot(p[0], p[1]), math.hypot(p[0] - 6, p[1])
            assert min(abs(d0 - 5), abs(d1 - 5)) < 1e-9  # on one circle
            assert min(d0, d1) >= 5 - 1e-9  # and not inside the other ball


def test_mesh_slice_has_chordal_error_and_direct_slice_has_none() -> None:
    lo, hi = uv_sphere_section_radii(10.0, 16, 32, 2.5)
    true = math.sqrt(100 - 2.5**2)
    assert 0.08 < true - lo < 0.09  # the mesh section misses the circle by 0.0876
    lo, hi = uv_sphere_section_radii(10.0, 16, 32, -9.95)
    assert math.sqrt(100 - 9.95**2) - hi > 0.4  # near the pole the error is ten times larger
    kind, center, fc, _ = classify(section(sphere((0, 0, 0), 100), F(5, 2)))
    assert kind == "ellipse" and -fc == F(375, 4)  # exactly true^2
